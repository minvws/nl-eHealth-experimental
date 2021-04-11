from DisclosureCertificate import DisclosureCertificate
from Disclosures import ImmunizationBorderControl, DisclosureBorderControl
from FhirInfoReader import FhirInfoReader

class BorderControlDisclosureBuilder:
    def __init__(self):
        self.__result = DisclosureBorderControl()
        self.__reader = None

    def build(self, patientId, info):
        self.__reader = FhirInfoReader(info)
        self.__result.nam = self.__reader.getPatientName(patientId)
        self.__result.pid = self.__reader.getPatientPersonId(patientId)
        self.__result.sex = self.__reader.getPatientSex(patientId)
        self.__result.dob = self.__reader.getPatientDateOfBirth(patientId)
        self.__result.v = self.__buildImmunizations(self.__reader.getImmunizationIdsForPatient(patientId))
        self.__result.c = DisclosureCertificate()
        return self.__result

    def __buildImmunizations(self, items):
        result = []
        for i in items:
            # TODO filter
            result.append(self.__buildImmunization(i))
        return result

    def __buildImmunization(self, immunizationId):
        result = ImmunizationBorderControl()
        result.tg = self.__reader.getImmunizationTargetDiseases(immunizationId)
        result.cd = self.__reader.getImmunizationVaccineCodes(immunizationId)
        result.mp = self.__reader.getImmunizationMedicalProducts(immunizationId)
        result.ah = self.__reader.getImmunizationAuthorizationHolders(immunizationId)
        result.sn = self.__reader.getImmunizationSeriesNumber(immunizationId)
        result.oc = self.__reader.getImmunizationOccurrence(immunizationId)
        result.lo = self.__reader.getImmunizationLocation(immunizationId)
        return result
