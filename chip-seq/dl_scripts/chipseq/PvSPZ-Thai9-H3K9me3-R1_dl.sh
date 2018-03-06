#!/bin/bash
#SBATCH --job-name=launchstuff
#SBATCH --ntasks=1
#SBATCH --mem=6G
#SBATCH --mail-user=vdp5@duke.edu
#SBATCH --output=test.tmp
SCRATCH=/data/wraycompute/vdp5/scratch/$SLURM_JOB_ID
source ~/.bash_profile
cd /data/wraycompute/vdp5/chip-seq
fastq-dump.2 --gzip SRR5298147
rename SRR5298147 PvSPZ-Thai9-H3K9me3-R1 *