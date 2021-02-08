"""
build_pb.py

Create a serialized protobuf of a given JSON message
Uses a hand-crafted minimal spec .proto file to extract just the fields required
from the source json and pack that into a protobuf
The protobuf object (NNN_pb2.py) is created by using:
   protoc [args...] --python_out [args...] NNN.proto
"""
import json
import protobuf_json
import smart_vacc_fhir_bundle_gc_pb2
import smart_vacc_fhir_bundle_gc1_pb2
import smart_vacc_fhir_bundle_gc2_pb2
import sys

from enum import IntEnum, unique
from pathlib import Path
from typing import Any


@unique
class DisclosureLevel(IntEnum):
    ZERO = 0
    ONE = 1
    TWO = 2


def __smart_vac_pb_factory(disclosure_level: DisclosureLevel) -> Any:
    if disclosure_level == DisclosureLevel.ZERO:
        return smart_vacc_fhir_bundle_gc_pb2.SmartVaccCert()
    elif disclosure_level == DisclosureLevel.ONE:
        return smart_vacc_fhir_bundle_gc1_pb2.SmartVaccCert1()
    elif disclosure_level == DisclosureLevel.TWO:
        return smart_vacc_fhir_bundle_gc2_pb2.SmartVaccCert2()
    else:
        print("INFO: defaulting to lowest (most private) disclosure level")
        return smart_vacc_fhir_bundle_gc_pb2.SmartVaccCert()


def __write_protobuf_from_json(json_source: Path, disclosure_level: DisclosureLevel) -> None:
    # populate protobuf object from json
    pb2 = __smart_vac_pb_factory(disclosure_level=disclosure_level)
    with open(json_source, "r") as f:
        svc_str: dict = json.loads(f.read())
        protobuf_json.json2pb(pb2, svc_str)
    # write out serialized protobuf
    suffix: str = f".{disclosure_level}.bin"
    out_file: Path = json_source.with_suffix(suffix=suffix)
    with open(out_file, "wb") as f:
        f.write(pb2.SerializeToString())


def serialize(json_source: Path) -> None:
    __write_protobuf_from_json(json_source=json_source, disclosure_level=DisclosureLevel.ZERO)
    __write_protobuf_from_json(json_source=json_source, disclosure_level=DisclosureLevel.ONE)
    __write_protobuf_from_json(json_source=json_source, disclosure_level=DisclosureLevel.TWO)


if __name__ == "__main__":
    # supply cmd line argument of the file containing the json
    serialize(json_source=Path(sys.argv[1]))
