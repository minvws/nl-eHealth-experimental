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

from pathlib import Path


def serialize(json_source: Path) -> None:
    svc_pb2 = smart_vacc_fhir_bundle_gc_pb2.SmartVaccCert()
    out_file = json_source.with_suffix(".bin")

    # populate protobuf object from json
    with open(json_source, "r") as f:
        svc_str = json.loads(f.read())
        pb2 = protobuf_json.json2pb(svc_pb2, svc_str)
    # write out serialized protobuf
    with open(out_file, "wb") as f:
        f.write(pb2.SerializeToString())

    ## LEVEL1
    svc_pb2 = smart_vacc_fhir_bundle_gc1_pb2.SmartVaccCert1()
    out_file = json_source.with_suffix(".1.bin")

    # populate protobuf object from json
    with open(json_source, "r") as f:
        svc_str = json.loads(f.read())
        pb2 = protobuf_json.json2pb(svc_pb2, svc_str)
    # write out serialized protobuf
    with open(out_file, "wb") as f:
        f.write(pb2.SerializeToString())
    
    ## LEVEL2
    svc_pb2 = smart_vacc_fhir_bundle_gc2_pb2.SmartVaccCert2()
    out_file = json_source.with_suffix(".2.bin")

    # populate protobuf object from json
    with open(json_source, "r") as f:
        svc_str = json.loads(f.read())
        pb2 = protobuf_json.json2pb(svc_pb2, svc_str)
    # write out serialized protobuf
    with open(out_file, "wb") as f:
        f.write(pb2.SerializeToString())


if __name__ == "__main__":
    # supply cmd line argument of the file containing the json
    serialize(Path(sys.argv[1]))
