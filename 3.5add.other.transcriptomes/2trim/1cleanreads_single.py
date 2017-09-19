#!/usr/bin/env python

#flash manual: http://ccb.jhu.edu/software/FLASH/MANUAL

#this script cleans reads using trimmomatic, merges reads using flash, and creates a read1 file, read2 file (these represent paired files) and an unpaired file

import os
import sys
import argparse
import multiprocessing


# an arguments portion in the code represents necessary inputs to give to the script. I usually use this to give the program a file that contains all the unique sample IDs which should be in the read file names
def get_args():
	parser = argparse.ArgumentParser(description="run blastx")


	required = parser.add_argument_group("required arguments") 
	required.add_argument("--map", help="textfile with samples to run and what fasta file to match it to", required=True) #A map file with the sample ID and the fasta file it goes to

	return parser.parse_args()


def align(element):


	#the adapters file should have both forward and reverse, and the universal adapters
	
	#this variables dict species the names for the input/out files
	variables = dict(
	adfile = 'adapters.fa',
	read1 = element + '.renamed.R1.fq',
	read2 = element + '.renamed.R2.fq',
	read1out = element + '.R1.trimmed.fq', 
	read1unpairedout = element + '.R1.trimmedunpaired.fq',
	read2out = element + '.R2.trimmed.fq',
	read2unpairedout = element + '.R2.trimmedunpaired.fq',
	sampleID = element) #name your output


	commands = """
	cp /pylon5/bi4s86p/phuong/nico.turridae/13add.other.transcriptomes/1rename/{read1} ./
	java -jar $TRIMMOMATIC_HOME/trimmomatic-0.36.jar SE -threads 63 -phred33 {read1} {read1out} ILLUMINACLIP:{adfile}:2:40:15 SLIDINGWINDOW:4:20 MINLEN:36 LEADING:15 TRAILING:15 > {sampleID}.trimm 2> {sampleID}.trimmerr
	cat {read1out} > {sampleID}.final.single.fq
	cp {sampleID}.final.single.fq /pylon5/bi4s86p/phuong/nico.turridae/13add.other.transcriptomes/2trim/
	cp {sampleID}.trimm /pylon5/bi4s86p/phuong/nico.turridae/13add.other.transcriptomes/2trim/
	cp {sampleID}.trimmerr /pylon5/bi4s86p/phuong/nico.turridae/13add.other.transcriptomes/2trim/
	""".format(**variables)


	#this bit of code executes the command

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)

mylist = []


args = get_args() #this is where the arguments from the def args code gets called upon

with open(args.map) as rfile:
	for line in rfile:
		line = line.strip()
		mylist.append(line)

#this bit is really not necessary. I could have done this by not having 'def main()' and just starting with the args=get_args() line, but the following code follows the logic of what preceded it.


pool = multiprocessing.Pool(5)
pool.map(align, mylist)






