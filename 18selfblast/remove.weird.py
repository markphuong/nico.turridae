import os
import sys

myfasta = open('turrid.2017.baits.renamed.fa', 'r')


alreadydict = dict()

for line in myfasta:

	if ">" in line:
		
		info = line.strip()[1:].split('|')

		

		if 'Conus' in line:
			locus = info[0] + '|' + info[-1]

			if locus in alreadydict:
				if "Crass" in line:
					alreadydict[locus].append('Crass')
				elif "Unedog_Gemm" in line:
					alreadydict[locus].append('Unedog_Gemm')
				elif 'Mitra' in line:
					alreadydict[locus].append('Mitra')
		
			else:
				if "Crass" in line:
					alreadydict[locus] = ['Crass']
				elif "Unedog_Gemm" in line:
					alreadydict[locus] = ['Unedog_Gemm']
				elif 'Mitra' in line:
					alreadydict[locus] = ['Mitra']
		else:
			continue


out = open('remove.these.loci', 'w')

badlist = []

for item in alreadydict:
	if len(list(set(alreadydict[item]))) == len(alreadydict[item]):
		continue
	else:
		out.write(item + '\n')
		badlist.append(item)

myfasta.close()
out.close()
myfasta = open('turrid.2017.baits.renamed.fa', 'r')

out = open('turried.2017.baits.renamed.weird.removed.fa', 'w')
alreadydict = dict()

for line in myfasta:

	if ">" in line:
		
		info = line.strip()[1:].split('|')

		

		if 'Conus' in line:
			locus = info[0] + '|' + info[-1]
			if locus in badlist:
				continue
			else:
				out.write(line)
				out.write(next(myfasta))
		else:
			out.write(line)
			out.write(next(myfasta))




































