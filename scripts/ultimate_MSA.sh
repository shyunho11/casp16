#!/bin/bash
#SBATCH -p cpu
#SBATCH -J UltimateMSA
#SBATCH --mem=320gb
#SBATCH -w node02
#SBATCH -c 64
#SBATCH -o log_ultimateMSA_%A.log

# resources
CPU=64

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <A3M file path> <FASTA file path> <query FASTA file>"
    exit 1
fi

set -e
source ~/.bashrc

# input
a3m_path=$1
fasta_path=$2
query_fasta=$3

# reformat.pl converts a3m to fasta
for file in "${a3m_path}/"*.a3m; do
    base_name=$(basename "$file" .a3m)
    reformat.pl a3m fas "$file" "${fasta_path}/${base_name}.fasta"
done

# collect all protein sequences
cat "${fasta_path}/"*.fasta > pre_ultimate.fasta
sed '/>/! s/-//g' pre_ultimate.fasta | tr '[:lower:]' '[:upper:]' > ultimate.fasta # remove gaps & force uppercase

mkdir -p mmseqs

# cluster and extract representative sequences to make ultimate DB
mmseqs createdb ultimate.fasta mmseqs/ultimate_db
mmseqs cluster mmseqs/ultimate_db mmseqs/clu_result mmseqs/tmp --min-seq-id 0.95 -c 0.15 --cov-mode 1 --threads $CPU
mmseqs result2repseq mmseqs/ultimate_db mmseqs/clu_result mmseqs/rep_seq
mmseqs createtsv mmseqs/ultimate_db mmseqs/rep_seq mmseqs/rep_seq.tsv
awk -F'\t' '{print ">"$1"\n"$2}' mmseqs/rep_seq.tsv > unique_ultimate.fasta
# cp ultimate.fasta unique_ultimate.fasta

# search query against ultimate DB to make ultimate MSA
mmseqs createdb unique_ultimate.fasta mmseqs/ultimate_db
mmseqs createdb $query_fasta mmseqs/query_db
mmseqs search mmseqs/query_db mmseqs/ultimate_db mmseqs/result mmseqs/tmp --num-iterations 5 -s 20 --max-seqs 3000 --min-seq-id 0.3 --search-type 1 --threads $CPU
mmseqs result2msa mmseqs/query_db mmseqs/ultimate_db mmseqs/result ultimate.a3m --msa-format-mode 2

# clean up
rm -r mmseqs
rm *.dbtype
rm *.index
rm *ultimate.fasta