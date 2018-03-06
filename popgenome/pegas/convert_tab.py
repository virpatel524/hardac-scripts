import os
import csv
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--tabfile', help="VCF file for use")
args = parser.parse_args()

data = list(csv.reader(open(args.tabfile),delimiter='\t'))

ind2samp = {}
samp2shit = {}


for index, alpha in enumerate(data[0][3:]):
	ind2samp[index] = alpha

print ind2samp

for alpha in data[1:]:
	for index, zeta in enumerate(alpha[3:]):
		beta = zeta.split('/')
		if beta[0] == '.':
			samp2shit.setdefault(ind2samp[index], []).append('N|N')
		else:
			samp2shit.setdefault(ind2samp[index], []).append('|'.join(beta))


newfle = open('/home/vdp5/data/tmp/zip/allele.txt', 'w')

for beta in samp2shit:
	newfle.write('{}\t{}\n'.format(beta, '\t'.join(samp2shit[beta])))

newfle.close()
