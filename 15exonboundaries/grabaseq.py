#!/usr/bin/env python

from Bio import SeqIO
import dendropy
import os
import sys
from collections import defaultdict
from pprint import pprint
import argparse
import multiprocessing

thefile = open('Lottia_genom.NI', 'r')

out = open('lottia_genome.subset', 'w')

for line in thefile:
	if 'supercontig:GCA_000327385.1:LOTGIsca_1:' in line:
		out.write(line)
		out.write(next(thefile))