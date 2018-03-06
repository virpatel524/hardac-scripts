import os
import csv
import sys
import argparse
import subprocess


holder="""#!/bin/bash
#
#SBATCH --job-name=test
#SBATCH --ntasks=1
#SBATCH --mem=8G
#SBATCH --mail-user=vdp5@duke.edu
#SBATCH -o /home/vdp5/slurm_out/{}_jobout.txt
SCRATCH=/data/wraycompute/vdp5/scratch/$SLURM_JOB_ID
source /gpfs/fs0/home/vdp5/.bash_profile
mkdir -p $SCRATCH
cd $SCRATCH
source ~/.bash_profile
module load jdk/1.8.0_45-fasrc01


module load R

{}

freallove=$(realpath /home/vdp5/data/bam/{}.bam)
filenombre=$(basename $freallove)
IFS='.' read -ra ADDR <<< $filenombre
base=$ADDR[0]
ref=/gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.fasta


# necessary step for downstream processing. The validation stringency is necessary for malaria since its genome is full of contigs
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/picard.jar AddOrReplaceReadGroups INPUT=$freallove OUTPUT=readgroups.bam RGID=1 RGLB=$base RGPL=illumina RGPU=unit1 RGSM=$base  VALIDATION_STRINGENCY=LENIENT

# this step is necessary for GATK, but note that it is NOT for tools like freebayes since they do their own duplicates processing.
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/picard.jar MarkDuplicates INPUT=readgroups.bam OUTPUT=dedup_reads.bam METRICS_FILE=metrics.txt  VALIDATION_STRINGENCY=LENIENT
rm -rf readgroups.bam
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/picard.jar BuildBamIndex INPUT=dedup_reads.bam  VALIDATION_STRINGENCY=LENIENT

# initial variant processing, using 4 cores. Note that we call full variants here, not the GVCF (which is what we want as the final output)
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T HaplotypeCaller -R $ref -I dedup_reads.bam -o raw_variants.vcf -nct 4


# we split up the variant types since SNPs and indels need different processing
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T SelectVariants -R $ref -V raw_variants.vcf -selectType SNP -o raw_snps.vcf
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T SelectVariants -R $ref -V raw_variants.vcf -selectType INDEL -o raw_indels.vcf
rm -rf raw_variants.vcf

#basic filters
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T VariantFiltration -R $ref -V raw_snps.vcf --filterExpression 'QD < 2.0 || FS > 60.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0 || SOR > 4.0' --filterName "basic_snp_filter" -o filtered_snps.vcf
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T VariantFiltration -R $ref -V raw_indels.vcf --filterExpression 'QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0 || SOR > 10.0' --filterName "basic_indel_filter" -o filtered_indels.vcf

# Here is our first recalibration step. We use the hard filtered SNPs set as the training set. It's not an issue that this set isn't totally accurate because we're going to do more rounds of processing later.
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T BaseRecalibrator -R $ref -I dedup_reads.bam -knownSites filtered_snps.vcf -knownSites filtered_indels.vcf -o recal_data.table
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T PrintReads -R $ref -I dedup_reads.bam -BQSR recal_data.table -o recal_reads.bam

# we call the second set here using the recalculated reads (variants2)
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T HaplotypeCaller -nct 4 -R $ref -I recal_reads.bam -o raw_variants2.vcf

#some cleanup
rm -rf *.idx raw_snps.vf raw_indels.vcf recal_reads.bam recal_data.table post_recal_data.table filtered_snps.vcf filtered_indels.vcf


java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T SelectVariants -R $ref -V raw_variants2.vcf -selectType SNP -o raw_snps.vcf
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T SelectVariants -R $ref -V raw_variants2.vcf -selectType INDEL -o raw_indels.vcf
rm -rf raw_variants2.vcf


java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T VariantFiltration -R $ref -V raw_snps.vcf --filterExpression 'QD < 2.0 || FS > 60.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0 || SOR > 4.0' --filterName "basic_snp_filter" -o filtered_snps.vcf
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T VariantFiltration -R $ref -V raw_indels.vcf --filterExpression 'QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0 || SOR > 10.0' --filterName "basic_indel_filter" -o filtered_indels.vcf

# really important to note that we use the dedup_reads file here as the input, not the printed reads from the last step. I have not tested what would happen if we used the recalculated reads here instead, but none of the guides I read seemed to do so.
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T BaseRecalibrator -R $ref -I dedup_reads.bam  -knownSites filtered_snps.vcf -knownSites filtered_indels.vcf -o recal_data.table
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T PrintReads -R $ref -I dedup_reads.bam -BQSR recal_data.table -o recal_reads.bam

# round 3
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T HaplotypeCaller -nct 4 -R $ref -I recal_reads.bam -o raw_variants3.vcf

java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T SelectVariants -R $ref -V raw_variants3.vcf -selectType SNP -o raw_snps.vcf
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T SelectVariants -R $ref -V raw_variants3.vcf -selectType INDEL -o raw_indels.vcf
rm -rf raw_variants3.vcf
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T VariantFiltration -R $ref -V raw_snps.vcf --filterExpression 'QD < 2.0 || FS > 60.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0 || SOR > 4.0' --filterName "basic_snp_filter" -o filtered_snps.vcf
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T VariantFiltration -R $ref -V raw_indels.vcf --filterExpression 'QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0 || SOR > 10.0' --filterName "basic_indel_filter" -o filtered_indels.vcf
# really important to note that we use the dedup_reads file here as the input, not the printed reads from the last step. I have not tested what would happen if we used the recalculated reads here instead, but none of the guides I read seemed to do so.
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T BaseRecalibrator -R $ref -I dedup_reads.bam  -knownSites filtered_snps.vcf -knownSites filtered_indels.vcf -o recal_data.table
java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T PrintReads -R $ref -I dedup_reads.bam -BQSR recal_data.table -o recal_reads.bam


java -jar -Xmx7g /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T HaplotypeCaller -nct 4 -R $ref -I recal_reads.bam --emitRefConfidence GVCF -o /gpfs/fs0/data/wraycompute/vdp5/gvcf/$base.g.vcf
rm -rf $SCRATCH

"""



parser = argparse.ArgumentParser()
parser.add_argument('--directory', help="Where the FASTQ GZ are held")
args = parser.parse_args()

samples = []

for alpha in os.listdir(args.directory):
	samples.append(alpha.split('.')[0][:-2])



# for alpha in os.listdir('/home/vdp5/data/gvcf/'):
# 	samp = alpha.split('.')[0]
# 	if samp in 
# 	samples.remove(samp)


commands = []

for theta in samples:
	newstr = 'srun --mem=8G bwa mem -M -t 4 -v 2 -A 2 -L 15 -U 9 -T 75 -k 19 -w 100 -d 100 -r 1.5 -c 10000 -B 4 -O 6 -E 1 {} {} | samtools view  -Sb - | samtools sort - -o /home/vdp5/data/bam/{}.bam'.format('/gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.fasta',os.path.join(args.directory , theta + '_1.fastq.gz'), theta)
	newfle = open('/tmp/{}_variant.sh'.format(theta), 'w')
	newfle.write(holder.format(theta, newstr, theta))
	newfle.close()
	commands.append('/tmp/{}_variant.sh'.format(theta))

outputfle = open('/tmp/launcher.sh', 'w')

for beta in commands:
	outputfle.write('sbatch --mem=8G {}\n'.format(beta))


outputfle.close()








