#!/usr/bin/env python

from __future__ import print_function
import argparse
import Bio.PDB
import gzip
import sys

def parse_input(inputfile,chains,atomName):
	parser = Bio.PDB.PDBParser()
	pdb = parser.get_structure('Protein',gzip.open(inputfile,"r"))
	model = pdb[0]
	atoms = []

	chosen = chains

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

		for residue in chosen:
			if (Bio.PDB.Polypeptide.is_aa(residue)):
				(het,sid,ic) = residue.id
				if (het == ' ' and atomName in residue):
					atoms.append(residue[atomName])

	elif (chosen[0] == 'All'):
		for chain in model:
			if (chain.get_id() != ' '):
				for residue in chain:
					if (Bio.PDB.Polypeptide.is_aa(residue)):
						(het,sid,ic) = residue.id
						if (het == ' ' and atomName in residue):
							atoms.append(residue[atomName])

	else:
		for chain in model:
			if (chain.get_id() != ' ' and chain.get_id() in chosen):
				for residue in chain:
					if (Bio.PDB.Polypeptide.is_aa(residue)):
						(het,sid,ic) = residue.id
						if (het == ' ' and atomName in residue):
							atoms.append(residue[atomName])


	print("Atoms: {0}".format(len(atoms)),file=sys.stdout)
	return atoms

def surface_atoms(inputfile,chains,atomName):
	basic_surface = {'A':129.0, 'R':274.0, 'N':195.0, 'D':193.0, 'C':167.0, 'E':223.0, 'Q':225.0, 'G':104.0, 'H':224.0, 'I':197.0, 'L':201.0, 'K':236.0, 'M':224.0, 'F':240.0, 'P':159.0, 'S':155.0, 'T':172.0, 'W':285.0, 'Y':263.0, 'V':174.0}
	parser = Bio.PDB.PDBParser()
	three_to_one = Bio.PDB.Polypeptide.three_to_one
	is_aa = Bio.PDB.Polypeptide.is_aa
	pdb = parser.get_structure('Protein',gzip.open(inputfile,"r"))
	model = pdb[0]
	dssp = Bio.PDB.DSSP(model,inputfile,dssp="mkdssp")
	atoms = []

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
				residue = dssp[(ch,res)]
				if residue[2] > 90:
					atoms.append(residue[0])
		# for residue in chosen:
		# 	if (Bio.PDB.Polypeptide.is_aa(residue)):
		# 		(het,sid,ic) = residue.id
		# 		if (het == ' ' and atomName in residue):
		# 			atoms.append(residue[atomName])

	# elif (chosen[0] == 'All'):
	# 	for chain in model:
	# 		if (chain.get_id() != ' '):
	# 			for residue in chain:
	# 				if (Bio.PDB.Polypeptide.is_aa(residue)):
	# 					(het,sid,ic) = residue.id
	# 					if (het == ' ' and atomName in residue):
	# 						atoms.append(residue[atomName])

	else:
		for (ch,res) in dssp_keys:
			if ch != ' ' and ch in chosen:
				residue = dssp[(ch,res)][0]
				(het,sid,ic) = residue.id
				if (not is_aa(residue) or het != ' ' or residue.get_resname() == 'UNK'):
					continue
				resid = three_to_one(residue.get_resname())
				acc = dssp[(ch,res)][2]
				if acc > 0.50:
					atoms.append(residue['CA'])

	print("Atoms: {0}".format(len(atoms)),file=sys.stdout)
	return atoms

def generate_graph(output,atoms,dist):
	edges=[]
	for i in range(0,len(atoms)):
		for j in range(i+1,len(atoms)):
			if dist > atoms[i] - atoms[j]:
				edges.append([i,j])

	edgeNum = len(edges)
	nodeNum = max(max(edges,key=lambda x:(x[1] if x[1]>x[0] else x[0]))) + 1
	
	# write header
	print("{0} {1}".format(nodeNum,edgeNum),file=output)

	# write edges
	for edge in edges:
		print("{0} {1}".format(edge[0],edge[1]),file=output)

def main():
	parser = argparse.ArgumentParser(prog='pdbtograph',description='Generates graph representation of atoms contained in a protein chain')
	parser.add_argument('inputfile',type=str)
	parser.add_argument('outputfile',type=argparse.FileType('w'))
	parser.add_argument('--max-dist','-d',dest='dist',nargs='?',type=float,default=6)
	parser.add_argument('--atom-name','-a',dest='atom',default='CA')
	parser.add_argument('--chain','-c',dest='chain',default=['Max'])
	args = parser.parse_args()
	atoms = parse_input( args.inputfile, args.chain, args.atom)
	#atoms = surface_atoms( args.inputfile, args.chain, args.atom)
	generate_graph( args.outputfile, atoms, args.dist)
	args.outputfile.close()

if __name__ == '__main__':
	main()

