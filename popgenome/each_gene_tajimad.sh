#!/bin/env bash

#SBATCH --ntasks=1
#SBATCH --mem=10G


source ~/.bash_profile
mkdir /home/vdp5/tmp/rscripts

rm -rf /home/vdp5/data/filtered_7.18.17/popgenome/tajima_allgenome.txt

for alpha in ./*.gz; do
	base=$(basename ${alpha})
	bash /gpfs/fs0/data/wraycompute/vdp5/slurm_scripts/popgenome/launchtajima_popgenome.sh ${alpha}
done


