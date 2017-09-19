import os
import sys


mynexus = open(sys.argv[1], 'r')

out = open(sys.argv[2], 'w')


for line in mynexus:
	if 'end;' in line:
		out.write(line)
		break
	else:
		out.write(line)