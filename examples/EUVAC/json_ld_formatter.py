from pathlib import Path

import ujson
from pyld import jsonld
from typing import Any


class JsonLdFormatter:
    __CONTEXT_FILE = "immu_context.jsonld"  # used for JSON-LD generation

    __JSONLD_CONTEXT_FILE: Path = Path(
        Path(__file__).parent.resolve(), "immu_context.jsonld"
    )

    EU_SCHEMA_ROOT = "https://github.com/ehn-digital-green-development"

    def map_json_to_ld(self, data_set: dict):
        # map each attribute if present - handles differences between disclosure levels
        # take schema id from schema.org if appropriate mapping available
        # else refer tp schema_root for custom schemas
        json_doc = {}
        json_doc["https://schema.org/Name"] = data_set["nam"]  # mandatory
        self.__map_optional(
            data_set, "pid", json_doc, f"{JsonLdFormatter.EU_SCHEMA_ROOT}/personIdentifier"
        )
        self.__map_optional(
            data_set, "sex", json_doc, f"{JsonLdFormatter.EU_SCHEMA_ROOT}/sex"
        )
        self.__map_optional(
            data_set, "dob", json_doc, "http://schema.org/birthDate"
        )
        json_doc[f"{JsonLdFormatter.EU_SCHEMA_ROOT}/vaccinations"] = self.__map_immunizations(
            data_set["v"]
        )
        json_doc[f"{JsonLdFormatter.EU_SCHEMA_ROOT}/uvci/metadata"] = self.__map_cert_metadata(
            data_set["c"]
        )

        with open(JsonLdFormatter.__JSONLD_CONTEXT_FILE, "r") as context_file:
            json_ctx: dict = ujson.load(context_file)
            compacted: dict = jsonld.compact(json_doc, json_ctx)
            return compacted

    def __map_optional(self, source, name, dest, schema):
        if name in source:
            dest[schema] = source[name]

    def __map_immunizations(self, items: list):
        result = []
        for i in items:
            result = {}
            # still can be a list
            result[f"{JsonLdFormatter.EU_SCHEMA_ROOT}/targetDiseases"] = i["tg"]
            self.__map_optional(
                items, "cd", result, f"{JsonLdFormatter.EU_SCHEMA_ROOT}/vaccineCode"
            )
            self.__map_optional(i, "mp", result, f"{JsonLdFormatter.EU_SCHEMA_ROOT}/medicalProduct")
            self.__map_optional(i, "ah", result, f"{JsonLdFormatter.EU_SCHEMA_ROOT}/authorizationHolder")
            self.__map_optional(i, "sn", result, f"{JsonLdFormatter.EU_SCHEMA_ROOT}/seriesDoses")
            self.__map_optional(i, "sc", result, f"{JsonLdFormatter.EU_SCHEMA_ROOT}/seriesCount")
            self.__map_optional(i, "lt", result, f"{JsonLdFormatter.EU_SCHEMA_ROOT}/lotNumber")
            self.__map_optional(i, "oc", result, f"{JsonLdFormatter.EU_SCHEMA_ROOT}/occurrence")
            self.__map_optional(i, "ao", result, f"{JsonLdFormatter.EU_SCHEMA_ROOT}/ao")
            self.__map_optional(i, "ap", result, f"{JsonLdFormatter.EU_SCHEMA_ROOT}/ap")
            self.__map_optional(i, "lo", result, "https://schema.org/location")
            self.__map_optional(i, "nx", result, f"{JsonLdFormatter.EU_SCHEMA_ROOT}/nextOccurrence")
        return result

    def __map_cert_metadata(self, cert: dict):
        result = {}
        result[f"{JsonLdFormatter.EU_SCHEMA_ROOT}/uvci/issuer"] = cert["is"]
        self.__map_optional(
            cert, "cid", result, f"{JsonLdFormatter.EU_SCHEMA_ROOT}/uvci"
        )
        result["https://schema.org/startDate"] = cert["st"]
        result["https://schema.org/endDate"] = cert["en"]
        result["https://schema.org/version"] = cert["vr"]
        result[f"{JsonLdFormatter.EU_SCHEMA_ROOT}/uvci/issuingAuthority"] = cert["ia"]
        return result

    def format(self, value) -> Any:
        # context is the string rep of context file
        doc = ""
        with open(JsonLdFormatter.__CONTEXT_FILE, "r") as context:
            compacted = jsonld.compact(doc, context.readlines())
        return compacted

    def serialize(self, json_ld: str) -> Any:
        pass
