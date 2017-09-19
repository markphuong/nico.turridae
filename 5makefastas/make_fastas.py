import sys
import os
from Bio.Seq import reverse_complement
from Bio.Seq import translate



myfasta = open(sys.argv[1], 'r')


for line in myfasta:
	if ">" in line:
		header = line.strip()
		seq = next(myfasta).strip()

		info = header.split('|')

		lottia = info[4]

		if int(info[-2]) > int(info[-1]):
			seq = reverse_complement(seq)
		else:
			seq = seq

		out = open(lottia + '_NT.fasta', 'a')

		outAA = open(lottia + '_AA.fasta', 'a')

		out.write(header + '\n')
		out.write(seq + '\n')

		outAA.write(header + '\n')
		outAA.write(translate(seq) + '\n')
		out.close()
		outAA.close()


