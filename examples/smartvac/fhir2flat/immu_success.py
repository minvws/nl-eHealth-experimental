import json
from pathlib import Path
from enum import auto, Enum

FHIR_JSON_ROOT = Path("..", "FHIR_JSON_Source_Examples")


class DisclosureLevel(Enum):
    BASIC = auto()
    BORDER = auto()
    MEDICAL = auto()


MIN_DATA_SET_KEYS = {
    DisclosureLevel.BASIC: [],
    DisclosureLevel.BORDER: [],
    DisclosureLevel.MEDICAL: []
}

with open(FHIR_JSON_ROOT / "immu_success.json") as f:
    json_source: dict = json.load(f)
