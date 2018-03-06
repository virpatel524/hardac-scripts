import os
import csv 
import sys


sampleswewant = list(csv.reader(open('/gpfs/fs0/data/wraycompute/vdp5/empty-scratch/fasta_alignemnts/samples_representative.txt'),delimiter='\t'))

sampleswewant = [a[0] for a in sampleswewant]

for beta in os.listdir('/home/vdp5/data/empty-scratch/fasta_alignemnts/fastas_real'):
	name = os.path.join('/home/vdp5/data/empty-scratch/fasta_alignemnts/fastas_real', beta)
	newname = '.'.join(name.split('.')[:-1] + ['selectedsamples',] + ['fasta'])
	newfle = open(newname, 'w')
	holden = list(csv.reader(open(name),delimiter='\t'))
	seta = False

	for link in holden:
		sampy = ''

		if link[0][0] == '>':
			for simmi in sampleswewant:
				if simmi in link[0][1:]:
					seta = True
					newfle.write(link[0] + '\n')
					break
				else:
					seta = False

			
		if link[0][0] != '>' and seta == True:
			newfle.write(link[0] + '\n')

	newfle.close()
