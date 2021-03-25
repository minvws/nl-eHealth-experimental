#!/bin/sh
#
# CSCA key
#
openssl genpkey -algorithm ED25519 > csca.key
openssl req -x509 \
	-subj '/CN=National CSCA of Friesland/C=FR/' \
	-key csca.key \
	-out csca.pem -nodes \
	-days 3650

# DSC keys
for i in 1 2 3 4 worker
do
openssl genpkey -algorithm ED25519 > dsc-$i.key 
openssl req -new \
	-subj "/CN=DSC number $i of Friesland/C=FR/" \
	-key dsc-$i.key -nodes |
openssl x509 -req -CA csca.pem -CAkey csca.key -set_serial $RANDOM \
	-days 1780  \
	-out dsc-$i.pem
done

cat dsc-*.pem > masterlist-dsc.pem

# Remove unneeded keys and certs
rm csca.key dsc-?.key dsc-?.pem
