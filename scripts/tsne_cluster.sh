#!/bin/bash
#SBATCH -p cpu
#SBATCH -J StructClust
#SBATCH --mem=32gb
#SBATCH -w node02
#SBATCH -c 8
#SBATCH -o log_cluster_%A.log

if [ -z "$1" ]; then
    echo "Usage: $0 <PDB files directory>"
    exit 1
fi

source ~/.bashrc
conda activate study

PDB_DIR=$1
NEW_DIR="${PDB_DIR/result_/tsne_}"

mkdir -p "$NEW_DIR"

cd "$NEW_DIR"

python -u /home/iu/casp16/scripts/cluster_with_tmscore.py "$PDB_DIR"
