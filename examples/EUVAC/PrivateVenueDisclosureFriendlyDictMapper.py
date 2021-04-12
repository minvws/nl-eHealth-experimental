from DisclosureLevel import DisclosureLevel
from CodeableConcept import CodeableConceptFriendlyDictMapper
from DisclosureCertificate import DisclosureCertificateFriendlyDictMapper
from Disclosures import DisclosurePrivateVenue

class PrivateVenueDisclosureFriendlyDictMapper:
    def build(self, value : DisclosurePrivateVenue):
        result = {}
        result["name"] = value.nam
        result["sex"] = value.sex
        result["immunizations"] = self.__buildImmunizations(value.v)
        result["certificate"] = DisclosureCertificateFriendlyDictMapper.build(value.c, DisclosureLevel.PrivateVenue)
        return result

    def __buildImmunizations(self, items):
        result = []
        for i in items:
            result.append(self.__buildImmunization(i))
        return result

    def __buildImmunization(self, value):
        result = {}
        result["targetDisease"] = CodeableConceptFriendlyDictMapper.buildList(value.tg)
        return result
