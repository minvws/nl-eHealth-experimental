from DisclosureCertificate import DisclosureCertificateBuilder
from DisclosureLevel import DisclosureLevel
from Disclosures import DisclosurePrivateVenue, ImmunizationPrivateVenue
from FhirInfoReader import FhirInfoReader


class PrivateVenueDisclosureBuilder:
    def __init__(self):
        self.__result = DisclosurePrivateVenue()
        self.__reader = None

    def build(self, patientId, info, cert):
        self.__reader = FhirInfoReader(info)
        self.__result.nam = self.__reader.getPatientName(patientId)
        self.__result.sex = self.__reader.getPatientSex(patientId)
        self.__result.v = self.__buildImmunizations(self.__reader.getImmunizationIdsForPatient(patientId))
        self.__result.c = DisclosureCertificateBuilder.build(cert, DisclosureLevel.PrivateVenue)
        return self.__result

    def __buildImmunizations(self, items):
        result = []
        for i in items:
            # TODO filter
            result.append(self.__buildImmunization(i))
        return result

    def __buildImmunization(self, immunizationId):
        result = ImmunizationPrivateVenue()
        result.tg = self.__reader.getImmunizationTargetDiseases(immunizationId)
        return result