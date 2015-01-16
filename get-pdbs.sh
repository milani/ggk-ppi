#!/bin/bash

IDS=`cat $1`
OUT=$2

for i in $IDS;
do
	PDB=${i:0:4}
	wget -nc http://www.rcsb.org/pdb/files/$PDB.pdb.gz -O $OUT/$PDB.pdb.gz
done
