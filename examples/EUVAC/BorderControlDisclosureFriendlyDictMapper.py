from CodeableConcept import CodeableConceptFriendlyDictMapper
from Disclosures import DisclosureBorderControl

class BorderControlDisclosureFriendlyDictMapper:
    def build(self, value: DisclosureBorderControl):
        result = {}
        result["name"] = value.nam
        result["personId"] = value.pid
        result["sex"] = value.sex
        result["dateOfBirth"] = value.dob
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
        result["targetDesease"] = CodeableConceptFriendlyDictMapper.buildList(value.tg)
        result["vaccineCode"] = CodeableConceptFriendlyDictMapper.buildList(value.cd)
        result["medicalProduct"] = CodeableConceptFriendlyDictMapper.buildList(value.mp)
        result["manufacturer"] = value.ah
        result["seriesNumber"] = value.sn
        result["occurance"] = value.oc
        result["location"] = value.lo
        return result

    def __buildCertificate(self, value):
        result = {}
        result["issuer"] = value.Is
        result["UVCI"] = value.id
        result["validFrom"] = value.st
        result["validUntil"] = value.en
        result["schemaVersion"] = value.vr
        result["issuingAuthorityCountry"] = value.ia
        return result