import os
import sys

mynewref = open('mynewlottiaref.fa', 'r')


alreadyhave = []

out = open('final_lottia_ref.fa', 'w')

myownref = []

for line in mynewref:
	if ">" in line:

		if '|' in line:
			alreadyhave.append(line.strip().split('|')[3])
			out.write('>' + line.split('|')[3] + '\n')
			myownref.append(line.strip().split('|')[3])
		else:
			out.write(line)
			alreadyhave.append(line.strip()[1:])
	else:
		out.write(line)

print len(alreadyhave)
print len(myownref)

mylottia = open('Lotgi1_GeneModels_FilteredModels1_aa.fasta.NI', 'r')



lottialist = []

for line in mylottia:
	if ">" in line:
		info = line.strip().split('|')
		lottialist.append(info[2])
		if info[2] in alreadyhave:
			continue
		else:
			out.write('>' + info[2] + '\n')
			out.write(next(mylottia))
print len(lottialist)
print len(list(set(lottialist)))













