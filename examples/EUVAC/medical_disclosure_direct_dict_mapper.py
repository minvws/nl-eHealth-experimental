from disclosure_level import DisclosureLevel
from fhir_info_collector import FhirInfo
from fhir_info_reader import FhirInfoReader
from ucvi_metadata_builder import UcviMetadataBuilder


class MedicalDisclosureDirectDictMapper:
    def __init__(self):
        self.__reader = None

    def build(self, patient_id, info: FhirInfo) -> dict:
        if self.__reader is not None:
            raise ValueError("Cannot reuse object.")

        self.__reader = FhirInfoReader(info)
        return {
            "nam": self.__reader.get_patient_name(patient_id),
            "pid": self.__reader.get_patient_person_id(patient_id),
            "sex": self.__reader.get_patient_sex(patient_id),
            "dob": self.__reader.get_patient_date_of_birth(patient_id),
            "v": self.__build_immunizations(
                self.__reader.get_immunization_ids_for_patient(patient_id)
            ),
            "c": UcviMetadataBuilder.build(
                self.__reader, patient_id, DisclosureLevel.Medical
            ),
        }

    def __build_immunizations(self, items):
        result = []
        for i in items:
            result.append(self.__build_immunization(i))
        return result

    def __build_immunization(self, immunization_id):
        return {
            "tg": self.__reader.get_immunization_target_diseases(immunization_id),
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
            "nx": self.__reader.get_immunization_next_occurrence(immunization_id),
        }
