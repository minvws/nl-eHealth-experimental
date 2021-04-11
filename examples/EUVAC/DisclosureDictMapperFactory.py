from BorderControlDisclosureDictMapper import BorderControlDisclosureDictMapper
from DisclosureLevel import DisclosureLevel
from MedicalDisclosureDictMapper import MedicalDisclosureDictMapper
from PrivateVenueDisclosureDictMapper import PrivateVenueDisclosureDictMapper


class DisclosureDictMapperFactory:
    @staticmethod
    def build(disclosure_level: DisclosureLevel):
        try:
            if disclosure_level == DisclosureLevel.PrivateVenue:
                return PrivateVenueDisclosureDictMapper()

            if disclosure_level == DisclosureLevel.BorderControl:
                return BorderControlDisclosureDictMapper()

            if disclosure_level == DisclosureLevel.Medical:
                return MedicalDisclosureDictMapper()

        except:
            return None

        raise ValueError("Disclosure level unknown.")