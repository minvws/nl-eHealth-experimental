// // Copyright 2021 De Staat der Nederlanden, Ministerie van Volksgezondheid, Welzijn en Sport.
// // Licensed under the EUROPEAN UNION PUBLIC LICENCE v. 1.2
// // SPDX-License-Identifier: EUPL-1.2

//https://tools.ietf.org/html/draft-faltstrom-baseBaseSize-01
//PROOF OF CONCEPT ONLY!!! NOT FOR PRODUCTION USE!!!
//Requires review by someone knowledgable of javascript
export class Base45Encoding {
    constructor() { 
        this._Encoding = new Array('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
                        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
                        'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '$', '%', '*', 
                        '+', '-', '.', '/', ':' );

        this._Decoding = {};
        for(var i = 0; i < this._Encoding.length; i++)
        {
            var k = this._Encoding[i];
            this._Decoding[k] = i;
        }
    }

    encode(buffer) 
    {
        if (buffer == null)
            throw new Error("buffer is null.");

        var result = new Array(Math.trunc(buffer.length / 2) * 3 + (buffer.length % 2 == 1 ? 2 : 0));

        if (result.length == 0)
            return '';

        var resultIndex = 0;
        var count2 = Math.trunc(buffer.length / 2) * 2;
        for (var i = 0; i < count2; i+=2)
        {
            var value = buffer[i] * 256 + buffer[i+1];
            result[resultIndex++] = this._Encoding[Math.trunc(value % 45)];
            result[resultIndex++] = this._Encoding[Math.trunc(value / 45) % 45];
            result[resultIndex++] = this._Encoding[Math.trunc(value / 2025) % 45];
        }

        if (Math.trunc(buffer.length % 2) == 0)
            return result.join('');

        result[resultIndex] = this._Encoding[buffer[buffer.length-1] % 45];
        result[result.length-1] = buffer[buffer.length-1] < 45 ? this._Encoding[0] : this._Encoding[Math.trunc(buffer[buffer.length-1] / 45) % 45]; 

        return result.join('');
    }

    decode(value)
    {
        if (value == null)
            throw new Error("value is null");

        if (value.length == 0)
            return new Uint8Array();

        var mod3 = value.length % 3;
        if (mod3 == 1)
            throw new Error("Incorrect length.");

        var chars = value.split('');
        var buffer = new Array(chars.length);
        for (var i = 0; i < chars.length; i++)
        {
            var lookup = chars[i];
            buffer[i] = this._Decoding[lookup];
            if (buffer[i] === undefined)
              throw new Error("Invalid character at position ".concat(i).concat("."));
        }

        var div3 = Math.trunc(buffer.length / 3);
        var result = new Uint8Array(div3 * 2 + (mod3 == 2 ? 1 : 0));
        var resultIndex = 0;
        var count3 = div3 * 3;
        for (var i = 0;  i < count3; )
        {
            var val = buffer[i++] + 45 * buffer[i++] + 2025 * buffer[i++];
            result[resultIndex++] = Math.trunc(val / 256) % 256; 
            result[resultIndex++] = Math.trunc(val % 256);
        }

        if (mod3 != 2) 
            return result;
        
        result[result.length-1] = Math.trunc(buffer[buffer.length-2] + 45 * buffer[buffer.length-1]);
        return result;
    }
}
