import io
from sys import getsizeof

import cbor2
import segno as qr
import zlib

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
from flask import (
    Flask,
    request,
    send_from_directory,
    render_template,
    send_file,
)

from werkzeug.routing import BaseConverter

from disclosure_level import DisclosureLevel
from fhir_query import FhirQuery
from json_ld_formatter import JsonLdFormatter
from min_data_set import MinDataSetFactory, MinDataSet

CERTIFICATE_FILE = "dsc-worker.pem"

app = Flask(__name__)

_page_state: dict = {}


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters["regex"] = RegexConverter


def __cose_sign(data: bytes) -> bytes:
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


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/<regex("scripts.js|styles.css|fhir_query_res.json"):file>')
def scripts_styles(file):
    return send_from_directory(directory="static", filename=file)


@app.route('/<regex("[a-z0-9\-]+\.(pem|key)"):file>')
def cryptofile(file):
    return send_from_directory(
        directory="static", filename=file, mimetype="application/x-pem-file"
    )


@app.route("/clear_all_fields", methods=["POST"])
def clear_all_fields():
    global _page_state
    _page_state = {}
    return render_template("index.html", page_state=_page_state)


@app.route("/query_fhir_server", methods=["POST", "GET"])
def query_fhir_server():
    fhir_server = request.form["fhir_server"] if "fhir_server" in request.form else None
    _page_state["qry_res"] = FhirQuery(fhir_server=fhir_server).find()
    _page_state["focus_btn"] = "btn_fhir_2_json"

    return render_template("index.html", page_state=_page_state)


# Was
# @app.route("/fhir2json", methods=["POST", "GET"])
# def fhir2json():
#     # pre-cond: /query_fhir_server called prior in order to set: _page_state["qry_res"]
#     min_data_set: dict = FhirQuery.annex1_min_data_set(
#         qry_res=_page_state["qry_res"],
#         disclosure_level=MinDataSetFactory.DisclosureLevel.PV,
#     )
#     _page_state["min_data_set"] = min_data_set
#     return ujson.dumps(min_data_set)


@app.route("/fhir2json", methods=["POST", "GET"])
def fhir2json():
    # pre-cond: /query_fhir_server called prior in order to set: _page_state["qry_res"]
    min_data_set: MinDataSet = MinDataSetFactory.create(DisclosureLevel.PrivateVenue)
    qry_res = _page_state["qry_res"]
    min_data_set.parse(qry_res)
    _page_state["min_data_set"] = min_data_set.as_json()
    _page_state["focus_btn"] = "btn_fhir_2_jsonld"
    return render_template("index.html", page_state=_page_state)


@app.route("/fhir2jsonld", methods=["POST", "GET"])
def fhir2jsonld():
    # pre-cond: /query_fhir_server called prior in order to set: _page_state["qry_res"]
    min_data_set: MinDataSet = MinDataSetFactory.create(DisclosureLevel.PrivateVenue)
    qry_res = _page_state["qry_res"]
    min_data_set.parse(qry_res)
    _page_state["min_data_set_jsonld"] = JsonLdFormatter().map_json_to_ld(
        min_data_set.as_dict_array()[0]
    )  # TODO select
    _page_state["focus_btn"] = "btn_fhir_2_jsonld_cborld"
    return render_template("index.html", page_state=_page_state)


@app.route("/fhir2jsoncbor", methods=["POST", "GET"])
def fhir2jsoncbor():
    cb = cbor2.dumps(_page_state["min_data_set_jsonld"])
    _page_state["min_data_set_jsonld_cborld"] = cb
    _page_state["focus_btn"] = "btn_fhir_2_jsoncborcose"
    return render_template("index.html", page_state=_page_state)


@app.route("/fhir2jsoncborcose", methods=["POST", "GET"])
def fhir2jsoncborcose():
    data: bytes = _page_state["min_data_set_jsonld_cborld"]
    cose_msg: bytes = __cose_sign(data=data)
    _page_state["min_data_set_jsoncborcose"] = cose_msg
    _page_state["focus_btn"] = "btn_fhir_2_cose_compress"
    return render_template("index.html", page_state=_page_state)


@app.route("/fhir2jsoncborcosezlib", methods=["POST", "GET"])
def fhir2jsoncborcosezlib():
    data = _page_state["min_data_set_jsoncborcose"]
    _page_state["cose_compress"] = zlib.compress(data, 9)
    _page_state["focus_btn"] = "btn_fhir_2_b45"
    return render_template("index.html", page_state=_page_state)


@app.route("/fhir2jsoncborcosezlibb45", methods=["POST", "GET"])
def fhir2jsoncborcosezlibb45():
    _page_state["b45"] = b45encode(_page_state["cose_compress"])
    _page_state["focus_btn"] = "btn_fhir2b45qr"
    return render_template("index.html", page_state=_page_state)


@app.route("/fhir2b45qr", methods=["POST", "GET"])
def fhir2jsoncborcosezlibb45qr():
    data = _page_state["b45"]
    # return qr.make(data,error='Q').svg_inline()
    buff = io.BytesIO()
    qr.make(data, error="Q").save(buff, kind="png", scale=6)
    buff.seek(0)
    return send_file(buff, mimetype="image/png")


@app.route("/fhir2size", methods=["POST", "GET"])
def fhir2size():
    fhir_query_response: dict = FhirQuery().find()
    min_data_set: MinDataSet = MinDataSetFactory.create(DisclosureLevel.PrivateVenue)

    qry_res = _page_state["qry_res"]
    min_data_set.parse(qry_res)
    json_std = min_data_set.as_json()
    json_ld: dict = min_data_set.as_jsonld()

    cb = cbor2.dumps(json_ld)
    cose_msg: bytes = __cose_sign(data=cb)
    cose_compressed: bytes = zlib.compress(cose_msg, 9)
    b45 = b45encode(cose_compressed)
    qr_img = qr.make(b45, error="Q")

    len_fhir = getsizeof(fhir_query_response)
    len_json = getsizeof(json_std)
    len_json_ld = getsizeof(json_ld)
    len_cbor = getsizeof(cb)
    len_cose = getsizeof(cose_msg)
    len_zlib = getsizeof(cose_compressed)
    len_b45 = getsizeof(b45)
    qr_img_s = len(qr_img.matrix)

    win = len_json - len_zlib
    winp = int(100 * win / len_json)

    _page_state["sizes"] = {
        "FHIR query response: ": len_fhir,
        "JSON: ": len_json,
        "JSON-LD: ": len_json_ld,
        "CBOR: ": len_cbor,
        "COSE: ": len_cose,
        "LZMA:": len_zlib,
        "Base45: ": len_b45,
        "QR mode: ": f"{qr_img.mode} (Should be 2/alphanumeric/b45)",
        "QR code: ": f"{qr_img.version} (1..40)",
        "QR matrix: ": f"{qr_img_s}x{qr_img_s} (raw pixels without border, number of cells)",
        "Win: ": f"{winp}%; {win} bytes saved with {len_zlib} (LZMA) bytes cf. {len_json} (JSON) bytes (FHIR was {len_fhir} bytes)",
    }
    _page_state["focus_btn"] = "btn_fhir2size"
    return render_template("index.html", page_state=_page_state)
