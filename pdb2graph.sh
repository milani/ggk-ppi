#!/bin/bash

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DISTANCE=$1
LIST_FILE="$PWD/$2"
PDBS="$PWD/$3"
OUTPUT_ROOT="$PWD/$4"

if [ ! -d $OUTPUT_ROOT ]; then
  mkdir -p $OUTPUT_ROOT
fi

if [ ! -d $PDBS ]; then
  echo "Could not find PDB files in the path specified ($PDBS)."
  exit 1
fi

LIST=`cat $LIST_FILE`

for PDBChain in $LIST
do
  PDB=${PDBChain:0:4}
  CHAIN=${PDBChain:5:6}
  if [ ! -f $OUTPUT_ROOT/$PDB-$CHAIN.edges ]; then
    $BIN_DIR/pdb2graph.py -a CA -d $DISTANCE $PDBS/$PDB.pdb.gz $OUTPUT_ROOT/$PDB-$CHAIN.edges -c $CHAIN
  fi
  #echo "**************************** Processing  $PDB-$CHAIN ****************************"
done
