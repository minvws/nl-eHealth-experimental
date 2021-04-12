from DisclosureLevel import DisclosureLevel
from FhirInfoCollector import FhirInfoCollector
from JsonParser import JsonParser
from PatientImmunizationBuilder import PatientImmunizationBuilder

class Annex1_min_data_set:

    @staticmethod
    def annex1_min_data_set(
            qry_res: dict, disclosure_level: DisclosureLevel, cert
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

        ret_data: dict = Annex1_min_data_set.__process_entries(qry_res, disclosure_level, cert)

        if "resourceType" in qry_res:
            if qry_res["resourceType"] == "Bundle":
                total_matches = qry_res["total"]
                ret_data["Total Matches"] = total_matches

        return ret_data

    @staticmethod
    def __process_entries(
            qry_res: dict, disclosure_level: DisclosureLevel, cert
    ) -> dict:
        result = {}

        # if "entry" in qry_res:
        disclosures = list()
        # for entry in qry_res["entry"]:

        collector = FhirInfoCollector()
        root = JsonParser.findPathSafe(qry_res, ["entry"])
        fhirInfo = collector.execute(root)

        for patientId in fhirInfo.immunizedPatients.keys():
            disclosure = PatientImmunizationBuilder.build(fhirInfo, patientId, disclosure_level, cert)
            # TODO check the shape of the data matches
            if disclosure is not None:
                disclosures.append(disclosure)

            result.update({"entries": disclosures})
        return result
