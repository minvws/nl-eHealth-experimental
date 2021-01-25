#!/bin/sh
set -e

# ES256 (ECDSA p256) 
openssl ecparam -name secp256k1 -genkey -noout -out ec.key
openssl ec -in ec.key -pubout -out ec.pub

# Sign something
#
openssl dgst -sha256 -sign ec.key payload.pb > signature.bin
openssl dgst -sha256 -verify ec.pub -signature signature.bin payload.pb

echo EC256 k1
echo pubkey: 
cat ec.pub
echo Sginature:
cat signature.bin | base64

openssl req -new -x509 -nodes -keyout x509.key -out x509.pub -subj /CN=CoronaPub -set_serial 81238912371298631278

openssl cms -binary -nosmimecap -nocerts -noattr -sign -signer x509.pub -inkey x509.key -outform DER -out signature-cms.bin -in payload.pb

echo
echo X509
cat x509.pub
echo
echo Signature using above cert:
cat signature-cms.bin | base64

# openssl asn1parse -inform DER -in signature-cms.bin 

cat signature-cms.bin payload.pb | xz -e --compress > qr.bin
cat qr.bin | qrencode -o qr.png -8 -l H

