#!/usr/bin/env python

import os
import sys
from collections import defaultdict

tblastx = open(sys.argv[2], 'r')

out = open(sys.argv[3], 'w')

out2 = open(sys.argv[4], 'w')

trinityfile = open(sys.argv[5], 'r')

contig_list = []
lottiadict = dict()

with open(sys.argv[1]) as rfile:
	for line in rfile:
		info = line.strip().split('\t')
		if info[0] in contig_list:
			continue
		else:
			contig_list.append(info[0])
			lottiadict[info[0]] = info[1]

lottia_list = []
contigdict = dict()

therealdict = dict()


for line in tblastx:
	info = line.strip().split('\t')
	if info[0] in lottia_list:
		continue
	else:
		lottia_list.append(info[0])
		try:
			if lottiadict[info[1]] == info[0]:
				therealdict[info[1]] = [info[0],info[6],info[7]]
				out2.write(line)
		except:
			continue
mybestprot = []
for line in trinityfile:

	if ">" in line:

		if 'len' in line:
			info = line.strip().split(' ')


			contigname = info[0][1:]
		else:
			info = line.strip().split('|')
			contigname = info[0][1:]

		
		if contigname in therealdict.keys():
			mybestprot.append(info[2])
			out.write(line.strip()+'|' + therealdict[contigname][1]+ '|' + therealdict[contigname][2] + '\n')
			out.write(next(trinityfile))










