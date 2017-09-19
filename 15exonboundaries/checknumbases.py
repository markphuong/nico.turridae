file1 = open('all_conoidea_markers_fixOrientation.fasta', 'r')
mylength = 0
for line in file1:
	if ">" in line:
		mylength += len(next(file1))

file2 = open('conoidea_baits_sliced.fasta', 'r')
mylen2 = 0
for line in file2:
	if ">" in line:
		mylen2 += len(next(file2).replace('-',''))

print mylength
print mylen2
if mylength == mylen2:
	print 'WOO'	

myseq = '---'
print len(myseq.replace('-',''))