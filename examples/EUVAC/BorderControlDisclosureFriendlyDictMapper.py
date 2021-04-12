from DisclosureLevel import DisclosureLevel
from CodeableConcept import CodeableConceptFriendlyDictMapper
from DisclosureCertificate import DisclosureCertificateFriendlyDictMapper
from Disclosures import DisclosureBorderControl

class BorderControlDisclosureFriendlyDictMapper:
    def build(self, value: DisclosureBorderControl):
        result = {}
        result["name"] = value.nam
        result["personId"] = value.pid
        result["sex"] = value.sex
        result["dateOfBirth"] = value.dob
        result["immunizations"] = self.__buildImmunizations(value.v)
        result["certificate"] = DisclosureCertificateFriendlyDictMapper.build(value.c, DisclosureLevel.BorderControl)
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
        result["occurrence"] = value.oc
        result["location"] = value.lo
        return result
