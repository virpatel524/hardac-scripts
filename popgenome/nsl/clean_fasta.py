import os
import sys
import csv
import argparse
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument('--fasta', help="fasta input")
args = parser.parse_args() 


newfle = open('/gpfs/fs0/data/wraycompute/vdp5/tmp/fastatmpers.fasta', 'w')

data = list(csv.reader(open(args.fasta),delimiter='\t'))

for beta in data:
	if '>' in beta[0]:
		print beta
		hold = beta[0].split(' ')[0]
		beta[0] = hold
	newfle.write('\t'.join(beta) + '\n')

newfle.close()


newstr = 'mv /gpfs/fs0/data/wraycompute/vdp5/tmp/fastatmpers.fasta {}'.format(args.fasta)
process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
process.wait()

