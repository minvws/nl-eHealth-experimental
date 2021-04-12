from DisclosureFriendlyDictMapperFactory import DisclosureFriendlyDictMapperFactory
from DisclosureLevel import DisclosureLevel
from Annex1_min_data_set import Annex1_min_data_set as a1

class MinDataSetDisplayFormatter:
    @staticmethod
    def build(data, cert):
        entries = []
        entries.append(MinDataSetDisplayFormatter.__buildAndFormatSet(data, DisclosureLevel.PrivateVenue, cert))
        entries.append(MinDataSetDisplayFormatter.__buildAndFormatSet(data, DisclosureLevel.BorderControl, cert))
        entries.append(MinDataSetDisplayFormatter.__buildAndFormatSet(data, DisclosureLevel.Medical, cert))
        result = {}
        result["entries"] = entries
        return result

    @staticmethod
    def __buildAndFormatSet(data, dl, cert):
        result = {}
        result["disclosureLevel"] = MinDataSetDisplayFormatter.__Format(dl)
        disclosures = a1.annex1_min_data_set(data, dl, cert)
        # result["Total Matches"] = disclosures["Total Matches"]
        entries = []
        for i in disclosures["entries"]:
            entries.append(DisclosureFriendlyDictMapperFactory.build(dl).build(i))
        result["entries"] = entries
        return result

    @staticmethod
    def __Format(dl):
        if dl == DisclosureLevel.PrivateVenue:
            return "PrivateVenue"
        if dl == DisclosureLevel.BorderControl:
            return "BorderControl"
        return "Medical"
