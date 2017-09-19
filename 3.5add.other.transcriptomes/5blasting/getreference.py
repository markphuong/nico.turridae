import os
import sys
from collections import defaultdict
import multiprocessing
from os import listdir
from os.path import isfile, join


thedir = [f for f in listdir('/pylon2/bi4s86p/phuong/caenogastropod/8makenewref/newrefs_16/') if isfile(join('/pylon2/bi4s86p/phuong/caenogastropod/8makenewref/newrefs_16/', f))]


out = open('mynewlottiaref.fa', 'w')

for thing in thedir:
	if '.mynewref.fa' in thing:
		
		myfile = open('/pylon2/bi4s86p/phuong/caenogastropod/8makenewref/newrefs_16/' +thing, 'r')
		for line in myfile:
			out.write(line.strip() + '\n')
		myfile.close()
			
