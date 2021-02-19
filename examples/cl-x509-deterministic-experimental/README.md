# Deterministic CL public key packaged in Subject Public Key field of X509 certificate

To run this experimental code run the following command in the directory:

`go run ./`

This example will first generate a safeprime Idemix keypair, and show how all parameters except the public modulus n can be generated deterministically. This allows to package the Idemix public key in the Subject Public Key field of a classic RSA X509 certificate.

The example also shows how the Idemix private key is usable as classic RSA key, for eample for revocation purpose. However, this usage is not recommended.