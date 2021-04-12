from CodeableConcept import CodeableConceptDictMapper
from DisclosureCertificate import DisclosureCertificateDictMapper
from DisclosureLevel import DisclosureLevel


class MedicalDisclosureDictMapper:
    def build(self, value):
        result = {}
        result["nam"] = value.nam
        result["pid"] = value.pid
        result["sex"] = value.sex
        result["dob"] = value.dob
        result["v"] = self.__buildImmunizations(value.v)
        result["c"] = DisclosureCertificateDictMapper.build(value.c, DisclosureLevel.Medical)
        return result

    def __buildImmunizations(self, items):
        result = []
        for i in items:
            result.append(self.__buildImmunization(i))
        return result

    def __buildImmunization(self, value):
        result = {}
        result["tg"] = CodeableConceptDictMapper.buildList(value.tg)
        result["cd"] = CodeableConceptDictMapper.buildList(value.cd)
        result["mp"] = CodeableConceptDictMapper.buildList(value.mp)
        result["ah"] = value.ah
        result["sn"] = value.sn
        result["sc"] = value.sc
        result["oc"] = value.oc
        result["ao"] = value.ao
        result["ap"] = value.ap
        result["lo"] = value.lo
        result["nx"] = value.nx
        return result
