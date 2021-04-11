from CodeableConcept import CodeableConceptDictMapper


class BorderControlDisclosureDictMapper:
    def build(self, value):
        result = {}
        result["nam"] = value.nam
        result["pid"] = value.pid
        result["sex"] = value.sex
        result["dob"] = value.dob
        result["v"] = self.__buildImmunizations(value.v)
        result["c"] = self.__buildCertificate(value.c)
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


    def __buildCertificate(self, value):
        result = {}
        result["tg"] = value.Is
        result["id"] = value.id
        result["st"] = value.st
        result["en"] = value.en
        result["vr"] = value.vr
        result["ia"] = value.ia
        return result