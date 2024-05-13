#!/bin/bash

# Get target ID (=parent directory name)
current_dir=$(pwd)
parent_dir=$(dirname "$current_dir")
target_id=$(basename "$parent_dir")

query_fasta="/home/iu/casp16/${target_id}/target.fasta"

if [ ! -f $query_fasta ]; then
    echo "File $query_fasta does not exist."
    exit 1
fi

sed '/>/! s/-//g' "${target_id}_virus.fasta" | tr '[:lower:]' '[:upper:]' > input.fasta

mkdir mmseqs

mmseqs createdb input.fasta mmseqs/input_db
mmseqs createdb $query_fasta mmseqs/query_db

mmseqs search mmseqs/query_db mmseqs/input_db mmseqs/result mmseqs/tmp --num-iterations 5 -s 20 --max-seqs 10000 --min-seq-id 0.3 --search-type 1
mmseqs result2msa mmseqs/query_db mmseqs/input_db mmseqs/result "${target_id}_virus.a3m" --msa-format-mode 2

rm -r mmseqs
rm *.dbtype
rm *.index