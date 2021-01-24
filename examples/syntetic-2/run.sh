#!/bin/sh
set -e

PYTHON=${PYTHON:-/opt/local/bin/python2.7}

test -d pbjson || git clone  git clone git@github.com:yinqiwen/pbjson.git
test -d protobuf-json || git@github.com:dpp-name/protobuf-json.git

echo "file	                        | plain	   | compressed"
echo "----------------------------------|----------|-----------------"
for i in *.json
do
	rm -f msg*

	# Create a protoc defintion based on the json
	#
	j=$(basename "$i" .json)
	(
		echo 'syntax = "proto2";'
		${PYTHON} pbjson/schema_parse.py "$i" 
	)> msg.proto

	# Create a python library from this proto definition
	#
        protoc -I=. --python_out=. msg.proto

	# Then use this defintiion to read in the json file
	# and output it using that proto as a protobuf
	#
        PYTHONPATH=.:protobuf-json /opt/local/bin/python2.7 ./json2pb.py  "$i" > "$j.pb"

	# FInally show the various file sizes.
	for ex in pb json xml
	do
		if test -f "$j.$ex"; then
			PLAIN=$(cat "$j.$ex" | wc -c)
			COMP=$(cat "$j.$ex" | xz --compress  -e | wc -c)
			echo "$j / $ex	| $PLAIN |	$COMP"
		fi
	done
done
