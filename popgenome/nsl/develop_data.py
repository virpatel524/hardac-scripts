import os
import csv
import argparse
import sys
import operator, math
import shutil


parser = argparse.ArgumentParser()
parser.add_argument('--directory', help="what directory to search")
parser.add_argument('--sample', help="sample")


args = parser.parse_args()

datatotal = []


for filename in os.listdir(args.directory):
	if '100bins.norm' in filename:
		data = list(csv.reader(open(os.path.join(args.directory, filename)),delimiter='\t'))
		chrom = filename.split('_')[0][3:]
		for it in data:

			datatotal.append([chrom, int(it[1]), abs(float(it[-2]))])

toppercentile = int(0.01 * len(datatotal))

sorted_datatotal = sorted(datatotal,key=operator.itemgetter(2), reverse=True)



tops = sorted_datatotal[:toppercentile + 1]


if not os.path.isdir('/home/vdp5/data/poptests/nsl/output/{}'.format(args.sample)):
	os.mkdir('/home/vdp5/data/poptests/nsl/output/{}'.format(args.sample))
else:
	shutil.rmtree('/home/vdp5/data/poptests/nsl/output/{}'.format(args.sample))
	os.mkdir('/home/vdp5/data/poptests/nsl/output/{}'.format(args.sample))

if not os.path.isdir('/home/vdp5/data/poptests/nsl/output/{}/txtfiles/'.format(args.sample)):
	os.mkdir('/home/vdp5/data/poptests/nsl/output/{}/txtfiles/'.format(args.sample))


newfle = open('/home/vdp5/data/poptests/nsl/output/{}/txtfiles/toplst.txt'.format(args.sample), 'w')


masterfle = open('/home/vdp5/data/poptests/nsl/output/{}/txtfiles/toplst-fullinfo.txt'.format(args.sample), 'w')

for beta in tops:
	newfle.write('{}\t{}\n'.format(beta[0], beta[1]))

masterfle.write('snp\tbp\tchrom\tpvalue\n')

for item in sorted_datatotal:
	masterfle.write('{}_{}\t{}\t{}\t{}\n'.format(item[0], item[1], item[1], item[0], item[2]))



newfle.close()
masterfle.close()