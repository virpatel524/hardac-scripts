import os
import csv
import sys

opener="""#!/bin/env bash

#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --output=/data/wraycompute/vdp5/slurm_out/{}_macs.out

module load gcc
module load R

macs2 callpeak -t {} -c {} -f BAMPE -g 2.88e7 -B -q 0.01 --broad -n {} --outdir /home/vdp5/data/chip-seq/macs2_output/{}"""


corresponding_list = list(csv.reader(open('/gpfs/fs0/data/wraycompute/vdp5/chip-seq/other/list_corresponding'),delimiter='\t'))

for alpha in corresponding_list:
	if len(alpha) != 3:
		continue
	base = '-'.join(alpha[0].split('-')[:3])
	holder = '-'.join(alpha[0].split('-')[:3]) + '.bam'
	input_holder = '-'.join(alpha[1].split('-')[:3]) + '.bam'
	treat = os.path.join('/gpfs/fs0/data/wraycompute/vdp5/bam', holder)
	cont = os.path.join('/gpfs/fs0/data/wraycompute/vdp5/bam', input_holder)


	try:
		os.mkdir(os.path.join('/home/vdp5/data/chip-seq/macs2_output/',alpha[2]))
	except: 
		x = 5

	newfle = open(os.path.join('/home/vdp5/scripts/chip-seq/macs2_scripts', alpha[2][:-3]) + '_macsrunner.sh' , 'w')

	newfle.write(opener.format(base, treat, cont, base, base))
	newfle.close()


