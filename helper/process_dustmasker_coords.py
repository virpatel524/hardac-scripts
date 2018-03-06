import csv 


data = list(csv.reader(open('/gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.dustmasker'),delimiter='\t'))
new_data = open('/gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.dustmasker.list', 'w')

chrom = ''

for alpha in data:
	tmp = alpha[0]
	if tmp[0] == '>':
		chrom = tmp[1:]
	else:
		zeta = alpha[0].split(' ')
		print zeta[-1]
		new_data.write('{}:{}-{}\n'.format(chrom, zeta[0], zeta[-1]))


new_data.close()