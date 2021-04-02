import requests


class FhirQueryImmunization:
    """ Performs FHIR Immunization queries against an HL7 FHIR R4 Server """

    # SERVICE_ROOT_URL = "https://fhir-open.cerner.com/r4/ec2458f2-1e24-41c8-b71b-0e701af7583d/"    # Cerner
    # SERVICE_ROOT_URL = "https://try.smilecdr.com:8000/baseR4/"    # SmileCDR
    SERVICE_ROOT_URL = "https://server.fire.ly/r4/"  # fire.ly
    ACCEPT_HEADER = {"Accept": "application/fhir+json"}

    @staticmethod
    def find():
        try:
            resp = requests.get(
                f"{FhirQueryImmunization.SERVICE_ROOT_URL}Immunization",
                headers=FhirQueryImmunization.ACCEPT_HEADER,
                params={"_summary": "data", "date": "ge2021-01-01"},
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
