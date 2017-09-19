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


#thedir = [f for f in os.listdir('/pylon5/bi4s86p/phuong/nico.turridae/8make.quick.tree/results/') if isfile(join('/pylon5/bi4s86p/phuong/nico.turridae/8make.quick.tree/results/', f))]
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




for thing in thedir:
        if '_NT.fasta.aligned_analyze.fasta.NI' in thing:

#                cmd = 'cp /pylon5/bi4s86p/phuong/caenogastropod/16aliscore/filtered/' + thing + ' ./'
#                os.system(cmd)


              


######### calculate pdist


		myfasta = open(thing, 'r')

		currentdict = dict()

		for line in myfasta:
			if ">" in line:
				ID = line.strip()[1:]
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
	
#		cmd = 'cp ' + thing + ' /pylon5/bi4s86p/phuong/caenogastropod/17pdist/mytest2'
#               os.system(cmd)
		





out = open('mypdistvalues', 'w')

out2 = open('mypdistmeans', 'w')

for item in pdistdict:

#	out = open(item.replace('|','.') + '.pdist' , 'w')
#	print len(pdistdict[item])

	out2.write(item.replace('|','\t') + '\t' + item.replace('|','.')+ '\t' + str(numpy.mean(pdistdict[item])) + '\n')
	
	for thing in pdistdict[item]:
		out.write(item.replace('|','\t') + '\t' + str(thing) + '\t'+item.replace('|','.')+'\n')
	
out.close()















