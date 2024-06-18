#!/bin/bash
#SBATCH -p gpu
#SBATCH -J Colab-Template
#SBATCH -c 8
#SBATCH --mem=48g
#SBATCH --gres=gpu:A5000:1
#SBATCH -o log_colab_%A.log


if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input FASTA file> <custom template path> <result directory postfix>"
    exit 1
fi

source ~/.bashrc
conda activate colabfold

echo "Running ColabFold in ${2}_v3 with templates in $(realpath $2)"
colabfold_batch $1 "${3}_v3" --templates --custom-template-path $2 --num-seeds 10 --model-type alphafold2_multimer_v3

echo "Running ColabFold in ${2}_v2 with templates in $(realpath $2)"
colabfold_batch $1 "${3}_v2" --templates --custom-template-path $2 --num-seeds 10 --model-type alphafold2_multimer_v2
