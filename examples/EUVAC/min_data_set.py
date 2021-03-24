from abc import ABC, abstractmethod
from enum import auto, Enum
from pyld import jsonld
from typing import Any, Optional


class Gender(Enum):
    M = auto()
    F = auto()
    O = auto()


class Certificate:
    """
    Simple POD data struct for certificate fields
    """

    def __init__(self):
        self.issuer = ""
        self.UVCI: str = Optional[None]  # NOT completed for DisclosureLevel PV
        self.validFrom = "2019-12-31"
        self.validUntil = "2019-12-31"
        self.schemaVersion = ""
        self.issuingAuthorityCountry = ""


class MinDataSet(ABC):
    """
    MinDataSet abstract base class: a derived class will be instantiated
    by MinDataSetFactory, depending on the required disclosure level
    """

    _CONTEXT_FILE = "immu_context.jsonld"  # used for JSON-LD generation

    def __init__(self):
        pass

    @property
    @abstractmethod
    def certificate(self) -> Certificate:
        pass

    @property
    @abstractmethod
    def pv(self) -> dict:
        pass

    # I don't find this particularly clean: will think of a better way
    # Property needs to be available at ABC level (for polymorphism, which 99% fits)
    # but this property should only available for a specific derived class (MinDataSetMD)
    # Maybe we just need to handle the concrete class instances rather than via polymorphism ->
    # also ugly as polymorphism really fits for 99% of the usage
    @property
    def md(self) -> dict:
        raise RuntimeError(f"property md not supported for concrete type {type(self)}")

    @abstractmethod
    def as_json_ld(self) -> Any:
        pass

    @abstractmethod
    def serialize(self, json_ld: str) -> Any:
        """
        serializes the JSON-LD to CBOR-LD binary
        :param json_ld: JSON-LD doc as string
        :return: JSON-LD serialized as CBOR-LD binary
        """
        pass


class MinDataSetPV(MinDataSet):
    """
    MinimumDataSet for Private Venues
    """

    def __init__(self):
        super().__init__()
        self.__pv = dict(
            legalName="", diseaseOrAgentTargeted="", startDateOfValidity=""
        )
        self.__certificate = Certificate()

    @property
    def certificate(self) -> Certificate:
        return self.__certificate

    @property
    def pv(self) -> dict:
        return self.__pv

    def as_json_ld(self) -> Any:
        # doc is json.dumps of this class's data
        # context is the string rep of context file
        doc = ""
        with open(MinDataSet._CONTEXT_FILE, "r") as context:
            compacted = jsonld.compact(doc, context.readlines())
        return compacted

    def serialize(self, json_ld: str) -> Any:
        pass


class MinDataSetBC(MinDataSetPV):
    """
    MinimumDataSet for Border Control
    Includes all [PV] fields
    Only difference to PV is that BC completes Certificate.UVCI field
    """

    def __init__(self):
        super().__init__()


class MinDataSetMD(MinDataSetBC):
    """
    MinimumDataSet for Medical
    Includes all [BC] fields
    """

    def __init__(self):
        super().__init__()
        self.__md = dict(
            personId="",
            dateOfBirth="",
            gender=Gender.O,
            marketingAuthorizationHolder="",
            vaccineCode="",
            vaccineMedicinalProduct="",
            batchLotNumber="",
            dateOfVaccination="",
            administeringCentre="",
            healthProfessionalId="",
            countryOfVaccination="",
            numberInSeries="",
            nextVaccinationDate="",
        )

    @property
    def md(self) -> dict:
        return self.__md


class MinDataSetFactory:
    """
    :class: MinDataSetFactory encapsulates MinDataSet class creation
    and provides a single point of reference for the levels of disclosure
    """

    class DisclosureLevel(Enum):
        """Enum for disclosure level. The disclosure level is representative
        of the intended use of the vaccination certificate and governs in accordance
        with the EU eHealthNetwork Annex 1 Minimum Dataset Specification for
        Vaccination Certificates
        """

        PV = auto()  # private venue, level 0
        BC = auto()  # border control, level 1
        MD = auto()  # medical, level 2

    @staticmethod
    def create(disclosure_level: DisclosureLevel) -> MinDataSet:
        """
        Factory method
        :param disclosure_level: determines which type of sub-class is returned
        :return: an object instance of a class derived from MinDataSet
        """
        if disclosure_level == MinDataSetFactory.DisclosureLevel.PV:
            return MinDataSetPV()
        elif disclosure_level == MinDataSetFactory.DisclosureLevel.BC:
            return MinDataSetBC()
        elif disclosure_level == MinDataSetFactory.DisclosureLevel.MD:
            return MinDataSetMD()
        else:
            raise ValueError(
                f"Unknown MinDataSetFactory.DisclosureLevel enumeration value: {disclosure_level}"
            )
