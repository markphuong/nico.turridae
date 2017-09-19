import os
import sys
from Bio.Seq import reverse_complement


myfile = open('adapterfile', 'r')

out = open('ADAPTERS.txt', 'w')

counter = 0

for line in myfile:
	
	out.write(">seq" + str(counter) + '\n')
	out.write(line.strip() + 'GCTCTTCCGATCT\n')

	counter += 1

	out.write(">seq" + str(counter) + '\n')
	out.write(reverse_complement(line.strip()+'GCTCTTCCGATCT') + '\n')

	counter += 1