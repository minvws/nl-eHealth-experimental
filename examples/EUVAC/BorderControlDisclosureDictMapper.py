from CodeableConcept import CodeableConceptDictMapper
from DisclosureCertificate import DisclosureCertificateDictMapper
from DisclosureLevel import DisclosureLevel


class BorderControlDisclosureDictMapper:
    def build(self, value):
        result = {}
        result["nam"] = value.nam
        result["pid"] = value.pid
        result["sex"] = value.sex
        result["dob"] = value.dob
        result["v"] = self.__buildImmunizations(value.v)
        result["c"] = DisclosureCertificateDictMapper.build(value.c, DisclosureLevel.BorderControl)
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
        result["oc"] = value.oc
        result["lo"] = value.lo
        return result
