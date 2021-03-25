"""Base45 encoding for QR Codeo

   Source: https://gist.github.com/jschlyter/23e5e138b3c474909aa16ece14cfc9bf
"""

QR_ALPHANUM_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"

def encode(b: bytes, charset: str = QR_ALPHANUM_CHARSET) -> str:
    """Convert bytes to base45-encoded string"""
    res = ""
    buf = list(b)
    while buf:
        if len(buf) >= 2:
            x = (buf.pop(0) << 8) + buf.pop(0)
            x2 = x
            c = x // 45 // 45
            x -= c * 45 * 45
            d = x // 45
            x -= d * 45
            e = x
            res += charset[c]
            res += charset[d]
            res += charset[e]
        else:
            x = buf.pop(0)
            x2 = x
            c = None
            d = x // 45
            x -= d * 45
            e = x
            res += charset[d]
            res += charset[e]
    return res

def decode(s: str, charset: str = QR_ALPHANUM_CHARSET) -> bytes:
    """Decode base45-encoded string to bytes"""
    res = []
    buf = [charset.index(c) for c in s]
    while buf:
        if len(buf) >= 3:
            (c, d, e) = (buf.pop(0), buf.pop(0), buf.pop(0))
            x = c * 45 * 45 + d * 45 + e
            a = x // 256
            b = x % 256
            res.extend([a, b])
        else:
            (d, e) = (buf.pop(0), buf.pop(0))
            c = None
            x = d * 45 + e
            a = x // 256
            b = x % 256
            res.extend([b])
    return bytes(res)

