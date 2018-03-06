#!/nfs/software/helmod/apps/Core/R_core/3.4.2-fasrc01/bin/R
#
#SBATCH --job-name=test
#SBATCH --ntasks=1
#SBATCH --mem=16G
#SBATCH --mail-user=vdp5@duke.edu
#SBATCH -o /home/vdp5/slurm_out/R_script.txt
#SBATCH --mail-type=ALL


library('LDJump')

LDJump("/gpfs/fs0/data/wraycompute/vdp5/empty-scratch/fasta_alignemnts/5iter_allvariants_filtered.rareremove.deploidcorrected.notrelevantremoved.nopirvirvariants.ann.vcf.LT635625.fasta", alpha = 0.05, segLength = 1000, pathLDhat = "/home/vdp5/src/LDhat/", format = "fasta", refName = NULL, start = NULL, thth = 0.005, constant = F, rescale = F, status = T, polyThres = 0)