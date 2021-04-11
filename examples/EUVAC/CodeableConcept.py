class CodeableConcept:
    def __init__(self, system, code):
        self.system = system
        self.code = code
        # omit display

class CodeableConceptFriendlyDictMapper:
    @staticmethod
    def build(value):
        result = {}
        result["system"] = value.system
        result["code"] = value.code
        # omit display
        return result

    @staticmethod
    def buildList(listValue):
        result = []
        for i in listValue:
            result.append(CodeableConceptFriendlyDictMapper.build(i))
        return result

class CodeableConceptDictMapper:
    @staticmethod
    def build(value):
        result = {}
        result["s"] = value.system
        result["c"] = value.code
        # omit display
        return result

    @staticmethod
    def buildList(listValue):
        result = []
        for i in listValue:
            result.append(CodeableConceptDictMapper.build(i))
        return result
