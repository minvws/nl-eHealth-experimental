from cryptography.x509 import Certificate

from DisclosureCertificateDirectDictMapper import DisclosureCertificateDirectDictMapper
from DisclosureLevel import DisclosureLevel
from FhirInfoCollector import FhirInfo
from FhirInfoReader import FhirInfoReader


class BorderControlDisclosureDirectDictMapper:
    def __init__(self):
        self.__reader = None

    def build(self, patient_id: str, info: FhirInfo, cert: Certificate):
        if self.__reader is not None:
            raise ValueError("Cannot reuse object.")
        self.__reader = FhirInfoReader(info)
        return {
            "nam": self.__reader.get_patient_name(patient_id),
            "pid": self.__reader.get_patient_person_id(patient_id),
            "dob": self.__reader.get_patient_date_of_birth(patient_id),
            "v": self.__build_immunizations(self.__reader.get_immunization_ids_for_patient(patient_id)),
            "c": DisclosureCertificateDirectDictMapper.build(cert, DisclosureLevel.BorderControl)
        }

    def __build_immunizations(self, items):
        result = []
        for i in items:
            result.append(self.__build_immunization(i))
        return result

    def __build_immunization(self, item_id):
        return {
            "tg": self.__reader.get_immunization_target_diseases(item_id),
            "cd": self.__reader.get_immunization_vaccine_codes(item_id),
            "mp": self.__reader.get_immunization_medical_products(item_id),
            "ah": self.__reader.get_immunization_authorization_holders(item_id),
            "sn": self.__reader.get_immunization_series_number(item_id),
            "oc": self.__reader.get_immunization_occurrence(item_id),
            "lo": self.__reader.get_immunization_location(item_id)
        }
