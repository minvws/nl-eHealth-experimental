import requests


class FhirQuery:
    """ Performs FHIR Immunization queries against an HL7 FHIR R4 Server """

    # SERVICE_ROOT_URL = "https://server.fire.ly/r4/"  # fire.ly
    SERVICE_ROOT_URL = "https://hl7eu.onfhir.io/r4/"  # HL7 EU FHIR Server
    ACCEPT_HEADER = {"Accept": "application/fhir+json"}

    def __init__(self, fhir_server: str = None):
        """
        :param fhir_server: Service Root URL for FHIR server,
        can be None in which case SERVICE_ROOT_URL will be used
        """
        # use "falsy" boolean eval for arg fhir_server here -> empty string also false etc
        self.__fhir_server = fhir_server if fhir_server else FhirQuery.SERVICE_ROOT_URL
        # self.__fhir_server shall end in '/' -> so we don't have to check anywhere else
        if self.__fhir_server[:-1] != "/":
            self.__fhir_server = self.__fhir_server + "/"

    def find(self, query_params: dict = None):
        """
        :param query_params:
        :return: (FHIR query result as dict, HTTP request as str)
        """
        try:
            resp = requests.get(
                f"{self.__fhir_server}Immunization",
                headers=FhirQuery.ACCEPT_HEADER,
                params={"_include": "*", "date": "ge2021-01-01"}
                if query_params is None
                else query_params,
            )
            resp.raise_for_status()
            dict_resp = resp.json()
            return dict_resp, str(resp.request)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error: {http_err}")
        except Exception as err:
            print(f"Other(requests) error: {err}")
