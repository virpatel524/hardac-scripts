import os
import csv
import sys
import argparse
import subprocess


holder="""#!/bin/bash
#
#SBATCH --job-name=test
#SBATCH --ntasks=1
#SBATCH --mem=8G
#SBATCH --mail-user=vdp5@duke.edu
#SBATCH -o /home/vdp5/slurm_out/{}_jobout.txt
SCRATCH=/data/wraycompute/vdp5/scratch/$SLURM_JOB_ID
source /gpfs/fs0/home/vdp5/.bash_profile
mkdir -p $SCRATCH
cd $SCRATCH
source ~/.bash_profile
module load jdk/1.8.0_45-fasrc01


module load R

{}
"""



parser = argparse.ArgumentParser()
parser.add_argument('--directory', help="Where the FASTQ GZ are held")
args = parser.parse_args()

samples = []

for alpha in os.listdir(args.directory):
	if 'Rep' not in alpha and alpha[-2:] == 'gz':	
		samples.append(alpha.split('.')[0][:-3])

commands = []

for theta in samples:
	print theta
	newstr = 'srun --mem=8G bowtie2 -x /gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.bowtie -1 {} -2 {} | samtools view  -Sb - | samtools sort - -o /home/vdp5/data/bam/{}.bam'.format( os.path.join(args.directory , theta + '-R1.fastq.gz'),  os.path.join(args.directory , theta + '-R2.fastq.gz'), theta)
	newfle = open('/tmp/{}_variant.sh'.format(theta), 'w')
	newfle.write(holder.format(theta, newstr, theta))
	newfle.close()
	commands.append('/tmp/{}_variant.sh'.format(theta))

outputfle = open('/tmp/launcher_chipseq.sh', 'w')

for beta in commands:
	outputfle.write('sbatch --mem=8G {}\n'.format(beta))

outputfle.close()



