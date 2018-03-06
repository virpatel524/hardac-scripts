import os
import csv
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--tabfile', help="file which has column 1 as sample name and column 2 as SRR name")
args = parser.parse_args() 


data = list(csv.reader(open(args.tabfile),delimiter='\t'))

for alpha in data:
	putin="""#!/bin/bash
#SBATCH --job-name=launchstuff
#SBATCH --ntasks=1
#SBATCH --mem=6G
#SBATCH --mail-user=vdp5@duke.edu
#SBATCH --output=test.tmp
source /gpfs/fs0/home/vdp5/.bash_profile
cd /data/wraycompute/vdp5/random_gz
fastq-dump.2 --gzip --split-files {}
rename {} {} *""".format(alpha[1], alpha[1], alpha[0])


	newfle = open('/tmp/dl_{}.sh'.format(alpha[0]), 'w')
	newfle.write(putin)
	newfle.close()
	newstr = 'cat /tmp/dl_{}.sh'.format(alpha[0])
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()
	newstr = 'sbatch /tmp/dl_{}.sh'.format(alpha[0])
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()
	newstr = 'rm -rf /tmp/dl_{}.sh'.format(alpha[0])
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

