from cryptography.x509 import Certificate

from BorderControlDisclosureDirectDictMapper import BorderControlDisclosureDirectDictMapper
from DisclosureLevel import DisclosureLevel
from FhirInfoCollector import FhirInfo
from MedicalDisclosureDirectDictMapper import MedicalDisclosureDirectDictMapper
from PrivateVenueDisclosureDirectDictMapper import PrivateVenueDisclosureDirectDictMapper


class PatientImmunizationDirectBuilder:
    @staticmethod
    def build(fhirInfo : FhirInfo, patient_id: str, disclosure_level: DisclosureLevel, cert: Certificate) -> dict:

        patient = fhirInfo.immunized_patients[patient_id]
        if patient is None:
            raise ValueError("qry_entry does not contain an immunized patient.")

        # Add the try/except block when mandatory data items throws exceptions when missing
        # e.g. replace use of Safe data finders and None checks.
        # try:

        if disclosure_level == DisclosureLevel.PrivateVenue:
            b = PrivateVenueDisclosureDirectDictMapper()
            return b.build(patient_id, fhirInfo, cert)

        if disclosure_level == DisclosureLevel.BorderControl:
            b = BorderControlDisclosureDirectDictMapper()
            return b.build(patient_id, fhirInfo, cert)

        if disclosure_level == DisclosureLevel.Medical:
            b = MedicalDisclosureDirectDictMapper()
            return b.build(patient_id, fhirInfo, cert)

        # except:
        #     return None

        raise ValueError("Disclosure level unknown.")