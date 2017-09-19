#!/usr/bin/env python

#this concatenates all read files into read1 and read2 files [if you get multiple read files per index from illumina]

import os
import sys
import argparse
import multiprocessing

#manip these variables



def concat(element):
	

	variables = dict(
	index = str(element))




	commands = """
	echo "Processing {index}"
	cp /pylon5/bi4s86p/phuong/nico.turridae/13add.other.transcriptomes/0data/{index}_1.fastq ./
        cp /pylon5/bi4s86p/phuong/nico.turridae/13add.other.transcriptomes/0data/{index}_2.fastq ./
	cat {index}_1.fastq | sed 's/ length*.*/\\/1/g' | sed 's/ HWI/HWI/'> {index}.renamed.R1.fq
        cat {index}_2.fastq | sed 's/ length*.*/\\/2/g'| sed 's/ HWI/HWI/'> {index}.renamed.R2.fq
	cp {index}.renamed.R1.fq /pylon5/bi4s86p/phuong/nico.turridae/13add.other.transcriptomes/1rename/
        cp {index}.renamed.R2.fq /pylon5/bi4s86p/phuong/nico.turridae/13add.other.transcriptomes/1rename/
	""".format(**variables)

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)

mylist = []

mapfile = open('mapfile', 'r')

for line in mapfile:
	mylist.append(line.strip())

pool = multiprocessing.Pool(40)
pool.map(concat, mylist)


