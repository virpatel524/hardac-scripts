#!/bin/sh
#SBATCH --ntasks=4
#SBATCH --output=/data/wraycompute/vdp5/slurm_out/haplotype_developtest.txt
#SBATCH --mem-per-cpu=4000
module load R

#boi ive changed this to be harcode

rm -rf /home/vdp5/data/poptests/ldhat/${1}
mkdir -p /home/vdp5/data/poptests/ldhat/${1}
cd /home/vdp5/data/poptests/ldhat/${1}
echo "require(LDJump)" > /home/vdp5/data/poptests/ldhat/${1}/${1}_haplotypegenerate.R
echo "LDJump(\"/gpfs/fs0/data/wraycompute/vdp5/genetic_map/ldhat/transferpot/5iter_allvariants_filtered.rareremove.deploidcorrected.notrelevantremoved.nopirvirvariants.ann.vcf.LT635621.headeredited.fasta.10reduced.fasta.removedheader.fasta\", alpha = 0.05, segLength = 1000, pathLDhat = \"/gpfs/fs0/data/wraycompute/vdp5/src/LDhat/\", format = \"fasta\", refName = NULL, start = NULL, thth = 0.01, constant = F,accept= T)" >> /home/vdp5/data/poptests/ldhat/${1}/${1}_haplotypegenerate.R

R CMD BATCH /home/vdp5/data/poptests/ldhat/${1}/${1}_haplotypegenerate.R

source ~/.bash_profile
emailme "donza ldjump"