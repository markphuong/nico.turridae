#!/usr/bin/env python

#REQUIRES: novoalign and samtools
#REQUIRES: a map file, with first column as sample ID, and second file as which fasta it goes to. The reason you have different fastas for different samples is because of divergent mtDNA genomes
#elements in the map file are separated by a tab

#This script aligns your paired and unpaired reads to a reference using novoalign, and makes a pileup file using samtools

import os
import sys
import argparse
import multiprocessing

#this is a wrap around for novoalign and samtools where each sample identifier was "index#" where # was a number between 1 - 50

def get_args(): #arguments needed to give to this script
	parser = argparse.ArgumentParser(description="run novoalign")

	#forces required argument to let it run
	required = parser.add_argument_group("required arguments") 
	required.add_argument("--map", help="textfile with samples to run and what fasta file to match it to", required=True) #A map file with the sample ID and the fasta file it goes to

	return parser.parse_args()

def align(element):




	variables = dict(
	threshold = element,
	another = int(element) + 8
	) #name your output


	commands = """
	python pick_loci_and_fix_double.py {threshold}
	python concatenatedFile.py turridae_mitophylo_{threshold}.nexus
	python trimmfile.py turridae_mitophylo_{threshold}.nexus turridae_mitophylo_headed_{threshold}.nexus
	python nexus2phylip.py turridae_mitophylo_headed_{threshold}.nexus turridae_mitophylo_{threshold}.phylip
	python countcompleteness.py turridae_mitophylo_headed_{threshold}.nexus turridae_mitophylo_headed_{threshold}.completeness
	""".format(**variables)



	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)

align(sys.argv[1])
