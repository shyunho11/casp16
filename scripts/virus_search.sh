#!/bin/bash
#SBATCH -p cpu
#SBATCH -J HHblits
#SBATCH --mem=320gb
#SBATCH -w node02
#SBATCH -c 64
#SBATCH -o log_virusMSA_%A.log

# resources
CPU=64
MEM=320

source ~/.bashrc

if [ -z $1 ]; then
    echo "Usage: $0 <input FASTA file>"
    exit 1
fi

# input and outputs
in_fasta="$1"
out_a3m="virus.msa0.a3m"
tmp_dir="virus_search"

mkdir -p $tmp_dir

# setup hhblits command
HHBLITS_VIRUS="hhblits -o /dev/null -mact 0.35 -maxfilt 100000000 -neffmax 20 -cov 25 -cpu $CPU -nodiff -realign_max 100000000 -maxseq 1000000 -maxmem $MEM -n 4 -d /public_data/db_protSeq/uniprot_sprot_vir70/uniprot_sprot_vir70"

# perform iterative searches against UniRef30
prev_a3m="$in_fasta"
for e in 1e-10 1e-6 1e-3
do
    echo "Running HHblits against uniprot_sprot_vir70 DB with E-value cutoff $e"
    $HHBLITS_VIRUS -i $prev_a3m -oa3m $tmp_dir/virus.$e.a3m -e $e -v 0
    hhfilter -id 95 -cov 75 -i $tmp_dir/virus.$e.a3m -o $tmp_dir/virus.$e.id95cov75.a3m
    hhfilter -id 95 -cov 50 -i $tmp_dir/virus.$e.a3m -o $tmp_dir/virus.$e.id95cov50.a3m
    prev_a3m="$tmp_dir/virus.$e.id95cov50.a3m"
    n75=`grep -c "^>" $tmp_dir/virus.$e.id95cov75.a3m`
    n50=`grep -c "^>" $tmp_dir/virus.$e.id95cov50.a3m`

    if ((n75>1000))
    then
        if [ ! -s $out_a3m ]
        then
            cp $tmp_dir/virus.$e.id95cov75.a3m $out_a3m
            echo "virus.${e}.id95cov75.a3m saved as ${out_a3m}"
            break
        fi
    elif ((n50>2000))
    then
        if [ ! -s $out_a3m ]
        then
            cp $tmp_dir/virus.$e.id95cov50.a3m $out_a3m
            echo "virus.${e}.id95cov50.a3m saved as ${out_a3m}"
            break
        fi
    else
        continue
    fi
done

if [ ! -s $out_a3m ]
then
    cp $prev_a3m $out_a3m
    echo "${prev_a3m} saved as ${out_a3m}"
fi
