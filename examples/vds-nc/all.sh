#!/bin/sh
set -e

for i in appendix-h stripped stripped-keyid
do
	sh gen.sh $i
done

