class CodeableConceptDirectDictMapper:
    @staticmethod
    def build(system, code):
        result = {}
        result["s"] = system
        result["c"] = code
        # omit display
        return result
