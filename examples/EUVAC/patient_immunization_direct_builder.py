from border_control_disclosure_direct_dict_mapper import BorderControlDisclosureDirectDictMapper
from disclosure_level import DisclosureLevel
from fhir_info_collector import FhirInfo
from medical_disclosure_direct_dict_mapper import MedicalDisclosureDirectDictMapper
from private_venue_disclosure_direct_dict_mapper import PrivateVenueDisclosureDirectDictMapper
from uvci_info import UvciInfo


class PatientImmunizationDirectBuilder:
    @staticmethod
    def build(fhirInfo : FhirInfo, patient_id: str, disclosure_level: DisclosureLevel, uvci: UvciInfo) -> dict:

        patient = fhirInfo.immunized_patients[patient_id]
        if patient is None:
            raise ValueError("qry_entry does not contain an immunized patient.")

        # Add the try/except block when mandatory data items throws exceptions when missing
        # e.g. replace use of Safe data finders and None checks.
        # try:

        if disclosure_level == DisclosureLevel.PrivateVenue:
            b = PrivateVenueDisclosureDirectDictMapper()
            return b.build(patient_id, fhirInfo, uvci)

        if disclosure_level == DisclosureLevel.BorderControl:
            b = BorderControlDisclosureDirectDictMapper()
            return b.build(patient_id, fhirInfo, uvci)

        if disclosure_level == DisclosureLevel.Medical:
            b = MedicalDisclosureDirectDictMapper()
            return b.build(patient_id, fhirInfo, uvci)

        # except:
        #     return None

        raise ValueError("Disclosure level unknown.")