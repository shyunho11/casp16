#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <unrelaxed PDB file directory>"
    exit 1
fi

unrelaxed_dir=$1
relaxed_dir="$(pwd)/final_relaxed"
mkdir -p $relaxed_dir

cd $unrelaxed_dir

# (New) Submit a separate sbatch job for each PDB file
for pdb_file in *.pdb; do
    model_name="${pdb_file%.*}"
    job_id=$(sbatch \
        -c 4 \
        -J FinalRelax \
        -o log_relax_$model_name.log \
        -p cpu \
        -w node02 \
        --mem=16g \
        --wrap "
            source ~/.bashrc
            conda activate RFdiffusion
            python -u /home/casp16/util/str_relax.py -pdb_fn $pdb_file -out_prefix 'RELAXED_$model_name'
            cp 'RELAXED_$model_name.pdb' '$relaxed_dir/$model_name.pdb'
            grep -H 'ENERGY of' log_relax_*.log > '$relaxed_dir/README.txt'
        " | awk '{print $4}')
    echo "Submitted relaxation job $job_id"
done
