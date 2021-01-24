#!/bin/sh
set -e

PYTHON=${PYTHON:-/opt/local/bin/python2.7}

test -d pbjson || git clone  git clone git@github.com:yinqiwen/pbjson.git
test -d protobuf-json || git@github.com:dpp-name/protobuf-json.git

${PYTHON} pbjson/schema_parse.py "Vaccination-FHIR-Bundle - GC.json" >  "Vaccination-FHIR-Bundle - GC.proto" 

protoc -I=. --python_out=. ./"Vaccination-FHIR-Bundle - GC.proto"

cp "Vaccination_FHIR_Bundle _ GC_pb2.py" msg_pb2.py

PYTHONPATH=.:protobuf-json /opt/local/bin/python2.7 ./json2pb.py  "Vaccination-FHIR-Bundle - GC.json"  >  "Vaccination-FHIR-Bundle - GC.pb"

echo "file	| 	plain	| 	compressed"
echo "----------|---------------|-----------------"

for i in pb json xml
do
	for j in *.$i
	do
		PLAIN=$(cat "$j" | wc -c)
		COMP=$(cat "$j" | xz --compress  -e | wc -c)
		echo "$j	| $PLAIN |	$COMP"
	done
done
