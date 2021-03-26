from fhir_query import FhirQueryImmunization
from flask import Flask, request, url_for
from immu_parser import ImmuEntryParser


class Fhir2QR:
    def __init__(self, fhir_server: str):
        self.__fhir_server: str = fhir_server

    def fhir_query_immu(self) -> dict:
        qry_res = FhirQueryImmunization.find()
        return qry_res


app = Flask(__name__)


@app.route("/")
def index():
    return url_for("static", filename="index.html")


@app.route("/fhir2qr", methods=["POST"])
def fhir2rr(fhir_server: str):
    fhir2qr_query = Fhir2QR(fhir_server=fhir_server)
    qry_res: dict = fhir2qr_query.fhir_query_immu()
    ret_data: dict = {}

    if "entry" in qry_res:
        for entry in qry_res["entry"]:
            parsed_entry: dict = ImmuEntryParser.extract_entry(qry_entry=entry)
            ret_data.update(parsed_entry)
    if "resourceType" in qry_res:
        if qry_res["resourceType"] == "Bundle":
            total_matches = qry_res["total"]
            ret_data["Total Matches"] = total_matches
    return ret_data
