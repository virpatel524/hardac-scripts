#!/bin/bash
#SBATCH --job-name=launchstuff
#SBATCH --ntasks=1
#SBATCH --mem=6G
#SBATCH --mail-user=vdp5@duke.edu
#SBATCH --output=test.tmp
SCRATCH=/data/wraycompute/vdp5/scratch/$SLURM_JOB_ID
source ~/.bash_profile
cd /data/wraycompute/vdp5/chip-seq
fastq-dump.2 --gzip SRR5298170
rename SRR5298170 PvSPZ-Thai10-Input-R2 *