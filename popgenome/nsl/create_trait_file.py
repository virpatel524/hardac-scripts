import os 
import csv
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--tabfile', help="tab file")
parser.add_argument('--chrom', help="chromosomes")
parser.add_argument('--locus', help="locus")
parser.add_argument('--sample', help="sample")
parser.add_argument('--range', help="range")


args = parser.parse_args()

popfile = list(csv.reader(open('/gpfs/fs0/data/wraycompute/vdp5/txt_files/popfiles/haplostyles_-VCF1-2.0_columnadded.txt'),delimiter='\t'))
tabdata = list(csv.reader(open(args.tabfile),delimiter='\t'))
samples = tabdata[0][3:]
storage = []
ancestral = ''


for beta in tabdata[1:]:
	if beta[1] == args.locus and beta[0] == args.chrom:
		storage = beta[3:]
		ancestral = beta[2]
		break


newfle = open('/home/vdp5/data/tmp/sampleitems_{}_{}.list'.format(args.range, args.sample), 'w')
goodsamps = []

for index, beta in enumerate(storage):
	if beta != './.':
		goodsamps.append(samples[index])
		newfle.write(samples[index] + '\n')

newfle.close()

print(len(goodsamps))
tabfilestr = args.tabfile
popout = '.'.join(tabfilestr.split('.')[:-1] + ['nonmissing', 'popargs'])
traitout = '.'.join(tabfilestr.split('.')[:-1] + ['nonmissing', 'traits'])

newfle = open(popout, 'w')

popmatrix = {}

samplst = []


for beta in popfile:
	popmatrix[beta[0]] = beta[-1]
	if beta[-1] not in samplst:
		samplst.append(beta[-1])

samplst = sorted(samplst)

newfle.write('\t{}\n'.format('\t'.join(samplst)))

key = sorted(goodsamps)

for beta in key:
	writer = [beta,]
	for alpha in samplst:
		if popmatrix[beta] == alpha:
			writer.append('1')
		else:
			writer.append('0')
	newfle.write('{}\n'.format('\t'.join(writer)))

newfle.close()

newfle = open(traitout, 'w')

newfle.write('\tANCESTRAL\tDERIVED\n')

anc = 0
der = 0
print 
print len(goodsamps)
for index, beta in enumerate(storage):
	if samples[index] not in goodsamps: continue
	writer = [samples[index],]
	if beta[0] == ancestral:
		writer = writer + ["1", "0"]
		anc += 1
	else:
		writer = writer + ["0", "1"]
		der += 1

	newfle.write('{}\n'.format('\t'.join(writer)))

forme = open('/home/vdp5/data/poptests/nsl/output/{}/txtfiles/percentages_ans-vs-derived.{}.txt'.format(args.sample, args.range), 'a')


print anc, der
calc = float(der) / (float(anc) + float(der))


forme.write('{}-{}\t{}\n'.format(args.chrom, args.locus, calc))


newfle.close()
