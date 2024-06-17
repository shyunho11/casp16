#!/bin/bash
#SBATCH -J FinalRelax
#SBATCH -p cpu
#SBATCH -c 4
#SBATCH --mem=32g
#SBATCH -w node01
#SBATCH -o log_relax_%A.log

# Check if the final model directory is given
if [ -z "$1" ]; then
    echo "Usage: $0 <final model path>"
    exit 1
else
    echo "Relaxing final models stored in: $1"
fi

source ~/.bashrc
conda activate RFdiffusion

cd $1

for file in *.pdb; do
    python -u /home/casp16/util/str_relax.py -pdb_fn $file -out_prefix "RELAXED_$(basename "${file%.*}")" # -disulf_cutoff 2.0
done

relaxed_dir="../final_relaxed"
mkdir -p $relaxed_dir

for file in RELAXED*.pdb; do
    filename=$(basename "$file")
    new_filename=${filename#RELAXED_}
    cp "$file" "$relaxed_dir/$new_filename"
    echo "File saved as $new_filename"
done
