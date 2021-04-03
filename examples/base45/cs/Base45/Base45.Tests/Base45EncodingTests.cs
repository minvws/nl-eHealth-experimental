// // Copyright 2021 De Staat der Nederlanden, Ministerie van Volksgezondheid, Welzijn en Sport.
// // Licensed under the EUROPEAN UNION PUBLIC LICENCE v. 1.2
// // SPDX-License-Identifier: EUPL-1.2

using System;
using Xunit;

namespace NL.MinVWS.Encoding.Base45.Tests
{
    public class Base45EncodingTests
    {
        [Theory]
        [InlineData("", "")]
        [InlineData("0", "31")]
        [InlineData("AB", "BB8")]
        [InlineData("Hello!!", "%69 VD92EX0")]
        [InlineData("base-45", "UJCLQE7W581")]
        public void Encode(string input, string output)
        {
            var buffer = System.Text.Encoding.ASCII.GetBytes(input);
            var encoded = Base45Encoding.Encode(buffer);
            Assert.Equal(output, encoded);
        }

        [Fact]
        public void Boundary45Equal()
        {
            var buffer = new byte[] { 45 };
            var encoded = Base45Encoding.Encode(buffer);
            Assert.Equal(2, encoded.Length);
            var decoded = Base45Encoding.Decode(encoded);
            Assert.Equal(buffer, decoded);
        }

        [Theory]
        [InlineData(0, "")]
        [InlineData(1, "00")]
        [InlineData(10, "000000000000000")]
        public void EncodeArrayOfZeros(int len, string output)
        {
            var encoded = Base45Encoding.Encode(new byte[len]);
            Assert.Equal(output, encoded);
        }

        [Theory]
        [InlineData(0, "")]
        [InlineData(1, "00")]
        [InlineData(10, "000000000000000")]
        public void DecodeArrayOfZeros(int len, string output)
        {
            var decoded = Base45Encoding.Decode(output);
            Assert.Equal(new byte[len], decoded);
        }

        [Theory]
        [InlineData("", "")]
        [InlineData("0", "31")]
        [InlineData("AB", "BB8")]
        [InlineData("Hello!!", "%69 VD92EX0")]
        [InlineData("base-45", "UJCLQE7W581")]
        public void Decode(string output, string input)
        {
            var decoded = Base45Encoding.Decode(input);
            Assert.Equal(output, System.Text.Encoding.ASCII.GetString(decoded));
        }

        [Fact]
        public void EncodeNullGoBang()
        {
            Assert.Throws<ArgumentNullException>(() => Base45Encoding.Encode(null));
        }

        [Fact]
        public void DecodeNullGoBang()
        {
            Assert.Throws<ArgumentNullException>(() => Base45Encoding.Decode(null));
        }

        [Theory]
        [InlineData("1")]
        [InlineData("1234")]
        [InlineData("1234567")]
        public void DecodeInvalidLengthGoBang(string input)
        {
            var ex = Assert.Throws<FormatException>(() => Base45Encoding.Decode(input));
            Assert.Contains("length", ex.Message);
        }

        [Theory]
        [InlineData("^^^")]
        [InlineData("^^^^^^")]
        public void DecodeInvalidCharacterGoBang(string input)
        {
            var ex = Assert.Throws<FormatException>(() => Base45Encoding.Decode(input));
            Assert.Contains("character", ex.Message);
        }
    }
}
