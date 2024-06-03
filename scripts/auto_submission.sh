#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <final model path>"
  exit 1
fi

input_directory="$1"

cd "$input_directory" || exit 1

current_directory=$(pwd)
group_name=$(basename "$current_directory" | cut -d'.' -f2)
target_id=$(basename "$(dirname "$current_directory")")

echo "Target ID: $target_id"
echo "Group Name: $group_name"
echo ""

for i in {1..5}
do
    echo "[model_$i.pdb]"
    stoich_info=$(grep "STOICH" model_$i.pdb)
    
    if [ -z "$stoich_info" ]; then
        echo "No stoich info (add if UNK)"
    else
        echo "$stoich_info"
    fi
    
    grep -B 1 "^TER" model_$i.pdb | awk '/^ATOM/ {chain_and_residue = substr($0, 22, 5); chain = substr(chain_and_residue, 1, 1); residue = substr(chain_and_residue, 2); print chain, residue}'
    
    echo ""
done

read -p "Proceed [y/n]?: " answer
if [[ "$answer" == "Y" || "$answer" == "y" ]]; then
    python /home/casp16/casp16_server/bin/submit_CASP16.py $target_id ${group_name^^}
    echo "Waiting for 10 seconds..."
    sleep 10
    python /home/casp16/casp16_server/bin/check_submit_status.py $target_id ${group_name}
else
    echo "Submission canceled."
fi
