import os
import csv
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--sample', help="VCF file for use")
parser.add_argument('--range', help="VCF file for use")
args = parser.parse_args()

samp = args.sample
ran = args.range


if not os.path.isdir('/home/vdp5/data/poptests/nsl/output/{}/{}/plink_ld'.format(samp, ran)):
	os.makedirs('/home/vdp5/data/poptests/nsl/output/{}/{}/plink_ld'.format(samp, ran))


for item in os.listdir('/home/vdp5/data/poptests/nsl/output/{}/{}/vcf/'.format(samp, ran)):
	if os.path.join('/home/vdp5/data/poptests/nsl/output/{}/{}/vcf/'.format(samp, ran), item).split('.')[-1] == 'vcf':
		if 'nonmissing' in item and 'pruned' not in item:
			potoutput = '.'.join(item.split('.')[:-1])
			tot = os.path.join('/home/vdp5/data/poptests/nsl/output/{}/{}/plink_ld'.format(samp, ran), potoutput)
			plinktot = os.path.join('/home/vdp5/data/poptests/nsl/output/{}/{}/plink_ld'.format(samp, ran), potoutput + '.blocksoutput')
			newstr = 'vcftools --vcf {} --plink --out {}'.format(os.path.join('/home/vdp5/data/poptests/nsl/output/{}/{}/vcf/'.format(samp, ran), item), tot)
			process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
			process.wait()
			newstr = 'plink --file {} --blocks no-pheno-req --out {}'.format(tot, plinktot)
			process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
			process.wait()			