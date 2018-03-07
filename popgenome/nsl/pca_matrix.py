import os
import csv
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--lociselected', help="VCF file for use")
parser.add_argument('--locinon', help="VCF file for use")
parser.add_argument('--tabfile', help="tabfile to search for")
args = parser.parse_args()

matrixsec = list(csv.reader(open(args.lociselected),delimiter='\t'))
matrixnon = list(csv.reader(open(args.locinon),delimiter='\t'))
tab = list(csv.reader(open(args.tabfile),delimiter='\t'))



aggregate = matrixsec

lociset = []
sampset = []

samp2matrix = {}

samps = tab[0][3:]

for beta in tab:
	for kappa in aggregate:
		if kappa[0] == beta[0] and kappa[1] == beta[1]:
			albase = beta[2]
			lociset.append('{}_{}'.format(beta[0], beta[1]))
			for index, samp in enumerate(beta[3:]):
				if samp[0] == albase or samp[0] == '.':
					samp2matrix.setdefault(samps[index], []).append('0')
				else:
					samp2matrix.setdefault(samps[index], []).append('1')


newdata = open('/home/vdp5/data/poptests/nsl/output/1-MT/txtfiles/matrix_selectonly_sampnamestoo.txt', 'w')

numer = open('/home/vdp5/data/poptests/nsl/output/1-MT/txtfiles/matrix_selectonly_sampnamestoo_number.txt', 'w')

counter = 0
for beta in lociset:
	counter += 1
	splitter = beta.split('_')
	whois = '0'
	for item in matrixsec:
		if item[0] == splitter[0] and item[1] == splitter[1]:
			whois = '1'
	numer.write('{}\t{}\t{}\n'.format(counter, whois, beta))

numer.close()

outputset = []

for beta in samp2matrix:
	samp2matrix[beta] = [beta,] + samp2matrix[beta]
	outputset.append(samp2matrix[beta])


newset = map(list, zip(*outputset)) 


for beta in newset:
	newdata.write('\t'.join(beta) + '\n')

newdata.close()



