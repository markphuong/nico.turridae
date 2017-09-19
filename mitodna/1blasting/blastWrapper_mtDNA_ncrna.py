#!/usr/bin/env python

#flash manual: http://ccb.jhu.edu/software/FLASH/MANUAL

#This script aligns your paired and unpaired reads to a reference using novoalign, and makes a pileup file using samtools

import os
import sys
import argparse
import multiprocessing

#this is a wrap around for novoalign and samtools where each sample identifier was "index#" where # was a number between 1 - 50

def get_args(): #arguments needed to give to this script
	parser = argparse.ArgumentParser(description="run blastx")

	#forces required argument to let it run
	required = parser.add_argument_group("required arguments") 
	required.add_argument("--map", help="textfile with samples to run and what fasta file to match it to", required=True) #A map file with the sample ID and the fasta file it goes to

	return parser.parse_args()

def align(element):

	variables = dict(
	trinity = element + '_assemblies_clustered.fasta',
	blastoutput = element + '.mt_ncrna.blastoutput',
	db = 'mt_ncrna_database.fa',
	index = element
	) #name your output


	commands = """
	blastn -query {trinity} -db {db} -outfmt 6 -out {blastoutput} -evalue 1e-10
	""".format(**variables)

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)

#def main():
args = get_args() 

	#Make a list of lists, each list within the list will have the first and second elements of the map file that are separated by a tab
mylist = []
with open(args.map) as rfile:
	for line in rfile:
		line = line.strip()
		align(line)
#		mylist.append(line)

	#start the multiprocessing
#	pool = multiprocessing.Pool()
#	pool.map(align, mylist)#run the function with the arguments

#if __name__ == "__main__": #run main over multiple processors
#	main()
