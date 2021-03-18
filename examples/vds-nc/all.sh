#!/bin/sh
set -e

for i in appendix-h stripped stripped-keyid
do
	sh gen.sh $i
done

openssl x509 -pubkey -in certifcate.pem -noout > public.pem
openssl ec -in public.pem -inform PEM -pubin -outform DER > public.der

# Extract Cert
cat appendix-h.json| jq '.Signature.Certificate'  | sed -e 's/^"//' -e 's/"$//' | base64 -d > certificate.der
openssl x509 -in certificate.der -inform DER -text -noout
openssl x509 -in certificate.der -inform DER > certificate.pem

# Extract signature
cat appendix-h.json| jq '.Signature.SignatureValue'  | sed -e 's/^"//' -e 's/"$//' | base64 -d > signature.bin

# verify the signature
#
gcc -o bin2asn1 bin2asn1.c; 
./bin2asn1 < signature.bin > signature.asn1              

cat appendix-h.json| jq --compact-output '.Data' > appendix-h-payload.json
perl -pi -e 'chomp if eof' appendix-h-payload.json

openssl dgst -sha512  -verify public.pem -signature signature.asn1 appendix-h-payload.json
