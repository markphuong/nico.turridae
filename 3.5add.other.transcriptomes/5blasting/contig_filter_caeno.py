import os
import sys
from collections import defaultdict

def checkoverlap(a, b):
	overlap = max(0, min(a[1], b[1]) - max(a[0], b[0]))
        length1 = len(range(a[0],a[1]+1))

	length2 = len(range(b[0],b[1]+1))

	ratio1 = float(overlap)/length1
	ratio2 = float(overlap)/length2

	return max(ratio1, ratio2)




######## grab best blast hit for every assembled transcript
bestblastdict = dict()


myblastx = open(sys.argv[1], 'r')

alreadyseen = []

for line in myblastx:
	info = line.strip().split('\t')

	if info[0] in alreadyseen:
		continue
	else:
		bestblastdict[info[0]] = info[1]
		alreadyseen.append(info[0])

myblastx.close()


######### generate a list of rbbhs by comparing rbbh of the tblastn to blastx

mytblastn = open(sys.argv[2], 'r')

rbbhloci = []
alreadyseen = []

for line in mytblastn:
	info = line.strip().split('\t')

	if info[0] in alreadyseen:
		continue
	else:
		if not info[1] in bestblastdict.keys():
			alreadyseen.append(info[0])
		elif info[0] == bestblastdict[info[1]]:
			rbbhloci.append(info[0])
			alreadyseen.append(info[0])
		else:
			alreadyseen.append(info[0])


mytblastn.close()

################## for all the loci in rbbh, write out the blast lines for the rbbh and other non overlapping regions (threshold is max 20% overlap between any two fragments that are already kept)



out = open(sys.argv[3], 'w')
mytblastn = open(sys.argv[2], 'r')

blastcoorddict = defaultdict(list)

for line in mytblastn:
	info = line.strip().split('\t')

	if not info[0] in rbbhloci:
		continue
	elif not info[1] in bestblastdict:
		continue	
	elif info[0] == bestblastdict[info[1]]:
		if info[0] in blastcoorddict:
			mycoords = [int(info[6]), int(info[7])]

			keep = 'yes'

			for mylist in blastcoorddict[info[0]]:
				if checkoverlap(mycoords, mylist) > .2:
					keep = 'no'
				else:
					continue
			if keep == 'yes':
				out.write(line)
				blastcoorddict[info[0]].append(mycoords)
			else:
				continue

		else:
			blastcoorddict[info[0]] = [[int(info[6]),int(info[7])]]
			out.write(line)
 	else:
		continue

out.close()

fastadict = dict()

myfasta = open(sys.argv[5], 'r')

for line in myfasta:
	header = line.strip()[1:]

	if ' ' in header:
		header = header.split(' ')[0]
	else:
		header = header
	seq = next(myfasta).strip()
	fastadict[header] = seq

	
	

myfilter = open(sys.argv[3], 'r')

out = open(sys.argv[4], 'w')

alreadyseen = []

for line in myfilter:
	info = line.strip().split('\t')

	if info[1] in alreadyseen:
		continue
	else:

		alreadyseen.append(info[1])
		out.write('>' + info[1] + '\n')
		out.write(fastadict[info[1]] + '\n')
	






















