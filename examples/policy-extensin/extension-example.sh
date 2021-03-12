#!/bin
set -e

if [ -e out/extension-example.key ]; then
	echo cowardly refuse to overwrite my kyes
	exit 1
fi
mkdir -p out
cd out

SUBJ='/CN=Extension Demo/C=EU'

openssl req -new -keyout extension-example.key -nodes -subj "${SUBJ}" |\
openssl x509 \
	-extfile ../cl.cnf -extensions cl \
	-extfile ../extension.cnf -extensions ext \
	-req -CAkey sub-ca.key -CA sub-ca.pem -set_serial 0x4FA2928C84BC8D18079A33F664D276C8CD9D7000 -out extension-example.pem

openssl x509 -noout -text -in extension-example.pem

# Create private Chipcard like client cert to import into email/browser
openssl pkcs12 -export \
	-inkey extension-example.key -in extension-example.pem \
	-CAfile client-chain.pem \
	-name "C.L. signature package" \
	-out extension-example.p12 -passout pass:12345678 

cat extension-example.key  extension-example.pem > extension-example.crt

echo OK
