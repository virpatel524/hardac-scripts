#script to identify top 6 closest relatives and then create a script that will allow for the selection process to take place

import os
import csv

for filename in os.listdir('/home/vdp5/data/poptests/hmmidb/'):
    if filename.endswith(".txt") or filename.endswith(".py"): 
       	hellur = os.path.join(directory, filename)
       	data = list(csv.reader(open(hellur),delimiter='\t'))
       	base = filename.split('.')[-2]
       	starterdict = {}
       	whoisstarter  = ''
       	partners = []
       	for beta in data[1:]:
       		if whoisstarter != beta[0]:
       			whoisstarter = beta[0]
       			partners = []
       		if len(partners < 5):
       			partners.append([])
       			