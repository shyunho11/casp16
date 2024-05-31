#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <query FASTA file> <custom DB FASTA file> <output A3M file>"
    exit 1
fi

query_fasta=$1
custom_db_fasta=$2
output_a3m=$3

sed '/>/! s/-//g' $custom_db_fasta | tr '[:lower:]' '[:upper:]' > custom.fasta

mkdir mmseqs

mmseqs createdb custom.fasta mmseqs/custom_db
mmseqs createdb $query_fasta mmseqs/query_db

mmseqs search mmseqs/query_db mmseqs/custom_db mmseqs/result mmseqs/tmp --num-iterations 5 -s 20 --max-seqs 10000 --min-seq-id 0.3 --search-type 1
mmseqs result2msa mmseqs/query_db mmseqs/custom_db mmseqs/result $output_a3m --msa-format-mode 2

rm -r mmseqs
rm *.dbtype
rm *.index
rm custom.fasta