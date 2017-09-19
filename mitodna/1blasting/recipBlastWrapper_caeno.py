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

	ID = element


	variables = dict(
	sample = ID
	) #name your output


	commands = """
	makeblastdb -dbtype nucl -in {sample}_assemblies_clustered.fasta.NI
	blastn -query lophigenome -db {sample}_assemblies_clustered.fasta.NI -outfmt 6 -out {sample}.blastn -evalue 1e-10 -num_threads 10
	python contig_filter_caeno.py {sample}.blastn {sample}_phylo_contigs.fa {sample}_assemblies_clustered.fasta.NI
	cp {sample}.blastn /pylon5/bi4s86p/phuong/nico.turridae/mitodna/1blasting/
	cp {sample}_phylo_contigs.fa /pylon5/bi4s86p/phuong/nico.turridae/mitodna/1blasting/
	""".format(**variables)

	

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)
mylist = []

args = get_args() 

	#Make a list of lists, each list within the list will have the first and second elements of the map file that are separated by a tab

with open(args.map) as rfile:
	for line in rfile:
		line = line.strip()
		mylist.append(line)

pool = multiprocessing.Pool(4)
pool.map(align, mylist)#run the function with the arguments









