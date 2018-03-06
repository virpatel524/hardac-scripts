#!/bin/bash
#
#SBATCH --job-name=test
#SBATCH --ntasks=1
#SBATCH --mem=10G
#SBATCH --mail-user=vdp5@duke.edu

module load gcc
module load R
cd /home/vdp5/data/src/DEploid/
utilities/dataExplore.r -vcf /home/vdp5/data/variant_staging/indiv_samples_deploid_11.20.17/${1}_alone.vcf -o /home/vdp5/data/variant_staging/deploid/outliers/${1}_outliers_ -plaf /home/vdp5/data/variant_staging/deploid/plafs/${1}_scenariominor_plaf.txt
dEploid -vcf /home/vdp5/data/variant_staging/indiv_samples_deploid_11.20.17/${1}_alone.vcf -o /home/vdp5/data/variant_staging/deploid/deploidout/${1} -plaf /home/vdp5/data/variant_staging/deploid/plafs/${1}_scenariominor_plaf.txt -noPanel  -exclude /home/vdp5/data/variant_staging/deploid/outliers/${1}_outliers_PotentialOutliers.txt
