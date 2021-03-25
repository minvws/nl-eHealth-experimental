#!env python3.8
import attr, sys

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

with open('dsc-worker.key','rb') as file:
  pem = file.read()
keyfile= load_pem_private_key(pem, password=None)
priv = keyfile.private_bytes(encoding=serialization.Encoding.Raw, format=serialization.PrivateFormat.Raw, encryption_algorithm=serialization.NoEncryption())

msg = Sign1Message(
	phdr = {Algorithm: EdDSA, KID: b'k1'},
	payload = 'Hello World'.encode('utf-8')
)

cose_key = {
	KpKty: KtyOKP,
	OKPKpCurve: Ed25519, # pk.curve,
	KpKeyOps: [SignOp, VerifyOp],
	OKPKpD: priv,
}

cose_key = CoseKey.from_dict(cose_key)

msg.key = cose_key
encoded = msg.encode()

sys.stdout.buffer.write(encoded)
