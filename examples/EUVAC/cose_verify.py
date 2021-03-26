#!env python3.8

import sys
import zlib
import argparse

import json
import cbor2

from base45 import b45decode
from base64 import b64decode

from cose.messages import Sign1Message, CoseMessage
from cose.messages import CoseMessage

from cose.headers import Algorithm, KID
from cose.curves import P256
from cose.algorithms import Es256, EdDSA

from cose.keys import CoseKey
from cose.keys.keyparam import KpKty, KpAlg, EC2KpD, EC2KpX, EC2KpY, EC2KpCurve
from cose.keys.keytype import KtyEC2
from cose.keys.keyops import SignOp, VerifyOp
from cose.keys.keyparam import KpKty, OKPKpX, KpKeyOps, OKPKpCurve
from cose.keys.keytype import KtyOKP

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

parser = argparse.ArgumentParser(
    description="Parse and validate a base45/zlib/cose/cbor QR."
)
parser.add_argument(
    "-B", "--base64", action="store_true", help="Use base64 instead of base45"
)
parser.add_argument(
    "-b", "--skip-base45", action="store_true", help="Skip base45 decoding"
)
parser.add_argument(
    "-z", "--skip-zlib", action="store_true", help="Skip zlib decompression"
)
parser.add_argument(
    "-i",
    "--ignore-signature",
    action="store_true",
    help="Ignore the signature, do not validate",
)
parser.add_argument("-c", "--cbor", action="store_true", help="Decode CBOR")
parser.add_argument(
    "cert", help="Certificate to validate against", default="dsc-worker.pem", nargs="?"
)
args = parser.parse_args()

cin = sys.stdin.buffer.read()

if args.base64:
    cin = b64decode(cin.decode("ASCII"))
else:
    if not args.skip_base45:
        cin = b45decode(cin.decode("ASCII"))
if not args.skip_zlib:
    cin = zlib.decompress(cin)

decoded = CoseMessage.decode(cin)

if not args.ignore_signature:
    with open(args.cert, "rb") as file:
        pem = file.read()
    cert = x509.load_pem_x509_certificate(pem)
    pub = cert.public_key().public_numbers()

    fingerprint = cert.fingerprint(hashes.SHA256())
    keyid = fingerprint[-8:]

    if decoded.phdr[KID] != keyid:
        raise Exception("KeyID is unknown (not mine) -- cannot verify.")

    decoded.key = CoseKey.from_dict(
        {
            KpKty: KtyEC2,
            EC2KpCurve: P256,  # Ought o be pk.curve - but the two libs clash
            KpAlg: Es256,  # ecdsa-with-SHA256
            EC2KpX: pub.x.to_bytes(32, byteorder="big"),
            EC2KpY: pub.y.to_bytes(32, byteorder="big"),
        }
    )

    if not decoded.verify_signature():
        raise Exception("faulty sig")

payload = decoded.payload

if args.cbor:
    payload = json.dumps(cbor2.loads(payload))
    print(payload)
    sys.exit(0)

sys.stdout.buffer.write(payload)
