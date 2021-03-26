# EUVAC - EU Vaccination Certificate Generation

## Pre-Requisites
1. [Docker](https://www.docker.com/) should be running 

## Quick Start
1. bash shell 
   1. ```./build_docker.sh```
   1. ```./run_docker.sh```
1. other
   1. ```docker build -t nl/euvac .```
   1. ```docker run --rm -p 9090:5000 nl/euvac```

## Default Settings
### Port Mappings
By default we map 9090 on host to 5000 in the docker container with the
```-p 9090:5000``` argument to ```docker run```. The target port of 5000 is set in the docker, 
but feel free to map some other host port, as required. 

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
2. Run the command: ```python3.8 cose_sign.py | python3.8 cose_verify.py```
3. You should see the output: ```Hello World!```
