from CodeableConceptDirectDictMapper import CodeableConceptDirectDictMapper
from JsonParser import JsonParser

'''
Used by disclosure builders to extract information fhir data structures
'''
class FhirInfoReader:
    def __init__(self, info):
        self._Info = info

    def getImmunizationIdsForPatient(self, patientId):
        return self._Info.immunizedPatients[patientId].immunizations

    def getPatientName(self, patientId):
        patient = self._Info.patients[patientId]
        name = JsonParser.findPath(patient, ["name"])[0]
        given = JsonParser.findPath(name, ["given"])[0]
        family = JsonParser.findPath(name, ["family"])
        return f'{given[0]}.{family}'

    def getPatientPersonId(self, patientId):
        return "a person Id TBA"

    def getPatientSex(self, patientId):
        return JsonParser.findPath(self._Info.patients[patientId], ["gender"])

    def getPatientDateOfBirth(self, patientId):
        return JsonParser.findPath(self._Info.patients[patientId], ["birthDate"])

    def getImmunizationTargetDiseases(self, immunizationId):
        protocolApplied = JsonParser.findPathSafe(self._Info.immunizations[immunizationId], ["protocolApplied"])
        if protocolApplied is None:
            # TODO if mandatory?
            return []

        if len(protocolApplied) == 0:
            # TODO if mandatory?
            return []

        # TODO handle more than one protocolApplied
        targetDisease = JsonParser.findPathSafe(protocolApplied[0], ["targetDisease"])
        if targetDisease is None:
            # TODO if mandatory?
            return []

        if len(targetDisease) == 0:
            # TODO if mandatory?
            return []

        candidates = self.getCodeableConcepts(targetDisease[0])
        # TODO filter
        # TODO format
        return candidates

    def getReferenceDefault(self, node):
        reference = JsonParser.findPathSafe(node, ["reference"])
        typeUri = JsonParser.findPathSafe(node, ["type"])
        if not reference is None and not typeUri is None:
            return f'{typeUri}/{reference}'

        # TODO fallback to ?
        # identifierNode = JsonParser.findPathSafe("identifier")
        displayText = JsonParser.findPathSafe(node, ["display"])
        return displayText  # cos we have a few with just this...

    def getCodeableConcepts(self, node):
        if isinstance(node, dict):
            coding = JsonParser.findPathSafe(node, ["coding"])
            if coding is not None:
                return self.getCodeableConceptsFromList(coding)

        raise ValueError("Cannot parse codeable concept.")

    def getCodeableConceptsFromList(self, items):
        result = []
        for i in items:
            system = i["system"]
            code = i["code"]
            if not (system is None or code is None):
                item = CodeableConceptDirectDictMapper.build(system, code)
                result.append(item)
        return result

    def getImmunizationVaccineCodes(self, immunizationId):
        i = self._Info.immunizations[immunizationId]
        items = self.getCodeableConcepts(JsonParser.findPath(i, ["vaccineCode"]))
        # TODO filter
        # TODO format
        return items

    def getImmunizationMedicalProducts(self, immunizationId):
        protocolApplied = JsonParser.findPathSafe(self._Info.immunizations[immunizationId], ["protocolApplied"])
        if protocolApplied is None:
            # TODO if mandatory?
            return []

        if len(protocolApplied) == 0:
            return []

        # TODO handle more than one protocolApplied
        targetDisease = JsonParser.findPathSafe(protocolApplied[0], ["?????????"])
        if targetDisease is None:
            return []

        items = self.getCodeableConcepts(targetDisease)
        # TODO filter
        # TODO format
        return items

    def getImmunizationAuthorizationHolders(self, immunizationId):
        manufacturer = JsonParser.findPathSafe(self._Info.immunizations[immunizationId], ["manufacturer"])
        if manufacturer is None:
            # TODO mandatory?
            return "TODO AuthorisationHolder not present."

        return self.getReferenceDefault(manufacturer)

    def getImmunizationSeriesNumber(self, immunizationId):
        result = JsonParser.findPathSafe(self._Info.immunizations[immunizationId], ["protocolApplied", "doseNumberPositiveInt"])
        # TODO action if missing?
        if result is None:
            return "TODO Series Number not present."

        return result

    def getImmunizationSeriesCount(self, immunizationId):
        result = JsonParser.findPathSafe(self._Info.immunizations[immunizationId], ["protocolApplied", "seriesDosesPositiveInt"])
        # TODO action if missing?
        if result is None:
            return "TODO Series Count not present."

        return result

    def getImmunizationLocation(self, immunizationId):
        reference = JsonParser.findPathSafe(self._Info.immunizations[immunizationId], ["location", "reference"])
        # TODO fallbacks?
        if reference is None:
            return "TODO Immunization Location not present."

        lookup = reference[9:]  # chop Location/ off the start of the reference
        loc = self._Info.locations[lookup]
        if loc is None:
            return "TODO Immunization Location not in search results."

        result = JsonParser.findPathSafe(loc, ["address", "country"])
        if result is None:
            return "TODO country not in location."

        return result

    def getImmunizationOccurrence(self, immunizationId):
        return JsonParser.findPathSafe(self._Info.immunizations[immunizationId], ["occurrenceDateTime"])

    def getImmunizationActorOrganization(self, immunizationId):
        performerList = JsonParser.findPathSafe(self._Info.immunizations[immunizationId], ["performer"])
        result = []
        for i in performerList:
            value = JsonParser.findPathSafe(i, ["actor", "reference"])
            if value is not None and value.startswith("Organization"):
                result.append(value)
        return result

    def getImmunizationActorPractitioner(self, immunizationId):
        performerList = JsonParser.findPathSafe(self._Info.immunizations[immunizationId], ["performer"])
        result = []
        for i in performerList:
            value = JsonParser.findPathSafe(i, ["actor", "reference"])
            if value is not None and value.startswith("Practitioner"):
                result.append(value)
        return result

    def getImmunizationNextOccurrence(self, immunizationId):
        return "TODO yyyy-mm-dd"

    def getImmunizationLotNumber(self, immunizationId):
        result = JsonParser.findPathSafe(self._Info.immunizations[immunizationId],
                                         ["lotNumber"])
        # TODO action if missing?
        if result is None:
            return "TODO Lot Number not present."

        return result
