import csv
import argparse
import sys
import os

sys.path.append(os.getcwd())
parser = argparse.ArgumentParser()
parser.add_argument('--coordfile', help="coordinates")
parser.add_argument('--filetoparse', help='which file you parsing')
parser.add_argument('--output', help='output file')
args = parser.parse_args()


coords = list(csv.reader(open(args.coordfile),delimiter='\t'))


logfile = open('/home/vdp5/data/tmp/logfile_tajima.txt', 'a')


start = coords[0]
end = coords[-1]


base = args.filetoparse.split('/')[-1].split('.')[0]





data="""
library('PopGenome')
GENOME.class <- readVCF("{}", 200000, "{}", {}, {})
GENOME.class <- neutrality.stats(GENOME.class)
tajima <- GENOME.class@Tajima.D
output <- paste('{}', '\t', tajima[1],sep="")
write(output, "{}")

""".format(args.filetoparse, start[0], int(start[1]) - 100, int(end[1]) + 100, base, '/home/vdp5/data/filtered_7.18.17/popgenome/indiv_values/{}_tajima.txt'.format(base))




logfile.write(data + '\n')
logfile.close()



newfle = open('/data/wraycompute/vdp5/tmp/rscripts/{}_rscript.R'.format(base), 'w')


print '/data/wraycompute/vdp5/tmp/rscripts/{}_rscript.R'.format(base)


newfle.write(data)
newfle.close()





