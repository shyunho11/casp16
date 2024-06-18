#!/bin/bash
#SBATCH -J Phase1
#SBATCH -p cpu
#SBATCH -c 4
#SBATCH --mem=16g
#SBATCH -w node01
#SBATCH -o log_phase1_%A.log

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <TARGET ID> [<stoichiometry>]"
    exit 1
fi

source /home/iu/.bashrc
export PATH=/opt/ohpc/pub/apps/anaconda3/bin/python:/opt/ohpc/pub/apps/anaconda3/sbin:/opt/ohpc/pub/mpi/libfabric/1.13.0/bin:/opt/ohpc/pub/mpi/ucx-ohpc/1.11.2/bin:/opt/ohpc/pub/libs/hwloc/bin:/opt/ohpc/pub/mpi/openmpi4-gnu12/4.1.4/bin:/opt/ohpc/pub/compiler/gcc/12.2.0/bin:/opt/ohpc/pub/utils/prun/2.2:/opt/ohpc/pub/utils/autotools/bin:/opt/ohpc/pub/bin:/home/iu/.local/bin:/home/iu/bin:/opt/ohpc/pub/apps/anaconda3/condabin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/var/lib/snapd/snap/bin:/home/software/bin:/home/software/git/CCMpred/bin:/home/software/git/hh-suite/build/bin:/home/software/git/hh-suite/build/scripts:/home/software/git/gremlin3/bin:/home/software/zdock3.0.2_linux_x64:/opt/dell/srvadmin/bin:/home/iu/nemo/ngc-cli:/home/software/bin:/home/software/git/CCMpred/bin:/home/software/git/hh-suite/build/bin:/home/software/git/hh-suite/build/scripts:/home/software/git/gremlin3/bin:/home/software/zdock3.0.2_linux_x64

TARGET_ID=$1
TARGET_DIR="/home/casp16/run/TS.human/$TARGET_ID"

echo "Running Phase 1[0] for $1"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Directory does not exist: $TARGET_DIR"
    exit 1
fi

cd "$TARGET_DIR"
mkdir -p BLAST

# Move subunits.fasta into the BLAST directory
if [ -f "subunits.fasta" ]; then
    cp subunits.fasta BLAST/
else
    echo "File subunits.fasta does not exist in $TARGET_DIR"
    exit 1
fi

cd BLAST

job_id1=$(sbatch /home/iu/casp16/scripts/hhblits_search.sh subunits.fasta | awk '{print $4}')
job_id2=$(sbatch --dependency=afterok:$job_id1 /home/iu/casp16/scripts/blast_search.sh subunits | awk '{print $4}')
job_id3=$(sbatch --dependency=afterok:$job_id2 /home/iu/casp16/scripts/ultimate_MSA.sh a3m fa subunits.fasta | awk '{print $4}')

if [ "$STOICHIOMETRY" == "A1" ]; then
    sbatch --dependency=afterok:$job_id3 \
           -c 8 \
           --mem=46g \
           --gres=gpu:A5000:1 \
           -J "${TARGET_ID}_UltMSA-Colab" \
           -o "${TARGET_DIR}/BLAST/log_auto_colab_%A.log" \
           --chdir="${TARGET_DIR}/BLAST" \
           --wrap="set -e; \
                   source /home/iu/.bashrc; \
                   conda activate colabfold; \
                   mkdir -p '${TARGET_DIR}/BLAST/result_ult_auto'; \
                   colabfold_batch '${TARGET_DIR}/BLAST/subunits.fasta' '${TARGET_DIR}/BLAST/result_ult_auto' --num-recycle 10 --recycle-early-stop-tolerance 0.3 --num-seeds 50 --templates; \
                   conda deactivate"
fi
