#!/bin
set -e

if [ -e out/fake-cl.key ]; then
	echo cowardly refuse to overwrite my kyes
	exit 1
fi
cd out

SUBJ='/CN=Camenisch Lysyanskaya Signature/O=eHealth demo/C=EU'

openssl req -new -keyout fake-cl.key -nodes -subj "${SUBJ}" |\
openssl x509 \
	-extfile ../cl.cnf -extensions cl \
	-extfile ../cl-key.cnf -extensions zkp \
	-req -CAkey sub-ca.key -CA sub-ca.pem -set_serial 0x4FA2928C84BC8D18079A33F664D276C8CD9D7000 -out fake-cl.pem

openssl x509 -noout -text -in fake-cl.pem

# Create private Chipcard like client cert to import into email/browser

openssl pkcs12 -export \
	-inkey fake-cl.key -in fake-cl.pem \
	-CAfile client-chain.pem \
	-name "C.L. signature package" \
	-out fake-cl.p12 -passout pass:12345678 

cat fake-cl.key  fake-cl.pem > fake-cl.crt

echo OK
