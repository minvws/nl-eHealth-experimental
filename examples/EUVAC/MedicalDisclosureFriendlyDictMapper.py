from DisclosureLevel import DisclosureLevel
from CodeableConcept import CodeableConceptFriendlyDictMapper
from DisclosureCertificate import DisclosureCertificateFriendlyDictMapper


class MedicalDisclosureFriendlyDictMapper():
    def build(self, value):
        result = {}
        result["name"] = value.nam
        result["personId"] = value.pid
        result["sex"] = value.sex
        result["dateOfBirth"] = value.dob
        result["immunizations"] = self.__buildImmunizations(value.v)
        result["certificate"] = DisclosureCertificateFriendlyDictMapper.build(value.c, DisclosureLevel.Medical)
        return result

    def __buildImmunizations(self, items):
        result = []
        for i in items:
            result.append(self.__buildImmunization(i))
        return result

    def __buildImmunization(self, value):
        result = {}
        result["targetDisease"] = CodeableConceptFriendlyDictMapper.buildList(value.tg)
        result["vaccineCode"] = CodeableConceptFriendlyDictMapper.buildList(value.cd)
        result["medicalProduct"] = CodeableConceptFriendlyDictMapper.buildList(value.mp)
        result["manufacturer"] = value.ah
        result["seriesNumber"] = value.sn
        result["seriesCount"] = value.sc
        result["occurrence"] = value.oc
        result["actorOrganisation"] = value.ao
        result["actorPractitioner"] = value.ap
        result["location"] = value.lo
        result["nextOccurrence"] = value.nx
        return result
