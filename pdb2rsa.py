#!/usr/bin/env python

from __future__ import print_function
import argparse
import Bio.PDB
import gzip
import sys

def surface_area(inputfile,chains):
	parser = Bio.PDB.PDBParser()
	three_to_one = Bio.PDB.Polypeptide.three_to_one
	is_aa = Bio.PDB.Polypeptide.is_aa
	pdb = parser.get_structure('Protein',gzip.open(inputfile,"r"))
	model = pdb[0]
	dssp = Bio.PDB.DSSP(model,inputfile,dssp="mkdssp")
	# basic_surface = {'A':115, 'R':225, 'D':150, 'N':160, 'C':135,'E':190, 'Q':180, 'G':75,  'H':195, 'I':175,'L':170, 'K':200, 'M':185, 'F':210, 'P':145,'S':115, 'T':140, 'W':255, 'Y':230, 'V':155, 'X':1}
	basic_surface = {'A':129.0, 'R':274.0, 'N':195.0, 'D':193.0, 'C':167.0, 'E':223.0, 'Q':225.0, 'G':104.0, 'H':224.0, 'I':197.0, 'L':201.0, 'K':236.0, 'M':224.0, 'F':240.0, 'P':159.0, 'S':155.0, 'T':172.0, 'W':285.0, 'Y':263.0, 'V':174.0}

	rsa = 0

	chosen = chains

	dssp_keys = list(dssp.keys())
	if (chosen[0] == 'Max'):
		chosen = 'A'
		max = 0

		for chain in model:
			if (chain.get_id() != ' ' and max < len(chain)):
				ppb=Bio.PDB.CaPPBuilder(7)
				for pp in ppb.build_peptides(chain):
					if pp.get_ca_list():
						max = len(chain)
						chosen = chain
						break

		chosen = chosen.get_id()

		for (ch,res) in dssp_keys:
			if ch == chosen:
				acc = dssp[(ch,res)][2]
				if residue[2] > 90:
					atoms.append(residue[0])

	else:
		for (ch,res) in dssp_keys:
			print(ch)
			if ch != ' ' and ch in chosen:
				residue = dssp[(ch,res)][0]
				(het,sid,ic) = residue.id
				print(residue)
				if (not is_aa(residue) or het != ' ' or residue.get_resname() == 'UNK'):
					continue
				resid = three_to_one(residue.get_resname())
				acc = dssp[(ch,res)][2]
				print(acc/basic_surface[resid])
				rsa += acc/basic_surface[resid]

	rsa = 100 if rsa > 100 else rsa
	return rsa

def main():
	parser = argparse.ArgumentParser(prog='pdb2rsa',description='Calculates mean RSA for a protein chain')
	parser.add_argument('inputfile',type=str)
	#parser.add_argument('outputfile',type=argparse.FileType('w'))
	parser.add_argument('--chain','-c',dest='chain',nargs='*',default=['Max'])
	args = parser.parse_args()

	rsa = surface_area(args.inputfile, args.chain)
	print("%.4f" %rsa)
	#args.outputfile.close()

if __name__ == '__main__':
	main()

