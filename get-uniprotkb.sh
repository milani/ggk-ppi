#!/bin/sh

IDS=`cat $1`
OUT=$2

for i in $IDS;
do
	wget -nc http://www.uniprot.org/uniprot/$i.txt -O $OUT/$i.txt
done
