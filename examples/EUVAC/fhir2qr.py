import io
import zlib
from typing import Tuple

import cbor2
import segno as qr
import ujson
from base45 import b45encode
from cose.algorithms import Es256
from cose.curves import P256
from cose.headers import Algorithm, KID
from cose.keys import CoseKey
from cose.keys.keyparam import KpAlg, EC2KpD, EC2KpCurve
from cose.keys.keyparam import KpKty
from cose.keys.keytype import KtyEC2
from cose.messages import Sign1Message
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from flask import Flask, request, send_from_directory, Response, send_file
from werkzeug.routing import BaseConverter

from fhir_query import FhirQueryImmunization
from immu_parser import ImmuEntryParser
from min_data_set import MinDataSet, MinDataSetFactory

app = Flask(__name__)


class Fhir2QR:
    def __init__(self, fhir_server: str):
        self.__fhir_server: str = fhir_server

    def fhir_query_immu(self) -> Tuple[dict, str]:
        qry_res, resp = FhirQueryImmunization.find()
        return qry_res, resp

    def annex1_min_data_set(
        self, qry_res: dict, disclosure_level: MinDataSetFactory.DisclosureLevel
    ) -> dict:
        """
        :param qry_res: the result of a FHIR query contained as a dict (result of e.g.json.loads())
        :type qry_res: dict
        :param disclosure_level: Disclosure Level according to EU eHealthNetwork Annex 1 Minimum Data Set
        :type disclosure_level: MinDataSetFactory.DisclosureLevel
        :return: dict containing EU eHealthNetwork Annex 1 Minimum Data Set
        """
        if qry_res is None:
            return {}
        ret_data: dict = self.__process_entries(qry_res=qry_res, disclosure_level=disclosure_level)
        if "resourceType" in qry_res:
            if qry_res["resourceType"] == "Bundle":
                total_matches = qry_res["total"]
                ret_data["Total Matches"] = total_matches
        return ret_data

    def __process_entries(self, qry_res: dict, disclosure_level: MinDataSetFactory.DisclosureLevel) -> dict:
        ret_data = {}
        if "entry" in qry_res:
            min_data_sets_annex1 = list()
            for entry in qry_res["entry"]:
                min_data_set: MinDataSet = ImmuEntryParser.extract_entry(
                    qry_entry=entry, disclosure_level=disclosure_level
                )
                if min_data_set is not None:
                    min_data_annex1 = min_data_set.pv
                    if (
                            disclosure_level == MinDataSetFactory.DisclosureLevel.MD
                            and min_data_set.md is not None
                    ):
                        min_data_annex1.update(min_data_set.md)
                    min_data_sets_annex1.append(min_data_annex1)
            ret_data.update({"entries": min_data_sets_annex1})
        return ret_data


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters["regex"] = RegexConverter


@app.route("/")
def index():
    return send_from_directory(directory="static", filename="index.html")


@app.route('/<regex("scripts.js|styles.css|fhir_query_res.json"):file>')
def scripts_styles(file):
    return send_from_directory(directory="static", filename=file)


@app.route('/<regex("[a-z0-9\-]+\.(pem|key)"):file>')
def cryptofile(file):
    return send_from_directory(
        directory="static", filename=file, mimetype="application/x-pem-file"
    )


@app.route("/fhir2json", methods=["POST", "GET"])
def fhir2json():
    fhir_server = request.form["fhir_server"] if "fhir_server" in request.form else ""
    fhir2qr = Fhir2QR(fhir_server=fhir_server)
    qry_res, req = fhir2qr.fhir_query_immu()
    app.logger.info(f"*** FHIR req: {req}")
    min_data_set: dict = fhir2qr.annex1_min_data_set(
        qry_res=qry_res, disclosure_level=MinDataSetFactory.DisclosureLevel.PV
    )
    return ujson.dumps(min_data_set)


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
