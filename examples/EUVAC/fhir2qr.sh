#!/bin/bash -e

# fhir2qr.sh - use this script to run the webserver standalone

# Make sure that the test certs have bean created
#
test -e dsc-worker.key || sh gen-csca-dsc.sh

export FLASK_APP=fhir2qr.py
export FLASK_ENV=development
flask run --host 127.0.0.1 --port 5000
