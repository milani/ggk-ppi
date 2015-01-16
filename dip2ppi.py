#!/usr/bin/env python

import argparse
import sys
import re


def parse_input(inputfile,outputfile):
	pairs = re.compile(r"^([^\|]*\|){0,2}uniprotkb:(?P<from>[A-Za-z0-9\-]*)\t([^\|]*\|){0,2}uniprotkb:(?P<to>[A-Za-z0-9\-]*)")
	lines = inputfile.readlines()

	for line in lines:
		matches = pairs.match(line)
		if matches:
			outputfile.write("%s %s\n" % (matches.group('from'),matches.group('to')))

	inputfile.close()

def main():
	parser = argparse.ArgumentParser(prog='dip2list',description='Convert DIP dataset to tab separated file of uniprot\\tpdb\\tchain')
	parser.add_argument('inputfile',type=argparse.FileType('r'))
	parser.add_argument('outputfile',type=argparse.FileType('w'))
	args = parser.parse_args()
	parse_input( args.inputfile, args.outputfile)
	args.outputfile.close()

if __name__ == '__main__':
	main()
