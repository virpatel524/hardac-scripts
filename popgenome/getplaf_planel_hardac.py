import vcf
import argparse
import sys
import os
import numpy
import csv


def check_call(var, name):
	if var.genotype(name).gt_type == None:
		return 'kill'
	else:
		return 'pass'




sys.path.append(os.getcwd())
parser = argparse.ArgumentParser()
parser.add_argument('--vcffile', help="VCF file for use")
parser.add_argument('--sampfile', help='who all will be processed')
args = parser.parse_args()
file = args.vcffile
whoall = list(csv.reader(open(args.sampfile),delimiter='\t'))








vcf_reader = vcf.Reader(open(args.vcffile, 'r'))



writers = []
plafs = []


for index, alpha in enumerate(whoall):
	name = alpha[0]
	vcf_writer = vcf.Writer(open('/home/vdp5/data/variant_staging/indiv_samples/{}_refined.vcf'.format(name),'w'), vcf_reader)
	newfle_minor = open('/home/vdp5/data/poptests/deploid/indiv_plaf/{}_scenariominor_plaf.txt'.format(name), 'w')
	newfle_minor.write('CHROM\tPOS\tPLAF\n')
	writers.append(vcf_writer)
	plafs.append(newfle_minor)


for index, rec in enumerate(vcf_reader):
	print(index)
	if rec.var_type != 'snp': continue
	for i in range(len(whoall)):
		name = whoall[i][0]
		if check_call(rec, name) == 'kill': continue
		writers[i].write_record(rec)
		majorallelefreq = 1 - float(rec.aaf[0])
		minorallelefreq = float(rec.aaf[0])
		plafs[i].write('{}\t{}\t{}\n'.format(rec.CHROM, rec.start + 1, minorallelefreq))



for i in range(len(whoall)):
	writers[i].close()
	plafs[i].close()

vcf_reader.close()


# for index, alpha in enumerate(whoall):

# 	if index > 100: break
# 	name = alpha[0]
# 	print name
# 	vcf_writer = vcf.Writer(open('/nfs/wraycompute/vir/variant_storage/indiv_samples/{}_refined.vcf'.format(name),'w'), vcf_reader)
# 	newfle_minor = open('/home/vdp5/projects/vivax_cambodia/data/poptests/deploid/indiv_plaf/{}_scenariominor_plaf.txt'.format(name), 'w')
# 	newfle_minor.write('CHROM\tPOS\tPLAF\n')
# 	vcf_reader = vcf.Reader(open(args.vcffile, 'r'))


# 	for index, rec in enumerate(vcf_reader):
# 		if rec.var_type != 'snp': continue
# 		if check_call(rec, name) == 'kill': continue
# 		vcf_writer.write_record(rec)


# 		majorallelefreq = 1 - float(rec.aaf[0])
# 		minorallelefreq = float(rec.aaf[0])
# 		newfle_minor.write('{}\t{}\t{}\n'.format(rec.CHROM, rec.start + 1, minorallelefreq))

# 	vcf_writer.close()
# 	vcf_reader.close()


# newfle_minor.close()