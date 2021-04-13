from enum import Enum, auto


class DisclosureLevel(Enum):
    """Enum for disclosure level. The disclosure level is representative
    of the intended use of the vaccination certificate and governs in accordance
    with the EU eHealthNetwork Annex 1 Minimum Dataset Specification for
    Vaccination Certificates
    """
    PrivateVenue = auto()
    BorderControl = auto()
    Medical = auto()
