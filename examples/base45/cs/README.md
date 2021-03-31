# A Base45 implementation in C#
## Base 45 Specification
Currently, Base45 is a draft IETF specification located at https://tools.ietf.org/html/draft-faltstrom-base45-02

This draft specification is implemented here using C# 9.0 and .NET 5 and has been tested in both Windows 10 and Linux (Mint 20.1, Ubuntu 20.04.2) environments.

## C# API

Encoding a byte array as a string:

```
    byte[] input = <initialise your array here>;
    string result = new Base45Encoding().Encode(input);
```

An exception is thrown for null input.

Decoding a string to a byte array:

```
    string input = <initialise your string here>;
    byte[] result = new Base45Encoding().Decode(input);
```

Exceptions iare thrown for null input, input with the wrong length or an input that contains a character that are is not in the base45 set.
