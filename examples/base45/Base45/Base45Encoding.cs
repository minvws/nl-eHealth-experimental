using System;
using System.Collections.Generic;

namespace NL.Mefitihe.Encoding
{
    /// <summary>
    /// https://tools.ietf.org/html/draft-faltstrom-base45-01
    /// </summary>
    public class Base45Encoding
    {
        private static readonly char[] _Encoding = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                                                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
                                                    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
                                                    'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '$', '%', '*', 
                                                    '+', '-', '.', '/', ':' };

        private static readonly Dictionary<char, int> _Decoding = new(45);

        static Base45Encoding()
        {
            for(var i = 0; i < _Encoding.Length; i++)
                _Decoding.Add(_Encoding[i], i);
        }

        public string Encode(byte[] buffer)
        {
            if (buffer == null)
                throw new ArgumentNullException(nameof(buffer));

            var result = new char[buffer.Length / 2 * 3 + (buffer.Length % 2 == 1 ? 2 : 0)];

            if (result.Length == 0)
                return string.Empty;

            var resultIndex = 0;
            var count2 = buffer.Length / 2 * 2;
            for (var i = 0; i < count2; i += 2)
            {
                var value = buffer[i] * 256 + buffer[i + 1];
                result[resultIndex++] = _Encoding[value % 45];
                result[resultIndex++] = _Encoding[value / 45 % 45];
                result[resultIndex++] = _Encoding[value / 2025 % 45];
            }

            if (buffer.Length % 2 == 0)
                return new string(result);

            result[resultIndex] = _Encoding[buffer[^1] % 45];
            
            //TODO test for buffer[^1] <= or < 45 ????
            result[^1] = buffer[^1] <= 45 ? _Encoding[0] : _Encoding[buffer[^1] / 45 % 45]; 

            return new string(result);
        }

        public byte[] Decode(string value)
        {
            if (value == null)
                throw new ArgumentNullException(nameof(value));

            if (value.Length == 0)
                return Array.Empty<byte>();

            var mod3 = value.Length % 3;
            if (mod3 == 1)
                throw new FormatException("Incorrect length.");

            var buffer = new int[value.Length];
            for (var i = 0; i < value.Length; i++)
            {
                if (_Decoding.TryGetValue(value[i], out var decoded))
                {
                    buffer[i] = decoded;
                    continue; //Earliest return on expected path.
                }

                throw new FormatException($"Invalid character at position {i}.");
            }

            var div3 = buffer.Length / 3;
            var result = new byte[div3 * 2 + (mod3 == 2 ? 1 : 0)];
            var resultIndex = 0;
            var count3 = div3 * 3;
            for (var i = 0;  i < count3; )
            {
                var val = buffer[i++] + 45 * buffer[i++] + 2025 * buffer[i++];
                result[resultIndex++] = Convert.ToByte(val / 256 % 256); 
                result[resultIndex++] = Convert.ToByte(val % 256);
            }

            if (mod3 != 2) 
                return result;
            
            result[^1] = Convert.ToByte(buffer[^2] + 45 * buffer[^1]);
            return result;
        }
    }
}