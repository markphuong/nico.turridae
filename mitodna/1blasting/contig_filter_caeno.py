import os
import sys
from collections import defaultdict

######### generate a list of rbbhs by comparing rbbh of the tblastn to blastx

mytblastn = open(sys.argv[1], 'r')


alreadyseen = []

for line in mytblastn:
	info = line.strip().split('\t')

	if info[1] in alreadyseen:
		continue
	else:
		alreadyseen.append(info[1])


mytblastn.close()

print alreadyseen

################## for all the loci in rbbh, write out the blast lines for the rbbh and other non overlapping regions (threshold is max 20% overlap between any two fragments that are already kept)


fastadict = dict()

myfasta = open(sys.argv[3], 'r')

for line in myfasta:
	header = line.strip()[1:]

	if ' ' in header:
		header = header.split(' ')[0]
	else:
		header = header
	seq = next(myfasta).strip()
	fastadict[header] = seq



out = open(sys.argv[2], 'w')



for thing in set(alreadyseen):
	out.write('>' + thing + '\n')
	out.write(fastadict[thing] + '\n')
	






















