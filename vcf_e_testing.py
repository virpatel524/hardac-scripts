#!/bin/env python2.7

#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --output=/data/wraycompute/vdp5/slurm_out/vcfedit.out


import vcf
import argparse
import sys 
import os







vcf_reader = vcf.Reader(open('/gpfs/fs0/data/wraycompute/vdp5/varfilter_dir/FLZR01000094.rarefiltered.vcf', 'r'))

vcf_writer = vcf.Writer(open('/home/vdp5/tmp/tmp_vcf_write.vcf.gz', 'w'), vcf_reader)



header = '/gpfs/fs0/data/wraycompute/vdp5/unaltered_vcf_7.5.17/5iter_allvariants_filtered.LT635617.vcf'



counter_low = 0
counter_total = 0


#1percent filtering

total_good = 0
total_all = 0


# for record in vcf_reader:
# 	total_number_of_reads = {}
# 	homalt = record.get_hom_alts()
# 	hets = record.get_hets()
# 	homref = record.get_hom_refs()

# 	for alpha in homref:
# 		tmp = alpha.data[0].split('/')
# 		allele = []

# 		for beta in tmp:
# 			allele.append(int(beta))

# 		for beta in allele:
# 			if beta not in total_number_of_reads:
# 				total_number_of_reads[beta] = 0

# 		for i in range(len(allele)):
# 			total_number_of_reads[allele[i]] += alpha.data[1][i]

# 	for alpha in hets:
# 		tmp = alpha.data[0].split('/')
# 		allele = []

# 		for beta in tmp:
# 			allele.append(int(beta))

# 		for beta in allele:
# 			if beta not in total_number_of_reads:
# 				total_number_of_reads[beta] = 0

# 		for i in range(len(allele)):
# 			total_number_of_reads[allele[i]] += alpha.data[1][i]


# 	for alpha in homref:
# 		tmp = alpha.data[0].split('/')
# 		allele = []

# 		for beta in tmp:
# 			allele.append(int(beta))

# 		for beta in allele:
# 			if beta not in total_number_of_reads:
# 				total_number_of_reads[beta] = 0

# 		for i in range(len(allele)):
# 			total_number_of_reads[allele[i]] += alpha.data[1][i]

# 	tot = 0

# 	for alpha in total_number_of_reads:
# 		tot += total_number_of_reads[alpha] 

# 	for alpha in total_number_of_reads:
# 		if alpha == 0:
# 			continue
# 		zeta = (float(total_number_of_reads[alpha]) / float(tot)) * 100
# 		if zeta > 1:
# 			vcf_writer.write_record(record)
# 			total_good += 1
# 		elif total_number_of_reads[alpha] > 10:
# 			total_good += 1
# 		total_all += 1
		
vcf_writer.close()
# tmp =  float(total_good) / float(total_all)


for record in vcf_reader:
	for sample in record.samples:
		print sample.gt_type, sample.data[2]
