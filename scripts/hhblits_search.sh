#!/bin/bash
#SBATCH -p cpu
#SBATCH -J HHblits
#SBATCH --mem=320gb
#SBATCH -w node02
#SBATCH -c 64
#SBATCH -o log_hhblits_%A.log

# resources
CPU=64
MEM=320

if [ -z "$1" ]; then
    echo "Usage: $0 <subunits.FASTA file>"
    exit 1
fi

source ~/.bashrc
mkdir -p a3m
mkdir -p subunits

# input
input_fasta=$1

# DB path
uniref="/public_data/db_protSeq/uniref30/2023_02/UniRef30_2023_02"
bfd="/public_data/db_protSeq/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt"

# Split the input fasta file into separate files for each subunit
awk '/^>/{s=++d".fasta"} {print > "subunits/"s}' $input_fasta

# Loop through each subunit file and run hhblits
for subunit_fasta in subunits/*.fasta; do
    input_name=$(basename "$subunit_fasta" .fasta)
    
    # Run HHblits on UniRef30 DB
    hhblits -i $subunit_fasta -d $uniref -oa3m "a3m/${input_name}_uniref30.a3m" -n 8 -mact 0.35 -maxfilt 100000000 -neffmax 20 -cov 25 -cpu $CPU -nodiff -realign_max 100000000 -maxseq 1000000 -maxmem $MEM

    # Run HHblits on BFD with UniRef30 MSA
    hhblits -i "a3m/${input_name}_uniref30.a3m" -d $bfd -oa3m "a3m/${input_name}_bfd.a3m" -n 8 -mact 0.35 -maxfilt 100000000 -neffmax 20 -cov 25 -cpu $CPU -nodiff -realign_max 100000000 -maxseq 1000000 -maxmem $MEM
done
