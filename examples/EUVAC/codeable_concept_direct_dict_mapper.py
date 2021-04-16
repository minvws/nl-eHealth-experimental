class CodeableConceptDirectDictMapper:
    @staticmethod
    def build(system, code):
        # omit display
        return {system: code}


# Urls for systems understood by this application
# Used for filtering CodeableConcepts e.g. for Vaccine Code or Target Disease.
class SystemUri:
    ICD10 = "http://hl7.org/fhir/sid/icd-10"
    SNOMED = "http://snomed.info/sct"
    WHOATC = "http://www.whocc.no/atc"  # J07 codes
    # usused "http://id.who.int/icd11/mms"
