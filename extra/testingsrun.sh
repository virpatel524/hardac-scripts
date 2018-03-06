for alpha in {1..30}; do
	sbatch testingsrun_mini.sh >> /tmp/jobsdone.txt
done


python /gpfs/fs0/data/wraycompute/vdp5/scripts/variant_processing/checkjobdone.py --out /tmp/jobsdone.txt

