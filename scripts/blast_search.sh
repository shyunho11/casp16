#!/bin/bash
#SBATCH -w node02
#SBATCH -J BLAST+
#SBATCH -c 64
#SBATCH --mem=320g
#SBATCH -o log_blast_%A.log

CPU=64

if [ -z "$1" ]; then
    echo "Usage: $0 <subunits FASTA directory>"
    exit 1
fi

fasta_dir=$1
out_dir="blastp"
seq_dir="fa"

source ~/.bashrc
mkdir -p $out_dir

NR="/local_data1/ncbi_blast_db/nr/nr"
TSA_NR="/local_data1/ncbi_blast_db/tsa_nr/tsa_nr"
ENV_NR="/local_data1/ncbi_blast_db/env_nr/env_nr"

for subunit_fasta in $fasta_dir/*.fasta; do
    input_name=$(basename "$subunit_fasta" .fasta)
    
    echo "Searching ${input_name} on nr DB"
    blastp -query $subunit_fasta -db $NR -out "$out_dir/${input_name}_nr.out" -evalue 1e-3 -num_threads $CPU -outfmt "7 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore sseq"
    
    echo "Searching ${input_name} on tsa_nr DB"
    blastp -query $subunit_fasta -db $TSA_NR -out "$out_dir/${input_name}_tsa_nr.out" -evalue 1e-3 -num_threads $CPU -outfmt "7 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore sseq"
    
    echo "Searching ${input_name} on env_nr DB"
    blastp -query $subunit_fasta -db $ENV_NR -out "$out_dir/${input_name}_env_nr.out" -evalue 1e-3 -num_threads $CPU -outfmt "7 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore sseq"
done

python /home/iu/casp16/python/blast_to_fasta.py $out_dir $seq_dir