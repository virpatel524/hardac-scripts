import os 
import csv
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--blocksfile', help="outputfile")
args = parser.parse_args()

for beta in list(csv.reader(open(args.blocksfile),delimiter='\t'))[7:]:
	print beta[5], beta[6]
	print int(beta[6]) - int(beta[5])


