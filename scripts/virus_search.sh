#!/bin/bash
#SBATCH -p cpu
#SBATCH -J HHblits
#SBATCH --mem=488gb
#SBATCH -w node02
#SBATCH -c 80
#SBATCH -o log_hhblits_%A.log

source ~/.bashrc

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input FASTA file> <output directory> <output tag>"
    exit 1
fi

# inputs
in_fasta="$1"
out_dir="$2"
tag="$3"

# resources
CPU=80
MEM=488

# sequence databases
PIPEDIR="/public_data/db_protSeq"
DB_UR30="$PIPEDIR/uniref30/2023_02/UniRef30_2023_02"
DB_BFD="$PIPEDIR/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt"
DB_VIRUS="$PIPEDIR/uniprot_sprot_vir70/uniprot_sprot_vir70"

# setup hhblits command
HHBLITS_UR30="hhblits -o /dev/null -mact 0.35 -maxfilt 100000000 -neffmax 20 -cov 25 -cpu $CPU -nodiff -realign_max 100000000 -maxseq 1000000 -maxmem $MEM -n 4 -d $DB_UR30"
HHBLITS_BFD="hhblits -o /dev/null -mact 0.35 -maxfilt 100000000 -neffmax 20 -cov 25 -cpu $CPU -nodiff -realign_max 100000000 -maxseq 1000000 -maxmem $MEM -n 4 -d $DB_BFD"
HHBLITS_VIRUS="hhblits -o /dev/null -mact 0.35 -maxfilt 100000000 -neffmax 20 -cov 25 -cpu $CPU -nodiff -realign_max 100000000 -maxseq 1000000 -maxmem $MEM -n 4 -d $DB_VIRUS"

mkdir -p $out_dir
mkdir -p $out_dir/hhblits
tmp_dir="$out_dir/hhblits"
out_prefix="$out_dir/$tag"

echo out_prefix $out_prefix

# perform iterative searches against UniRef30
prev_a3m="$in_fasta"
for e in 1e-10 1e-6 1e-3
do
    echo "Running HHblits against uniprot_sprot_vir70 DB with E-value cutoff $e"
    $HHBLITS_VIRUS -i $prev_a3m -oa3m $tmp_dir/t000_.$e.a3m -e $e -v 0
    hhfilter -id 95 -cov 75 -i $tmp_dir/t000_.$e.a3m -o $tmp_dir/t000_.$e.id95cov75.a3m
    hhfilter -id 95 -cov 50 -i $tmp_dir/t000_.$e.a3m -o $tmp_dir/t000_.$e.id95cov50.a3m
    prev_a3m="$tmp_dir/t000_.$e.id95cov50.a3m"
    n75=`grep -c "^>" $tmp_dir/t000_.$e.id95cov75.a3m`
    n50=`grep -c "^>" $tmp_dir/t000_.$e.id95cov50.a3m`

    if ((n75>1000))
    then
        if [ ! -s ${out_prefix}.msa0.a3m ]
        then
            cp $tmp_dir/t000_.$e.id95cov75.a3m ${out_prefix}.virus.msa0.a3m
            echo "t000_.${e}.id95cov75.a3m saved as ${out_prefix}.virus.msa0.a3m"
            break
        fi
    elif ((n50>2000))
    then
        if [ ! -s ${out_prefix}.msa0.a3m ]
        then
            cp $tmp_dir/t000_.$e.id95cov50.a3m ${out_prefix}.virus.msa0.a3m
            echo "t000_.${e}.id95cov50.a3m saved as ${out_prefix}.virus.msa0.a3m"
            break
        fi
    else
        continue
    fi
done

if [ ! -s ${out_prefix}.virus.msa0.a3m ]
then
    cp $prev_a3m ${out_prefix}.virus.msa0.a3m
    echo "${prev_a3m} saved as ${out_prefix}.virus.msa0.a3m"
fi