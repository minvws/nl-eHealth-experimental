from pyld import jsonld
from typing import Any

class JsonLdFormatter:

    __CONTEXT_FILE = "immu_context.jsonld"  # used for JSON-LD generation

    def format(self, value) -> Any:
        # context is the string rep of context file
        doc = ""
        with open(JsonLdFormatter.__CONTEXT_FILE, "r") as context:
            compacted = jsonld.compact(doc, context.readlines())
        return compacted

    def serialize(self, json_ld: str) -> Any:
        pass