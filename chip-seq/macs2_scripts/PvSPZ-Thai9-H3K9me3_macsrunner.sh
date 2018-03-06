#!/bin/env bash

#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --output=/data/wraycompute/vdp5/slurm_out/PvSPZ-Thai9-H3K9me3_macs.out

module load gcc
module load R

macs2 callpeak -t /gpfs/fs0/data/wraycompute/vdp5/bam/PvSPZ-Thai9-H3K9me3.bam -c /gpfs/fs0/data/wraycompute/vdp5/bam/PvSPZ-Thai9-Input.bam -f BAMPE -g 2.88e7 -B -q 0.01 --broad -n PvSPZ-Thai9-H3K9me3 --outdir /home/vdp5/data/chip-seq/macs2_output/PvSPZ-Thai9-H3K9me3