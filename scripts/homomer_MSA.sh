#!/bin/bash

# Check if the correct number of arguments is given
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input file name> <stoichiometry info>"
    exit 1
fi

# Assign command line arguments to variables
input_file=$1
stoich_info=$2
stoich_number=$(echo "$stoich_info" | grep -o '[0-9]\+')
output_file="${input_file%.*}_$stoich_info.a3m"

# Extract the first sequence and record its length in the header
first_sequence=$(awk '/^>/{if (seqlen) exit; getline; while ($0 !~ /^>/ && $0) {seq = seq $0; getline}; seqlen = length(seq)} END {print seq}' "$input_file" | tr -d '\n')
sequence_length=${#first_sequence}
header="#${sequence_length}	$stoich_number"

echo "$header" > "$output_file"
cat "$input_file" >> "$output_file"

echo "Multimer MSA saved as $output_file"
