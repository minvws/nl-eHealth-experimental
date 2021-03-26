#!env python3.8
import sys
import zlib

from cose.algorithms import EdDSA
from cose.curves import Ed25519
from cose.headers import Algorithm, KID
from cose.keys import CoseKey
from cose.keys.keyops import SignOp, VerifyOp
from cose.keys.keyparam import KpKty, OKPKpD, KpKeyOps, OKPKpCurve
from cose.keys.keytype import KtyOKP
from cose.messages import Sign1Message
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key

import base45

with open("dsc-worker.key", "rb") as file:
    pem = file.read()
keyfile = load_pem_private_key(pem, password=None)
priv = keyfile.private_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PrivateFormat.Raw,
    encryption_algorithm=serialization.NoEncryption(),
)

msg = Sign1Message(
    phdr={Algorithm: EdDSA, KID: b"k1"}, payload="Hello World".encode("utf-8")
)

cose_key = {
    KpKty: KtyOKP,
    OKPKpCurve: Ed25519,  # pk.curve,
    KpKeyOps: [SignOp, VerifyOp],
    OKPKpD: priv,
}

cose_key = CoseKey.from_dict(cose_key)

msg.key = cose_key
encoded = msg.encode()

out = zlib.compress(encoded, 9)
# sys.stdout.buffer.write(out)

b45 = base45.b45encode(out)
sys.stdout.write(b45)
