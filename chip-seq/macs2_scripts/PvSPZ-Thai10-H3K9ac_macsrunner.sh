#!/bin/env bash

#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --output=/data/wraycompute/vdp5/slurm_out/PvSPZ-Thai10-H3K9ac_macs.out

module load gcc
module load R

macs2 callpeak -t /gpfs/fs0/data/wraycompute/vdp5/bam/PvSPZ-Thai10-H3K9ac.bam -c /gpfs/fs0/data/wraycompute/vdp5/bam/PvSPZ-Thai10-Input.bam -f BAMPE -g 2.88e7 -B -q 0.01 --broad -n PvSPZ-Thai10-H3K9ac --outdir /home/vdp5/data/chip-seq/macs2_output/PvSPZ-Thai10-H3K9ac