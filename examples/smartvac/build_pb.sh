#!/bin/bash -e

COMPRESS=0
PYTHON_BIN=$(which python3)
PYTHON_SCRIPT=build_pb.py
JSON_SOURCE="Vaccination-FHIR-Bundle - GC.json"
PB_FROM_JSON=$(basename "${JSON_SOURCE}" .json)

if (( COMPRESS != 0 )); then
  COMPRESSOR=$(which xz)
  COMPRESS_OPTS="-e -f"
  COMPRESS_EXT="xz"
fi

PYTHONPATH=.:protobuf-json "${PYTHON_BIN}" "${PYTHON_SCRIPT}" "${JSON_SOURCE}"

# some simple size stats
wc -c "${JSON_SOURCE}"

for disclosure_level in {0..2};
do
  pb_json="${PB_FROM_JSON}.${disclosure_level}.bin"
  wc -c "${pb_json}"
  if (( COMPRESS != 0 )); then
    ${COMPRESSOR} ${COMPRESS_OPTS} "${pb_json}"
    wc -c "${pb_json}.${COMPRESS_EXT}"
  fi
done
