const cose = require('cose-js')
const fs = require('fs')
const rawHash = require("sha256-uint8array").createHash;
const { PEM, ASN1, Class, Tag } = require('@fidm/asn1')
const { Certificate, PrivateKey } = require('@fidm/x509')
const zlib = require('pako');
var cbor = require('cbor');


const cert = Certificate.fromPEM(fs.readFileSync('./dsc-worker.pem'))
var bytes = new Uint8Array(cert.raw);

const fingerprint = rawHash().update(cert.raw).digest();
const keyID = fingerprint.slice(0,8)

const pk = PrivateKey.fromPEM(fs.readFileSync('./dsc-worker.p8'))

var uint8ToBase45 = (function (exports) {
  'use strict';

  var encode = function encode(uint8array) {
    var output = [];

    for (var i = 0, length = uint8array.length; i < length; i+=2) {
      if (uint8array.length -i > 1) {
         var x = (uint8array[i]<<8)+ uint8array[i+1]
         var [ e, x ]  = divmod(x, 45*45)
         var [ d, c ] = divmod(x, 45)
         output.push(fromCharCode(c) + fromCharCode(d) + fromCharCode(e))
     } else {
         var x = uint8array[i]
         var [ d, c ] = divmod(x, 45)
         output.push(fromCharCode(c) + fromCharCode(d))
     }
    }
    return output.join('');
  };

  var divmod = function divmod(a,b) {
    var remainder = a
    var quotient = 0
    if (a > b) {
        remainder = a % b
	quotient = (a - remainder) / b
    }
    return [ quotient, remainder ]
  }

  const BASE45_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
  var fromCharCode = function fromCharCode(c) {
    return BASE45_CHARSET.charAt(c);
  };

  var decode = function decode(chars) {
    return Uint8Array.from(atob(chars), asCharCode);
  };

  exports.decode = decode;
  exports.encode = encode;

  return exports;

}({}));

// Highly ES256 specific - extract the 'D' for signing.
//
const keyD = Buffer.from(pk.keyRaw.slice(7,7+32))

const buffer = Buffer.alloc(4_096);
var len = fs.readSync(process.stdin.fd, buffer, 0, buffer.length)
var data = JSON.parse(buffer.slice(0,len))
const plaintext= cbor.encode(data)

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
  buf = zlib.deflate(buf)
  buf = uint8ToBase45.encode(buf)
  process.stdout.write(Buffer.from(buf).toString())
}).catch((error) => {
  console.log(error);
});
