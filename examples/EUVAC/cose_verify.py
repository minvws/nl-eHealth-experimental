#!env python3.8

import attr
import zlib
from base45 import b45decode

from cose.messages import Sign1Message, CoseMessage
from cose.keys import CoseKey
from cose.headers import Algorithm, KID
from cose.algorithms import EdDSA
from cose.curves import Ed25519
from cose.keys.keyparam import KpKty, OKPKpD, OKPKpX, KpKeyOps, OKPKpCurve
from cose.keys.keytype import KtyOKP
from cose.keys.keyops import SignOp, VerifyOp

from cryptography import x509
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends.openssl import ec
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives import serialization 

from binascii import unhexlify, hexlify
import sys

b45in = sys.stdin.read()
cin = b45decode(b45in)
encoded = zlib.decompress(cin)

with open('dsc-worker.pem','rb') as file:
  pem = file.read()
cert = x509.load_pem_x509_certificate(pem)
pub = cert.public_key().public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)
fingerprint = cert.fingerprint(hashes.SHA256())
keyid = fingerprint[-8:]

decoded = CoseMessage.decode(encoded)

if (decoded.phdr[KID] != keyid):
  raise Exception('KeyID is unknown (not mine) -- cannot verify.')

decoded.key = CoseKey.from_dict({
        KpKty: KtyOKP,
        OKPKpCurve: Ed25519, 
        KpKeyOps: [SignOp, VerifyOp],
        OKPKpX: pub,
})


if (not decoded.verify_signature()) :
  raise Exception('faulty sig')

print(decoded.payload)
