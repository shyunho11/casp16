#!/bin/bash
#SBATCH -p cpu
#SBATCH -J HHblits
#SBATCH --mem=488gb
#SBATCH -w node02
#SBATCH -c 80
#SBATCH -o log_hhblits_%A.log

source ~/.bashrc

if [ ! -d "a3m" ]; then
    mkdir a3m
fi

# Get target ID (=parent directory name)
current_dir=$(pwd)
parent_dir=$(dirname "$current_dir")
target_id=$(basename "$parent_dir")

input_fasta="/home/iu/casp16/${target_id}/target.fasta"

# Run HHblits on UniRef30 DB
hhblits -i $input_fasta -d /public_data/db_protSeq/uniref30/2023_02/UniRef30_2023_02 -oa3m "a3m/${target_id}_uniref30.a3m" -n 8 -cpu 96

# Run HHblits on BFD with UniRef30 MSA
hhblits -i "a3m/${target_id}_uniref30.a3m" -d /public_data/db_protSeq/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt -oa3m "a3m/${target_id}_bfd.a3m" -n 8 -cpu 96
