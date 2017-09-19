import os
import sys
from collections import defaultdict
from Bio.Seq import reverse_complement
from Bio.Seq import translate



myfastadict = dict()
myaadict = dict()

myfasta = open('Lotgi1_GeneModels_FilteredModels1_nt.fasta.NI', 'r')

for line in myfasta:
	if ">" in line:
		info = line.strip().split('|')
		myfastadict[info[2]] = [line.strip(), next(myfasta).strip()]

myaa = open('Lotgi1_GeneModels_FilteredModels1_aa.fasta.NI', 'r')

for line in myaa:
	if ">" in line:
		info = line.strip().split('|')
		myaadict[info[2]] = [line.strip(), next(myaa).strip()]


thedir = [f for f in os.listdir('.') if os.path.isfile(f)]


for thing in thedir:
	if 'AA.fasta' in thing:
		ID = thing.split('_')[0]

		if ID in myaadict:
			out = open(ID + '_AA.fasta', 'a')

			out.write(myaadict[ID][0] + '\n')
			out.write(myaadict[ID][1] + '\n')
			out.close()
	elif 'NT.fasta' in thing:
		ID = thing.split('_')[0]

		if ID in myfastadict:
			out = open(ID + '_NT.fasta', 'a')
			
			out.write(myfastadict[ID][0] + '\n')
			out.write(myfastadict[ID][1] + '\n')
			out.close()

	else:
		print 'fuck'
