#!/bin/sh
set -e

PYTHON=${PYTHON:-/opt/local/bin/python2.7}

test -d pbjson || git clone git@github.com:aoeuidht/pbjson.git
test -d protobuf-json || git clone git@github.com:dpp-name/protobuf-json.git
test -d fhir-formats || git clone git@github.com:vadi2/fhir-formats.git

echo "file	                     | proto    | plain	   | compressed"
echo "-----------------------------|----------|----------|-----------------"
ls *.json *.xml | sed -e 's/\.[a-z]*//' | sort -u | while read base
do
	rm -f msg*

	# check if there is a json version; if not - create it from the XML
	#
	if ! test -e "$base.json"; then
		echo Creating json version from XML for $base
		${LUA51} ./fhir-xml2json "$base.xml" > "$base.json"
	fi
	# Create a protoc defintion based on the json
	#
	(
		echo 'syntax = "proto2";'
		${PYTHON} ./pbjson/schema_parse.py "$base.json" 
	)> msg.proto

	# Create a python library from this proto definition
	#
        protoc -I=. --python_out=. msg.proto

	# Then use this defintiion to read in the json file
	# and output it using that proto as a protobuf
	#
        PYTHONPATH=.:protobuf-json /opt/local/bin/python2.7 ./json2pb.py  "$base.json" > "$base.pb"

	# FInally show the various file sizes.
	JJ=$base
	for ex in pb json xml
	do
		if test -f "$base.$ex"; then
			PLAIN=$(cat "$base.$ex" | wc -c)
			COMP=$(cat "$base.$ex" | xz --compress  -e | wc -c)
			echo "$JJ	| $ex	| $PLAIN |	$COMP"
			JJ="                            "
		fi
	done
done
