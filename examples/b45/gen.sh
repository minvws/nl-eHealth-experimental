QRFLAGS="-m 0 -s 1  "
set -e

gs() {
F=`file x.png | sed -e 's/.*data, //' -e 's/,.*//'`
set $F
L=`expr $1 \* $3`
echo "$F 	$L pixels"
}

for E in L M H Q
do
rm -f x.png
/bin/echo -n "plain/8		$E	"
cat appendix-h.json| qrencode ${QRFLAGS} -8 -l $E -o x.png 2>/dev/null &&  gs  || echo FAIL

/bin/echo -n "b45/8		$E	"
cat appendix-h.json| ~/go/bin/qrbase45tool  -i /dev/stdin -o /dev/stdout | qrencode  -8 ${QRFLAGS}  --l $E -o x.png 2>/dev/null && gs || echo FAIL

/bin/echo -n "b45/2		$E	"
cat appendix-h.json| ~/go/bin/qrbase45tool  -i /dev/stdin -o /dev/stdout | qrencode  ${QRFLAGS} -v 2 -l $E -o x.png 2>/dev/null && gs || echo FAIL

/bin/echo -n "zl/8		$E	"
cat appendix-h.json| openssl zlib | qrencode ${QRFLAGS} -8 -l $E -o x.png; gs

/bin/echo -n "zl/b45/2	$E	"
cat appendix-h.json| openssl zlib | ~/go/bin/qrbase45tool  -i /dev/stdin -o /dev/stdout | qrencode ${QRFLAGS}  -v2 -l $E -o x.png; gs

/bin/echo -n "C/zl/8		$E	"
cat appendix-h.json| json2cbor | openssl zlib | qrencode ${QRFLAGS} -8 -l $E -o x.png; gs

/bin/echo -n "C/zl/b45/2	$E	"
cat appendix-h.json| json2cbor | openssl zlib | ~/go/bin/qrbase45tool  -i /dev/stdin -o /dev/stdout | qrencode ${QRFLAGS}  -v2 -l $E -o x.png; gs

echo
done

