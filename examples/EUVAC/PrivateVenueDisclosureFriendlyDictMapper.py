from CodeableConcept import CodeableConceptFriendlyDictMapper
from Disclosures import DisclosurePrivateVenue

class PrivateVenueDisclosureFriendlyDictMapper:
    def build(self, value : DisclosurePrivateVenue):
        result = {}
        result["name"] = value.nam
        result["sex"] = value.sex
        result["immunizations"] = self.__buildImmunizations(value.v)
        result["certificate"] = self.__buildCertificate(value.c)
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

    def __buildCertificate(self, value):
        result = {}
        result["issuer"] = value.Is
        result["validFrom"] = value.st
        result["validUntil"] = value.en
        result["schemaVersion"] = value.vr
        result["issuingAuthorityCountry"] = value.ia
        return result
