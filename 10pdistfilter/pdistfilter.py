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


cutoffdict = dict()

cutoffs = open('mycutoffs', 'r')

for line in cutoffs:
	info = line.strip().split('\t')

	cutoffdict[info[0]] = float(info[1])



for thing in thedir:
#        if '130484' in thing:
        if '_NT.fasta.aligned_analyze.fasta' in thing:




              


######### calculate pdist


		myfasta = open(thing, 'r')

		currentdict = dict()

		numtaxa = 0

		for line in myfasta:
			if ">" in line:
				ID = line.strip().split('|')[0][1:]
				seq = next(myfasta).strip()
				currentdict[ID] = seq
				numtaxa += 1

		counterdict = dict()

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
					elif ID1 in cutoffdict:
						if myvalue > cutoffdict[ID1]:
							if species1 in counterdict:
								counterdict[species1] += 1
							else:
								counterdict[species1] = 1
							if species2 in counterdict:
								counterdict[species2] += 1
							else:
								counterdict[species2] = 1
						else:
							continue
					else:
						if myvalue > cutoffdict[ID2]:
							if species1 in counterdict:
								counterdict[species1] += 1
							else:
								counterdict[species1] = 1
							if species2 in counterdict:
								counterdict[species2] += 1
							else:
								counterdict[species2] = 1
						else:
							continue
		myfasta.close()	
		print thing
		print counterdict
		print numtaxa
		print len(counterdict)
		outremoved = open(thing + '.pdistremoved', 'w')
		removelist = []
		for species in counterdict:
			if float(counterdict[species])/float(numtaxa) >= .1:
				removelist.append(species)
				outremoved.write(species + '\n')
			else:
				continue
		outremoved.close()

		if float(len(removelist))/float(numtaxa) > 0.2:
			filtered = open('entire_locus_removed', 'a')
			filtered.write(thing + '\n')
			filtered.close()
		else:

			outfasta = open(thing + '.pdist', 'w')


			myfasta = open(thing, 'r')

			for line in myfasta:
				if ">" in line:
					if line.strip()[1:] in removelist:
						continue
					else:
						outfasta.write(line)
						outfasta.write(next(myfasta))
			myfasta.close()
			outfasta.close()
