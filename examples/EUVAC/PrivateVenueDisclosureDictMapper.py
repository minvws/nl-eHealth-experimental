from CodeableConcept import CodeableConceptDictMapper


class PrivateVenueDisclosureDictMapper:
    def build(self, value):
        result = {}
        result["nam"] = value.nam
        result["sex"] = value.sex
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
        return result

    def __buildCertificate(self, value):
        result = {}
        result["tg"] = value.Is
        result["st"] = value.st
        result["en"] = value.en
        result["vr"] = value.vr
        result["ia"] = value.ia
        return result