#!/bin/env python2.7

#SBATCH --ntasks=1
#SBATCH --mem=8G
#SBATCH --output=/data/wraycompute/vdp5/slurm_out/openuphaplo

import os
import csv
import sys
import argparse
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument('--sample', help="Sample name")
parser.add_argument('--mastervcf', help="Master VCF")
parser.add_argument('--range', help="Master VCF")
args = parser.parse_args()


chromdata = list(csv.reader(open('/gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.lengths'),delimiter='\t'))

chromlengths = {}

for beta in chromdata:
	chromlengths[beta[0]] = int(beta[1])

topsets = list(csv.reader(open('/gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/randomset100.20minor.txt'.format(args.sample)),delimiter='\t'))

if not os.path.isdir('/home/vdp5/data/poptests/nsl/output/{}/control'.format(args.sample)):
	os.mkdir('/home/vdp5/data/poptests/nsl/output/{}/control'.format(args.sample))

if not os.path.isdir('/home/vdp5/data/poptests/nsl/output/{}/control/{}/'.format(args.sample, args.range)):
	os.mkdir('/home/vdp5/data/poptests/nsl/output/{}/control/{}/'.format(args.sample, args.range))

if not os.path.isdir('/home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/'.format(args.sample, args.range)):
	os.mkdir('/home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/'.format(args.sample, args.range))

if not os.path.isdir('/home/vdp5/data/poptests/nsl/output/{}/control/{}/fasta/'.format(args.sample, args.range)):
	os.mkdir('/home/vdp5/data/poptests/nsl/output/{}/control/{}/fasta/'.format(args.sample, args.range))

for beta in topsets:
	if  chromlengths[beta[0]] - int(beta[1]) <= int(args.range):
		end = chromlengths[beta[0]] - 1
		start = int(beta[1]) - int(args.range)
	if int(beta[1]) - int(args.range) <= 0:
		start = 1
		end = int(beta[1]) + int(args.range)
	else:
		start = int(beta[1]) - int(args.range)
		end = int(beta[1]) + int(args.range)

	newstr = 'java -Xmx15000m -jar /gpfs/fs0/data/wraycompute/vdp5/src/GenomeAnalysisTK.jar -T SelectVariants -V {} -R /gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.fasta -L {} -o /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.vcf'.format(args.mastervcf, '{}:{}-{}'.format(beta[0], start, end), args.sample, args.range, beta[0], beta[1], args.range)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

	newstr = 'bgzip -c /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.vcf > /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.vcf.gz'.format(args.sample, args.range, beta[0], beta[1], args.range, args.sample, args.range, beta[0], beta[1], args.range)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

	newstr = 'tabix -p vcf /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.vcf.gz'.format(args.sample, args.range, beta[0], beta[1], args.range)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()


	bigtab_str = '/home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.tab'.format(args.sample, args.range, beta[0], beta[1], args.range)
	newstr = 'zcat /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.vcf.gz | vcf-to-tab > {}'.format(args.sample, args.range, beta[0], beta[1], args.range, bigtab_str)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()


	logger = open('/gpfs/fs0/data/wraycompute/vdp5/tmp/log.txt','w')

	newstr = 'python2.7 /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/create_trait_file.py --tabfile {} --chrom {} --locus {} --sample {} --range {}'.format(bigtab_str, beta[0], beta[1], args.sample, args.range)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

	logger.write(newstr)

	logger.close()

	newstr = 'java -Xmx15000m -jar /gpfs/fs0/data/wraycompute/vdp5/src/GenomeAnalysisTK.jar -T SelectVariants -V /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.vcf -R /gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.fasta  -o /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.nonmissing.vcf -sf /home/vdp5/data/tmp/sampleitems_{}_{}.list'.format(args.sample, args.range, beta[0], beta[1], args.range, args.sample, args.range, beta[0], beta[1], args.range, args.range, args.sample)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

	newstr = 'bgzip -c /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.nonmissing.vcf > /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.nonmissing.vcf.gz'.format(args.sample, args.range, beta[0], beta[1], args.range, args.sample, args.range, beta[0], beta[1], args.range)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

	newstr = 'tabix -p vcf /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.nonmissing.vcf.gz'.format(args.sample, args.range, beta[0], beta[1], args.range)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()






	bigvcf_str = '/home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.nonmissing.vcf.gz'.format(args.sample, args.range, beta[0], beta[1], args.range)
	bigfasta_str = '/home/vdp5/data/poptests/nsl/output/{}/control/{}/fasta/{}_{}_{}-range.nonmissing.fasta'.format(args.sample, args.range, beta[0], beta[1], args.range)
	bignexus_str = '/home/vdp5/data/poptests/nsl/output/{}/control/{}/fasta/{}_{}_{}-range.nonmissing'.format(args.sample, args.range, beta[0], beta[1], args.range)
	bigvcf_str_pruned = '/home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.nonmissing.pruned'.format(args.sample, args.range, beta[0], beta[1], args.range)
	bigfasta_str_pruned = '/home/vdp5/data/poptests/nsl/output/{}/control/{}/fasta/{}_{}_{}-range.nonmissing.pruned.fasta'.format(args.sample, args.range, beta[0], beta[1], args.range)
	bignexus_str_pruned = '/home/vdp5/data/poptests/nsl/output/{}/control/{}/fasta/{}_{}_{}-range.nonmissing.pruned'.format(args.sample, args.range, beta[0], beta[1], args.range)


	newstr = 'plink --vcf {} --indep-pairwise 50 10 0.5 --out /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/prunedset --double-id --allow-extra-chr'.format(bigvcf_str, args.sample, args.range) 
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

	newstr = 'plink --vcf {} --extract /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/prunedset.prune.in --double-id --allow-extra-chr --make-bed --out  /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/prunedData'.format(bigvcf_str, args.sample, args.range, args.sample, args.range) 
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

	newstr = 'plink --bfile /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/prunedData --recode vcf --out {} --double-id --allow-extra-chr'.format(args.sample, args.range, bigvcf_str_pruned)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait() 


	newstr = 'bgzip -c /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.nonmissing.pruned.vcf > /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.nonmissing.pruned.vcf.gz'.format(args.sample, args.range, beta[0], beta[1], args.range, args.sample, args.range, beta[0], beta[1], args.range)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

	newstr = 'tabix -p vcf /home/vdp5/data/poptests/nsl/output/{}/control/{}/vcf/{}_{}_{}-range.nonmissing.pruned.vcf.gz'.format(args.sample, args.range, beta[0], beta[1], args.range)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

	newstr = 'python2.7 /gpfs/fs0/data/wraycompute/vdp5/bin/alignment-from-vcf.py /gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.fasta {} {} {} {} 1 {} '.format(bigvcf_str, beta[0], start, end, bigfasta_str)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

	newstr = 'python2.7 /gpfs/fs0/data/wraycompute/vdp5/bin/alignment-from-vcf.py /gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.fasta {}.vcf.gz {} {} {} 1 {} '.format(bigvcf_str_pruned, beta[0], start, end, bigfasta_str_pruned)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

	newstr = 'python2.7 /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/clean_fasta.py --fasta {}'.format(bigfasta_str)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

	newstr = 'python2.7 /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/clean_fasta_pruned.py --fasta {}'.format(bigfasta_str_pruned)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

	newstr = ' Rscript /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/convert_fasta2nexus.R {}'.format(bigfasta_str)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()

	newstr = ' Rscript /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/convert_fasta2nexus_pruned.R {}'.format(bigfasta_str_pruned)
	process = subprocess.Popen([newstr,], stdout=subprocess.PIPE,shell=True)
	process.wait()