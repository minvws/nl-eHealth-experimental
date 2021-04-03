// // Copyright 2021 De Staat der Nederlanden, Ministerie van Volksgezondheid, Welzijn en Sport.
// // Licensed under the EUROPEAN UNION PUBLIC LICENCE v. 1.2
// // SPDX-License-Identifier: EUPL-1.2

import { Base45Encoding } from './base45';

//Tests
var e = new Base45Encoding();

var te = new TextEncoder();
console.log("Encoding...");
console.log("empty should be empty: '".concat(e.Encode(te.encode(""))).concat("'"));
console.log("0 should be 31: '".concat(e.Encode(te.encode("0"))).concat("'"));
console.log("AB should be BB8: '".concat(e.Encode(te.encode("AB"))).concat("'"));
console.log("Hello!! should be %69 VD92EX0: '".concat(e.Encode(te.encode("Hello!!"))).concat("'"));
console.log("base-45 should be UJCLQE7W581: '".concat(e.Encode(te.encode("base-45"))).concat("'"));

console.log("Decoding...");

var td = new TextDecoder();
console.log("31 should be 0: '".concat(td.decode(e.Decode("31"))).concat("'"));
console.log("BB8 should be AB: '".concat(td.decode(e.Decode("BB8"))).concat("'"));
console.log("%69 VD92EX0 should be Hello!!: '".concat(td.decode(e.Decode("%69 VD92EX0"))).concat("'"));
console.log("UJCLQE7W581 should be base-45: '".concat(td.decode(e.Decode("UJCLQE7W581"))).concat("'"));

console.log("+++End+++");

//e.Decode("  ^");
e.Decode();
