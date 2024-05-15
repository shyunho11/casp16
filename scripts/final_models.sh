#!/bin/bash

# Check if directory argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <model directory>"
    exit 1
fi

# Define the directory containing the models
model_dir=$1
final_dir="final_unrelaxed"
mkdir -p $final_dir

# Step 1: Parse scores from filenames and sort them
declare -a model_info
while IFS= read -r filename; do
    if [ -f "$model_dir/$filename" ] && [[ $filename =~ "candidate" ]]; then
        base_name="${filename%.*}"  # Remove extension
        score="${base_name##*_}"   # Get the substring after the last '_'
    
        if [[ "$score" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
            model_info+=("$score $filename")
        fi
    fi
done < <(ls -p "$model_dir" | grep -v /)  # List only files, excluding directories

# Step 2: Sort the array by score (highest first), save all results to a file
IFS=$'\n' sorted=($(sort -rn -k1 <<<"${model_info[*]}"))
unset IFS

cat /dev/null >| "$model_dir/top_final_models.txt" # reset to empty file
for i in "${sorted[@]}"; do
    echo "$i" >> "$model_dir/top_final_models.txt"
done

# Step 3: Copy only the top 5 files, using a counter to stop when exceeding 5
counter=1
while IFS=" " read -r score filename; do
    if [ $counter -le 5 ]; then
        new_name="model_${counter}.pdb"
        cp "$model_dir/$filename" "$final_dir/$new_name"
        echo "File $filename saved as $new_name"
        ((counter++))
    else
        break
    fi
done < "$model_dir/top_final_models.txt"
