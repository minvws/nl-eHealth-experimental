#!/bin/bash -e
dotnet_ver=$(/home/euvac/.dotnet/dotnet --version)
echo "dotnet version is: ${dotnet_ver}"
ip addr
export FLASK_APP=fhir2qr.py
export FLASK_ENV=development
flask run --host 0.0.0.0
