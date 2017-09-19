import os
import sys


myfasta = open('conoidea_baits_FINAL.fasta', 'r')

out = open('additional.conoidea.fa', 'w')

totallength = 0
for line in myfasta:
	if ">" in line:
		if 'exon' in line:
			info = line.strip().split('|')
			if info[-1].count('_') > 1:
				continue
			else:
				seq = next(myfasta).strip()

				if len(seq) > 120:
					out.write(line)
					out.write(seq + '\n')
					totallength += len(seq)

print totallength