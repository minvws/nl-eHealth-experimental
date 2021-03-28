from flask import Flask, request, send_from_directory
from fhir_query import FhirQueryImmunization
from immu_parser import ImmuEntryParser
from min_data_set import MinDataSet


class Fhir2QR:
    def __init__(self, fhir_server: str):
        self.__fhir_server: str = fhir_server

    def fhir_query_immu(self) -> dict:
        qry_res = FhirQueryImmunization.find()
        return qry_res


app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory(directory="static", filename="index.html")


@app.route("/fhir2qr", methods=["POST"])
def fhir2qr():
    fhir_server = request.form["fhir_server"]
    fhir2qr_query = Fhir2QR(fhir_server=fhir_server)
    qry_res: dict = fhir2qr_query.fhir_query_immu()
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
    return ret_data
