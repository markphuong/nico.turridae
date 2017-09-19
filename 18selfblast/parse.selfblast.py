import os
import sys
import numpy

############## load in selfblast, if loci/exon combo is not the same, add it to badlist

myblast = open('turrid.selfblast', 'r')


badlist = []

for line in myblast:
	info = line.strip().split('\t')

	seq1 = info[0].split('|')

	seq2 = info[1].split('|')


	locus1 =seq1[0]+'|' + seq1[-1]

	locus2 =seq2[0]+'|' + seq2[-1]

	if locus1 == locus2:
		continue


	else:
		badlist.append(info[0])
		badlist.append(info[1])



########## initialize files
myfasta = open('turried.2017.baits.renamed.weird.removed.fa', 'r')

mymap = open('seq.renamed', 'w')

out1 = open('turrid.2017.baits.SET.1.fa' ,'w') #all sequences

out2 = open('turrid.2017.baits.SET.2.fa' ,'w') #removed conoidea baits below 180bp

locusdict = dict()

seqlength = 0

counter = 0

for line in myfasta:
	if ">" in line:
		ID = line.strip()[1:]

		seq = next(myfasta).strip()
		info = line.strip()[1:].split('|')



		locus = info[0]+'|' + info[-1]	


		if ID in badlist:
			continue
		else:

##########################################
# get num seq per loci, only add to sequence length at first instance of a locus

			if locus in locusdict:
				locusdict[locus] += 1
			else:
				locusdict[locus] = 1
				seqlength += len(seq)
			counter += 1


###################################### rename sequences and write out header map file

			mymap.write(ID + '\tseq' + str(counter) + '\n')

			out1.write('>seq' + str(counter) + '\n')
			out1.write(seq + '\n')

############## for conus sequences, only add if >180bp

			if 'Conus' in line:
				if len(seq) >= 180:
					out2.write('>seq' + str(counter) + '\n')
					out2.write(seq + '\n')
				else:
					what = 'what'
			else:
				out2.write('>seq' + str(counter) + '\n')
				out2.write(seq + '\n')


print seqlength


######## write out num sequences per lottia prot id/exon pair

mynumloci = open('loci.turrid.counts', 'w')

for item in locusdict:
	mynumloci.write(item + '\t' + str(locusdict[item]) + '\n')
	






















