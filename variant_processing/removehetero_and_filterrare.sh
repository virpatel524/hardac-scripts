#!/bin/env bash

#SBATCH --ntasks=1
#SBATCH --mem=30G
#SBATCH --output=/data/wraycompute/vdp5/slurm_out/vcfedit_master.out

source ~/.bash_profile
module load java

vcffile=/data/wraycompute/vdp5/filtered_7.18.17/5iter_allvariants_filtered.vcf
restargs=/data/wraycompute/vdp5/scripts/vcf_editing.py
outputfile=/data/wraycompute/vdp5/filtered_7.18.17/5iter_allvariants_filtered.heteroremove.rareremove.vcf
heterozygotes=/data/wraycompute/vdp5/variant_associated_data/multiplicity_clear.list

now=`date +"%m_%d_%Y"`

tmpdir=/data/wraycompute/vdp5/tmp/splitvcf_${now}
mkdir -p ${tmpdir}


ln -s $vcffile ${tmpdir}/heteroremoved_${now}_withhetero.vcf
gatk -T SelectVariants -R $DATADIR/reference_data/PVP01.fasta  -xl_sf $heterozygotes -V ${tmpdir}/heteroremoved_${now}_withhetero.vcf -o ${tmpdir}/heteroremoved_${now}.vcf -XL /gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.dustmasker.bed
rm -rf ${tmpdir}/heteroremoved_${now}_withhetero.vcf

holdvcf=${tmpdir}/heteroremoved_${now}.vcf
outputtmpdir=/data/wraycompute/vdp5/tmp/splitout_${now}
mkdir -p ${outputtmpdir}

basevcf=$(basename $vcffile)

ln -s $holdvcf $tmpdir/${basevcf}.heteroremove.vcf
holdvcf=$tmpdir/${basevcf}.heteroremove.vcf

cd $tmpdir

java -jar -Xmx9800m /gpfs/fs0/data/wraycompute/vdp5/src/snpEff/SnpSift.jar split $holdvcf


rm -rf $holdvcf
rm -rf ${tmpdir}/heteroremoved_${now}.vcf
rm -rf /data/wraycompute/vdp5/variant_associated_data/variant_count_data.txt
touch /data/wraycompute/vdp5/variant_associated_data/variant_count_data.txt
rm -rf ${tmpdir}/*.idx


for alpha in ${tmpdir}/*.vcf; do
	sbatch ${restargs} --vcffile ${alpha} --outdir ${outputtmpdir} >> /tmp/jobsrunning.txt
done

python /gpfs/fs0/data/wraycompute/vdp5/scripts/variant_processing/checkjobdone.py --out /tmp/jobsrunning.txt
rm -rf /tmp/jobsrunning.txt

cd ${outputtmpdir}

rm -rf *.gz

for alpha in ./*.vcf; do
    bgzip $alpha
done
wait 

for alpha in ./*.vcf.gz; do
    tabix -hp vcf $alpha
done
wait

vcf-concat *.vcf.gz | gzip -c > ${outputfile}.tmp



rm -rf ${tmpdir} &
rm -rf ${outputtmpdir} &
wait


module load bcftools
bcftools query -l ${outputfile}.tmp > /tmp/goodsamples.txt

cd /data/wraycompute/vdp5/scripts/variant_processing



srun parse_matrix_missingness.py --samplelst /tmp/goodsamples.txt

rm -rf /tmp/goodsamples.txt

gzip -dc < ${outputfile}.tmp > /data/wraycompute/vdp5/tmp/temporoni.vcf
java -jar -Xmx9800m /gpfs/fs0/data/wraycompute/vdp5/bin/GenomeAnalysisTK.jar -T SelectVariants -R $DATADIR/reference_data/PVP01.fasta -xl_sf /gpfs/fs0/data/wraycompute/vdp5/variant_associated_data/lowcallrate_needtoremove.list -V /data/wraycompute/vdp5/tmp/temporoni.vcf  -o /data/wraycompute/vdp5/tmp/temporoni_2.vcf -U ALLOW_SEQ_DICT_INCOMPATIBILITY

sbatch --mem=30G /gpfs/fs0/data/wraycompute/vdp5/scripts/variant_processing/highheterozygotesite_data_processing.py --vcffile /data/wraycompute/vdp5/tmp/temporoni_2.vcf --output $outputfile >> /tmp/jobsrunning.txt
python /gpfs/fs0/data/wraycompute/vdp5/scripts/variant_processing/checkjobdone.py --out /tmp/jobsrunning.txt


rm -rf /tmp/jobsrunning.txt


rm -rf ${outputfile}.tmp ${outputfile}.tmp.1 /data/wraycompute/vdp5/tmp/temporoni.vcf /data/wraycompute/vdp5/tmp/temporoni_2.vcf
emailme "boiiii we out here"