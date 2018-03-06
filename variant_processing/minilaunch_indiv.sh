#!/bin/bash
#
#SBATCH --job-name=test
#SBATCH --ntasks=1
#SBATCH --mem=5G
#SBATCH --mail-user=vdp5@duke.edu
#SBATCH -o /home/vdp5/slurm_out/hiya.txt
#SBATCH --mail-type=ALL
source /gpfs/fs0/home/vdp5/.bash_profile

module load java/1.8.0_45-fasrc01
java -Xmx4800m -jar /gpfs/fs0/data/wraycompute/vdp5/src/GenomeAnalysisTK.jar -T SelectVariants -sn $1 -V /home/vdp5/data/variant_staging/indiv_samples_deploid/$1_refined.vcf  -R /gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.fasta -o /home/vdp5/data/variant_staging/indiv_samples_deploid/$1_alone.vcf