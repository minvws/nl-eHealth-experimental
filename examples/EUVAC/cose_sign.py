#!env python3.8
import sys
import zlib
from base45 import b45encode

from cose.algorithms import EdDSA
from cose.curves import Ed25519
from cose.headers import Algorithm, KID
from cose.keys import CoseKey
from cose.keys.keyops import SignOp, VerifyOp

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key


# Note - we only need the public key for the KeyID calcualtion - we're not actually using it.
with open('dsc-worker.pem','rb') as file:
  pem = file.read()
cert = x509.load_pem_x509_certificate(pem)
fingerprint = cert.fingerprint(hashes.SHA256())
keyid = fingerprint[-8:]

# Read in the private key that we use to actually sign this
#
with open('dsc-worker.key','rb') as file:
  pem = file.read()
keyfile= load_pem_private_key(pem, password=None)
priv = keyfile.private_bytes(
    encoding=serialization.Encoding.Raw, 
    format=serialization.PrivateFormat.Raw, 
    encryption_algorithm=serialization.NoEncryption()
)

# Prepare a message to sign; specifying algorithm and keyid
# that we (will) use
#
msg = Sign1Message(
	phdr = {Algorithm: EdDSA, KID: keyid},
	payload = 'Hello World'.encode('utf-8')
)

# Create the signing key.
cose_key = {
	KpKty: KtyOKP,
	OKPKpCurve: Ed25519, # Ought to be pk.curve - but the two libs clash
	KpKeyOps: [SignOp, VerifyOp],
	OKPKpD: priv,
}

# Encode the message (which includes signing)
#
msg.key= CoseKey.from_dict(cose_key)
encoded = msg.encode()

# Compress with ZLIB
#
out = zlib.compress(encoded,9)
# sys.stdout.buffer.write(out)

# And base45 encode the result
#
b45 = b45encode(out)

sys.stdout.write(b45)
