from DisclosureLevel import DisclosureLevel
from CodeableConcept import CodeableConceptDictMapper
from DisclosureCertificate import DisclosureCertificateDictMapper


class PrivateVenueDisclosureDictMapper:
    def build(self, value):
        result = {}
        result["nam"] = value.nam
        result["sex"] = value.sex
        result["v"] = self.__buildImmunizations(value.v)
        result["c"] = DisclosureCertificateDictMapper.build(value.c, DisclosureLevel.PrivateVenue)
        return result

    def __buildImmunizations(self, items):
        result = []
        for i in items:
            result.append(self.__buildImmunization(i))
        return result

    def __buildImmunization(self, value):
        result = {}
        result["tg"] = CodeableConceptDictMapper.buildList(value.tg)
        return result
