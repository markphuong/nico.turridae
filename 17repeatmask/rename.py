import os
import sys


mapout = open('mymap', 'w')

out = open('turrid.seq.fa', 'w')

myfasta  = open('turrid.2017.baits.sliced.filtered.add', 'r')

counter = 0
for line in myfasta:
	if ">" in line:
		mapout.write(line.strip() + '\tseq' + str(counter) + '\n')

		out.write('>seq' + str(counter) + '\n')
		out.write(next(myfasta))

		counter += 1