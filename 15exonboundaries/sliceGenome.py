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


protein = open('Lottia.pep.reduced','r')

genome = open('Lottia.dna.reduced', 'r')
genomedict = dict()

for line in genome:
	if ">" in line:
		info = line.strip().split(' ')
		info = ':'.join(info[2].split(':')[:-3]) + ':'
		genomedict[info] = next(genome).strip()

out = open('Lottia.genome.sliced.reduced','w')

for line in protein:
	if ">" in line:
		info = line.strip().split(' ')
		protein = info[0].split('P')[1]

		info = info[2].split(':')
		start = int(info[-3])
		end = int(info[-2])
		strand = int(info[-1])
		

		query = ':'.join(info[:-3]) + ':'
		if strand == -1:
			output = ">" + protein + '|' + line.strip()[1:] + '\n'
			out.write(output)
			out.write(reverse_complement(genomedict[query][start-1:end])+'\n')
		else:
			output = ">" + protein + '|' + line.strip()[1:] + '\n'
			out.write(output)
			out.write(genomedict[query][start-1:end]+'\n')
			













		