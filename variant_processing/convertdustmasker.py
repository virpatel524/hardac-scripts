import os
import csv
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--file', help='file')
args = parser.parse_args()
data = list(csv.reader(open(args.file),delimiter='\t'))



intervals = []
current_chrom = ''


for alpha in data:
	if alpha[0][0] == '>':
		current_chrom = alpha[0][1:]
	else:
		tmp = alpha[0].split(' ')
		newstuff = '{}:{}-{}'.format(current_chrom, tmp[0], tmp[-1])
		intervals.append(newstuff)


newfle = open('/data/wraycompute/vdp5/tmp/interval_dustmasker.list', 'w')

for alpha in intervals:
	newfle.write(alpha + '\n')


newfle.close()