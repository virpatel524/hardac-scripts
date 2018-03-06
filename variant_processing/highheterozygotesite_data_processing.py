#!/bin/env python2.7

#SBATCH --ntasks=1
#SBATCH --output=/data/wraycompute/vdp5/slurm_out/vcfedit_testingops.out


import os
import csv
import sys
import vcf
import numpy
import argparse
import resource
import math


import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pylab

accountfle = open('/data/wraycompute/vdp5/tmp/accounts.txt', 'w')

accountfle.write('newwwwws\n')
accountfle.close()


sys.path.append(os.getcwd())
parser = argparse.ArgumentParser()
parser.add_argument('--vcffile', help="VCF file for use")
parser.add_argument('--output', help='output file')
args = parser.parse_args()

file = args.vcffile


vcf_reader = vcf.Reader(open(file, 'r'))

vcf_writer = vcf.Writer(open(args.output, 'w'), vcf_reader)


holderbase = {}

snps_base = {'0.0-0.05': [], '0.05-0.10': [], '0.10-0.15': [], '0.15-0.20': [], '0.20-0.25': [],
             '0.25-0.30': [], '0.30-0.35': [], '0.35-0.40': [], '0.40-0.45': [], '0.45-0.50': []}

counter = -1
for record in vcf_reader:
    counter += 1
    recid = '{}:{}-{}'.format(record.CHROM, record.start, record.end)
    countersample = 0
    datasummer = 0
    hets = 0
    hethomocounter = 0
    try:
        for alpha in record.samples:
            if int(alpha.data[1][0]) + int(alpha.data[1][1]) == 0:
              continue
            datasummer += (float(alpha.data[1][0]) / float(int(alpha.data[1][0]) + int(alpha.data[1][1])))
            countersample += 1
            if int(alpha.data[1][0]) + int(alpha.data[1][1]) > 5:
                hethomocounter += 1
                if int(alpha.data[1][0]) > 2 and int(alpha.data[1][1]) > 2:
                    hets += 1
    except:
      continue
    if hethomocounter == 0: continue
    datasummer = datasummer * float(1.0 / float(countersample))
    maf = min([datasummer, 1.0 - datasummer])
    probhet = float(hets) / float(hethomocounter)



    package = [counter, probhet]


    if maf < 0.05:
        snps_base['0.0-0.05'].append(package)
        holderbase[recid] = [probhet, '0.0-0.05']
    if maf > 0.05 and maf <= 0.10:
        snps_base['0.05-0.10'].append(package)
        holderbase[recid] = [probhet, '0.05-0.10']
    if maf > 0.10 and maf <= 0.15:
        snps_base['0.10-0.15'].append(package)
        holderbase[recid] = [probhet, '0.10-0.15']
    if maf > 0.15 and maf <= 0.20:
        snps_base['0.15-0.20'].append(package)
        holderbase[recid] = [probhet, '0.15-0.20']
    if maf > 0.20 and maf <= 0.25:
        snps_base['0.20-0.25'].append(package)
        holderbase[recid] = [probhet, '0.20-0.25']
    if maf > 0.25 and maf <= 0.30:
        snps_base['0.25-0.30'].append(package)
        holderbase[recid] = [probhet, '0.25-0.30']        
    if maf > 0.30 and maf <= 0.35:
        snps_base['0.30-0.35'].append(package)
        holderbase[recid] = [probhet, '0.30-0.35'] 
    if maf > 0.35 and maf <= 0.40:
        snps_base['0.35-0.40'].append(package)
        holderbase[recid] = [probhet, '0.35-0.40'] 
    if maf > 0.40 and maf <= 0.45:
        snps_base['0.40-0.45'].append(package)
        holderbase[recid] = [probhet, '0.40-0.45'] 
    if maf > 0.45 and maf <= 0.50:
        snps_base['0.45-0.50'].append(package)
        holderbase[recid] = [probhet, '0.45-0.50'] 




normalizedaverage_dict = {}
finalrecords = []


accountfle = open('/data/wraycompute/vdp5/tmp/accounts.txt', 'a')
accountfle.write('passed dis shit')

for alpha in snps_base:
    lstbuild = []
    for beta in snps_base[alpha]:
        lstbuild.append(beta[1])
    normalizedaverage_dict[alpha] = numpy.mean(lstbuild)
print normalizedaverage_dict



newfle = open('/data/wraycompute/vdp5/tmp/holderdict.txt','w')

for alpha in holderbase:
    newfle.write('{}\t{}\t{}\n'.format(alpha, holderbase[alpha][0], holderbase[alpha][1]))

newfle.close()

newfle = open('/data/wraycompute/vdp5/tmp/normalizeddict.txt', 'w')

for beta in normalizedaverage_dict:
    newfle.write('{}\t{}\n'.format(beta, normalizedaverage_dict[beta]))

newfle.close()

os.system('sendmail virpatel3@gmail.com < "Boi shit written "')



vcf_reader = vcf.Reader(open(file, 'r'))

lstscores = []


counter = -1
for record in vcf_reader:
    counter += 1
    recid = '{}:{}-{}'.format(record.CHROM, record.start, record.end)
    procurehet = holderbase[recid]
    alpha = procurehet[-1]
    snpscore = 1
    for zeta in record.samples:
        datum = zeta.data
        if int(datum[1][0]) + int(datum[1][1]) < 5:
            abba = 5
        elif int(datum[1][0]) > 2 and int(datum[1][1]) > 2:
            snpscore *= normalizedaverage_dict[alpha]
        else:
            snpscore *= (1.0 - normalizedaverage_dict[alpha])
    print beta[0]
    snpscore = -1.0 * (1.0 / float(len(record.samples))) * numpy.log(snpscore)
    lstscores.append(snpscore)
    if snpscore < 0.5:
        vcf_writer.write_record(record)

    accountfle = open('/data/wraycompute/vdp5/tmp/accounts.txt', 'a')
    accountfle.write('{}\n'.format(counter))
    accountfle.close()



vcf_writer.close()

lstscores = sorted(lstscores)

zeta = range(1, len(lstscores) + 1)

plt.plot(zeta, lstscores)
plt.ylabel('Scores')
plt.xlabel('SNPs')
plt.title('Normalized Log Heterozygoizity Scores')
plt.xlim([0, len(zeta) + 1])
plt.savefig('/data/wraycompute/vdp5/variant_associated_data/normalized_heterorate.pdf')