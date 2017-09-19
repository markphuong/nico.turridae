#!/usr/bin/env python

import os
import sys
from collections import defaultdict

myRBH = open(sys.argv[1], 'r')

######myRBH proteins

myRBHprot = []
for line in myRBH:
	info = line.strip().split('\t')
	myRBHprot.append(info[0])

		
##check original blast output file to see if fragments overlap, and if they don't, put it into a dictionary/list and 
##and pull those sequences out of the original fastafile
tblastx = open(sys.argv[2], 'r')

tempdict = defaultdict(list)

out = open(sys.argv[3], 'w')

keeplist = []
keepdict = dict()

fastafile2 = open(sys.argv[4], 'r')

out3 = open(sys.argv[5], 'w')

myseqdict = dict()

for line in fastafile2:
	if ">" in line:
		info = line.strip().split('|')[0][1:]
		myseqdict[info] = [line, next(fastafile2)]


for line in tblastx:
	info = line.strip().split('\t')
#	print tempdict
	if not info[0] in myRBHprot:
		continue

	elif info[0] in tempdict.keys():
		x = range(tempdict[info[0]][0], tempdict[info[0]][1])
		y = range(int(info[6]), int(info[7]))
		xs = set(x)
		ys = set(y)
		theintlength = len(list(xs.intersection(ys)))
		if theintlength > 20:
			continue
		else:
			if info[0] == myseqdict[info[1]][0].split('|')[2] and info[0] in myRBHprot:
				out.write(line)
				out3.write(myseqdict[info[1]][0].strip() + '|' + info[6] + '|' + info[7] + '\n')
				out3.write(myseqdict[info[1]][1])

	else:
		tempdict[info[0]] = [int(info[6]), int(info[7])]



















