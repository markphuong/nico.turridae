import os
import sys

myfasta = open(sys.argv[1] , 'r')

out = open(sys.argv[2], 'w')

for line in myfasta:
	if "#" in line or "begin" in line or 'datatype' in line or 'matrix' in line or line == ';\n' or 'end' in line:
		continue

	elif 'nchar' in line:
		nchar = int(line.strip().split('=')[-1][:-1])
		print nchar
	else:
		myseq = line.strip()
		mylength = nchar - myseq.count('-') - myseq.count('?') - myseq.count('n')
#		print myseq.count('-')
#		print myseq.count('?')
		mylength = float(mylength)
#		print line[:13]
#		print mylength/573854

		out.write(line[:13] + '\t' + str(mylength/nchar) + '\n') ######### modify line[:13] to change how much of the name is outputted
