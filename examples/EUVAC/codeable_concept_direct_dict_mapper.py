class CodeableConceptDirectDictMapper:
    @staticmethod
    def build(system, code):
        # omit display
        return {"s": system, "c": code}
