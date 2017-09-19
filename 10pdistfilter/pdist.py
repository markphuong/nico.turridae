import os
import sys
from os.path import isfile, join
import numpy

def pdist(seq1, seq2):
        """Sequences must be strings, have the same length, and be aligned"""
        num = 0
        diff = 0
        for i, nucleotide in enumerate(seq1):
                couple = [nucleotide, seq2[i]]
                if couple[0] == "-" or couple[0] == 'X':
                        continue
                elif couple[1] == "-" or couple[1] == 'X':
                        continue
                elif couple[0] == couple[1]:
                        num += 1
                elif not couple[0] == couple[1]:
                        num += 1
                        diff += 1
        if num == 0:
                return 'NA'
        else:
                pdist = float(diff)/float(num)
                return pdist


thedir = [f for f in os.listdir('.') if os.path.isfile(f)]



pdistdict = dict()

mapfile = open('mapfile', 'r')

specieslist = []

for item in mapfile:
	specieslist.append(item.strip())


for species1 in specieslist:
	for species2 in specieslist:
		ID1 = species1 + '|' + species2
		ID2 = species2 + '|' + species1

		if species1 == species2:
			continue
		elif ID1 in pdistdict.keys() or ID2 in pdistdict.keys():
			continue
		else:
			pdistdict[ID1] = []




              


######### calculate pdist

for thing in thedir:
        if '_NT.fasta.aligned_analyze.fasta.NI' in thing:


		myfasta = open(thing, 'r')

		currentdict = dict()

		for line in myfasta:
			if ">" in line:
				ID = line.strip().split('|')[0][1:]
				seq = next(myfasta).strip()
				currentdict[ID] = seq
		myfasta.close()	

		alreadyseen = []
		for species1 in currentdict:
			for species2 in currentdict:
				ID1 = species1 + '|' + species2
				ID2 = species2 + '|' + species1
				myvalue = pdist(currentdict[species1], currentdict[species2])
				if ID1 in alreadyseen or ID2 in alreadyseen:
					continue
				else:
					alreadyseen.append(ID1)
					alreadyseen.append(ID2)
					if species1 == species2:
						continue
					elif myvalue == 'NA':
						continue
					elif ID1 in pdistdict:
						pdistdict[ID1].append(myvalue)
					else:
						pdistdict[ID2].append(myvalue)
	

out = open('mycutoffs', 'w')






for item in pdistdict:
	print len(pdistdict[item])
	
	out.write(item + '\t' + str(numpy.percentile(pdistdict[item],90)) + '\n')

out.close()

