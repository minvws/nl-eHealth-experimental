from CodeableConcept import CodeableConceptFriendlyDictMapper


class MedicalDisclosureFriendlyDictMapper():
    def build(self, value):
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

    def __buildCertificate(self, value):
        result = {}
        result["issuer"] = value.Is
        result["identifier"] = value.id
        result["validFrom"] = value.st
        result["validTo"] = value.en
        result["schemaVersion"] = value.vr
        result["issuingAuthorityCountry"] = value.ia
        return result