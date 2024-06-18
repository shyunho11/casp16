#!/bin/bash
#SBATCH -p gpu
#SBATCH -J Colab-Unpaired
#SBATCH -c 8
#SBATCH --mem=48g
#SBATCH --gres=gpu:A5000:1
#SBATCH -o log_colab_%A.log


if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input FASTA file> <result directory postfix>"
    exit 1
fi

source ~/.bashrc
conda activate colabfold

echo "Running ColabFold in ${2}_v3 with unpaired MSA"
colabfold_batch $1 "${2}_v3" --pair-mode unpaired --num-seeds 5 --model-type alphafold2_multimer_v3

echo "Running ColabFold in ${2}_v2 with unpaired MSA"
colabfold_batch $1 "${2}_v2" --pair-mode unpaired --num-seeds 5 --model-type alphafold2_multimer_v2
