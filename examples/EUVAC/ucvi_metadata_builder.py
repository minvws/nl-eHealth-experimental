from disclosure_level import DisclosureLevel
from fhir_info_reader import FhirInfoReader
from uvci_reader import UvciReader


class UcviMetadataBuilder:
    @staticmethod
    def build(
        fhir_info_reader: FhirInfoReader,
        patient_id: str,
        disclosure_level: DisclosureLevel,
    ):
        last_id = fhir_info_reader.get_last_immunization_id(patient_id)
        if last_id is None:
            return ValueError("Attempt to read patient without immunizations.")

        last = fhir_info_reader.get_info().immunizations[last_id]
        uvci_reader = UvciReader(last["uvci"]["value"])
        return {
            "is": uvci_reader.get_issuing_authority(),
            "id": uvci_reader.get_identifer(disclosure_level.PrivateVenue),
            "st": last["uvci"]["validFrom"],
            "en": last["uvci"]["validUntil"],
            "vr": uvci_reader.get_schema_version(),
            "ia": uvci_reader.get_issuing_authority(),
        }
