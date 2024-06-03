#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <prefix of directories containing PDB files>"
    exit 1
fi

prefix=$1
candidates_dir="candidates"

mkdir -p "$candidates_dir"

# Find all .pdb files in subdirectories starting with the prefix and rename them
find . -type d -name "${prefix}*" | while read -r sub_dir; do
    for pdb_file in "$sub_dir"/*.pdb; do
        if [[ -f "$pdb_file" ]]; then
            # Extract the rank from the original filename
            rank=$(basename "$pdb_file" | sed -n 's/.*_rank_\([0-9]\+\)_.*/\1/p')
            if [[ -n "$rank" ]]; then
                new_name="candidate_$(basename "$sub_dir")_rank${rank}.pdb"
                cp "$pdb_file" "$candidates_dir/$new_name"
                echo "File saved as $new_name"
            else
                echo "Rank not found in $pdb_file"
            fi
        else
            echo "No .pdb files found in $sub_dir"
        fi
    done
done
