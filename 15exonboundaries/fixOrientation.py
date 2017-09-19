#!/usr/bin/env python

import os
import sys
import argparse
import multiprocessing
import dendropy
from collections import defaultdict
from Bio.Seq import translate
from Bio.Seq import reverse_complement
from Bio import SearchIO

blastxfile = open('fixOrientation.blastx', 'r')

seenlist = []

reverselist = []

for line in blastxfile:
	if 'index' in line:
		start = int(line.strip().split('\t')[6])
		end = int(line.strip().split('\t')[7])
		info = line.strip().split('\t')[0].split('|')[-1].split('_')[-1]
		if info in seenlist:
			continue
		else:
			seenlist.append(info)
			if start > end:
				reverselist.append(info)
			else:
				continue


mybaits = open('all_conoidea_markers.fasta', 'r')

out = open('all_conoidea_markers_fixOrientation.fasta', 'w')

for line in mybaits:
	if "Mitra" in line:
		out.write(line)
		out.write(next(mybaits))
	elif ">" in line:
#		print line
		info = line.strip().split('|')[-1].split('_')[1]
		if info in reverselist:
			out.write(line)
			out.write(reverse_complement(next(mybaits).strip())+'\n')
		else:
			out.write(line)
			out.write(next(mybaits))
















