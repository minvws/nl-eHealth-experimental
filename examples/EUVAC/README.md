# EUVAC - EU Vaccination Certificate Generation

## Pre-Requisites
1. [Docker](https://www.docker.com/) should be running 

## Quick Start
1. bash shell 
   1. ```./build_docker.sh```
   1. ```./run_docker.sh```
1. other
   1. ```docker build -t nl/euvac .```
   1. ```docker run --rm -p 9010:5000 nl/euvac```

## Default Settings
### Port Mappings
By default we map 9010 on host to 5000 in the docker container with the
```-p 9010:5000``` argument to ```docker run```. The target port of 5000 is set in the docker, 
but feel free to map some other host port, as required.

### FHIR Test Servers
A list of public FHIR test servers can be found at:
https://confluence.hl7.org/display/FHIR/Public+Test+Servers

Standard HTTP accept header for FHIR R4: ```Accept: application/fhir+json```

I am using the current, stable FHIR Release 4 endpoints on these public FHIR test servers:

| Name | FHIR R4 Service Root URL |
| ---: | :----------------------- |
| HL7 EU FHIR | https://hl7eu.onfhir.io/r4 |
| Firely | https://server.fire.ly/r4/ |

### FHIR2QR Home Page
Assuming you have used the default host:container port mapping of 9010:NNNN, 
then you should be able to open a browser in your host environment (the one in which 
the docker daemon is running), enter ```localhost:9010``` in the URL/Address bar and 
view the FHIR2QR home page.

## Testing COSE (round-trip)

For round-trip testing of ```cose_sign.py``` and ```cose_verify.py``` take the string ```Hello World!``` and:
1. COSE sign
   1. encrpyt into COSE message
   1. ZLIB compress
   1. Base45 encode 
1. COSE verify     
   1. Base45 decode
   1. ZLIB decompress
   1. decrypt from COSE message

### Test Steps

1. Generate the CSCA and DSC with ```./gen-csca-dsc.sh```	
1. Run the command: ```echo "Hello World!" | python3.8 cose_sign.py | python3.8 cose_verify.py```
1. You should see the output: ```Hello World!```

Or if you want to use JSON also CBOR in and out:

```echo '{ "Foo":1, "Bar":{ "Field1": "a value",   "integer":1212112121 }}' | python3.8 cose_sign.py --cbor | python3.8 cose_verify.py --cbor```

Which should output:

```{"Foo": 1, "Bar": {"Field1": "a value", "integer": 1212112121}}```

# Testing COSE from Austrian website

Testing against the AT cases:

1. Fetch the Base64 from https://dev.a-sit.at/certservice
1. Remove the first 2 bytes and do

   ```pbpaste| sed -e 's/^00//' | python3.8 cose_verify.py --base64 --ignore-signature --cbor```
