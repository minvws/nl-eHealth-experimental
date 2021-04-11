from JsonParser import JsonParser


class ImmunizedPatient:
    def __init__(self):
        self.immunizations = []


class FhirInfo:
    def __init__(self):
        self.immunizedPatients = {}
        self.immunizations = {}
        self.patients = {}
        self.locations = {}
        self.organisations = {}
        self.practitioners = {}


class FhirInfoCollector:
    def __init__(self):
        self._result = FhirInfo()
    '''
    Cleans up and indexes an initial result of an FHIR search result.
    root is the parent element of a resources collection
    TODO move reference resolving here - such as location
    TODO make this the command to find/build the necessary input for a disclosure
    '''
    def execute(self, root):
        # index contents, strip noise nodes
        for i in root:
            node = JsonParser.findPathSafe(i, ["resource"])
            if node is None:
                continue
            nodeType = JsonParser.findPathSafe(i, ["resource", "resourceType"])
            if nodeType is None:
                continue
            nodeId = JsonParser.findPath(i, ["resource", "id"])
            if nodeId is None:
                continue
            if nodeType == "Immunization":
                self._result.immunizations[nodeId] = node
                continue
            if nodeType == "Patient":
                self._result.patients[nodeId] = node
                continue
            if nodeType == "Location":
                self._result.locations[nodeId] = node
                continue
            if nodeType == "Organization":
                self._result.organisations[nodeId] = node
                continue
            # TODO any practitioners in root?

        # resolve references, map immunizations to patient
        for i in self._result.immunizations.values():
            self._resolvePatients(i)
            self._resolvePerformers(i)
            patientId = JsonParser.findPathSafe(i, ["patient", "id"])
            if patientId is None:
                continue

            if patientId not in self._result.immunizedPatients:
                self._result.immunizedPatients[patientId] = ImmunizedPatient()

            self._result.immunizedPatients[patientId].immunizations.append(JsonParser.findPath(i, ["id"]))

        return self._result

    def _resolvePatients(self, immunization):
        patientId = JsonParser.findPathSafe(immunization, ["patient", "patientId"])
        if not patientId is None and not patientId in self._result.patients.keys():
            self._result.patients[patientId] = self.__resolveReference("Patient/" + patientId)

    def _resolvePerformers(self, immunization):
        actors = JsonParser.findPathSafe(immunization, ["performer"])
        if actors is None:
            return

        for i in actors:
            ref = JsonParser.findPathSafe(i, ["reference"])
            if ref is None:
                continue
            if ref.startswith("Organization/") and not ref in self._result.organisations:
                found = self.__resolveReference(ref)
                self._result.organisations[ref] = found
            if ref.startswith("Practitioner/") and not ref in self._result.practitioners:
                found = self.__resolveReference(ref)
                self._result.practitioners[ref] = found

    def __resolveReference(self, item):
        #     try:
        #         resp = requests.get(
        #             f'{FhirQuery.SERVICE_ROOT_URL}{item}',
        #             headers=FhirQuery.ACCEPT_HEADER,
        #             params={"_summary": "data"},
        #         )
        #         resp.raise_for_status()
        #         return resp.json()
        #     except requests.exceptions.HTTPError as http_err:
        #         print(f"HTTP error: {http_err}")
        #     except Exception as err:
        #         print(f"Other(requests) error: {err}")
        return None