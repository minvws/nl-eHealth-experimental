#!/bin
set -e

if !  mkdir out; then
	echo cowardly refuse to overwrite my kyes
	exit 1
fi
cd out

# Generate a root cert voor de staat der Nederlanden 
#
# openssl x509 -noout -issuer -in RootCA.pem -subject -nameopt RFC2253,compat 
openssl req -x509 -out ca.pem -keyout ca.key -nodes -subj '/CN=Staat der Nederlanden Root CA - G3/O=Staat der Nederlanden/C=NL'

# openssl x509 -noout -issuer -in DomOrganisatiePersoonCA-G3.pem -subject -nameopt RFC2253,compat 
openssl req -new -keyout sub-ca.key -nodes \
	-subj '/C=NL/O=Staat der Nederlanden/CN=Staat der Nederlanden Organisatie Persoon CA - G3' |\
openssl x509 \
	-extfile ../zorgverlener.cnf -extensions subca \
	-req -CAkey ca.key -CA ca.pem -set_serial 1010 -out sub-ca.pem

# openssl x509 -in real-huisarts.pem -CA sub-ca.pem -CAkey sub-ca.key -set_serial 1234 | openssl x509 -noout -nameopt RFC2253,compat

SUBJ='/title=Huisarts/serialNumber=000066600/CN=Hermanus Boerhave/T=Huisarts/O=Hermanus Boerhave/C=NL'
openssl req -new -keyout fake-huisarts.key -nodes -subj "${SUBJ}" |\
openssl x509 \
	-extfile ../zorgverlener.cnf -extensions huisarts \
	-req -CAkey sub-ca.key -CA sub-ca.pem -set_serial 0x4FA2928C84BC8D18079A33F664D276C8CD9D7000 -out fake-huisarts.pem

openssl x509 -noout -text -in fake-huisarts.pem

cat fake-huisarts.key  fake-huisarts.pem > fake-huisarts.crt

cat ca.pem sub-ca.pem > client-chain.pem

# for testing purposes - fake server sert (dispensing with alt names)
#
openssl req -new -keyout system-ca.key -nodes \
	-subj '/C=NL/O=Staat der Nederlanden/CN=Staat der Nederlanden Organisatie - Server Stuff' |\
openssl x509 \
	-extfile ../zorgverlener.cnf -extensions subca \
	-req -CAkey ca.key -CA ca.pem -set_serial 2010 -out system-ca.pem

openssl req -new  -keyout server.key -nodes \
	-subj '/CN=uzi-test.webweaving.org'  |\
   openssl x509 -req -CAkey system-ca.key -CA system-ca.pem \
	-extfile ../server.cnf -extensions server \
	-set_serial 2020 -out server.pem

cat ca.pem system-ca.pem > server-chain.pem

# Create CA to import into browser

openssl x509 -in ca.pem -out ca.crt -outform DER

# Create private Chipcard like client cert to import into email/browser

openssl pkcs12 -export \
	-inkey fake-huisarts.key -in fake-huisarts.pem \
	-CAfile client-chain.pem \
	-name "UZI pass (fake) for Hermanus Boerhave" \
	-out fake-huisarts.p12 -passout pass:12345678 

cat fake-huisarts.key  fake-huisarts.pem > fake-huisarts

echo OK
