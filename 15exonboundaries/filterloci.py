import os
import sys


myfasta = open('turrid.2017.baits.fa.sliced', 'r')


out = open('turrid.2017.baits.fa.sliced.filtered', 'w')

totallength = 0

locilist = []

out2 = open('loci.list.transcriptome', 'w')

locidict = dict()


for line in myfasta:
	if ">" in line:
		seq = next(myfasta).strip()

		seq = seq.replace('-','')





		if len(seq) >= 120:
			GC = (seq.count('C') + seq.count('G')) / float(len(seq))
			if GC < 0.3 or GC > 0.7:
				print line
				print GC
				continue
			else:

				out.write(line)
				out.write(seq + '\n')
				
				mykey = line.strip()[1:].split('|')[0] + '|' + line.strip()[1:].split('|')[-1]
				if mykey in locidict:
					locidict[mykey] += 1
				else:
					locidict[mykey] = 1
					totallength += len(seq)
		else:
			continue

for item in locidict:
	out2.write(item + '\t' + str(locidict[item]) + '\n')

print totallength
