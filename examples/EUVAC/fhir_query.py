import requests
from typing import Optional, Tuple


class FhirQueryImmunization:
    """ Performs FHIR Immunization queries against an HL7 FHIR R4 Server """

    # SERVICE_ROOT_URL = "https://server.fire.ly/r4/"  # fire.ly
    SERVICE_ROOT_URL = "https://hl7eu.onfhir.io/r4/"    # HL7 EU FHIR Server
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
                fhir_server = FhirQueryImmunization.SERVICE_ROOT_URL
            resp = requests.get(
                f"{fhir_server}Immunization",
                headers=FhirQueryImmunization.ACCEPT_HEADER,
                params={"_include": "*", "date": "ge2021-01-01"},
            )
            resp.raise_for_status()
            dict_resp = resp.json()
            return dict_resp, str(resp.request)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error: {http_err}")
        except Exception as err:
            print(f"Other(requests) error: {err}")

    @staticmethod
    def resolve_patient(resource: dict) -> dict:
        patient: dict = resource["patient"]
        if "reference" not in patient:
            # reference already resolved (via "?_include=" in FHIR query?), so just return it
            return patient

        patient_uri = patient["reference"]
        try:
            resp = requests.get(
                f"{FhirQueryImmunization.SERVICE_ROOT_URL}{patient_uri}",
                headers=FhirQueryImmunization.ACCEPT_HEADER,
                params={"_summary": "data"},
            )
            resp.raise_for_status()
            dict_resp = resp.json()
            patient_resp: dict = {}
            # take first name element in list, this tends to be the "default" version in use
            if "name" in dict_resp:
                patient_resp["name"] = dict_resp["name"][0]
            if "birthDate" in dict_resp:
                patient_resp["birthDate"] = dict_resp["birthDate"]
            if "gender" in dict_resp:
                patient_resp["gender"] = dict_resp["gender"]
            if "identifier" in dict_resp:
                patient_resp["identifier"] = dict_resp["identifier"]
            return patient_resp
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error: {http_err}")
        except Exception as err:
            print(f"Other(requests) error: {err}")
