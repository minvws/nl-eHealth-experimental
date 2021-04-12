from DisclosureCertificateDirectDictMapper import DisclosureCertificateDirectDictMapper
from DisclosureLevel import DisclosureLevel
from FhirInfoReader import FhirInfoReader


class MedicalDisclosureDirectDictMapper:
    def __init__(self):
        self.__reader = None

    def build(self, patientId, info, cert):
        if self.__reader is not None:
            raise ValueError("Cannot reuse object.")

        self.__reader = FhirInfoReader(info)
        result = {}
        result["nam"] = self.__reader.getPatientName(patientId)
        result["pid"] = self.__reader.getPatientPersonId(patientId)
        result["sex"] = self.__reader.getPatientSex(patientId)
        result["dob"] = self.__reader.getPatientDateOfBirth(patientId)
        result["v"] = self.__buildImmunizations(self.__reader.getImmunizationIdsForPatient(patientId))
        result["c"] = DisclosureCertificateDirectDictMapper.build(cert, DisclosureLevel.Medical)
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
        result["sc"] = self.__reader.getImmunizationSeriesCount(immunizationId)
        result["lt"] = self.__reader.getImmunizationLotNumber(immunizationId)
        result["oc"] = self.__reader.getImmunizationOccurrence(immunizationId)
        result["ao"] = self.__reader.getImmunizationActorOrganization(immunizationId)
        result["ap"] = self.__reader.getImmunizationActorPractitioner(immunizationId)
        result["lo"] = self.__reader.getImmunizationLocation(immunizationId)
        result["nx"] = self.__reader.getImmunizationNextOccurrence(immunizationId)
        return result

