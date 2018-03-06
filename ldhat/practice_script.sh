#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --mem=10G
#SBATCH --output=/data/wraycompute/vdp5/slurm_out/ldhattesting.out

source ~/.bash_profile

pairwise -seq /gpfs/fs0/data/wraycompute/vdp5/genetic_map/ldhat/transferpot/5iter_allvariants_filtered.rareremove.deploidcorrected.notrelevantremoved.nopirvirvariants.ann.vcf.LT635621.sites.txt -loc /gpfs/fs0/data/wraycompute/vdp5/genetic_map/ldhat/transferpot/5iter_allvariants_filtered.rareremove.deploidcorrected.notrelevantremoved.nopirvirvariants.ann.vcf.LT635621.locs.txt --prefix /gpfs/fs0/data/wraycompute/vdp5/genetic_map/ldhat/transferpot/5iter_allvariants_filtered.rareremove.deploidcorrected.notrelevantremoved.nopirvirvariants.ann.vcf.LT635621.output -lk /gpfs/fs0/data/wraycompute/vdp5/genetic_map/lkset/outputs/10indiv_lk_n50_t0.001new_lk.txt 

emailme "donza"