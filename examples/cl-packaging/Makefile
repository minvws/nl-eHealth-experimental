CFLAGS=-I/opt/local/include
LDFLAGS=-L/opt/local/lib
LIBS=-lxml2 -lcrypto

all: out out/fake-cl.pem xml2asn1 cl-key.cnf cl.xml
	# openssl asn1parse -in out/fake-cl.pem -offset 555
	./xml2asn1 -p cl.xml

out/fake-cl.pem: cl-key.cnf
	sh cl-sign.sh

cl-key.cnf: xml2asn1 cl.xml
	./xml2asn1 -c cl.xml > cl-key.cnf

xml2asn1: xml2asn1.c
	gcc -Wall -Werror ${CFLAGS} -o xml2asn1 xml2asn1.c ${LDFLAGS} ${LIBS}

out:
	sh resign.sh


clean:
	rm -rf xml2asn1.o xml2asn1.core xml2asn1.dSYM cl-key.cnf out

