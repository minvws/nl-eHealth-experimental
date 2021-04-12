from cryptography.x509 import Certificate

from DisclosureCertificateDirectDictMapper import DisclosureCertificateDirectDictMapper
from DisclosureLevel import DisclosureLevel
from FhirInfoCollector import FhirInfo
from FhirInfoReader import FhirInfoReader


class PrivateVenueDisclosureDirectDictMapper:
    def __init__(self):
        self.__reader = None

    def build(self, patient_id: str, info: FhirInfo, cert: Certificate)-> dict:
        if self.__reader is not None:
            raise ValueError("Cannot reuse object.")

        self.__reader = FhirInfoReader(info)
        return {"nam": self.__reader.get_patient_name(patient_id),
                  "v": self.__build_immunizations(self.__reader.get_immunization_ids_for_patient(patient_id)),
                  "c": DisclosureCertificateDirectDictMapper.build(cert, DisclosureLevel.PrivateVenue)}

    def __build_immunizations(self, items):
        result = []
        for i in items:
            result.append(self.__build_immunization(i))
        return result

    def __build_immunization(self, immunization_id):
        return {"tg": self.__reader.get_immunization_target_diseases(immunization_id)}
