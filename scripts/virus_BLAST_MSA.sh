#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <query FASTA file> <Virus sequence FASTA file> <output A3M file>"
    exit 1
fi

query_fasta=$1
virus_fasta=$2
output_a3m=$3

sed '/>/! s/-//g' $virus_fasta | tr '[:lower:]' '[:upper:]' > input.fasta

mkdir mmseqs

mmseqs createdb input.fasta mmseqs/input_db
mmseqs createdb $query_fasta mmseqs/query_db

mmseqs search mmseqs/query_db mmseqs/input_db mmseqs/result mmseqs/tmp --num-iterations 5 -s 20 --max-seqs 10000 --min-seq-id 0.3 --search-type 1
mmseqs result2msa mmseqs/query_db mmseqs/input_db mmseqs/result virus_tmp.a3m --msa-format-mode 2
#hhfilter -id 95 -cov 75 -i virus_tmp.a3m -o $output_a3m

rm -r mmseqs
rm *.dbtype
rm *.index
rm virus_tmp.a3m