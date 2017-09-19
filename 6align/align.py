import os
import sys
import argparse
import multiprocessing

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]


for thing in thedir:
	if 'NT.fasta' in thing:
		myfasta = open(thing, 'r')

		ID = thing.split('_')[0]

#		nameslist = []

		refseq = ''
		refkey = ''
		
		for line in myfasta:
			if ">" in line:
				myseq = next(myfasta).strip()

				if len(myseq) > len(refseq):
					refseq = myseq
					refkey = line.strip()
		
		myfasta.close()

		refout = open(ID + '.ref', 'w')
		otherout = open(ID+'.other','w')

		myfasta = open(thing, 'r')


		for line in myfasta:
			if ">" in line:
				if line.strip() == refkey:
					refout.write(line)
					refout.write(next(myfasta))
				else:
					otherout.write(line)
					otherout.write(next(myfasta))
		refout.close()
		otherout.close()
		myfasta.close()
		
		cmd = 'mafft --addfragments ' + ID + '.other ' + ID +'.ref > ' + thing + '.aligned'
		print cmd
		os.system(cmd)
		cmd = 'cp ' + thing + '.aligned /pylon5/bi4s86p/phuong/nico.turridae/6align/aligned'
		os.system(cmd)





















