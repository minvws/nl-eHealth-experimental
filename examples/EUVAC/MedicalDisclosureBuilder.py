from DisclosureCertificate import DisclosureCertificateBuilder
from DisclosureLevel import DisclosureLevel
from Disclosures import DisclosureMedical, ImmunizationMedical
from FhirInfoReader import FhirInfoReader


class MedicalDisclosureBuilder:
    def __init__(self):
        self.__result = DisclosureMedical()
        self.__reader = None

    def build(self, patientId, info, cert):
        if self.__reader is not None:
            raise ValueError("Cannot reuse object.")

        self.__reader = FhirInfoReader(info)
        self.__result.nam = self.__reader.getPatientName(patientId)
        self.__result.pid = self.__reader.getPatientPersonId(patientId)
        self.__result.sex = self.__reader.getPatientSex(patientId)
        self.__result.dob = self.__reader.getPatientDateOfBirth(patientId)
        self.__result.v = self.__buildImmunizations(self.__reader.getImmunizationIdsForPatient(patientId))
        self.__result.c = DisclosureCertificateBuilder.build(cert, DisclosureLevel.Medical)
        return self.__result

    def __buildImmunizations(self, items):
        result = []
        for i in items:
            # TODO filter
            result.append(self.__buildImmunization(i))
        return result

    def __buildImmunization(self, immunizationId):
        result = ImmunizationMedical()
        result.tg = self.__reader.getImmunizationTargetDiseases(immunizationId)
        result.cd = self.__reader.getImmunizationVaccineCodes(immunizationId)
        result.mp = self.__reader.getImmunizationMedicalProducts(immunizationId)
        result.ah = self.__reader.getImmunizationAuthorizationHolders(immunizationId)
        result.sn = self.__reader.getImmunizationSeriesNumber(immunizationId)
        result.sc = self.__reader.getImmunizationSeriesCount(immunizationId)
        result.oc = self.__reader.getImmunizationOccurrence(immunizationId)
        result.ao = self.__reader.getImmunizationActorOrganization(immunizationId)
        result.ap = self.__reader.getImmunizationActorPractitioner(immunizationId)
        result.lo = self.__reader.getImmunizationLocation(immunizationId)
        result.nx = self.__reader.getImmunizationNextOccurrence(immunizationId)
        return result
