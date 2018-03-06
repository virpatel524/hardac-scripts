data='''
#!/bin/bash
#
#SBATCH --job-name=test
#SBATCH --ntasks=1
#SBATCH --mem=20G
#SBATCH --mail-user=vdp5@duke.edu
#SBATCH -o /home/vdp5/slurm_out/jobout.txt
SCRATCH=/data/wraycompute/vdp5/scratch/$SLURM_JOB_ID
source /gpfs/fs0/home/vdp5/.bash_profile
mkdir -p $SCRATCH
cd $SCRATCH

# Notice that this is for PVP01
module load jdk/1.8.0_45-fasrc01

java -jar -Xmx18g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T GenotypeGVCFs -R /gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.fasta -V /gpfs/fs0/data/wraycompute/vdp5/variants_out_gvcf/BB012.g.vcf {} -o /data/wraycompute/vdp5/variants_out/all_variants_out.vc

'''

stringout = ''
import os
for filename in os.listdir("/data/wraycompute/vdp5/variants_out_gvcf"):
	newpath = os.path.join('/data/wraycompute/vdp5/variants_out_gvcf', filename)
	if '.idx' not in newpath:
		stringout += '-V {} '.format(newpath)

newfle = open('/gpfs/fs0/data/wraycompute/vdp5/slurm_scripts/call_GenotypeGVCFs_batch.sh', 'w')

newfle.write(data.format(stringout))
newfle.close()
		



