#arg is dir name

cd /home/vdp5/data/poptests/nsl/input/${1}



while read p; do
  nSL -samfile chr${p}_samples.txt -hapfile chr${p}_haplotype.txt -adfile chr${p}_ansder.txt > chr${p}_nSL.txt
done < /gpfs/fs0/data/wraycompute/vdp5/reference_data/PVP01.chromosomes

for beta in ./*nSL.txt; do
	python2.7 /gpfs/fs0/data/wraycompute/vdp5/scripts/popgenome/nsl/convert_4_norm.py --nsl ${beta}
done

norm --ihs --files *nSL.selscan.txt


