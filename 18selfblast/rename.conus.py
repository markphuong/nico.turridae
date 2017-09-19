import os
import sys



myfasta = open('turrid.2017.baits.transcriptome.phylogenetics.fa.sliced.filtered.rm', 'r')


outfasta = open('turrid.2017.baits.renamed.fa', 'w')

out = open('rename.conus.map', 'w')

alreadydict = dict()

for line in myfasta:

	if ">" in line:
		
		info = line.strip()[1:].split('|')

		

		if '_' in info[-1]:
			if 'Mitra' in info[0]:
				newID = [info[1].split('_')[1], 'Mitra', 'Conus', info[-4], info[-3], info[-2], info[-1].replace('_','')]
			elif 'Crass' in line:
				newID = [info[-2].split('_')[1], 'Crass' , 'Conus', info[-5], info[-4], info[-3], info[-1].replace('_','')] 
			else:
				newID = [info[-2].split('_')[1], 'Unedog_Gemm' , 'Conus', info[-5], info[-4], info[-3], info[-1].replace('_','')] 
				
			outfasta.write('>' + '|'.join(newID) + '\n')
			outfasta.write(next(myfasta))
			out.write(line.strip() + '\t' + '|'.join(newID) + '\n')
		else:
			outfasta.write(line)
			outfasta.write(next(myfasta))
			















