#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <TARGET ID>"
  exit 1
fi

TARGET_ID="$1"

if [[ ${TARGET_ID:1:1} -ne 2 ]]; then
  echo "Error: The first number after the prefix must be 2."
  exit 1
fi

python /home/iu/casp16/python/prepare_phase2_run.py $1

PHASE1_TARGET_ID="${TARGET_ID:0:1}1${TARGET_ID:2}"

# Set the variables
URL="https://casp-capri.sinbios.plbs.fr/index.php/s/TTqScLKZM5W6ZFi/download?path=%2F&files=${PHASE1_TARGET_ID}_MassiveFold.tar.gz"
TARGET_DIR="/home/casp16/run/TS.human/${TARGET_ID}"
TAR_FILE="${TARGET_DIR}/${PHASE1_TARGET_ID}_MassiveFold.tar.gz"

mkdir -p "${TARGET_DIR}"

curl -L "${URL}" -o "${TAR_FILE}"

tar -xzvf "${TAR_FILE}" -C "${TARGET_DIR}"
mv "${TARGET_DIR}/${PHASE1_TARGET_ID}" "${TARGET_DIR}/target.decoys"

echo "File downloaded and extracted to ${TARGET_DIR}/target.decoys"

bash "run_phase2_${TARGET_ID}.sh"

sbatch /home/iu/casp16/extra/send_telegram.sh "Phase 2 run for ${TARGET_ID} has now finished"
