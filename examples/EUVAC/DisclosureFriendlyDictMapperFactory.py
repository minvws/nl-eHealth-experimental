from BorderControlDisclosureFriendlyDictMapper import BorderControlDisclosureFriendlyDictMapper
from DisclosureLevel import DisclosureLevel
from MedicalDisclosureFriendlyDictMapper import MedicalDisclosureFriendlyDictMapper
from PrivateVenueDisclosureFriendlyDictMapper import PrivateVenueDisclosureFriendlyDictMapper


class DisclosureFriendlyDictMapperFactory:
    @staticmethod
    def build(disclosure_level: DisclosureLevel):
        try:
            if disclosure_level == DisclosureLevel.PrivateVenue:
                return PrivateVenueDisclosureFriendlyDictMapper()

            if disclosure_level == DisclosureLevel.BorderControl:
                return BorderControlDisclosureFriendlyDictMapper()

            if disclosure_level == DisclosureLevel.Medical:
                return MedicalDisclosureFriendlyDictMapper()

        except:
            return None

        raise ValueError("Disclosure level unknown.")