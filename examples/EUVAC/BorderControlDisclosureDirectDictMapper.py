from DisclosureCertificateDirectDictMapper import DisclosureCertificateDirectDictMapper
from DisclosureLevel import DisclosureLevel
from FhirInfoReader import FhirInfoReader


class BorderControlDisclosureDirectDictMapper:
    def __init__(self):
        self.__reader = None

    def build(self, patientId, info, cert):
        if self.__reader is not None:
            raise ValueError("Cannot reuse object.")

        self.__reader = FhirInfoReader(info)
        result = {}
        result["nam"] = self.__reader.getPatientName(patientId)
        result["pid"] = self.__reader.getPatientPersonId(patientId)
        result["dob"] = self.__reader.getPatientDateOfBirth(patientId)
        result["v"] = self.__buildImmunizations(self.__reader.getImmunizationIdsForPatient(patientId))
        result["c"] = DisclosureCertificateDirectDictMapper.build(cert, DisclosureLevel.BorderControl)
        return result

    def __buildImmunizations(self, items):
        result = []
        for i in items:
            result.append(self.__buildImmunization(i))
        return result

    def __buildImmunization(self, immunizationId):
        result = {}
        result["tg"] = self.__reader.getImmunizationTargetDiseases(immunizationId)
        result["cd"] = self.__reader.getImmunizationVaccineCodes(immunizationId)
        result["mp"] = self.__reader.getImmunizationMedicalProducts(immunizationId)
        result["ah"] = self.__reader.getImmunizationAuthorizationHolders(immunizationId)
        result["sn"] = self.__reader.getImmunizationSeriesNumber(immunizationId)
        result["oc"] = self.__reader.getImmunizationOccurrence(immunizationId)
        result["lo"] = self.__reader.getImmunizationLocation(immunizationId)
        return result