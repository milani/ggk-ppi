#!/usr/bin/env python

import argparse
import sys
import os
import re
import subprocess

def choose_uniprot(text):
	grp = re.compile(r"^[^/]*/(?P<entry>([A-Z0-9\.:]*\.txt:DR)([^\n]*)(\n(\2)([^\n]*))*)$",re.M)
	resol = re.compile(r"^([A-Z0-9\.:]*)\.txt:DR\s+PDB; ([A-Z0-9]{4});\s+(X-ray|NMR|EM);\s+([0-9\.\-]+)(\s+A){0,1}; ([A-Za-z0-9])",re.M)
	n = [m.groupdict() for m in grp.finditer(text)]
	mapping = {}
	for i in n:
		resols = resol.findall(i['entry'])
		if len(resols) is not 0:
			top = min(resols, key = lambda t: 100.0 if t[3] == '-' else float(t[3]))
			mapping["%s-%s" % (top[1],top[5])] = top[0]

	return mapping

def parse_input(inputfile,outputfile,repo):
	pdb = inputfile.read()
	inputfile.close()

	pdbIds = pdb.split()
	uniqueIds = set(pdbIds)
	grep = subprocess.check_output("find %s -type f | xargs grep 'PDB;'" % repo,shell=True)
	mapping = choose_uniprot(grep)
	iterator = iter(pdbIds)
	for pdbId in iterator:
		try:
			map1 = mapping[pdbId]
			map2 = mapping[next(iterator)]
			if map1 != map2:
				outputfile.write("%s %s\n" % (map1,map2))
			else:
				print(pdbId)
		except:
			print("excp")

	outputfile.close()

def main():
	parser = argparse.ArgumentParser(prog='pdb2ppi',description='Convert back pdb ids to uniprotkb accession number')
	parser.add_argument('inputfile',type=argparse.FileType('r'))	
	parser.add_argument('outputfile',type=argparse.FileType('w'))
	parser.add_argument('--repository-dir','-r',dest='repo',type=str)
	args = parser.parse_args()
	parse_input( args.inputfile, args.outputfile,args.repo)

if __name__ == '__main__':
	main()
