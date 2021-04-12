from enum import auto, Enum


class DisclosureLevel(Enum):
    """Enum for disclosure level. The disclosure level is representative
    of the intended use of the vaccination certificate and governs in accordance
    with the EU eHealthNetwork Annex 1 Minimum Dataset Specification for
    Vaccination Certificates
    """

    PV = auto()  # private venue, level 0
    BC = auto()  # border control, level 1
    MD = auto()  # medical, level 2
