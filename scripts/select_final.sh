#!/bin/bash

# Check if the input file is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <AF2Rank output file>"
  exit 1
fi

input_file="$1"

mkdir -p final_unrelaxed

# Extract the top .pdb file names and their paths
top_files=$(awk 'NR > 1 {print $2}' "$input_file" | head -n 5)

# Copy and rename the top files
counter=1
for file in $top_files; do
  cp "candidates/$file" "final_unrelaxed/model_${counter}.pdb"
  echo "File $file saved as model_${counter}.pdb"
  counter=$((counter + 1))
done