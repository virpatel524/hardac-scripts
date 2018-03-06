import os 
import csv
import sys


sourcenames_2files = {}
import subprocess

for alpha in os.listdir('/data/wraycompute/vdp5/bam'):
	if 'PvSPZ' in alpha:
		if 'Rep' in alpha: 
			src = '-'.join(alpha.split('-')[:-2])
			sourcenames_2files.setdefault(src, []).append(os.path.join('/data/wraycompute/vdp5/bam', alpha))
		else:
			src = '-'.join(alpha.split('-')[:-1])
			sourcenames_2files.setdefault(src, []).append(os.path.join('/data/wraycompute/vdp5/bam', alpha))

for alpha in sourcenames_2files:
	outputter = 'samtools merge {} {} '.format(os.path.join('/home/vdp5/data/bam/chipseq_combined', '{}_combined.bam'.format(alpha)), ' '.join(sourcenames_2files[alpha]))
	process = subprocess.Popen([outputter,], stdout=subprocess.PIPE,shell=True)
	process.wait()

