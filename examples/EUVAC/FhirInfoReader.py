from CodeableConceptDirectDictMapper import CodeableConceptDirectDictMapper
from JsonParser import JsonParser

'''
Used by disclosure builders to extract information fhir data structures
'''


class FhirInfoReader:
    def __init__(self, info):
        self.__Info = info

    def get_immunization_ids_for_patient(self, patient_id):
        return self.__Info.immunizedPatients[patient_id].immunizations

    def get_patient_name(self, patient_id):
        patient = self.__Info.patients[patient_id]
        name = JsonParser.find_path(patient, ["name"])[0]
        given = JsonParser.find_path(name, ["given"])[0]
        family = JsonParser.find_path(name, ["family"])
        return f'{given[0]}.{family}'

    # noinspection PyMethodMayBeStatic
    def get_patient_person_id(self, patient_id):
        return "a person Id TBA"

    def get_patient_sex(self, patient_id):
        return JsonParser.find_path(self.__Info.patients[patient_id], ["gender"])

    def get_patient_date_of_birth(self, patient_id):
        return JsonParser.find_path(self.__Info.patients[patient_id], ["birthDate"])

    def get_immunization_target_diseases(self, immunization_id: str):
        protocolApplied = JsonParser.find_path_safe(self.__Info.immunizations[immunization_id], ["protocolApplied"])
        if protocolApplied is None:
            # TODO if mandatory?
            return []

        if len(protocolApplied) == 0:
            # TODO if mandatory?
            return []

        # TODO handle more than one protocolApplied
        targetDisease = JsonParser.find_path_safe(protocolApplied[0], ["targetDisease"])
        if targetDisease is None:
            # TODO if mandatory?
            return []

        if len(targetDisease) == 0:
            # TODO if mandatory?
            return []

        candidates = self.__get_codeable_concepts(targetDisease[0])
        # TODO filter
        # TODO format
        return candidates

    def __get_reference_default(self, node):
        reference = JsonParser.find_path_safe(node, ["reference"])
        typeUri = JsonParser.find_path_safe(node, ["type"])
        if reference is not None and typeUri is not None:
            return f'{typeUri}/{reference}'

        # TODO fallback to ?
        # identifierNode = JsonParser.findPathSafe("identifier")
        displayText = JsonParser.find_path_safe(node, ["display"])
        return displayText  # cos we have a few with just this...

    def __get_codeable_concepts(self, node):
        if isinstance(node, dict):
            coding = JsonParser.find_path_safe(node, ["coding"])
            if coding is not None:
                return self.__get_codeable_concepts_from_list(coding)

        raise ValueError("Cannot parse codeable concept.")

    def __get_codeable_concepts_from_list(self, items):
        result = []
        for i in items:
            system = i["system"]
            code = i["code"]
            if not (system is None or code is None):
                item = CodeableConceptDirectDictMapper.build(system, code)
                result.append(item)
        return result

    def get_immunization_vaccine_codes(self, immunization_id: str):
        i = self.__Info.immunizations[immunization_id]
        items = self.__get_codeable_concepts(JsonParser.find_path(i, ["vaccineCode"]))
        # TODO filter
        # TODO format
        return items

    def get_immunization_medical_products(self, immunization_id: str):
        protocolApplied = JsonParser.find_path_safe(self.__Info.immunizations[immunization_id], ["protocolApplied"])
        if protocolApplied is None:
            # TODO if mandatory?
            return []

        if len(protocolApplied) == 0:
            return []

        # TODO handle more than one protocolApplied
        targetDisease = JsonParser.find_path_safe(protocolApplied[0], ["?????????"])
        if targetDisease is None:
            return []

        items = self.__get_codeable_concepts(targetDisease)
        # TODO filter
        # TODO format
        return items

    def get_immunization_authorization_holders(self, immunization_id: str):
        manufacturer = JsonParser.find_path_safe(self.__Info.immunizations[immunization_id], ["manufacturer"])
        if manufacturer is None:
            # TODO mandatory?
            return "TODO AuthorisationHolder not present."

        return self.__get_reference_default(manufacturer)

    def get_immunization_series_number(self, immunization_id: str):
        result = JsonParser.find_path_safe(self.__Info.immunizations[immunization_id],
                                           ["protocolApplied", "doseNumberPositiveInt"])
        # TODO action if missing?
        if result is None:
            return "TODO Series Number not present."

        return result

    def get_immunization_series_count(self, immunization_id: str):
        result = JsonParser.find_path_safe(self.__Info.immunizations[immunization_id],
                                           ["protocolApplied", "seriesDosesPositiveInt"])
        # TODO action if missing?
        if result is None:
            return "TODO Series Count not present."

        return result

    def get_immunization_location(self, immunization_id: str):
        reference = JsonParser.find_path_safe(self.__Info.immunizations[immunization_id], ["location", "reference"])
        # TODO fallbacks?
        if reference is None:
            return "TODO Immunization Location not present."

        lookup = reference[9:]  # chop Location/ off the start of the reference
        loc = self.__Info.locations[lookup]
        if loc is None:
            return "TODO Immunization Location not in search results."

        result = JsonParser.find_path_safe(loc, ["address", "country"])
        if result is None:
            return "TODO country not in location."

        return result

    def get_immunization_occurrence(self, immunization_id: str):
        return JsonParser.find_path_safe(self.__Info.immunizations[immunization_id], ["occurrenceDateTime"])

    def get_immunization_actor_organization(self, immunization_id: str):
        performerList = JsonParser.find_path_safe(self.__Info.immunizations[immunization_id], ["performer"])
        result = []
        for i in performerList:
            value = JsonParser.find_path_safe(i, ["actor", "reference"])
            if value is not None and value.startswith("Organization"):
                result.append(value)
        return result

    def get_immunization_actor_practitioner(self, immunization_id: str):
        performerList = JsonParser.find_path_safe(self.__Info.immunizations[immunization_id], ["performer"])
        result = []
        for i in performerList:
            value = JsonParser.find_path_safe(i, ["actor", "reference"])
            if value is not None and value.startswith("Practitioner"):
                result.append(value)
        return result

    def get_immunization_next_occurrence(self, immunization_id: str):
        return "TODO yyyy-mm-dd"

    def get_immunization_lot_number(self, immunization_id: str):
        result = JsonParser.find_path_safe(self.__Info.immunizations[immunization_id],
                                           ["lotNumber"])
        # TODO action if missing?
        if result is None:
            return "TODO Lot Number not present."

        return result
