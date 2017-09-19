import os
import sys
import operator

myfasta = open(sys.argv[1], 'r')

fastadict = dict()

###############
group1file = open(sys.argv[2], 'r')


group1 = []

for line in group1file:
	group1.append(line.strip())

####################
group2file = open(sys.argv[3], 'r')


group2 = []

for line in group2file:
	group2.append(line.strip())



##############################
group1dict = dict()

group2dict = dict()

for line in myfasta:
	if '>' in line:
		seq = next(myfasta).strip()


		ID = line.strip()[1:]
		fastadict[ID] = seq

	
		reallength = seq.replace('-','').replace('n','') # remove - and n's
		if ID in group1:
			group1dict[ID] = len(reallength)
		elif ID in group2:
			group2dict[ID] = len(reallength)
		else:
			continue
if len(group1dict) > 0 and len(group2dict) > 2:
	mybestg1 = max(group1dict.iteritems(), key=operator.itemgetter(1))[0]

	mybestg2 = max(group2dict.iteritems(), key=operator.itemgetter(1))[0]


	fastaID = sys.argv[1].split('_')[0]

	groupID = sys.argv[4]

	out = open(fastaID + '_' + groupID + '.fa', 'w')

	out.write('>' + mybestg1 + '\n')
	out.write(fastadict[mybestg1] + '\n')

	out.write('>' + mybestg2 + '\n')
	out.write(fastadict[mybestg2] + '\n')












