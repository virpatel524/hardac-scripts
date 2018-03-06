import os 
import csv
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--vcftab', help="VCF file for use")
parser.add_argument('--output', help="VCF file for use")


args = parser.parse_args()
data = list(csv.reader(open(args.vcftab),delimiter='\t'))

newfle = open(args.output, 'w')

for alpha in data[1:]:
	ref = alpha[2]
	stringer = ''
	for beta in alpha[3:]:
		tmp = beta.split('/')
		if tmp[0] == '.':
			stringer += '9'
		elif tmp[0] == ref and tmp[1] == ref:
			stringer += '2'
		elif tmp[0] == ref and tmp[1] != ref:
			stringer += '0'
		elif tmp[0] != ref and tmp[1] != ref:
			stringer += '0'
	newfle.write('{}\n'.format(stringer))


newfle.close()