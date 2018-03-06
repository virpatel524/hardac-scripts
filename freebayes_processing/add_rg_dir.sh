source /gpfs/fs0/home/vdp5/.bash_profile 
for alpha in /data/wraycompute/vdp5/sequences_bam_cambodia/*; do
	zeta=$(basename $alpha)
	IFS='_' read -ra ADDR <<< $zeta
	base=${ADDR[0]}
	echo $base
	sleep 1s
	sbatch -o /home/vdp5/slurm_out/${base}_addrg_md.out /gpfs/fs0/data/wraycompute/vdp5/slurm_scripts/addrg_cambodia_seq_2.18.17.sh $alpha $base
done

