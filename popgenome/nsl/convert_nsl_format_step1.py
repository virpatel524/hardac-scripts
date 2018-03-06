#!/bin/env python2.7

#SBATCH --ntasks=1
#SBATCH --mem=8G
#SBATCH --output=/data/wraycompute/vdp5/slurm_out/openuphaplo

import os
import csv
import argparse
import sys
import vcf


parser = argparse.ArgumentParser()
parser.add_argument('--vcfdir', help="vcf file to parse")
parser.add_argument('--sample', help='sample name')
args = parser.parse_args()


holdem="""---
pop: All
build: PVP01
hapmap_release: lol
start:
stop:
snps:
"""


samples = []
converts = {}

convertraw = list(csv.reader(open('/gpfs/fs0/data/wraycompute/vdp5/txt_files/sample2shortcut.txt'),delimiter='\t'))

for beta in convertraw:
	converts[beta[0]] = beta[1]

for file in os.listdir(args.vcfdir):
	if 'FLZR' in file:
		continue
	vcf_reader = vcf.Reader(open(os.path.join(args.vcfdir, file), 'r'))
	chromdata = {}
	for record in vcf_reader:
		chromdata.setdefault(record.CHROM, []).append(record)
		if len(samples) == 0:
			for sam in record.samples:
				samples.append(sam.sample)
				
	if not os.path.isdir('/home/vdp5/data/poptests/nsl/input/{}'.format(args.sample)):
		os.mkdir('/home/vdp5/data/poptests/nsl/input/{}'.format(args.sample))


	for chrom in chromdata:
		newfle = open('/home/vdp5/data/poptests/nsl/input/{}/chr{}_samples.txt'.format(args.sample, chrom), 'w')
		for beta in samples:
			newfle.write(converts[beta] + '\n')
		newfle.close()

		setofall = []
		strbig = {}
		newfle = open('/home/vdp5/data/poptests/nsl/input/{}/chr{}_ansder.txt'.format(args.sample, chrom), 'w')
		counter = 0
		for beta in chromdata[chrom]:
			for call in beta.samples:
				if call.sample not in strbig:
					if call.gt_bases == None:
						strbig[call.sample] = 'N'
					else:
						strbig[call.sample] = call.gt_bases[0]
				else:
					if call.gt_bases == None:
						strbig[call.sample] = strbig[call.sample] + 'N'
					else:
						strbig[call.sample] = strbig[call.sample] + call.gt_bases[0]
			counter += 1
			newfle.write('rs{}\t{}\t{}\n'.format(counter, beta.REF, beta.ALT[0]))
			setofall.append(['rs{}'.format(counter), beta.POS])
		newfle.close()

		newfle = open('/home/vdp5/data/poptests/nsl/input/{}/chr{}_haplotype.txt'.format(args.sample, chrom), 'w')
		newfle.write(holdem)
		for it in setofall:
			newfle.write('  - {}: {}\n'.format(it[0], it[1]))
		newfle.write('phased_haplotypes:\n')

		for sinca in sorted(samples):
			newfle.write('  - {}: {}\n'.format(converts[sinca], strbig[sinca]))
		newfle.close()