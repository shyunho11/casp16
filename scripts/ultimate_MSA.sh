#!/bin/bash

for file in a3m/*.a3m; do
    # Extract the base name without the extension
    base_name=$(basename "$file" .a3m)
    # Use reformat.pl to convert from a3m to fasta
    reformat.pl a3m fas "$file" "${base_name}.fasta"
done

cat *.fasta > ultimate.fasta
sed '/>/! s/-//g' ultimate.fasta | tr '[:lower:]' '[:upper:]' > input.fasta

mkdir mmseqs

mmseqs createdb input.fasta mmseqs/input_db
mmseqs cluster mmseqs/input_db mmseqs/clu_result mmseqs/tmp --min-seq-id 0.95 -c 0.15 --cov-mode 1
mmseqs result2repseq mmseqs/input_db mmseqs/clu_result mmseqs/rep_seq
mmseqs createtsv mmseqs/input_db mmseqs/rep_seq mmseqs/rep_seq.tsv
awk -F'\t' '{print ">"$1"\n"$2}' mmseqs/rep_seq.tsv > unique_input.fasta


mmseqs createdb unique_input.fasta mmseqs/input_db

# Get target ID (=parent directory name)
current_dir=$(pwd)
parent_dir=$(dirname "$current_dir")
target_id=$(basename "$parent_dir")
query_fasta="/home/iu/casp16/${target_id}/target.fasta"

if [ ! -f $query_fasta ]; then
    echo "File $query_fasta does not exist."
    exit 1
fi

mmseqs createdb $query_fasta mmseqs/query_db

mmseqs search mmseqs/query_db mmseqs/input_db mmseqs/result mmseqs/tmp --num-iterations 5 -s 20 --max-seqs 10000 --min-seq-id 0.3 --search-type 1
mmseqs result2msa mmseqs/query_db mmseqs/input_db mmseqs/result ultimate.a3m --msa-format-mode 2

rm -r mmseqs
rm *.dbtype
rm *.index