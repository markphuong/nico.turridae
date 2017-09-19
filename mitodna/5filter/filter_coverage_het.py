import os
import sys
import numpy
from collections import defaultdict
from Bio.Seq import reverse_complement



#################################### get dictionary of the overlappers


myremoved = open('removed_overlappers', 'r')

removed = defaultdict(list)

for line in myremoved:
	info = line.strip().split('\t')

	if info[0] in removed.keys():
		removed[info[0]].append('\t'.join(info[2:]))
	else:
		removed[info[0]] = ['\t'.join(info[2:])]


##################### alternative alleles dictionary

altdict =defaultdict(dict)

myalternatives = open('alternative_alleles', 'r')

for line in myalternatives:
	info = line.strip().split('\t')

	if info[0] in altdict.keys() and info[1] in altdict[info[0]].keys():

		altdict[info[0]][info[1]].append([int(info[2]), info[3], info[4]])
	else:
		altdict[info[0]][info[1]] = [ [int(info[2]), info[3], info[4]] ]
		


#outhet = open('removed_high_het', 'w')
outcov = open('removed_low_cov', 'w') 
thedir = [f for f in os.listdir('.') if os.path.isfile(f)]

mapfile = open('mapfile', 'r')


for thing in mapfile:
	if 'yay' == 'yay':


		
		ID = thing.strip()

####################### load dictionary of sequences
		myfasta = open(ID + '_mito_contigs.fasta', 'r')

		fastadict = dict()

		for line in myfasta:
			if ">" in line:
				header = line.strip()[1:]
				seq = next(myfasta).strip()

				seq = list(seq)

				if header in altdict[ID]:
					for item in altdict[ID][header]:
						if ',' in item[1]:
							seq[item[0]-1] = 'N'
						elif item[2] == '1/1':
							seq[item[0]-1] = item[1]
						else:
							continue


				fastadict[header] = ''.join(seq)

####################### load dictionary of coverage

		mycov = open(ID + '.cov', 'r')

		covdict = dict()

		for line in mycov:
			info = line.strip().split('######')

			covlist = info[1][1:-1].split(', ')

			covlist = [int(thing) for thing in covlist]
			covdict[info[0]] = covlist

###################### load dictionary of heterozygosity

#		myhet = open(ID + '.6.1.het', 'r')

#		hetdict = dict()

#		for line in myhet:
#			info = line.strip().split('######')

#			hetlist = info[1][1:-1].split(', ')

#			hetlist = [int(thing) for thing in hetlist]
#			hetdict[info[0]] = hetlist		

################## load recip blast to get a list of blasted contigs

		myblast = open(ID + '_filtered_recipblast', 'r')

		blastlist = []

		for line in myblast:
			blastlist.append(line.strip().split('\t')[1])

		myblast.close()

################ some contigs may not show up in the VCF file, so you have to create lists of 0's and put them in your cov and het dictionaries

		for thing in set(blastlist):
			if thing in covdict.keys():
				continue
			else:
				covdict[thing] = [0]*4000

#		for thing in set(blastlist):
#			if thing in hetdict.keys():
#				continue
#			else:
#				hetdict[thing] = [0]*4000

################## parse information through the blast output
		myblast = open(ID + '_filtered_recipblast', 'r')



		keeplist = [] #list of blast information you want to keep

#		myhetlist = [] # list of heterozygosity values you want to keep


##################################################

		speciescov = open(ID + '_coverage', 'w')
#		specieshet = open(ID + '_heterozygosity', 'w')


		for line in myblast:
			info = line.strip().split('\t')

############### ignore the overlappers
			if line.strip() in removed[ID]:
				continue
			else:

##################### if I don't want to ignore it, store start and end

				if int(info[8]) > int(info[9]):
					start = int(info[9])
					end = int(info[8])
				else:
					start = int(info[8])
					end = int(info[9])	

				myseq = fastadict[info[1]][start-1:end] # my sequence
				thecov = covdict[info[1]][start-1:end] #corresponding coverage
#				thehet = hetdict[info[1]][start-1:end] # corresponding heterozygosity


							
				
				outseq = '' #will mask regions with less than 5X coverage
				covcounter = 0 #will count coverage across entire sequence length
#				hetcounter = 0 #will only count heterozygous positions where coverage is at least 5X
				lengthcounter = 0 #modified length due to positions being removed from low coverage (less than 5X)

				for i in range(0,len(myseq)):
					covcounter += thecov[i]

					if thecov[i] > 0:
						outseq = outseq + myseq[i]
						#hetcounter += thehet[i]
						lengthcounter += 1

					else:
						outseq = outseq + 'N'


				# if you don't have at least 4X coverage in >= 70% of the sequence, remove it

				speciescov.write(info[0] + '\t' + info[1] + '\t' + str(float(covcounter)/len(myseq)) + '\n')

				if float(lengthcounter)/len(myseq) < 0.7:
					outcov.write(ID + '\t' + 'low_cov' + '\t'+ line)

				else:
#other wise, append a list of information, including the (a) target, (b) contig (c) coverage (d) modified heterozygosity (e) percent of the sequence above a certain amount of bp, (d) the final sequence with replaced 'N's, and (e) the blast output line)
					keeplist.append([info[0], info[1], float(covcounter)/len(myseq), 0, float(lengthcounter)/len(myseq), outseq,  line])
					#myhetlist.append(float(hetcounter)/lengthcounter)
					#specieshet.write(info[0] + '\t' + info[1] + '\t' +str(float(hetcounter)/lengthcounter) + '\n')
	

############ remove sequences where heterozygosity is equal to or above 2 standard deviations away from the mean

	#	themean = numpy.mean(myhetlist)
	#	stdev = numpy.std(myhetlist)

	#	mycutoff = themean + stdev*2



		out = open(ID + '_mitoloci_v2.fa', 'w')


		for item in keeplist:
#			if item[3] >= mycutoff:
#				outhet.write(ID + '\t' + 'high_het' + '\t' + item[-1])

#			else:
			myblastline = item[-1]
			myblastline = myblastline.strip().split('\t')

			mylottia = ''
			if '|' in item[0]:
				if len(item[0].split('|')) > 6:
					mylottia = item[0].split('|')[3]
				else:
					mylottia = item[0].split('|')[2]
			else:
				mylottia = item[0]

#header includes 1. species name 2. assembled contig ID 3. coverage 4. percent sequence above a certain number of bp 5. lottia target 6. lot start 7. lot end 8. seq start 9. seq end
			out.write(">" + ID + '|' + item[1] + '|' + str(item[2])  + '|' + str(item[4]) + '|' + mylottia + '|' + myblastline[6]  + '|' + myblastline[7] + '|' + myblastline[8] + '|' + myblastline[9] +'\n')
			if int(myblastline[9]) > int(myblastline[8]):
				out.write(item[-2] + '\n')
			else:
				out.write(reverse_complement(item[-2]) + '\n')


			
				#if lengthcounter == 0:
				#	out.write('\t'.join([info[0], info[1], str(float(covcounter)/len(myseq)), '0', str(float(lengthcounter)/len(myseq))]) + '\n'), 
				#else:
				#	out.write('\t'.join([info[0], info[1], str(float(covcounter)/len(myseq)), str(float(hetcounter)/lengthcounter), str(float(lengthcounter)/len(myseq))]) + '\n'), 
					
				


		out.close()
		myfasta.close()
		mycov.close()
#		myhet.close()
		myblast.close()
#		specieshet.close()
		speciescov.close()













