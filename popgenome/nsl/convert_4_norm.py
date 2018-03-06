import os 
import csv
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--nsl', help="nSL file we want")
args = parser.parse_args()

root = args.nsl

newnsl = '.'.join(args.nsl.split('.')[:-1]) + '.selscan.txt'

newfle = open(newnsl, 'w')

for beta in list(csv.reader(open(args.nsl),delimiter='\t'))[1:]:
	locid = beta[0]
	loc = beta[1]
	sl = beta[2]
	freq = float(beta[4]) / 100.0
	newfle.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(locid, loc, freq, 0, 0, sl))

newfle.close()

