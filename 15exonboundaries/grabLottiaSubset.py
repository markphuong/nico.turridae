#!/usr/bin/env python

import os
import sys
import argparse
import multiprocessing

from collections import defaultdict
from Bio.Seq import translate
from Bio.Seq import reverse_complement
from Bio import SearchIO



myIDs = []


myfasta = open('conus.2017.baits.transcriptome.phylogenetics.fa', 'r')

for line in myfasta:
	if ">" in line:
		myIDs.append(line.strip().split('|')[0][1:])



protein = open('Lottia_gigantea.GCA_000327385.1.pep.all.fa.NI', 'r')

infolist = []

out = open('Lottia.pep.reduced', 'w')

for line in protein:
	if ">" in line:

		protID = line.strip().split(' ')[0][7:]

		if protID in myIDs:

			out.write(line)
			out.write(next(protein))
			info = line.strip().split(' ')
			info = ':'.join(info[2].split(':')[:-3]) + ':'
			infolist.append(info)

print infolist

out.close()

genome = open('Lottia_gigantea.GCA_000327385.1.dna.toplevel.fa.NI', 'r')

out = open('Lottia.dna.reduced', 'w')

for line in genome:
	if ">" in line:
		info = line.strip().split(' ')
		info = ':'.join(info[2].split(':')[:-3]) + ':'
		if info in infolist:
			out.write(line)
			out.write(next(genome))

out.close()


#print infolist
genome = open('Lottia_gigantea.GCA_000327385.1.cds.all.fa.NI', 'r')

out = open('Lottia.cds.reduced', 'w')

for line in genome:
	if ">" in line:
		info = line.strip().split(' ')
		info = info[0].split('T')[1]

		if info in myIDs:
			out.write(line)
			out.write(next(genome))

