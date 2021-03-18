#!/bin/sh
#
set -e

FILE=${1:-appendix-h}

mkdir -p out
cp $FILE.json out
cd out

# Lint to verify json in appendix
#
jsonlint-3.8 ${FILE}.json

# Create pretty print version
#
json_pp < ${FILE}.json > ${FILE}-pretty.json

# CBOR both and compare sizes
#
json2cbor ${FILE}.json > ${FILE}.cbor
json2cbor ${FILE}-pretty.json > ${FILE}-pretty.cbor

L1=$(wc -c <${FILE}.cbor)
L2=$(wc -c <${FILE}-pretty.cbor)
[ $L1 == $L2 ]

# Compress both the json and the CBOR for comparison
#
cat ${FILE}.cbor | xz -9 > ${FILE}.cbor.Z
cat ${FILE}.json | xz -9 > ${FILE}.json.Z

cat ${FILE}.cbor | gzip -c -9 > ${FILE}.cbor.gz
cat ${FILE}.json | gzip -c -9 > ${FILE}.json.gz

cat ${FILE}.cbor | openssl zlib > ${FILE}.cbor.zlib
cat ${FILE}.json | openssl zlib > ${FILE}.json.zlib

echo Sizes:
for i in ${FILE}.json ${FILE}.cbor ${FILE}.*.Z ${FILE}.*.gz ${FILE}.*.zlib
do
	wc -c $i
done | sort -nr
