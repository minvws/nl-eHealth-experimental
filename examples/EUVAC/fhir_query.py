import requests
from typing import Optional


class FhirQuery:
    """ Performs FHIR Immunization queries against an HL7 FHIR R4 Server """

    # SERVICE_ROOT_URL = "https://server.fire.ly/r4/"  # fire.ly
    SERVICE_ROOT_URL = "https://hl7eu.onfhir.io/r4/"  # HL7 EU FHIR Server
    ACCEPT_HEADER = {"Accept": "application/fhir+json"}

    @staticmethod
    def find(fhir_server: Optional[str] = None):
        """
        :param fhir_server: Service Root URL for FHIR server,
        can be None in which case SERVICE_ROOT_URL will be used
        :return: FHIR query result as dict, HTTP request as str
        """
        try:
            if fhir_server is None:
                fhir_server = FhirQuery.SERVICE_ROOT_URL
            resp = requests.get(
                f"{fhir_server}Immunization",
                headers=FhirQuery.ACCEPT_HEADER,
                params={"_include": "*", "date": "ge2021-01-01"},
            )
            resp.raise_for_status()
            dict_resp = resp.json()
            FhirQuery.__resolve_patients(entries=dict_resp["entry"])
            return dict_resp, str(resp.request)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error: {http_err}")
        except Exception as err:
            print(f"Other(requests) error: {err}")

    @staticmethod
    def __resolve_patients(entries: list):
        for entry in entries:
            if FhirQuery.__entry_has_immu_patient_ref(entry=entry):
                patient: dict = entry["resource"]["patient"]
                try:
                    resp = requests.get(
                        # TODO: fix so we use obj instance with fhir_server set at ctor time
                        f'{FhirQuery.SERVICE_ROOT_URL}{patient["reference"]}',
                        headers=FhirQuery.ACCEPT_HEADER,
                        params={"_summary": "data"},
                    )
                    resp.raise_for_status()
                    entry["resource"]["patient"] = resp.json()
                except requests.exceptions.HTTPError as http_err:
                    print(f"HTTP error: {http_err}")
                except Exception as err:
                    print(f"Other(requests) error: {err}")

    @staticmethod
    def __entry_has_immu_patient_ref(entry: dict) -> bool:
        return (
                "resource" in entry
                and "resourceType" in entry["resource"]
                and "patient" in entry["resource"]
                and "Immunization" == entry["resource"]["resourceType"]
                and "reference" in entry["resource"]["patient"]
        )
