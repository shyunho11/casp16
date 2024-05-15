#!/bin/bash
#SBATCH -J FinalRelax
#SBATCH -p cpu
#SBATCH -c 4
#SBATCH --mem=32g
#SBATCH -w node01
#SBATCH -o log_minimize_%A.log

# Function to add TER tags to a PDB file
add_ter_tags() {
    local infile=$1
    local outfile=$2

    awk '
    BEGIN {prev_chain = ""}
    {
        if ($1 == "ATOM" || $1 == "HETATM") {
            if (prev_chain != "" && $5 != prev_chain) {
                print "TER"
            }
            prev_chain = $5
            print $0
        } else {
            print $0
        }
    }
    END {
        if (prev_chain != "") {
            print "TER"
        }
    }' "$infile" > "$outfile"
}

# Check if the final model directory is given
if [ -z "$1" ]; then
    echo "Usage: $0 <final model path>"
    exit 1
else
    echo "Relaxing final models stored in: $1"
fi

source ~/.bashrc
conda activate RFdiffusion

python -u /home/iu/casp16/private/relax_final_models.py $1

relaxed_dir="final_relaxed"
mkdir -p $relaxed_dir

for file in "$1"RELAXED_model_*.pdb; do
    filename=$(basename "$file")
    new_filename=${filename#RELAXED_}
    add_ter_tags "$file" "$relaxed_dir/$new_filename"
    echo "File saved as $new_filename"
done
