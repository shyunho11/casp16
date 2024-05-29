#!/bin/bash
#SBATCH -w node02
#SBATCH -J BLAST+
#SBATCH -c 80
#SBATCH --mem=488g
#SBATCH -o log_blast_%A.log

if [ -z "$1" ]; then
    echo "Usage: $0 <input FASTA file>"
    exit 1
fi

save_dir="blastp"

mkdir -p $save_dir

NR="/local_data1/ncbi_blast_db/nr/nr"
TSA_NR="/local_data1/ncbi_blast_db/tsa_nr/tsa_nr"
ENV_NR="/local_data1/ncbi_blast_db/env_nr/env_nr"

blastp -query $1 -db $NR -out "$save_dir/nr.out" -evalue 1e-3 -num_threads 80 -outfmt "7 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore sseq"
blastp -query $1 -db $TSA_NR -out "$save_dir/tsa_nr.out" -evalue 1e-3 -num_threads 80 -outfmt "7 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore sseq"
blastp -query $1 -db $TSA_NR -out "$save_dir/env_nr.out" -evalue 1e-3 -num_threads 80 -outfmt "7 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore sseq"
