from json_parser import JsonParser
from uvci_example_builder import UvciExampleBuilder


class ImmunizedPatient:
    def __init__(self):
        self.immunizations = []


class FhirInfo:
    def __init__(self):
        self.immunized_patients = {}
        self.immunizations = {}
        self.patients = {}
        self.locations = {}
        self.organisations = {}
        self.practitioners = {}


class FhirInfoCollector:
    def __init__(self):
        self.__result = FhirInfo()

    """
    Cleans up and indexes an initial result of an FHIR search result.
    root is the parent element of a resources collection
    TODO move reference resolving here - such as location
    TODO make this the command to find/build the necessary input for a disclosure
    """

    def execute(self, root: dict) -> FhirInfo:
        # index contents, strip noise nodes
        for i in root:
            node = JsonParser.find_path_safe(i, ["resource"])
            if node is None:
                continue
            node_type = JsonParser.find_path_safe(i, ["resource", "resourceType"])
            if node_type is None:
                continue
            node_id = JsonParser.find_path(i, ["resource", "id"])
            if node_id is None:
                continue
            if node_type == "Immunization":
                self.__result.immunizations[node_id] = node
                continue
            if node_type == "Patient":
                self.__result.patients[node_id] = node
                continue
            if node_type == "Location":
                self.__result.locations[node_id] = node
                continue
            if node_type == "Organization":
                self.__result.organisations[node_id] = node
                continue
            # TODO any practitioners in root?

        # map immunizations to patient
        # add an example semi-realistic UVCI to each immunization
        for i in self.__result.immunizations.values():
            # TODO was patient_id = JsonParser.findPathSafe(i, ["patient", "id"])
            patient_id = JsonParser.find_path_safe(i, ["patient", "reference"])
            if patient_id is None:
                continue

            patient_id = patient_id[8:]

            if patient_id not in self.__result.immunized_patients:
                self.__result.immunized_patients[patient_id] = ImmunizedPatient()

            self.__result.immunized_patients[patient_id].immunizations.append(
                JsonParser.find_path(i, ["id"])
            )
            i["uvci"] = {
                "value": UvciExampleBuilder.get_example(),
                "validFrom": "2021-01-01",
                "validUntil": "2022-02-03",
            }
        return self.__result
