from DisclosureCertificate import DisclosureCertificate
from Disclosures import DisclosurePrivateVenue, ImmunizationPrivateVenue
from FhirInfoReader import FhirInfoReader


class PrivateVenueDisclosureBuilder:
    def __init__(self):
        self._result = DisclosurePrivateVenue()
        self._reader = None

    def build(self, patientId, info):
        self._reader = FhirInfoReader(info)
        self._result.nam = self._reader.getPatientName(patientId)
        self._result.sex = self._reader.getPatientSex(patientId)
        self._result.v = self.__buildImmunizations(self._reader.getImmunizationIdsForPatient(patientId))
        self._result.c = DisclosureCertificate()
        return self._result


    def __buildImmunizations(self, items):
        result = []
        for i in items:
            # TODO filter
            result.append(self.__buildImmunization(i))
        return result


    def __buildImmunization(self, immunizationId):
        result = ImmunizationPrivateVenue()
        result.tg = self._reader.getImmunizationTargetDiseases(immunizationId)
        return result