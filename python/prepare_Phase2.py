import os
import sys
from casp.web import *

if len(sys.argv) != 2:
    print("Usage: python prepare_phase2_run.py <TARGET ID>")
    sys.exit(1)

target = get_target_by_id(sys.argv[1])

if target.empty:
    exit(1)
else:
    print("*"*10 + "TARGET INFO" + "*"*10)
    print(target)
    
target_id = target['Tar-id']
stoichiom = target['Stoichiom.']
mer = 'monomer' if stoichiom == 'A1' else 'multimer'
n_chains = sum(subunit[1] for subunit in parse_stoichiometry(stoichiom))
chains_string = ','.join(chr(65 + i) for i in range(n_chains))

save_target_files(target_id, stoichiom)
save_target_template(target_id)

# Define the content of the .sh file
script_content_1 = """#!/bin/bash

source /home/iu/.bashrc
export PATH=/opt/ohpc/pub/apps/anaconda3/bin/python:/opt/ohpc/pub/apps/anaconda3/sbin:/opt/ohpc/pub/mpi/libfabric/1.13.0/bin:/opt/ohpc/pub/mpi/ucx-ohpc/1.11.2/bin:/opt/ohpc/pub/libs/hwloc/bin:/opt/ohpc/pub/mpi/openmpi4-gnu12/4.1.4/bin:/opt/ohpc/pub/compiler/gcc/12.2.0/bin:/opt/ohpc/pub/utils/prun/2.2:/opt/ohpc/pub/utils/autotools/bin:/opt/ohpc/pub/bin:/home/iu/.local/bin:/home/iu/bin:/opt/ohpc/pub/apps/anaconda3/condabin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/var/lib/snapd/snap/bin:/home/software/bin:/home/software/git/CCMpred/bin:/home/software/git/hh-suite/build/bin:/home/software/git/hh-suite/build/scripts:/home/software/git/gremlin3/bin:/home/software/zdock3.0.2_linux_x64:/opt/dell/srvadmin/bin:/home/iu/nemo/ngc-cli:/home/software/bin:/home/software/git/CCMpred/bin:/home/software/git/hh-suite/build/bin:/home/software/git/hh-suite/build/scripts:/home/software/git/gremlin3/bin:/home/software/zdock3.0.2_linux_x64

# written by Heesoo Ki
# wrapper for sbatch
submit() {
    if [ -n "$job_prev" ]; then
        job_id=$(sbatch --dependency=afterok:$job_prev "$@" | sed 's/Submitted batch job //')
    else
        job_id=$(sbatch "$@" | sed 's/Submitted batch job //')
    fi
    echo $job_id # the "return" value
    echo $job_id >>/dev/stderr
}

set -e
"""

script_content_2 = f"""
# Inputs to change:
TARGET="{target_id}"
CHAIN="{chains_string}"
FASTA_PATH="/home/casp16/run/TS.human/{target_id}/target.fasta"
RAW_DATA_DIR="/home/casp16/run/TS.human/{target_id}/target.decoys"
MER="{mer}" # monomer or multimer
SUBMIT_FORMAT="/home/casp16/run/TS.human/{target_id}/submit_template.txt" # path to submit template (ref: CASP16 homepage)
"""

script_content_3 = """
# Inputs:
BASE_DIR="/home/casp16/run/TS.human/${TARGET}"
NODE="gpu"
NODE_CPU="cpu"
CPU="4"
MEM="46"
DATA_DIR="/home/fullmoon/software/af2rank/"
RUN_SCRIPT_DIR="/home/casp16/run/TS.human/T2201/utils/"


############################################################
# 1. AF2Rank set-up
############################################################

job_prev=$(submit -p $NODE_CPU -c $CPU --mem=${MEM}g -w node01 \
    -J "${TARGET}.AF2Rank_setup" \
    -o "stdout" \
    -e "stderr" \
    --wrap="source ~/.bashrc; conda activate base; \
            echo \\"Preparing AF2Rank\\"; \
            python /home/iu/casp16/python/prepare_AF2Rank_advanced.py \
            --base_dir $BASE_DIR \
            --decoy_data_dir $RAW_DATA_DIR \
            --chain_list $CHAIN \
            --state $MER")

############################################################
# 2. Run AF2Rank
############################################################

# run with AF version
job_prev=$(submit -p $NODE -c $CPU --mem=${MEM}g --gres=gpu:A5000:1 \
    -J "${TARGET}.AF2Rank.AF" \
    -o "${BASE_DIR}/Massivefold.AF2Rank/ver.AF/%x.out" \
    -e "${BASE_DIR}/Massivefold.AF2Rank/ver.AF/%x.err" \
    --chdir="${BASE_DIR}/Massivefold.AF2Rank/ver.AF" \
    --wrap="set -e; \
            source ~/.bashrc; \
            conda activate af2rank; \
            python3 /home/fullmoon/software/af2rank/revised_af2rank_no_native_xTag.py --data_dir ${DATA_DIR} --chain ${CHAIN} --decoy_dir ${BASE_DIR}/Massivefold.AF2Rank/inputs --output_dir ${BASE_DIR}/Massivefold.AF2Rank/ver.AF ; \
            conda deactivate")

############################################################
# 3. Get rank from AF2Rank outputs
############################################################

job_prev=$(submit -p $NODE_CPU -c $CPU --mem=${MEM}g -w node01 \
    -J "${TARGET}.get.rank.AF" \
    -o "stdout" \
    -e "stderr" \
    --chdir="${BASE_DIR}/Massivefold.AF2Rank/ver.AF" \
    --wrap="source ~/.bashrc; conda activate base; \
            echo \\"Ranking AF2Rank outputs\\"; \
            python $RUN_SCRIPT_DIR/get_rank_from_output.py ${BASE_DIR}/Massivefold.AF2Rank/ver.AF/${TARGET}.AF2Rank.AF.out")

############################################################
# 4. Colabfold set-up
############################################################

job_prev=$(submit -p $NODE_CPU -c $CPU --mem=${MEM}g -w node01 \
    -J "${TARGET}.Colabfold_setup" \
    -o "stdout" \
    -e "stderr" \
    --chdir="${BASE_DIR}/Massivefold.AF2Rank" \
    --wrap="source ~/.bashrc; conda activate base; \
            echo \\"Preparing Colabfold\\"; \
            python /home/iu/casp16/python/prepare_ColabFold_advanced.py --base_dir $BASE_DIR --state $MER")

############################################################
# 5. Run Colabfold
############################################################

job_prev=$(submit -p $NODE -c $CPU --mem=${MEM}g --gres=gpu:A5000:1 \
    -J "${TARGET}.Colabfold" \
    -o "${BASE_DIR}/Massivefold.colabfold/%x.out" \
    -e "${BASE_DIR}/Massivefold.colabfold/%x.err" \
    --chdir="${BASE_DIR}/Massivefold.colabfold" \
    --wrap="set -e; \
            source /home/mink/.bashrc; \
            conda activate colabfold; \
            colabfold_batch ${FASTA_PATH} --num-recycle 20 --recycle-early-stop-tolerance 0.5 --num-seeds 10 --templates --custom-template-path ${BASE_DIR}/Massivefold.colabfold/templates ${BASE_DIR}/Massivefold.colabfold/model ; \
            conda deactivate")

############################################################
# 6. Emin setup (Select models from Colabfold outputs)
############################################################

job_prev=$(submit -p $NODE_CPU -c $CPU --mem=${MEM}g -w node01 \
    -J "${TARGET}.Emin_setup" \
    -o "stdout" \
    -e "stderr" \
    --chdir="${BASE_DIR}/Massivefold.colabfold" \
    --wrap="source ~/.bashrc; conda activate base; \
            echo \\"Preparing Emin\\"; \
            python /home/iu/casp16/python/prepare_Emin_advanced.py --base_dir $BASE_DIR --state $MER")

############################################################
# 7. Energy minimization
############################################################

job_prev=$(submit -p $NODE_CPU -c $CPU --mem=${MEM}g -w node01 \
    -J "${TARGET}.Emin" \
    -o "stdout" \
    -e "stderr" \
    --chdir="${BASE_DIR}/models_before_Emin" \
    --wrap="source /home/mink/.bashrc; conda activate RFdiffusion; \
            echo \\"Running Emin\\"; \
            python /home/casp16/run/TS.human/T2201/utils/str_relax_for_dir.py -pdb_dir /home/casp16/run/TS.human/${TARGET}/models_before_Emin -out_prefix /home/casp16/run/TS.human/${TARGET}/models_before_Emin/E_MIN; \
            echo \\"All files processed.\\"")

############################################################
# 8. Prepare submit
############################################################

job_prev=$(submit -p $NODE_CPU -c $CPU --mem=${MEM}g -w node01 \
    -J "${TARGET}.prepare.submit" \
    -o "stdout" \
    -e "stderr" \
    --chdir="${BASE_DIR}" \
    --wrap="source ~/.bashrc; conda activate base; \
            echo \\"Preparing Submit\\"; \
            python $RUN_SCRIPT_DIR/prepare_submit.py --base_dir $BASE_DIR")

############################################################
# 9. Match format for CASP16
############################################################

job_prev=$(submit -p $NODE_CPU -c $CPU --mem=${MEM}g -w node01 \
    -J "${TARGET}.match.format" \
    -o "stdout" \
    -e "stderr" \
    --chdir="${BASE_DIR}" \
    --wrap="source ~/.bashrc; conda activate base; \
            echo \\"Matching Format\\"; \
            python -u /home/casp16/run/TS.human/T2201/utils/fix_to_submit_format_revised.py --model_dir $BASE_DIR/pre.model.human --format_pdb $SUBMIT_FORMAT --output_dir $BASE_DIR/model.human")

job_prev=$(submit -p $NODE_CPU -c $CPU --mem=${MEM}g -w node01 \
    -J "${TARGET}.match.format" \
    -o "stdout" \
    -e "stderr" \
    --chdir="${BASE_DIR}" \
    --wrap="source ~/.bashrc; conda activate base; \
            echo \\"Matching Format\\"; \
            python -u /home/casp16/run/TS.human/T2201/utils/fix_to_submit_format_revised.py --model_dir $BASE_DIR/pre.model.faker --format_pdb $SUBMIT_FORMAT --output_dir $BASE_DIR/model.faker; \
            sbatch /home/iu/casp16/extra/send_telegram.sh \\"Phase 2 run for ${TARGET} has FINISHED!\\"")
"""

# Define the file name for the .sh file
script_filename = f'/home/casp16/run/TS.human/{target_id}/run_phase2_{target_id}.sh'

# Write the script content to the .sh file
with open(script_filename, 'w') as file:
    file.write(script_content_1)
    file.write(script_content_2)
    file.write(script_content_3)

# Make the .sh file executable
os.chmod(script_filename, 0o755)
