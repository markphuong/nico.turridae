#!/usr/bin/env python

#REQUIRES: novoalign and samtools
#REQUIRES: a map file, with first column as sample ID, and second file as which fasta it goes to. The reason you have different fastas for different samples is because of divergent mtDNA genomes
#elements in the map file are separated by a tab

#This script aligns your paired and unpaired reads to a reference using novoalign, and makes a pileup file using samtools

import os
import sys
import argparse
import multiprocessing
from os.path import isfile, join

#this is a wrap around for novoalign and samtools where each sample identifier was "index#" where # was a number between 1 - 50

def get_args(): #arguments needed to give to this script
	parser = argparse.ArgumentParser(description="run novoalign")

	#forces required argument to let it run
	required = parser.add_argument_group("required arguments") 
	required.add_argument("--map", help="textfile with samples to run and what fasta file to match it to", required=True) #A map file with the sample ID and the fasta file it goes to

	return parser.parse_args()

def align(element):





	thedir = [f for f in os.listdir('/pylon5/bi4s86p/phuong/nico.turridae/10pdistfilter/results/') if isfile(join('/pylon5/bi4s86p/phuong/nico.turridae/10pdistfilter/results/', f))]

	for thing in thedir:
		if 'removed' in thing:
			continue
		elif 'pdist' in thing:
			print thing
			variables = dict(
			filename = thing,
			setname = element
			) #name your output

			commands = """
			cp /pylon5/bi4s86p/phuong/nico.turridae/10pdistfilter/results/{filename} ./
			python pick.best.seqs.py {filename} {setname}.group1 {setname}.group2 {setname}
			""".format(**variables)


			cmd_list = commands.split("\n")
			for cmd in cmd_list:
				os.system(cmd)
		else:
			continue

mylist = []
def main():
	args = get_args() 

	#Make a list of lists, each list within the list will have the first and second elements of the map file that are separated by a tab

	with open(args.map) as rfile:
		for line in rfile:
			line = line.strip()
			align(line)


if __name__ == "__main__": #run main over multiple processors
	main()


