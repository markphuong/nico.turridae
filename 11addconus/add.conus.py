import os
import sys
from os.path import isfile, join




thedir = [f for f in os.listdir('.') if os.path.isfile(f)]
otherdir = [f for f in os.listdir('/pylon2/bi4s86p/phuong/bait.design.2017/phylogenetics/1transcriptome.markers/8pdist/results') if isfile(join('/pylon2/bi4s86p/phuong/bait.design.2017/phylogenetics/1transcriptome.markers/8pdist/results', f))]

otherdir = set(otherdir)


for thing in thedir:
	if '.pdist' in thing:

		conusthing = thing.replace('.NI','')

		outfile = thing.split('_')[0] + '.conus.added.fa'

		if conusthing in otherdir:	
			cmd = 'cp /pylon2/bi4s86p/phuong/bait.design.2017/phylogenetics/1transcriptome.markers/8pdist/results/' + conusthing + ' ./'

			os.system(cmd)

			cmd = 'mafft --add ' + conusthing + ' ' + thing + ' > ' + outfile

			os.system(cmd)

		else:
			cmd = 'mv ' + thing + ' ' + outfile
			os.system(cmd)
