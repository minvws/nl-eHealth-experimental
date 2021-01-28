#!/bin/bash -e

COMPRESSOR=$(which xz)
COMPRESS_OPTS="-e -f"
PYTHON_BIN=$(which python3)
PYTHON_SCRIPT=build_pb.py
JSON_SOURCE="Vaccination-FHIR-Bundle - GC.json"
PB_FROM_JSON=$(basename "${JSON_SOURCE}" .json)
PB_FROM_JSON="${PB_FROM_JSON}.bin"

PYTHONPATH=.:protobuf-json "${PYTHON_BIN}" "${PYTHON_SCRIPT}" "${JSON_SOURCE}"

# some simple size stats
wc -c "${JSON_SOURCE}"
wc -c "${PB_FROM_JSON}"
${COMPRESSOR} ${COMPRESS_OPTS} "${PB_FROM_JSON}"
wc -c "${PB_FROM_JSON}.xz"
