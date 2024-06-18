#!/bin/bash
#SBATCH -p gpu
#SBATCH -J Colab-Quick
#SBATCH -c 8
#SBATCH --mem=48g
#SBATCH --gres=gpu:A6000:1
#SBATCH -o log_colab_%A.log


if [ -z "$1" ]; then
    echo "Usage: $0 <input MSA file>"
    exit 1
fi

source ~/.bashrc
conda activate colabfold

quick_dir="result_quick"
mkdir -p $quick_dir

echo "Running ColabFold in $quick_dir"
colabfold_batch $1 $quick_dir --model-type alphafold2_multimer_v3 --recycle-early-stop-tolerance 0.7 --num-recycle 40
