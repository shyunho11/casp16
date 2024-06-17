#!/bin/bash
#SBATCH -p gpu
#SBATCH --gres=gpu:A6000:1
#SBATCH -J AF2Rank
#SBATCH --mem=46g
#SBATCH -c 4
#SBATCH -o log_af2rank_%A.log

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <decoy directory path> <number of chains>"
    exit 1
fi

set -e
source ~/.bashrc
conda activate af2rank

get_chain_text() {
    local num=$1
    local letters=()
    
    for ((i=0; i<num; i++)); do
        letter=$(printf "\x$(printf %x $((65 + i)))")
        letters+=("$letter")
    done
    
    IFS=','; echo "${letters[*]}"
}

data_dir="/home/iu/casp16/af2rank/"
decoy_dir=$1
chain=$(get_chain_text $2)

python3 /home/iu/casp16/af2rank/af2rank_no_native_xTag.py --data_dir ${data_dir} --chain ${chain} --decoy_dir ${decoy_dir} --output_dir .

mv af2rank_output "$(basename $1)_af2rank_output"
rm 0.pdb 
rm 1.pdb

log_file="log_af2rank_${SLURM_JOB_ID}.log"
python -u /home/iu/casp16/python/parse_af2rank_log.py $log_file

mkdir -p final_unrelaxed

if [ $2 -ge 2 ]; then
    rank_file="RANK_BY_CUSTOM_SCORE.csv"
else
    rank_file="RANK_BY_COMPOSITE.csv"
fi

top_files=$(awk -F',' 'NR > 1 {print $1}' "$rank_file" | head -n 5)

counter=1
for file in $top_files; do
    cp "$decoy_dir/$file" "final_unrelaxed/model_${counter}.pdb"
    echo "File $file saved as model_${counter}.pdb"
    counter=$((counter + 1))
done
