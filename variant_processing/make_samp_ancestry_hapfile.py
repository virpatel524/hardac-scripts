import os
import csv
import vcf


vcf_reader = vcf.Reader(open('/gpfs/fs0/data/wraycompute/vdp5/filtered_7.18.17/5iter_allvariants_filtered.rareremove.deploidcorrected.notrelevantremoved.chromcorrected.ann.vcf', 'r'))

