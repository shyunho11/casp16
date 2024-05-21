#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 <directory1> <directory2> ... <directoryN>"
    exit 1
fi

candidates_dir="pre_candidates"
mkdir -p "$candidates_dir"

process_directory() {
    input_dir=$1

    # Step 1: Read ColabFold log after 'reranking models'
    data=$(awk '/reranking models by/{flag=1} flag' "$input_dir/log.txt")

    # Step 2: Calculate pLDDT * pTM * ipTM (if exists), then sort and take top 5
    echo "$data" | grep 'rank_' | awk '{ 
        rank = $1
        model_name = $3
        match($4, /=([0-9.]+)/, arr)
        pLDDT = arr[1]
        match($5, /=([0-9.]+)/, arr)
        pTM = arr[1]
        score = pLDDT * pTM

        if ($6 ~ /ipTM=/) {
            match($6, /=([0-9.]+)/, arr)
            ipTM = arr[1]
            score *= ipTM
        }

        printf "%s %s %.2f\n", rank, model_name, score
    }' | sort -k3,3nr > "$input_dir/top_models.txt"

    cat "$input_dir/top_models.txt"

    # Step 3: Find corresponding .pdb files and copy them to the final directory with new names
    while IFS=" " read -r rank model_name score; do
        pdb_file=$(find "$input_dir" -name "*${model_name}*.pdb")
        if [[ -n "$pdb_file" ]]; then
            new_filename="candidate_$(basename "$input_dir")_${rank}_${score}.pdb"
            cp "$pdb_file" "$candidates_dir/$new_filename"
            echo "File saved as $new_filename"
        else
            echo "File not found for model $model_name"
        fi
    done < "$input_dir/top_models.txt"
}

# Iterate over each directory provided as argument
for dir in "$@"; do
    if [ -d "$dir" ]; then
        process_directory "$dir"
    else
        echo "Directory $dir not found"
    fi
done

final_candidates_dir="candidates"
mkdir -p $final_candidates_dir

# Step 1: Parse scores from filenames and sort them
declare -a model_info
while IFS= read -r filename; do
    if [ -f "$candidates_dir/$filename" ] && [[ $filename =~ "candidate" ]]; then
        base_name="${filename%.*}"  # Remove extension
        score="${base_name##*_}"   # Get the substring after the last '_'
    
        if [[ "$score" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
            model_info+=("$score $filename")
        fi
    fi
done < <(ls -p "$candidates_dir" | grep -v /)  # List only files, excluding directories

# Step 2: Sort the array by score (highest first), save all results to a file
IFS=$'\n' sorted=($(sort -rn -k1 <<<"${model_info[*]}"))
unset IFS

cat /dev/null >| "$candidates_dir/top_final_models.txt" # reset to empty file
for i in "${sorted[@]}"; do
    echo "$i" >> "$candidates_dir/top_final_models.txt"
done

# Step 3: Copy only the top 5 files, using a counter to stop when exceeding 5
counter=1
while IFS=" " read -r score filename; do
    if [ $counter -le 50 ]; then
        cp "$candidates_dir/$filename" "$final_candidates_dir"
        echo "Final model ${counter} : $filename"
        ((counter++))
    else
        break
    fi
done < "$candidates_dir/top_final_models.txt"
