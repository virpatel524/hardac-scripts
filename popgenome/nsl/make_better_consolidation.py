import os 
import csv
import sys
import argparse
import shutil


parser = argparse.ArgumentParser()
parser.add_argument('--sample', help="VCF file for use")
args = parser.parse_args()

root = '/home/vdp5/data/poptests/nsl/output/{}/'.format(args.sample)

if not os.path.isdir(os.path.join(root, 'consolidated')):
	os.mkdir(os.path.join(root, 'consolidated'))

goodies = []


for beta in os.listdir(os.path.join(root, '1000', 'vcf')):
	if 'nonmissing.traits' in beta:
		param = beta.split('/')[-1]
		param = '_'.join(param.split('_')[:2])
		goodies.append(param)

for beta in goodies:
	if not os.path.isdir((os.path.join(root, 'consolidated/', beta))):
		os.mkdir(os.path.join(root, 'consolidated/', beta))

for theta in ['1000', '2000', '5000', '10000', '20000']:
	for beta in goodies:
		if not os.path.isdir((os.path.join(root, 'consolidated/', beta, theta))):
			os.mkdir(os.path.join(root, 'consolidated/', beta, theta))
		shutil.copy(os.path.join(root,theta, 'fasta', '{}_{}-range.nonmissing.nex'.format(beta, theta)),os.path.join(root, 'consolidated/', beta,theta, '{}_{}-range.nonmissing.nex'.format(beta, theta) ))
		shutil.copy(os.path.join(root,theta, 'vcf', '{}_{}-range.nonmissing.popargs'.format(beta, theta)),os.path.join(root, 'consolidated/', beta, theta,  '{}_{}-range.nonmissing.popargs'.format(beta, theta)))
		shutil.copy(os.path.join(root,theta, 'vcf', '{}_{}-range.nonmissing.traits'.format(beta, theta)),os.path.join(root, 'consolidated/', beta, theta, '{}_{}-range.nonmissing.traits'.format(beta, theta)))



