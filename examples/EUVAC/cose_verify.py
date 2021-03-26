#!env python3.8
import base45
import sys
import zlib

from cose.curves import Ed25519
from cose.keys import CoseKey
from cose.keys.keyops import SignOp, VerifyOp
from cose.keys.keyparam import KpKty, OKPKpX, KpKeyOps, OKPKpCurve
from cose.keys.keytype import KtyOKP
from cose.messages import CoseMessage
from cryptography import x509
from cryptography.hazmat.primitives import serialization

b45in = sys.stdin.read()
cin = base45.b45decode(b45in)
# cin = sys.stdin.buffer.read()
encoded = zlib.decompress(cin)

with open("dsc-worker.pem", "rb") as file:
    pem = file.read()
cert = x509.load_pem_x509_certificate(pem)
pub = cert.public_key().public_bytes(
    encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
)

decoded = CoseMessage.decode(encoded)
decoded.key = CoseKey.from_dict(
    {KpKty: KtyOKP, OKPKpCurve: Ed25519, KpKeyOps: [SignOp, VerifyOp], OKPKpX: pub}
)
if decoded.verify_signature():
    print("Happy")
    print(decoded.payload.decode('UTF_8'))
else:
    print("FAIL")
