import os 
import argparse
import sys
import csv
from subprocess import Popen, PIPE
import time


parser = argparse.ArgumentParser()
parser.add_argument('--out', help="VCF file for use")
args = parser.parse_args()

fle = args.out

data = list(csv.reader(open(args.out),delimiter='\t'))

joblst = []
runninglst = []

for alpha in data:
	joblst.append(alpha[0].split(' ')[-1])

purnpike = True 

counter = 0
while(purnpike):
	counter += 1
	(stdout, stderr) = Popen(["echo", "HI"], stdout=PIPE).communicate()
	purnpike = False
	time.sleep(5)
	(stdout, stderr) = Popen(["squeue", '-u', "vdp5"], stdout=PIPE).communicate()
	for alpha in stdout.split(' '):
		if len(alpha) >= 7:
			runninglst.append(alpha)
	for beta in joblst:
		if beta in runninglst:
			purnpike = True

	runninglst = []

