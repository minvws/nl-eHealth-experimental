const cose = require('cose-js')
const fs = require('fs')
const forge = require('node-forge')
const { pki, md } = forge
const rawHash = require("sha256-uint8array").createHash;

const { PEM, ASN1, Class, Tag } = require('@fidm/asn1')
const { Certificate, PrivateKey } = require('@fidm/x509')

const sha256 = require('crypto-js/sha256')
const CryptoJS = require('crypto-js')

const cert = Certificate.fromPEM(fs.readFileSync('./dsc-worker.pem'))
var bytes = new Uint8Array(cert.raw);

const fingerprint = rawHash().update(cert.raw).digest();
const keyID = fingerprint.slice(0,8)
console.log("KeyID: " + keyID)
console.log("     0x"+ Buffer.from(keyID).toString('hex'))

const pk = PrivateKey.fromPEM(fs.readFileSync('./dsc-worker.p8'))
// Highly ES256 specific
const keyD = Buffer.from(pk.keyRaw.slice(7,7+32))
 
const plaintext = Buffer.from('foo')

const headers = {
  'p': {'alg': 'ES256', 'kid': keyID }, 
  'u': {}
};
const signer = {
  'key': {
    'd': keyD 
  }
};

cose.sign.create(
  headers,
  plaintext,
  signer)
.then((buf) => {
  console.log(buf.toString('base64'));
}).catch((error) => {
  console.log(error);
});
