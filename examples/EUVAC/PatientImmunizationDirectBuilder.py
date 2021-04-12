from BorderControlDisclosureDirectDictMapper import BorderControlDisclosureDirectDictMapper
from DisclosureLevel import DisclosureLevel
from FhirInfoCollector import FhirInfo
from MedicalDisclosureDirectDictMapper import MedicalDisclosureDirectDictMapper
from PrivateVenueDisclosureDirectDictMapper import PrivateVenueDisclosureDirectDictMapper


class PatientImmunizationDirectBuilder:
    @staticmethod
    def build(fhirInfo : FhirInfo, patientId: str, disclosure_level: DisclosureLevel, cert):

        patient = fhirInfo.immunizedPatients[patientId]
        if patient is None:
            raise ValueError("qry_entry does not contain an immunized patient.")

        # Add the try/except block when mandatory data items throws exceptions when missing
        # e.g. replace use of Safe data finders and None checks.
        # try:

        if disclosure_level == DisclosureLevel.PrivateVenue:
            b = PrivateVenueDisclosureDirectDictMapper()
            return b.build(patientId, fhirInfo, cert)

        if disclosure_level == DisclosureLevel.BorderControl:
            b = BorderControlDisclosureDirectDictMapper()
            return b.build(patientId, fhirInfo, cert)

        if disclosure_level == DisclosureLevel.Medical:
            b = MedicalDisclosureDirectDictMapper()
            return b.build(patientId, fhirInfo, cert)

        # except:
        #     return None

        raise ValueError("Disclosure level unknown.")