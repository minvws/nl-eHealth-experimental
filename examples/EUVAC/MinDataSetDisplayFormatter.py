from DisclosureFriendlyDictMapperFactory import DisclosureFriendlyDictMapperFactory
from DisclosureLevel import DisclosureLevel
from Annex1_min_data_set import Annex1_min_data_set as a1

class MinDataSetDisplayFormatter:
    @staticmethod
    def build(data):
        entries = []
        entries.append(MinDataSetDisplayFormatter.__buildAndFormatSet(data, DisclosureLevel.PrivateVenue))
        entries.append(MinDataSetDisplayFormatter.__buildAndFormatSet(data, DisclosureLevel.BorderControl))
        entries.append(MinDataSetDisplayFormatter.__buildAndFormatSet(data, DisclosureLevel.Medical))
        result = {}
        result["entries"] = entries
        return result

    @staticmethod
    def __buildAndFormatSet(data, dl):
        result = {}
        result["disclosureLevel"] = MinDataSetDisplayFormatter.__Format(dl)
        disclosures = a1.annex1_min_data_set(data, dl)
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
