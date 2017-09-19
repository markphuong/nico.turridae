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


protein = open('LottiaReduced.prot', 'r')

infolist = []

for line in protein:
	if ">" in line:
		info = line.strip().split(' ')
		info = info[0].split('P')[1]
		infolist.append(info)

#print infolist
genome = open('Lottia_cds.NI', 'r')

out = open('Lottia_cds_subset.NI', 'w')

for line in genome:
	if ">" in line:
		info = line.strip().split(' ')
		info = info[0].split('T')[1]

		if info in infolist:
			out.write(line)
			out.write(next(genome))