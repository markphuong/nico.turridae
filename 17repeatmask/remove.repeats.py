import os
import sys



mymap = open('mymap', 'r')

namedict = dict()

for line in mymap:
	info = line.strip().split('\t')
	namedict[info[1]] = info[0]

myfasta = open('turrid.seq.fa', 'r')


out = open('turrid.2017.baits.transcriptome.phylogenetics.fa.sliced.filtered.rm', 'w')


rmfile = open('RM2_turrid.seq.fa_1502145568.out', 'r')



badlist = []

for line in rmfile:
	if 'seq' in line:
		info = line.strip().split(' ')

		for thing in info:
			if 'seq' in thing:
				badlist.append(thing)
				break


print badlist
print len(badlist)
print len(list(set(badlist)))

for line in myfasta:
	if ">" in line:
		if line.strip()[1:] in badlist:
			continue
		else:
			out.write(namedict[line.strip()[1:]] + '\n')
			out.write(next(myfasta))
