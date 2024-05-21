#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <final model path>"
  exit 1
fi

input_directory="$1"
group_name=$(basename "$input_directory" | cut -d'.' -f2)

cd $input_directory
current_directory=$(pwd)
target_id=$(basename "$(dirname "$current_directory")")

echo "Target ID: $target_id"
echo "Group Name: $group_name"
echo ""

for i in {1..5}
do
    echo "[model_$i.pdb]"
    stoich_info=$(grep "STOICH" model_$i.pdb)
    
    if [ -z "$stoich_info" ]; then
        echo "No stoich info"
    else
        echo "$stoich_info"
    fi
    
    grep -B 1 "^TER" model_$i.pdb | awk '/^ATOM/ {print $5, $6}'
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
