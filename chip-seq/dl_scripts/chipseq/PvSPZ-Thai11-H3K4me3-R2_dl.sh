#!/bin/bash
#SBATCH --job-name=launchstuff
#SBATCH --ntasks=1
#SBATCH --mem=6G
#SBATCH --mail-user=vdp5@duke.edu
#SBATCH --output=test.tmp
SCRATCH=/data/wraycompute/vdp5/scratch/$SLURM_JOB_ID
source ~/.bash_profile
cd /data/wraycompute/vdp5/chip-seq
fastq-dump.2 --gzip SRR5298129
rename SRR5298129 PvSPZ-Thai11-H3K4me3-R2 *