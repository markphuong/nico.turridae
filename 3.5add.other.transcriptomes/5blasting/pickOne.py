#!/usr/bin/env python

#this script will perform a reciprocal blast, and check for chimeric contigs and break them apart.

import os
import sys
import argparse
import multiprocessing
import dendropy
from collections import defaultdict

blast1 = sys.argv[1] #blastx output

out = open(sys.argv[4], 'w') #final fasta file

blast1_dict = dict()

blastlist = []

with open(blast1) as rfile:
	for line in rfile:
		info = line.strip().split('\t')
		if info[0] in blast1_dict.keys():
			continue

		else:
			blast1_dict[info[0]] = info[1]
mt_ncrna_dict = dict()

#mt_ncrna blast output
with open(sys.argv[2]) as rfile:
	for line in rfile:
		info = line.strip().split('\t')
                if info[0] in blast1_dict.keys():
                        continue

                else:
                        mt_ncrna_dict[info[0]] = info[1]

#print mt_ncrna_dict

#original clustered fasta file for name change
with open(sys.argv[3]) as rfile:
	for line in rfile:
		if ">" in line:
			if "len" in line:
				name = line.strip().split(' ')[0][1:]
			else:
				name = line.strip()[1:]
			seq = next(rfile)
			if name in blast1_dict.keys():
				protein = blast1_dict[name]
			else:
				protein = 'unannotated'
			if name in mt_ncrna_dict.keys():
				mt_ncrna = mt_ncrna_dict[name].replace('|','')
			else:
				mt_ncrna = 'not_junk'
			out.write(">" + name + '|' + sys.argv[3].split('_')[0]+ '|' + protein + '|' + mt_ncrna + '\n')
			out.write(seq)
