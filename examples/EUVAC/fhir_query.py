import requests
from immu_parser import ImmuEntryParser
from min_data_set import MinDataSet, MinDataSetFactory
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
            FhirQuery.resolve_patients(entries=dict_resp["entry"])
            return dict_resp, str(resp.request)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error: {http_err}")
        except Exception as err:
            print(f"Other(requests) error: {err}")

    @staticmethod
    def resolve_patients(entries: list):
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
    def annex1_min_data_set(
        qry_res: dict, disclosure_level: MinDataSetFactory.DisclosureLevel
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
        ret_data: dict = FhirQuery.__process_entries(
            qry_res=qry_res, disclosure_level=disclosure_level
        )
        if "resourceType" in qry_res:
            if qry_res["resourceType"] == "Bundle":
                total_matches = qry_res["total"]
                ret_data["Total Matches"] = total_matches
        return ret_data

    @staticmethod
    def __process_entries(
        qry_res: dict, disclosure_level: MinDataSetFactory.DisclosureLevel
    ) -> dict:
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

    @staticmethod
    def __entry_has_immu_patient_ref(entry: dict) -> bool:
        return (
            "resource" in entry
            and "resourceType" in entry["resource"]
            and "patient" in entry["resource"]
            and "Immunization" == entry["resource"]["resourceType"]
            and "reference" in entry["resource"]["patient"]
        )
