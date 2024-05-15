#!/bin/bash

# Check if directory argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

input_dir=$1
candidates_dir="candidates"
mkdir -p "$candidates_dir"

# Step 1: Read ColabFold log after 'reranking models'
data=$(awk '/reranking models by/{flag=1} flag' "$input_dir/log.txt")

# Step 2: Calculate pLDDT * pTM * ipTM, then sort and take top 5
echo "$data" | grep 'rank_' | awk '{ 
    model_name = $3
    match($4, /=([0-9.]+)/, arr)
    pLDDT = arr[1]
    match($5, /=([0-9.]+)/, arr)
    pTM = arr[1]
    match($6, /=([0-9.]+)/, arr)
    ipTM = arr[1]
    score = pLDDT * pTM * ipTM
    printf "%s %.2f\n", model_name, score
}' | sort -k2,2nr > "$input_dir/top_models.txt"

cat "$input_dir/top_models.txt"

# Step 3: Find corresponding .pdb files and copy them to the final directory with new names
while IFS=" " read -r model_name score; do
    pdb_file=$(find "$input_dir" -name "*${model_name}*.pdb")
    if [[ -n "$pdb_file" ]]; then
        cp "$pdb_file" "$candidates_dir/candidate_$(basename "$input_dir")_${score}.pdb"
        echo "File saved as candidate_$(basename "$input_dir")_${score}.pdb"
    else
        echo "File not found"
    fi
done < "$input_dir/top_models.txt"
