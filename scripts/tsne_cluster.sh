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

cd $1
output_dir="tsne_result"

source ~/.bashrc
conda activate study

python -u /home/iu/casp16/python/cluster_with_tmscore.py . $output_dir

cd $output_dir

for input_file in cluster_*.txt; do
    cluster_name=$(basename "$input_file" .txt)
    OUTPUT_TAR="${cluster_name}.tar"
    TEMP_DIR=$(mktemp -d)
    
    while IFS= read -r file; do
        file=$(echo "$file" | xargs)
        if [[ -f "../$file" ]]; then
            cp "../$file" "$TEMP_DIR/"
        else
            echo "File not found: $file"
        fi
    done < "$input_file"

    tar -cvf "$OUTPUT_TAR" -C "$TEMP_DIR" .
    rm -rf "$TEMP_DIR"
    
    echo "Files from $input_file have been compressed into $OUTPUT_TAR"
done