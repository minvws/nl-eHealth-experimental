import requests
from immu_parser import ImmuEntryParser
from pprint import PrettyPrinter


class FhirImmunization:
    """ Performs FHIR Immunization queries against an HL7 FHIR R4 Server """

    # SERVICE_ROOT_URL = "https://fhir-open.cerner.com/r4/ec2458f2-1e24-41c8-b71b-0e701af7583d/"    # Cerner
    # SERVICE_ROOT_URL = "https://try.smilecdr.com:8000/baseR4/"    # SmileCDR
    SERVICE_ROOT_URL = "https://server.fire.ly/r4/"  # fire.ly
    ACCEPT_HEADER = {"Accept": "application/fhir+json"}

    @staticmethod
    def find():
        try:
            resp = requests.get(
                f"{FhirImmunization.SERVICE_ROOT_URL}Immunization",
                headers=FhirImmunization.ACCEPT_HEADER,
                params={
                    "_summary": "data",
                    "date": "ge2021-01-01",
                },
            )
            resp.raise_for_status()
            dict_resp = resp.json()
            return dict_resp
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error: {http_err}")
        except Exception as err:
            print(f"Other(requests) error: {err}")

    @staticmethod
    def resolve_patient(entry: dict) -> dict:
        patient_uri = entry["resource"]["patient"]
        try:
            resp = requests.get(
                patient_uri,
                headers=FhirImmunization.ACCEPT_HEADER,
                params={"_summary": "data"},
            )
            resp.raise_for_status()
            dict_resp = resp.json()
            return dict_resp
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error: {http_err}")
        except Exception as err:
            print(f"Other(requests) error: {err}")


if __name__ == "__main__":
    pp = PrettyPrinter(indent=2)
    qry_res = FhirImmunization.find()
    if "entry" in qry_res:
        for qry_entry in qry_res["entry"]:
            if "resource" in qry_entry:
                patient = FhirImmunization.resolve_patient(entry=qry_entry)
                pp.pprint(
                    ImmuEntryParser.json(
                        entry=qry_entry,
                        patient=patient,
                        disclosure_level=ImmuEntryParser.DisclosureLevel.MD,
                    )
                )
