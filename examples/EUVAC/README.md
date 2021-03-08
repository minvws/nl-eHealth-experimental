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
By default we map 8080 on host to 3030 in the docker container
