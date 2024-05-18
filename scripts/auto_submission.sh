#!/bin/bash

# THIS SCRIPT MUST BE LOCATED AT THE TARGET DIRECTORY (ex. /home/casp16/run/TS.human/T1201/)
# FINAL MODELS SHOULD BE LOCATED IN THE SAME DIRECTORY

tar_id=$(basename "$(pwd)")
echo "***** Starting submission for $tar_id *****"

read -p "Which group do you want to submit? " group_name
if [ -f "submitted.$group_name" ]; then
    # Ask if user wants to submit again
    read -p "You have already submitted. Do you want to submit again? (y/n) " answer
    if [[ "$answer" == "n" ]]; then
        echo "Submission cancelled."
        exit 0
    else
        rm "submitted.$group_name"
        rm -r "submit.$group_name"
    fi
fi

dir_name="model.$group_name"

echo "Checking PDB files in $dir_name..."

for pdb_file in "$dir_name"/*.pdb; do
    echo "Processing $pdb_file..."
    total_plddt=0
    count=0
    while read -r line; do
        if [[ $line =~ ^ATOM ]]; then
            plddt_value=$(echo "$line" | awk '{print $11}')
            # Check for invalid pLDDT values
            if (( $(echo "$plddt_value < 0 || $plddt_value > 100" | bc) )); then
                echo "Error: pLDDT value $plddt_value out of valid range (0-100) in $pdb_file"
                exit 1
            fi
            # Summing pLDDT values and counting entries
            total_plddt=$(echo "$total_plddt + $plddt_value" | bc)
            ((count++))
        fi
    done < "$pdb_file"
    
    # Check if the pdb file is empty (or corrupted)
    if [ $count -gt 0 ]; then
        average_plddt=$(echo "scale=2; $total_plddt / $count" | bc)
        echo "[Average pLDDT value] : $average_plddt"
    else
        echo "Error: no valid ATOM records found in $pdb_file."
        exit 1
    fi
done

python /home/casp16/casp16_server/bin/submit_CASP16.py $tar_id ${group_name^^}
