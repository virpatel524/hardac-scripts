#!/bin/env bash

#SBATCH --ntasks=1
#SBATCH --mem=16G
#SBATCH --output=/data/wraycompute/vdp5/slurm_out/openuphaplo

source ~/.bash_profile

sample=${1}
vcfsamp=${2}
vcftotal=${3}

module load java/1.8.0_45-fasrc01



mkdir -p /home/vdp5/data/poptests/nsl/output/${1}/txtfiles/
mkdir -p /home/vdp5/data/poptests/nsl/input/${1}/splitted/
base=$(basename ${2})

cp ${2} /home/vdp5/data/poptests/nsl/input/${1}/splitted/${base}
java -jar /gpfs/fs0/data/wraycompute/vdp5/src/snpEff/SnpSift.jar split /home/vdp5/data/poptests/nsl/input/${1}/splitted/${base}
rm -rf /home/vdp5/data/poptests/nsl/input/${1}/splitted/${base}



# python2.7 /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/convert_nsl_format_step1.py --vcfdir /home/vdp5/data/poptests/nsl/input/${1}/splitted/ --sample ${1}
# rm -rf /home/vdp5/data/poptests/nsl/input/${1}/splitted/
# bash /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/launch_nsl.sh ${1}
python2.7 /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/develop_data.py --directory /gpfs/fs0/data/wraycompute/vdp5/poptests/nsl/input/${sample}/ --sample ${1} --mastervcf ${3}
sbatch /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/rangelaunch.py --sample ${sample} --mastervcf ${vcftotal} --range 2000
sbatch /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/rangelaunch.py --sample ${sample} --mastervcf ${vcftotal} --range 1000
sbatch /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/rangelaunch.py --sample ${sample} --mastervcf ${vcftotal} --range 5000
sbatch /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/rangelaunch.py --sample ${sample} --mastervcf ${vcftotal} --range 10000
sbatch /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/rangelaunch.py --sample ${sample} --mastervcf ${vcftotal} --range 20000

# python2.7 /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/make_better_consolidation.py --sample ${sample}
