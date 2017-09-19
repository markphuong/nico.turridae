import os
import sys
from collections import defaultdict
import argparse
import multiprocessing

from os.path import isfile, join


###### create consensus between exons in multiple sequences

def create_consensus(seq1, seq2):
        """Sequences must be strings, have the same length, and be aligned"""
        out_seq = ""

	counter = 0

        for i, nucleotide in enumerate(seq1):
                couple = [nucleotide, seq2[i]]
                if couple[0] == "-" or couple[0] == 'n':
                        out_seq += couple[1]
                elif couple[1] == "-" or couple[1] == 'n':
                        out_seq += couple[0]
                elif couple[0] == couple[1]:
                        out_seq += couple[0]
                elif not couple[0] == couple[1]:
                        out_seq += couple[0]
			counter += 1
        return [out_seq, counter]











def make_consensus(thing):
	failed = 'no'
	if 'mitogenome.all.aligned.fa' in thing:
		print thing

		cmd = "python makesomethingNotInterleaved.py " + thing + " " + thing + ".NI"
		os.system(cmd)

		myfasta = open(thing + '.NI', 'r')

		fastadict = defaultdict()

		for line in myfasta:
			if ">" in line:
		
				ID = line.strip().split('|')[0][1:]

				seq = next(myfasta).strip()

				if ID in fastadict:		
					fastadict[ID].append([line, seq])
				else:
					fastadict[ID] = [[line, seq]]


		out = open(thing + '_analyze.fasta', 'w')
		for key in fastadict:
			if len(fastadict[key]) == 1:
				out.write(">" + key + '\n')
				out.write(fastadict[key][0][1] + '\n')
			else:
				mylist = fastadict[key]


				########## store sequences into a new dictionary, ordered by the first coordinate of the blast query on the lottia protein so you analyze sequences in order
				tempdict = dict()
				for item in mylist:
					tempdict[int(item[0].split('|')[-4])] = item[1]


				mytempkeys = sorted(tempdict) # holds the keys, which are the start of the blast query on the lottia protein ID taken from the fasta header

				##################### 
				n = 2
				different = 0



				consensus = create_consensus(tempdict[mytempkeys[0]], tempdict[mytempkeys[1]])

				consensus_seq = consensus[0]

				different = different + consensus[1]

				while n < len(mylist):

					consensus = create_consensus(consensus_seq, tempdict[mytempkeys[n]])

					consensus_seq = consensus[0]
					different = different + consensus[1]

					n += 1

					

				if different > 5:
					continue
					failed = 'yes'
					#out.write(">" + key + '\n')
					#out.write(consensus_seq + '\n')
				else:
					out.write(">" + key + '\n')
					out.write(consensus_seq + '\n')
		out.close()

		

		cmd = "cp " + thing + "_analyze.fasta /pylon5/bi4s86p/phuong/nico.turridae/mitodna/7consensus"
		os.system(cmd)		
		
thedir = [f for f in os.listdir('.') if os.path.isfile(f)]
mylist = []

for thing in thedir:
	if 'mitogenome.all.aligned.fa' in thing:

		mylist.append(thing)


pool = multiprocessing.Pool(62)
pool.map(make_consensus, mylist)#run the function with the arguments








