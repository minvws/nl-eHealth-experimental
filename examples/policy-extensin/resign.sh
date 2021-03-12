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

openssl req -new -keyout sub-ca.key -nodes \
	-subj '/C=NL/O=Staat der Nederlanden/CN=Staat der Nederlanden Organisatie Vaccination CA - G3' |\
openssl x509 \
	-extfile ../zorgverlener.cnf -extensions subca \
	-req -CAkey ca.key -CA ca.pem -set_serial 1010 -out sub-ca.pem

cat ca.pem sub-ca.pem > client-chain.pem

# for testing purposes - fake server sert (dispensing with alt names)
#
openssl req -new -keyout system-ca.key -nodes \
	-subj '/C=NL/O=Staat der Nederlanden/CN=Staat der Nederlanden Organisatie - Server Stuff' |\
openssl x509 \
	-extfile ../zorgverlener.cnf -extensions subca \
	-req -CAkey ca.key -CA ca.pem -set_serial 2010 -out system-ca.pem

cat ca.pem system-ca.pem > server-chain.pem

# Create CA to import into browser

openssl x509 -in ca.pem -out ca.crt -outform DER

echo OK
