#!/bin/env bash

#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --output=/data/wraycompute/vdp5/slurm_out/macs.out

module load gcc
module load R

macs2 callpeak -t /gpfs/fs0/data/wraycompute/vdp5/bam/PvSPZ-Thai10-H3K9me3-R1.bam -c /gpfs/fs0/data/wraycompute/vdp5/chip-seq/chipseq_combined/PvSPZ-Thai10-Input_combined.bam -f BAM -g 2.88e7 -B -q 0.01