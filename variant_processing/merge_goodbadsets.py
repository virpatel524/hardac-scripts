import os
import csv


datagood = list(csv.reader(open(
    '/gpfs/fs0/data/wraycompute/vdp5/variant_associated_data/lowcallrate_removed_samples.list'), delimiter='\t'))
databad = list(csv.reader(open(
    '/gpfs/fs0/data/wraycompute/vdp5/variant_associated_data/multiplicity_clear.txt'), delimiter='\t'))


datagood = [a[0] for a in datagood]
databad = [a[0] for a in databad]


finset = []


for alpha in datagood:
    if alpha not in databad:
        finset.append(alpha)


print len(finset)
