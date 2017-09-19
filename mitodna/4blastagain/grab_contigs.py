import os
import sys

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]


mapfile = open('mapfile', 'r')

for line in mapfile:
	ID = line.strip()
		


	blastlist = []


	myblast = open(ID + '_filtered_recipblast', 'r')

	for line in myblast:

		info = line.strip().split('\t')
		blastlist.append(info[1])			



	out = open(ID + '_mito_contigs.fasta', 'w')

	myfasta = open(ID + '_assemblies_clustered.fasta.NI', 'r')

	for line in myfasta:
		if ">" in line:
			if "TRINITY" in line:
				contig = line.strip()[1:].split(' ')[0]
			else:

				contig = line.strip()[1:]
			if contig in set(blastlist):
				out.write(">" + contig + '\n')
				out.write(next(myfasta))

	out.close()

	print len(list(set(blastlist)))
	print ID



