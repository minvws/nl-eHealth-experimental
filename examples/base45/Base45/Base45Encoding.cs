using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

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

            var result = new StringBuilder();
            var twoBytes = (buffer.Length / 2) * 2;
            for (var i = 0; i < twoBytes; i += 2)
                result.Append(IntToStringFast(buffer[i] * 256 + buffer[i + 1]));

            if (buffer.Length % 2 == 1)
                result.Append(IntToStringFast(buffer.Last()).PadRight(2, _Encoding[0]));

            return result.ToString();
        }

        public byte[] Decode(string value)
        {
            if (value == null)
                throw new ArgumentNullException(nameof(value)); //TODO or return new byte[0] ?

            if (value.Length == 0)
                return new byte[0];

            var mod = value.Length % 3;
            if (mod == 1)
                throw new FormatException("Incorrect length.");

            if (value.Any(x => !_Decoding.ContainsKey(x))) //Storing the mapping at this point undesirable cos it doubles memory usage
                throw new FormatException("Invalid characters.");

            var div = value.Length / 3;
            var result = new byte[div * 2 + (mod == 2 ? 1 : 0)];
            var resultIndex = 0;
            for (var i = 0; i < div * 3; i += 3)
            {
                var chunk = DecodeChunk(value.ToCharArray(i, 3));
                Array.Copy(chunk, 0, result, resultIndex, 2);
                resultIndex += 2;
            }

            if (mod == 2)
            {
                var chunk = DecodeChunk(value.ToCharArray(div * 3, 2));
                Array.Copy(chunk, 0, result, resultIndex, 1);
            }

            return result;
        }

        private static byte[] DecodeChunk(char[] chunk)
        {
            var value = ChunkToInt(chunk);
            var buffer = new byte[chunk.Length - 1]; //Cos value length 3 -> 2 bytes and 2 -> 1.
            for (var j = buffer.Length - 1; j >= 0; j--)
            {
                buffer[j] = Convert.ToByte(value % 256);
                value /= 256;
            }

            return buffer.ToArray();
        }

        private static int ChunkToInt(char[] chunk)
        {
            var result = 0;
            var factor = 1;
            foreach (var i in chunk)
            {
                result += _Decoding[i] * factor;
                factor *= 45;
            }

            return result;
        }

        /// <summary>
        /// Inspired by https://stackoverflow.com/questions/923771/quickest-way-to-convert-a-base-10-number-to-any-base-in-net
        /// TODO fill the result directly in reverse and murder the do while
        /// </summary>
        private static string IntToStringFast(int value)
        {
            const int bufferSize = 3;
            var i = bufferSize;
            var buffer = new char[i];
            do
            {
                buffer[--i] = _Encoding[value % 45];
                value = value / 45;
            }
            while (value > 0);

            var result = new char[bufferSize - i];
            Array.Copy(buffer, i, result, 0, bufferSize - i);

            return new string(result.Reverse().ToArray());
        }
    }
}