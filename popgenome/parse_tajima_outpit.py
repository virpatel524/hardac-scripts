import os
import sys
import csv
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--dir')
args = vars(parser.parse_args())


tajima_dict = {}

lst = []

for filename in os.listdir(args['dir']):
	data = list(csv.reader(open(os.path.join(args['dir'], filename)),delimiter='\t'))[0]
	if data[1] != 'NA':
		newlst = [float(data[1]), data[0]]
		lst.append(newlst)

lst = sorted(lst)

newfle = open('/gpfs/fs0/data/wraycompute/vdp5/filtered_7.18.17/popgenome/tajima_ranked.txt', 'w')

for alpha in lst:
	newfle.write('{}\t{}\n'.format(alpha[1], alpha[0]))

newfle.close()