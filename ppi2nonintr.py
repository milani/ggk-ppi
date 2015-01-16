#!/usr/bin/env python

import argparse
import sys
import os
import re
import subprocess
import itertools
import random

def parse_input(inputfile,outputfile,allinteracts):
	ppi = inputfile.read()
	inputfile.close()

	allppi = allinteracts.read()
	allinteracts.close()
	alls = allppi.split()

	uniprotIds = ppi.split()
	uniqueIds = set(uniprotIds)

	iterator = iter(uniprotIds)

	interactions = list()
	for uniprotId in iterator:
		interactions.append((uniprotId,next(iterator)))

	iterator = iter(alls)
	negatome = list()
	for uniprotId in iterator:
		negatome.append((uniprotId,next(iterator)))

	product = itertools.product(uniqueIds,uniqueIds)
	products = list(product)

	noninteractions = list()

	sample_size = len(interactions)

	while len(noninteractions) < sample_size:
		sample = random.choice(products)
		if sample not in interactions and sample[1] != sample[0] and sample in negatome:
			noninteractions.append(sample)

	for (i,j) in iter(noninteractions):
		outputfile.write("%s %s\n" % (i,j) )

	# for uniprotId in iterator:
	# 	try:
	# 		outputfile.write("%s %s\n" % (mapping[uniprotId],mapping[next(iterator)]))
	# 	except:
	# 		print("excp")
		
	
	outputfile.close()

def main():
	parser = argparse.ArgumentParser(prog='ppi2nonintr',description='Generates a non-interaction set for a ppi network')
	parser.add_argument('inputfile',type=argparse.FileType('r'))	
	parser.add_argument('allinteracts',type=argparse.FileType('r'))
	parser.add_argument('outputfile',type=argparse.FileType('w'))
	args = parser.parse_args()
	parse_input( args.inputfile, args.outputfile, args.allinteracts)

if __name__ == '__main__':
	main()
