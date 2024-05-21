#!/bin/bash
#SBATCH -p cpu
#SBATCH -J HHblits
#SBATCH --mem=488gb
#SBATCH -w node02
#SBATCH -c 80
#SBATCH -o log_hhblits_%A.log

if [ -z "$1" ]; then
    echo "Usage: $0 <query FASTA file>"
    exit 1
fi

source ~/.bashrc
mkdir -p a3m

input_fasta=$1
input_name=$(basename "$input_fasta" .fasta)

# Run HHblits on UniRef30 DB
hhblits -i $input_fasta -d /public_data/db_protSeq/uniref30/2023_02/UniRef30_2023_02 -oa3m "a3m/${input_name}_uniref30.a3m" -n 8 -cpu 96

# Run HHblits on BFD with UniRef30 MSA
hhblits -i "a3m/${input_name}_uniref30.a3m" -d /public_data/db_protSeq/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt -oa3m "a3m/${input_name}_bfd.a3m" -n 8 -cpu 96
