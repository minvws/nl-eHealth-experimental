#!/bin/bash -e
dotnet_ver=$(/home/euvac/.dotnet/dotnet --version)
echo "dotnet version is: ${dotnet_ver}"
ip addr
# modprobe -v ip_tables
# modprobe -v iptable_nat
awall enable flask
export FLASK_APP=fhir2qr.py
export FLASK_DEBUG=1
flask run --host 0.0.0.0
