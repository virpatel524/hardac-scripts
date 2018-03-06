# spits out the samples which feature only one haplotype so that we can select a) for the samples which can be included in our analysis and b) correct samples when they feature heterozygote calls

import vcf
import os 
import csv
import numpy as np


goodies = []
for filename in os.listdir('/home/vdp5/data/variant_staging/deploid/deploidout'):
    if filename.endswith(".prop"):
    	name = open(os.path.join('/home/vdp5/data/variant_staging/deploid/deploidout', filename))
    	samp = filename.split('.')[0]
        data = list(csv.reader(name,delimiter='\t'))
        data = map(list, zip(*data))
        for index, alpha in enumerate(data):
        	si = [float(a) for a in alpha]
        	if np.mean(si) > 0.70:
        		goodies.append([samp,index])



fle = open('/gpfs/fs0/data/wraycompute/vdp5/variant_associated_data/MOI1_11.22.17.txt', 'w')
fle2 = open('/gpfs/fs0/data/wraycompute/vdp5/variant_associated_data/MOI1_11.22.17_withindexhap.txt', 'w')


for alpha in goodies:
    print alpha
    if 'BR' in alpha:
        continue
    fle2.write('{}\t{}\n'.format(alpha[0], alpha[1]))
    fle.write('{}\n'.format(alpha[0]))

fle2.close()
