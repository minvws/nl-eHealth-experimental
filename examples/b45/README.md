
# Various encoding options.

* plain: as is
* 8: force 8 bits even if less bits/symbol (e.g. 5.5. bits for base45) are an option
* 2: use best bits per symbol (i.e. less than 8 if possible) 
* b45: use base45 encoding
* zl: use zlib for compression
* C: use CBOR
* Az: uze Aztec rather than Qr.

Note - the Aztec is set to '25%' (detault is 23%) as to match the normal 'Q' level.

```
encoding        ECC         payload     pixels                       modules
plain/8         L           1391        125 x 125       15625 pixels (level 26)
b45/8           L           2027        149 x 149       22201 pixels (level 33)
b45/2           L           2027        125 x 125       15625 pixels (level 27)
zl/8            L            913        101 x 101       10201 pixels (level 20)
zl/b45/2        L           1330        101 x 101       10201 pixels (level 20)
C/zl/8          L            883        101 x 101       10201 pixels (level 20)
C/zl/b45/2      L           1287        101 x 101       10201 pixels (level 20)

plain/8         M           1391        141 x 141       19881 pixels (level 31)
b45/8           M           2027        169 x 169       28561 pixels (level 38)
b45/2           M           2027        141 x 141       19881 pixels (level 31)
zl/8            M            913        117 x 117       13689 pixels (level 25)
zl/b45/2        M           1330        117 x 117       13689 pixels (level 25)
C/zl/8          M            883        113 x 113       12769 pixels (level 24)
C/zl/b45/2      M           1287        113 x 113       12769 pixels (level 24)

plain/8         Q           1391        165 x 165       27225 pixels (level 37)
b45/8           Q           2027        FAIL (max at 40@H is 1273 bytes)
b45/2           Q           2027        165 x 165       27225 pixels (level 37)
zl/8            Q            913        137 x 137       18769 pixels (level 30)
zl/b45/2        Q           1330        137 x 137       18769 pixels (level 30)
C/zl/8          Q            883        133 x 133       17689 pixels (level 29)
C/zl/b45/2      Q           1287        133 x 133       17689 pixels (level 29)
C/zl/b45/2/Az   Q           1287        133 x 133       17689 pixels

plain/8         H           1391        FAIL (max at 40@H is 1273 bytes)
b45/8           H           2027        FAIL (max at 40@H is 1273 bytes)
b45/2           H           2027        FAIL (max at 40@H is 1273 bytes)
zl/8            H            913        153 x 153       23409 pixels (level 34)
zl/b45/2        H           1330        153 x 153       23409 pixels (level 34)
C/zl/8          H            883        149 x 149       22201 pixels (level 33)
C/zl/b45/2      H           1287        149 x 149       22201 pixels (level 33)

