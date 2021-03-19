QRFLAGS="-m 0 -s 1"
set -e

gs() {
rm -f x.png; touch x.png
cat > x.raw
X=`cat x.raw | wc -c`
l=40
for i in 40 39 38 37 36 35 34 33 32 31 30 29 28 27 26 25 24 23 20 19 18 17 16 15 14 13 12 11 10 9 8
do
	cat x.raw | qrencode ${QRFLAGS} -v$i $*  -l $E -o xx.png 2>/dev/null || break
	if ! cmp -s xx.png x.png ; then
		cp xx.png x.png
		l=$i
		continue
	fi


	F=`file x.png | sed -e 's/.*data, //' -e 's/,.*//'`
	set $F
	L=`expr $1 \* $3`
	echo "$X	$F 	$L pixels (level $l)"
	return
done
echo "$X	FAIL"
}

for E in L M Q H
do
rm -f x.png
/bin/echo -n "plain/8		$E	"
cat appendix-h.json| gs 

/bin/echo -n "b45/8		$E	"
cat appendix-h.json| ~/go/bin/qrbase45tool  -i /dev/stdin -o /dev/stdout | gs -8

/bin/echo -n "b45/2		$E	"
cat appendix-h.json| ~/go/bin/qrbase45tool  -i /dev/stdin -o /dev/stdout | gs

/bin/echo -n "zl/8		$E	"
cat appendix-h.json| openssl zlib | gs -8

/bin/echo -n "zl/b45/2	$E	"
cat appendix-h.json| openssl zlib | ~/go/bin/qrbase45tool  -i /dev/stdin -o /dev/stdout | gs

/bin/echo -n "C/zl/8		$E	"
cat appendix-h.json| json2cbor | openssl zlib | gs -8

/bin/echo -n "C/zl/b45/2	$E	"
cat appendix-h.json| json2cbor | openssl zlib | ~/go/bin/qrbase45tool  -i /dev/stdin -o /dev/stdout | gs

echo
done

