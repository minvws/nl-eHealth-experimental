import requests
from typing import Optional


class FhirQueryImmunization:
    """ Performs FHIR Immunization queries against an HL7 FHIR R4 Server """

    # SERVICE_ROOT_URL = "https://server.fire.ly/r4/"  # fire.ly
    SERVICE_ROOT_URL = "https://hl7eu.onfhir.io/r4/"    # HL7 EU FHIR Server
    ACCEPT_HEADER = {"Accept": "application/fhir+json"}

    @staticmethod
    def find(fhir_server: Optional[str] = None) -> dict:
        """
        :param fhir_server: Service Root URL for FHIR server,
        can be None in which case SERVICE_ROOT_URL will be used
        :return: FHIR query result as dict
        """
        try:
            if fhir_server is None:
                fhir_server = FhirQueryImmunization.SERVICE_ROOT_URL
            resp = requests.get(
                f"{fhir_server}Immunization",
                headers=FhirQueryImmunization.ACCEPT_HEADER,
                params={"_summary": "data", "date": "ge2021-01-01",
                        "_include": "*"},
            )
            resp.raise_for_status()
            dict_resp = resp.json()
            return dict_resp
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error: {http_err}")
        except Exception as err:
            print(f"Other(requests) error: {err}")

    @staticmethod
    def resolve_patient(resource: dict) -> dict:
        patient_uri = resource["patient"]
        # Patient class?
        return {
            "name": "Gaby",
            "identifier": "ABC",
            "gender": "F",
            "birthDate": "2001-01-01",
        }
        # try:
        #     resp = requests.get(
        #         patient_uri,
        #         headers=FhirQueryImmunization.ACCEPT_HEADER,
        #         params={"_summary": "data"},
        #     )
        #     resp.raise_for_status()
        #     dict_resp = resp.json()
        #     return dict_resp
        # except requests.exceptions.HTTPError as http_err:
        #     print(f"HTTP error: {http_err}")
        # except Exception as err:
        #     print(f"Other(requests) error: {err}")
