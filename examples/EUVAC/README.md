# EUVAC - EU Vaccination Certificate Generation

## Pre-Requisites
1. [Docker](https://www.docker.com/) should be running 

## Quick Start
1. bash shell 
   1. ```./build_docker.sh```
   1. ```./run_docker.sh```
1. other
   1. ```docker build -t nl/euvac .```
   1. ```docker run --rm -p 8080:3030 nl/euvac```

## Default Settings
### Port Mappings
By default we map 8080 on host to 3030 in the docker container with the
```-p 8080:3030``` argument to ```docker run```. The target port of 3030 is set in the docker, 
but feel free to map some other host port to 3030, as required. 

### FHIR Test Servers
A list of public FHIR test servers can be found at:
https://confluence.hl7.org/display/FHIR/Public+Test+Servers

Standard HTTP accept header for FHIR R4: ```Accept: application/fhir+json```

I am using the current, stable FHIR Release 4 endpoints on these public FHIR test servers:

| Name | FHIR R4 Service Root URL |
| ---: | :----------------------- |
| Firely | https://server.fire.ly/r4/ |
| SmileCDR | https://try.smilecdr.com:8000/baseR4/ |
| Cerner Open Sandbox | https://fhir-open.cerner.com/r4/ec2458f2-1e24-41c8-b71b-0e701af7583d/ |

## Testing cose

Take the string 'Hello'; COSE it, ZLIB compress and then Base45 and back.

1. generate the CSCA and DSC with ```./gen-csca-dsc.sh```	
2. run the command: ``` python3.8 cose_sign.py | python3.8 cose_verify.py```

Testing against the AU cases:

1. Fetch the Base64 from https://dev.a-sit.at/certservice
2. Remove the first 2 bytes and do

   ```pbpaste| sed -e 's/^00//' | python3.8 cose_verify.py --base64 --ignore-signature --cbor```

