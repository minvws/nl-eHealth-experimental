import json

from abc import ABC, abstractmethod
from disclosure_level import DisclosureLevel
from pathlib import Path
from pyld import jsonld
from typing import Any, List, NamedTuple, Optional
from vacc_entry_parser import VaccEntryParser


class Certificate:
    """
    Simple POD data struct for certificate fields
    """

    def __init__(self):
        self.issuer = ""
        self.UVCI: str = Optional[None]  # NOT completed for DisclosureLevel PV
        self.validFrom = ""
        self.validUntil = ""
        self.schemaVersion = ""
        self.issuingAuthorityCountry = ""


class MinDataSet(ABC):
    """
    MinDataSet abstract base class: a derived class will be instantiated
    by MinDataSetFactory, depending on the required disclosure level
    """

    __JSONLD_CONTEXT_FILE: Path = Path(
        Path(__file__).parent.resolve(), "immu_context.jsonld"
    )

    def __init__(self):
        pass

    @abstractmethod
    def parse(self, qry_res: dict) -> None:
        """
        Parse the FHIR response into the fields appropriate for the particular
        sub-class of MinDataSet.
        :param qry_res: JSON FHIR query response as dict (e.g. as return from json.loads())
        :return: None: the data is parsed into the concrete object
        """

    @abstractmethod
    def as_dict(self) -> List[dict]:
        pass

    def as_json(self) -> str:
        return json.dumps(self.as_dict())

    def as_json_ld(self) -> Any:
        with open(MinDataSet.__JSONLD_CONTEXT_FILE, "r") as context:
            compacted = jsonld.compact(self.as_json(), context.readlines())
            return compacted

    @staticmethod
    def _has_entries(qry_res: dict) -> bool:
        return (
            qry_res  # falsy in boolean context
            and "resourceType" in qry_res
            and qry_res["resourceType"] == "Bundle"
            and "total" in qry_res
            and qry_res["total"] > 0
        )


class MinDataSetPV(MinDataSet):
    """
    MinimumDataSet for Private Venues
    """

    def __init__(self):
        super().__init__()
        self.__certificate = Certificate()
        self.__entries: List[dict] = list()

    def parse(self, qry_res: dict) -> None:
        if MinDataSet._has_entries(qry_res=qry_res):
            entry_parser: VaccEntryParser = VaccEntryParser(qry_res=qry_res)
            for entry in qry_res["entry"]:
                pv: dict = entry_parser.resolve_entry(
                    entry=entry, disclosure_level=DisclosureLevel.PV
                )
                if pv:
                    self.__entries.append(pv)

    @property
    def certificate(self) -> Certificate:
        return self.__certificate

    def as_dict(self) -> List[dict]:
        return self.__entries

    def as_json(self) -> str:
        return json.dumps(self.as_dict())


class MinDataSetBC(MinDataSet):
    """
    MinimumDataSet for Border Control
    """

    def __init__(self):
        super().__init__()
        self.__entries: List[dict] = list()

    def parse(self, qry_res: dict) -> None:
        if MinDataSet._has_entries(qry_res=qry_res):
            entry_parser: VaccEntryParser = VaccEntryParser(qry_res=qry_res)
            for entry in qry_res["entry"]:
                bc: dict = entry_parser.resolve_entry(
                    entry=entry, disclosure_level=DisclosureLevel.BC
                )
                if bc:
                    self.__entries.append(bc)

    def as_dict(self) -> List[dict]:
        return self.__entries


class MinDataSetMD(MinDataSet):
    """
    MinimumDataSet for Medical
    """

    def __init__(self):
        super().__init__()
        self.__entries: List[dict] = list()

    def parse(self, qry_res: dict) -> None:
        if MinDataSet._has_entries(qry_res=qry_res):
            entry_parser: VaccEntryParser = VaccEntryParser(qry_res=qry_res)
            for entry in qry_res["entry"]:
                md: dict = entry_parser.resolve_entry(
                    entry=entry, disclosure_level=DisclosureLevel.MD
                )
                if md:
                    self.__entries.append(md)

    def as_dict(self) -> List[dict]:
        return self.__entries


class MinDataSetFactory:
    """
    :class: MinDataSetFactory encapsulates MinDataSet class creation
    and provides a single point of reference for the levels of disclosure
    """

    @staticmethod
    def create(disclosure_level: DisclosureLevel) -> MinDataSet:
        """
        Factory method
        :param disclosure_level: determines which type of sub-class is returned
        :return: an object instance of a class derived from MinDataSet
        """
        if disclosure_level == DisclosureLevel.PV:
            return MinDataSetPV()
        elif disclosure_level == DisclosureLevel.BC:
            return MinDataSetBC()
        elif disclosure_level == DisclosureLevel.MD:
            return MinDataSetMD()
        else:
            raise ValueError(
                f"Unknown DisclosureLevel enumeration value: {disclosure_level}"
            )
