from cryptography.x509 import Certificate

from DisclosureCertificateDirectDictMapper import DisclosureCertificateDirectDictMapper
from DisclosureLevel import DisclosureLevel
from FhirInfoCollector import FhirInfo
from FhirInfoReader import FhirInfoReader


class MedicalDisclosureDirectDictMapper:
    def __init__(self):
        self.__reader = None

    def build(self, patientId, info: FhirInfo, cert: Certificate) -> dict:
        if self.__reader is not None:
            raise ValueError("Cannot reuse object.")

        self.__reader = FhirInfoReader(info)
        return {"nam": self.__reader.get_patient_name(patientId),
                  "pid": self.__reader.get_patient_person_id(patientId),
                  "sex": self.__reader.get_patient_sex(patientId),
                  "dob": self.__reader.get_patient_date_of_birth(patientId),
                  "v": self.__build_immunizations(self.__reader.get_immunization_ids_for_patient(patientId)),
                  "c": DisclosureCertificateDirectDictMapper.build(cert, DisclosureLevel.Medical)}

    def __build_immunizations(self, items):
        result = []
        for i in items:
            result.append(self.__build_immunization(i))
        return result

    def __build_immunization(self, immunization_id):
        return {"tg": self.__reader.get_immunization_target_diseases(immunization_id),
                  "cd": self.__reader.get_immunization_vaccine_codes(immunization_id),
                  "mp": self.__reader.get_immunization_medical_products(immunization_id),
                  "ah": self.__reader.get_immunization_authorization_holders(immunization_id),
                  "sn": self.__reader.get_immunization_series_number(immunization_id),
                  "sc": self.__reader.get_immunization_series_count(immunization_id),
                  "lt": self.__reader.get_immunization_lot_number(immunization_id),
                  "oc": self.__reader.get_immunization_occurrence(immunization_id),
                  "ao": self.__reader.get_immunization_actor_organization(immunization_id),
                  "ap": self.__reader.get_immunization_actor_practitioner(immunization_id),
                  "lo": self.__reader.get_immunization_location(immunization_id),
                  "nx": self.__reader.get_immunization_next_occurrence(immunization_id)}

