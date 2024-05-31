#!/bin/bash
#SBATCH -p gpu
#SBATCH -J UltMSA-Colab
#SBATCH -c 8
#SBATCH --mem=48g
#SBATCH --gres=gpu:A5000:1
#SBATCH -o log_colab_default_%A.log


if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input FASTA file> <result directory postfix>"
    exit 1
fi

source ~/.bashrc
conda activate colabfold

colabfold_batch $1 "${2}_v3" --num-seeds 5 --model-type alphafold2_multimer_v3
colabfold_batch $1 "${2}_v2" --num-seeds 5 --model-type alphafold2_multimer_v2

