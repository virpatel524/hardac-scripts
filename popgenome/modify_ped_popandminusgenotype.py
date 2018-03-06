import csv
import os
import re
import sys

csv.field_size_limit(sys.maxsize)


base = list(csv.reader(open('/gpfs/fs0/data/wraycompute/vdp5/filtered_7.18.17/5iter_allvariants_filtered.heteroremove.rareremove.noheteroconsid.samps'),delimiter='\t'))

sampdict = {}


for alpha in base:
	if '_' in alpha[0]:
		tmp = alpha[0].split('_')
		samp = tmp[0].upper()
		sampdict[alpha[0]] = samp
		continue
	match = re.match(r"([a-z]+)([0-9]+)", alpha[0], re.I)
	if match:
		items = match.groups()
		samp = items[0]
		if samp == 'BB' or samp == 'KP' or samp == 'OM':
			samp = 'CAMBODIA'
		sampdict[alpha[0]] = samp

ped = list(csv.reader(open('/gpfs/fs0/data/wraycompute/vdp5/filtered_7.18.17/5iter_allvariants_filtered.heteroremove.rareremove.noheteroconsid.ped'),delimiter='\t'))
newped = open('/gpfs/fs0/data/wraycompute/vdp5/filtered_7.18.17/5iter_allvariants_filtered.heteroremove.rareremove.noheteroconsid.edited.ped', 'w')

for index, alpha in enumerate(ped):
	newstuff = ped[0][0].split(' ')
	newstuff[0] = sampdict[base[index][0]]
	newstuff[1] = base[index][0]
	newstuff[4] = '2'
	newstuff[5] = '0'
	newstuff = '\t'.join(newstuff)
	newped.write(newstuff + '\n')

newped.close()

mapfile = list(csv.reader(open('/gpfs/fs0/data/wraycompute/vdp5/filtered_7.18.17/5iter_allvariants_filtered.heteroremove.rareremove.noheteroconsid.map'),delimiter='\t'))
newmap = open('/gpfs/fs0/data/wraycompute/vdp5/filtered_7.18.17/5iter_allvariants_filtered.heteroremove.rareremove.noheteroconsid.edited.map', 'w')
for alpha in mapfile:
	alpha[1] = '{}_{}'.format(alpha[0], alpha[-1])
	newmap.write('{}\n'.format('\t'.join(alpha)))

newmap.close()