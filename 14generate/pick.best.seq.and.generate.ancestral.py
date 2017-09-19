#!/usr/bin/env python

from Bio import SeqIO
import os
import sys
from collections import defaultdict
from pprint import pprint
import argparse
import multiprocessing
import re
from os import listdir
from os.path import isfile, join


def checkoverlap(seq1, seq2):
	num = 0
	diff = 0



	for i, nucleotide in enumerate(seq1):
		couple = [nucleotide, seq2[i]]
		if couple[0] == "-":
			continue
		elif couple[1] == "-":
			continue
		else:
			num += 1


	return float(num)/len(seq1)

def pdist(seq1, seq2):
	"""Sequences must be strings, have the same length, and be aligned"""
	num = 0
	diff = 0
	for i, nucleotide in enumerate(seq1):
		couple = [nucleotide, seq2[i]]
		if couple[0] == "-":
			continue
		elif couple[1] == "-":
			continue
		elif couple[0] == couple[1]:
			num += 1
		elif not couple[0] == couple[1]:
			num += 1
			diff += 1
	if num == 0:
		return 'nope'
	else:
		pdist = float(diff)/float(num)
		return str(pdist)[0:6]

def getancestral(athing, reference,ID, set):
	test = open('tempseq', 'w')
	reference = reference + '\n'
	athing = athing + '\n'
	refname = '>Ref' + '\n'
	conoideaname = '>otherseq' + '\n'
	test.write(refname)
	test.write(reference)
	test.write(conoideaname)
	test.write(athing)
	test.close()
	cmd = '/home/phuong/FastML.v3.1/programs/fastml/fastml -s tempseq -g -qf'
	os.system(cmd)
	ancestralfile = open('seq.marginal.txt', 'r')
	for line in ancestralfile:
		if ">N1" in line:
			ancestral = next(ancestralfile).strip()
	#		print ancestral

	cmd = 'mv ' + 'seq.marginal.txt ' + '/pylon5/bi4s86p/phuong/nico.turridae/14generate/results/' + ID + '_ancestral_' + set 
	os.system(cmd)

	return [ancestral, pdist(reference.strip(), athing.strip()), pdist(reference.strip(), ancestral), pdist(athing.strip(), ancestral)]
	


onlyfiles = [f for f in os.listdir('.') if os.path.isfile(f)]

ancestralfile = open('turrid.2017.baits.fa', 'w')

for thing in onlyfiles:

	if '.fa' in thing:

		ID = thing.split('_')[0]
		
		set = thing.split('_')[1].split('.')[0]


		myfasta = open(thing, 'r')




		for line in myfasta:
			if ">" in line:
				id1 = line.strip()[1:]
				seq1 = next(myfasta).strip().replace('n','-').upper()
				id2 = next(myfasta).strip()[1:]
				seq2 = next(myfasta).strip().replace('n','-').upper()

		myfasta.close()

		ancestral = getancestral(seq1, seq2, ID, set)

		output = ">" + ID + '|' + id1 + '|' + id2 + '|'+ ancestral[1] + '|' + ancestral[2] + '|' + ancestral[3] + '\n'
		ancestralfile.write(output)
		ancestralfile.write(ancestral[0] + '\n')


ancestralfile.close()





