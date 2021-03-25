#!env python3.8
import attr

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
from cryptography.hazmat.backends.openssl import ec
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives import serialization 

from binascii import unhexlify, hexlify
import sys

encoded = sys.stdin.buffer.read()

with open('dsc-worker.pem','rb') as file:
  pem = file.read()
cert = x509.load_pem_x509_certificate(pem)
pub = cert.public_key().public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)

decoded = CoseMessage.decode(encoded)
decoded.key = CoseKey.from_dict({
        KpKty: KtyOKP,
        OKPKpCurve: Ed25519, 
        KpKeyOps: [SignOp, VerifyOp],
        OKPKpX: pub,
})
if (decoded.verify_signature()) :
  print("Happy")
  print(decoded.payload)
else:
  print("FAIL")

