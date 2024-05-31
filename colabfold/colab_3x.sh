#!/bin/bash
#SBATCH -p gpu
#SBATCH -J UltMSA-Colab
#SBATCH -c 8
#SBATCH --mem=48g
#SBATCH --gres=gpu:A5000:1
#SBATCH -o log_colab_3x_%A.log

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <orignal A3M file> <9050 A3M file> <9575 A3M file> <result directory postfix>"
    exit 1
fi

POSTFIX=$4

source ~/.bashrc
conda activate colabfold

colabfold_batch $1 "${POSTFIX}_v3" --num-seeds 5 --model-type alphafold2_multimer_v3
colabfold_batch $1 "${POSTFIX}_v2" --num-seeds 5 --model-type alphafold2_multimer_v2

colabfold_batch $2 "${POSTFIX}9050_v3" --num-seeds 5 --model-type alphafold2_multimer_v3
colabfold_batch $2 "${POSTFIX}9050_v2" --num-seeds 5 --model-type alphafold2_multimer_v2

colabfold_batch $3 "${POSTFIX}9575_v3" --num-seeds 5 --model-type alphafold2_multimer_v3
colabfold_batch $3 "${POSTFIX}9575_v2" --num-seeds 5 --model-type alphafold2_multimer_v2
