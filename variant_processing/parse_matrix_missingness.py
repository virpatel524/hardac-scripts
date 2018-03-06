#!/data/wraycompute/vdp5/bin/bin/python2.7
#
# SBATCH --ntasks=1
# SBATCH --mem=8G
# SBATCH --output=/data/wraycompute/vdp5/slurm_out/vcfedit.out

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pylab
import csv
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('--samplelst', help='sample list')
args = parser.parse_args()


heta = ['SNP_LIST', ]


samples = list(csv.reader(open(args.samplelst), delimiter='\t'))
samples = [a[0] for a in samples]

samples = heta + samples

data = list(csv.reader(open(
    '/gpfs/fs0/data/wraycompute/vdp5/variant_associated_data/variant_count_data.txt'), delimiter='\t'))


data = [samples, ] + data


totalnum_called_dict = {}
snptots = []

for alpha in data[1:]:
    snp = alpha[0]
    rest = alpha[1:]
    rest = [float(a) for a in rest]
    rest = sum(rest)
    totalnum_called_dict[snp] = rest
    snptots.append(rest)

os.system('echo "3"')


snptots = sorted(snptots)
sample_snps = map(list, zip(*data))
sample_snps_ordered = sample_snps[1:]

totalsampcallrate = {}
samptots = []

for beta in sample_snps_ordered:
    samp = beta[0]
    rest = beta[1:]
    rest = [float(a) for a in rest]
    rest = sum(rest)
    totalsampcallrate[samp] = rest
    samptots.append(rest)

samptots = sorted(samptots)


print 'step 4'

zeta = range(1, len(snptots) + 1)

plt.plot(zeta, snptots)
plt.ylabel('Number of Samples')
plt.xlabel('SNPs')
plt.title('SNP Call Rate Across All Samples')
plt.xlim([0, len(zeta) + 1])
plt.savefig('/data/wraycompute/vdp5/variant_associated_data/snpcallrate.pdf')

plt.close()


zeta = range(1, len(samptots) + 1)

plt.plot(zeta, samptots)
plt.ylabel('Number of SNPs')
plt.xlabel('Sample Order')
plt.title('Sample Call Rate Across All SNPs')
plt.xlim([0, len(zeta) + 1])
plt.savefig('/data/wraycompute/vdp5/variant_associated_data/sampcallrate.pdf')

plt.close()

badsamples = []

for alpha in totalsampcallrate:
    if totalsampcallrate[alpha] < 350000:
        badsamples.append(alpha)


print totalsampcallrate


newfle = open(
    '/gpfs/fs0/data/wraycompute/vdp5/variant_associated_data/lowcallrate_needtoremove.list', 'w')


for alpha in badsamples:
    newfle.write(alpha + '\n')

newfle.close()
