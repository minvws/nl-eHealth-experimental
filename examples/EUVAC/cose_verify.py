#!env python3.8

import sys
import zlib

from base45 import b45decode
from cose.curves import Ed25519
from cose.headers import KID
from cose.keys import CoseKey
from cose.keys.keyops import SignOp, VerifyOp
from cose.keys.keyparam import KpKty, OKPKpX, KpKeyOps, OKPKpCurve
from cose.keys.keytype import KtyOKP
from cose.messages import CoseMessage
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

b45in = sys.stdin.read()
cin = b45decode(b45in)
encoded = zlib.decompress(cin)

decoded = CoseMessage.decode(encoded)

if len(sys.argv) != 2 or sys.argv[1] != "--ignore-signature":
    with open("dsc-worker.pem", "rb") as file:
        pem = file.read()
    cert = x509.load_pem_x509_certificate(pem)
    pub = cert.public_key().public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )
    fingerprint = cert.fingerprint(hashes.SHA256())
    keyid = fingerprint[-8:]

    if decoded.phdr[KID] != keyid:
        raise Exception("KeyID is unknown (not mine) -- cannot verify.")

    decoded.key = CoseKey.from_dict(
        {KpKty: KtyOKP, OKPKpCurve: Ed25519, KpKeyOps: [SignOp, VerifyOp], OKPKpX: pub}
    )

    if not decoded.verify_signature():
        raise Exception("faulty sig")

print(decoded.payload.decode('UTF-8'))
