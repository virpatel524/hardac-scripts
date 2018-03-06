import os 
import csv
import sys
csv.field_size_limit(sys.maxsize)

txt = list(csv.reader(open('/gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.fasta'),delimiter='\t'))

counter = 0

for alpha in txt:
	if alpha[0][0] != '>':
		block = alpha[0]
		zeta = len([a for a in block if a !='N'])
		print len(block), zeta
		counter += zeta


print counter
