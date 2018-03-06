#!/data/wraycompute/vdp5/bin/bin/python2.7
#
# SBATCH --ntasks=1
# SBATCH --mem=30G
# SBATCH --output=/data/wraycompute/vdp5/slurm_out/vcfedit.out

# this create creates a geno file for processing by hmmIDB.

import os 
import csv
import sys


data = list(csv.reader(open('/gpfs/fs0/data/wraycompute/vdp5/filtered_7.18.17/5iter_allvariants_filtered.heteroremove.rareremove.noheteroconsid.vcf'),delimiter='\t'))
newfle = open('/gpfs/fs0/data/wraycompute/vdp5/filtered_7.18.17/5iter_allvariants_filtered.heteroremove.rareremove.noheteroconsid.geno', 'w')

samples = []


for alpha in data:
	matrix = []
	if '##' in alpha[0]:
		newfle.write('\t'.join(alpha) + '\n')

	elif '#CHROM' in alpha[0]:
		samples = alpha[9:]
		newfle.write('chrom\tpos\t' + '\t'.join(samples) + '\n')
	else:
		matrix.append(alpha[0])
		matrix.append(alpha[1])
		for beta in alpha[9:]:
			marker = beta[:3].split('/')
			if marker[0] == '.':
				matrix.append('-1')
			elif marker[0] == marker[1]:
				matrix.append(marker[0])
			else:
				tmp = beta.split(':')
				tmp = tmp[1].split(',')
				tmp = [float(a) for a in tmp]
				tot = tmp[1] + tmp[0]
				if tot < 4:
					matrix.append('-1')
					continue
				a = tmp[0] / (tmp[1] + tmp[0])
				b = tmp[1] / (tmp[1] + tmp[0])
				if a > 0.75:
					matrix.append('0')
				elif b > 0.75:
					matrix.append('1')
				else:
					matrix.append('-1')

		newfle.write('\t'.join(matrix) + '\n')

newfle.close()
