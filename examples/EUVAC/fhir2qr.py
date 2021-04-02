from flask import Flask, request, send_from_directory, Response, send_file
from fhir_query import FhirQueryImmunization
from immu_parser import ImmuEntryParser
from min_data_set import MinDataSet
from werkzeug.routing import BaseConverter

import sys
import io
import zlib
import argparse
import json
import cbor2
import segno as qr
import ujson

from base45 import b45encode
from cose.algorithms import Es256
from cose.curves import P256
from cose.algorithms import Es256, EdDSA
from cose.keys.keyparam import KpKty, KpAlg, EC2KpD, EC2KpX, EC2KpY, EC2KpCurve
from cose.headers import Algorithm, KID
from cose.keys import CoseKey
from cose.keys.keyparam import KpAlg, EC2KpD, EC2KpCurve
from cose.keys.keyparam import KpKty
from cose.keys.keytype import KtyEC2
from cose.messages import Sign1Message
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key


class Fhir2QR:
    def __init__(self, fhir_server: str):
        self.__fhir_server: str = fhir_server

    def fhir_query_immu(self) -> dict:
        qry_res = FhirQueryImmunization.find()
        return qry_res


app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters["regex"] = RegexConverter


@app.route("/")
def index():
    return send_from_directory(directory="static", filename="index.html")


@app.route("/scripts.js")
def scripts():
    return send_from_directory(directory="static", filename="scripts.js")


@app.route("/styles.css")
def styles():
    return send_from_directory(directory="static", filename="styles.css")


@app.route("/fhir_query_res.json")
def fhir_query_res():
    return send_from_directory(directory="static", filename="fhir_query_res.json")


@app.route('/<regex("[a-z0-9\-]+\.(pem|key)"):file>')
def cryptofile(file):
    return send_from_directory(
        directory="static", filename=file, mimetype="application/x-pem-file"
    )


@app.route("/fhir2json", methods=["POST", "GET"])
def fhir2json():
    fhir_json = request.form["fhir"]

    if not fhir_json or len(fhir_json) < 2:
        fhir_server = (
            request.form["fhir_server"] if "fhir_server" in request.form else ""
        )
        fhir2qr_query = Fhir2QR(fhir_server=fhir_server)
        qry_res, req = fhir2qr_query.fhir_query_immu()
        print(req)
    else:
        qry_res = json.loads(fhir_json)

    ret_data: dict = {}

    if qry_res is not None:
        if "entry" in qry_res:
            for entry in qry_res["entry"]:
                min_data_set: MinDataSet = ImmuEntryParser.extract_entry(
                    qry_entry=entry
                )
                if min_data_set is not None:
                    ret_data.update(min_data_set.pv)
                    if min_data_set.md is not None:
                        ret_data.update(min_data_set.md)
        if "resourceType" in qry_res:
            if qry_res["resourceType"] == "Bundle":
                total_matches = qry_res["total"]
                ret_data["Total Matches"] = total_matches
    else:
        ret_data[
            "FHIR2QR"
        ] = f"No entries found to match FHIR query on FHIR server: {fhir_server}"
    return ujson.dumps(ret_data)


@app.route("/fhir2jsoncbor", methods=["POST", "GET"])
def fhir2jsoncbor():
    data = ujson.loads(fhir2json())
    cb = cbor2.dumps(data)
    # return Response(cb,mimetype='text/plain')
    return cb


@app.route("/fhir2jsoncborcose", methods=["POST", "GET"])
def fhir2jsoncborcose():
    data = fhir2jsoncbor()
    with open("dsc-worker.pem", "rb") as file:
        pem = file.read()
    cert = x509.load_pem_x509_certificate(pem)
    fingerprint = cert.fingerprint(hashes.SHA256())
    keyid = fingerprint[-8:]

    with open("dsc-worker.key", "rb") as file:
        pem = file.read()
    keyfile = load_pem_private_key(pem, password=None)
    priv = keyfile.private_numbers().private_value.to_bytes(32, byteorder="big")

    msg = Sign1Message(phdr={Algorithm: Es256, KID: keyid}, payload=data)

    cose_key = {
        KpKty: KtyEC2,
        KpAlg: Es256,  # ecdsa-with-SHA256
        EC2KpCurve: P256,  # Ought to be pk.curve - but the two libs clash
        EC2KpD: priv,
    }
    msg.key = CoseKey.from_dict(cose_key)

    return msg.encode()


@app.route("/fhir2jsoncborcosezlib", methods=["POST", "GET"])
def fhir2jsoncborcosezlib():
    data = fhir2jsoncborcose()
    return zlib.compress(data, 9)


@app.route("/fhir2jsoncborcosezlibb45", methods=["POST", "GET"])
def fhir2jsoncborcosezlibb45():
    data = fhir2jsoncborcosezlib()
    b45 = b45encode(data)
    return b45


@app.route("/fhir2jsoncborcosezlibb45qr", methods=["POST", "GET"])
def fhir2jsoncborcosezlibb45qr():
    data = fhir2jsoncborcosezlibb45()
    # return qr.make(data,error='Q').svg_inline()
    buff = io.BytesIO()
    qr.make(data, error="Q").save(buff, kind="png", scale=6)
    buff.seek(0)
    return send_file(buff, mimetype="image/png")


@app.route("/fhir2size", methods=["POST", "GET"])
def fhir2size():
    step1 = fhir2json()

    len_fhir = 0
    len_json = len(ujson.dumps(fhir2json()))
    len_cbor = len(fhir2jsoncbor())
    len_cose = len(fhir2jsoncborcose())
    len_zlib = len(fhir2jsoncborcosezlib())

    b45 = fhir2jsoncborcosezlibb45()
    len_b45 = len(b45)

    img = qr.make(b45, error="Q")
    img_s = len(img.matrix)

    win = len_json - len_zlib
    winp = int(100 * win / len_json)

    return Response(
        f"Sizes:\n JSON:   {len_json}\n CBOR:   {len_cbor}\n COSE:   {len_cose}\n ZLIB:   {len_zlib}\n B45 :   {len_b45}\n QR mode: {img.mode} (Should be 2/alphanumeric/b45)\n QR code: {img.version} (1..40)\n QR matrix: {img_s}x{img_s} (raw pixels without border)\n\nWin: {winp}%; {win} bytes saved on {len_json} bytes (FHIR was {len_fhir} bytes)",
        mimetype="text/plain",
    )
