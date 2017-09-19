#!/usr/bin/env python

import os
import sys
import argparse
import multiprocessing
import dendropy
from collections import defaultdict
from Bio.Seq import translate
from Bio.Seq import reverse_complement
from Bio import SearchIO

def slicethis(mybaitseq, mylottiaseq, mycutlist, newstart1):

#	print mybaitseq
#	print mylottiaseq
#	print mycutlist

	startpos = mycutlist[1] + newstart1
	print startpos
	returnthis = []
	tempseq = ''

	n=0
	myindex = startpos
	start = 0
#	print range(startpos,len(mylottiaseq))
	for i in range(startpos,len(mylottiaseq)):
#		print
		thing = mylottiaseq[i]

		if thing == '-':
			myindex += 1
			continue
		else:
			tempseq = tempseq + thing

			if tempseq == mycutlist[0][n]:
	#			print n
				if (n+1) == len(mycutlist[0]):
					returnthis.append(mybaitseq[start:])
					break
				else:
					returnthis.append(mybaitseq[start:myindex+1])
					start = myindex+1
					n+=1
					tempseq = ''
					myindex +=1
	#				print returnthis
			else:
				myindex += 1
				continue
#	print returnthis
#	print tempseq
#	print mycutlist
	return returnthis

badfile = open('badfile', 'w')


def exonerate(theProteinName,seqlen,seq):
	mylist = []
	cmd = '/home/phuong/exonerate-2.2.0-x86_64/bin/exonerate --model est2genome mycds mygenome > exoneratefile'
	os.system(cmd)
	all_qresult = list(SearchIO.parse('exoneratefile', 'exonerate-text'))



	if len(range(all_qresult[0][0][0].query_range[0],all_qresult[0][0][0].query_range[0])) == seqlen:
		startpos = 0

		hsp = all_qresult[0][0][0]
		for i in range(0,len(hsp)):
			start = hsp[i].query_start
			end = hsp[i].query_end
			print start
			print end

			newseq = seq.strip()[start:end]

			mylist.append(newseq)
	elif float(len(range(all_qresult[0][0][0].query_range[0],all_qresult[0][0][0].query_range[1])))/float(seqlen) < 0.90:
	#	print float(len(range(all_qresult[0][0][0].query_range[0],all_qresult[0][0][0].query_range[1])))/float(seqlen)
#		print all_qresult[0][0][0].query_range[0]
#		print all_qresult[0][0][0].query_range[1]
		
#		print seqlen
#		print float(len(range(all_qresult[0][0][0].query_range[0],all_qresult[0][0][0].query_range[0]))/seqlen)
		myflag = 'yes'
		hsp = all_qresult[0][0][1]
		startpos = hsp[0].query_start
		for i in range(0,len(hsp)):
			start = hsp[i].query_start
			end = hsp[i].query_end
			print start
			print end

			newseq = seq.strip()[start:end]

			mylist.append(newseq)	
	else:
		myflag = 'no'
		hsp = all_qresult[0][0][0]
		startpos = hsp[0].query_start
		for i in range(0,len(hsp)):
			start = hsp[i].query_start
			end = hsp[i].query_end
			print start
			print end

			newseq = seq.strip()[start:end]

			mylist.append(newseq)		

	return mylist, startpos, myflag



		

out=open('turrid.2017.baits.fa.sliced', 'w')

#out=open('test.sliced', 'w')

lotcds = open('Lottia.cds.reduced', 'r')

lotcdsSeqDict = dict()

for line in lotcds:
	if ">" in line:
		info = line.strip().split(' ')
		ID = info[0].split('T')[1]
		lotcdsSeqDict[ID] = next(lotcds).strip()
	else:
		continue

#print lotcdsSeqDict
genome = open('Lottia.genome.sliced.reduced', 'r')

genomeSeqDict = dict()

for line in genome:
	if ">" in line:
		info = line.strip().split(' ')
		ID = info[0].split('|')[1].split('P')[1]
		genomeSeqDict[ID] = next(genome).strip()
	else:
		continue

#print genomeSeqDict

conoideabaits = open('turrid.2017.baits.fa', 'r')

#conoideabaits = open('testseq.fa', 'r')

protein = open('Lottia.pep.reduced' ,'r')

proteinDict = dict()

for line in protein:
	if ">" in line:
		info = line.strip().split(' ')[0].split('P')[1]
		proteinDict[info] = next(protein).strip()

#print proteinDict
weirdlist =[]
didnotblastlist = []
wrongbaitlist = []


notinlist = []

for line in conoideabaits:
	if ">" in line:

		info = line.strip().split('|')[0][1:]

		if not info in lotcdsSeqDict.keys():
			notinlist.append(info)
			continue

		out1 = open('mycds', 'w')
		out1.write(">lotcds" + '\n')
		out1.write(lotcdsSeqDict[info]+'\n')
		out2 = open('mygenome', 'w')
		out2.write(">lotgenome" + '\n')
		out2.write(genomeSeqDict[info] +'\n')
		out1.close()
		out2.close()

		mycutlist = exonerate(info,len(lotcdsSeqDict[info]),lotcdsSeqDict[info])
		if mycutlist[2] == 'yes':
			badfile.write('poor_alignment:'+line)


		mybaitseq = next(conoideabaits).strip().replace('L','').replace('-','')
		mybaitfile = open('mybait','w')
		mybaitfile.write('>mybait_'+info+'\n')
		mybaitfile.write(mybaitseq+'\n')
		mybaitfile.close()

		myprotfile = open('myprot', 'w')
		myprotfile.write('>myprot_' + info + '\n')
		myprotfile.write(proteinDict[info] +'\n')
		myprotfile.close()
		cmd = 'makeblastdb -dbtype prot -in myprot'
		os.system(cmd)
		cmd1 = 'blastx -query mybait -db myprot -outfmt 6 -out myblast -evalue 1e-10 -word_size 2'
		os.system(cmd1)
		with open('myblast', 'r') as f:
			first_line = f.readline()
		f.close()
#		print first_line
		if first_line == '':
			didnotblastlist.append(line)
			out.write(line)
			out.write(mybaitseq + '\n')
		else:

			first_line = first_line.split('\t')
			qstart = int(first_line[6])
			qend = int(first_line[7])
			dbstart = int(first_line[8])
			dbend = int(first_line[9])

		#	print len(lotcdsSeqDict[info])
		#	print len(mybaitseq)

			alignFile = open('alignthis','w')
			alignFile.write('>mybait_'+info+'\n')
			alignFile.write(mybaitseq[qstart-1:qend]+'\n')	
			alignFile.write('>lottia' + '\n')
			alignFile.write(lotcdsSeqDict[info][(dbstart-1)*3:(dbend*3)] + '\n')		
			alignFile.close()

			cmd = 'mafft --preservecase alignthis > alignthis.aligned'
			cmd1 = 'python makesomethingNotInterleaved.py alignthis.aligned alignthis.aligned.NI'
			os.system(cmd)
			os.system(cmd1)

			myalignedfile = open('alignthis.aligned.NI', 'r')

			
			for line1 in myalignedfile:
				if 'mybait' in line1:	
					mybaitsequence = next(myalignedfile).strip()
				elif 'lottia' in line1:
					mylottiaseq = next(myalignedfile).strip()
			myalignedfile.close()

			leftsideLottia = lotcdsSeqDict[info][:(dbstart-1)*3]
			rightsideLottia = lotcdsSeqDict[info][(dbend*3):]

			if qstart == 1:
				addbaitleft = ''
			else:
				addbaitleft = mybaitseq[0:qstart-1]


			if qend-qstart+1 == len(mybaitseq):
				addbaitright = ''
			else:
				addbaitright = mybaitseq[qend:]


			mybaitsequence = addbaitleft + len(leftsideLottia)*'-'  + mybaitsequence  + addbaitright + len(rightsideLottia)*'-'

			mylottiaseq = len(addbaitleft)*'-' + leftsideLottia +  mylottiaseq  + len(addbaitright)*'-' + rightsideLottia

#			print mylottiaseq
			
			myslicedseqs = slicethis(mybaitsequence, mylottiaseq, mycutlist, len(addbaitleft))
			
#			print myslicedseqs
			mycounter = 0
			checkbaits = ''
			for exon in myslicedseqs:
				out.write( line.strip() + '|exon' + str(mycounter) + '\n')
				out.write(exon+'\n')
				mycounter +=1
				checkbaits = checkbaits+ exon

			if float(qend-qstart+1)/len(mybaitseq) < 0.95:
			
				weirdlist.append(line)
			else:
				weirdlist = weirdlist
			if checkbaits.replace('-','') == mybaitseq.replace('-',''):
				continue
			else:
#				print checkbaits.replace('-','')
#				print mybaitsequence
				wrongbaitlist.append(line)
			
						



			

	else:
		continue


#print weirdlist
#print didnotblastlist


badfile.write('didnotblastlist')
badfile.write(','.join(didnotblastlist))
badfile.write('\n')
badfile.write('wrongbaitlist')
badfile.write(','.join(wrongbaitlist))
badfile.write('\n')
badfile.write('weirdlist')
badfile.write(','.join(weirdlist))
badfile.write('\n')




print notinlist




