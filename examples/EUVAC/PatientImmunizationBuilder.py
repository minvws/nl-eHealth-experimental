from BorderControlDisclosureBuilder import BorderControlDisclosureBuilder
from DisclosureLevel import DisclosureLevel
from FhirInfoCollector import FhirInfo
from MedicalDisclosureBuilder import MedicalDisclosureBuilder
from PrivateVenueDisclosureBuilder import PrivateVenueDisclosureBuilder


class PatientImmunizationBuilder:
    @staticmethod
    def build(fhirInfo : FhirInfo, patientId: str, disclosure_level: DisclosureLevel, cert):

        patient = fhirInfo.immunizedPatients[patientId]
        if patient is None:
            raise ValueError("qry_entry does not contain an immunized patient.")

        # Add the try/except block when mandatory data items throws exceptions when missing
        # e.g. replace use of Safe data finders and None checks.
        # try:

        if disclosure_level == DisclosureLevel.PrivateVenue:
            b = PrivateVenueDisclosureBuilder()
            return b.build(patientId, fhirInfo, cert)

        if disclosure_level == DisclosureLevel.BorderControl:
            b = BorderControlDisclosureBuilder()
            return b.build(patientId, fhirInfo, cert)

        if disclosure_level == DisclosureLevel.Medical:
            b = MedicalDisclosureBuilder()
            return b.build(patientId, fhirInfo, cert)

        # except:
        #     return None

        raise ValueError("Disclosure level unknown.")

