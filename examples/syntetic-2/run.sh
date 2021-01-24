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

	j=$(basename "$i" .json)
	(
		echo 'syntax = "proto2";'
		${PYTHON} pbjson/schema_parse.py "$i" 
	)> msg.proto
        protoc -I=. --python_out=. msg.proto

        PYTHONPATH=.:protobuf-json /opt/local/bin/python2.7 ./json2pb.py  "$i" > "$j.pb"

	for ex in pb json xml
	do
		PLAIN=$(cat "$j.$ex" | wc -c)
		COMP=$(cat "$j.$ex" | xz --compress  -e | wc -c)
		echo "$j / $ex	| $PLAIN |	$COMP"
	done
done
