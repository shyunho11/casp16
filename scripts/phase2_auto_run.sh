#!/bin/bash
#SBATCH -J Phase2
#SBATCH -p cpu
#SBATCH -c 4
#SBATCH --mem=16g
#SBATCH -w node01
#SBATCH -o log_phase2_%A.log

send_alert() {
    local message="$1"
    sbatch /home/iu/casp16/extra/send_telegram.sh "$message"
}

if [ -z "$1" ]; then
    echo "Usage: $0 <TARGET ID>"
    exit 1
fi

TARGET_ID="$1"

python /home/iu/casp16/python/prepare_Phase2.py "$1"

PHASE1_TARGET_ID="${TARGET_ID:0:1}1${TARGET_ID:2}"

TARGET_DIR="/home/casp16/run/TS.human/${TARGET_ID}"
TAR_FILE="${TARGET_DIR}/${PHASE1_TARGET_ID}_MassiveFold.tar.gz"

mkdir -p "${TARGET_DIR}"
chmod 775 "${TARGET_DIR}"

# Set the variables
CSV_URL="https://casp-capri.sinbios.plbs.fr/index.php/s/TTqScLKZM5W6ZFi/download?path=%2F&files=CASP_MF_links.csv"
CSV_FILE="CASP_MF_links.csv"
URL=$(awk -F, -v target="$PHASE1_TARGET_ID" '$1 == target {print $2}' $CSV_FILE)
rm $CSV_FILE

wget -O "${TAR_FILE}" "${URL}"
if [ $? -ne 0 ]; then
    send_alert "ERROR: Failed to download MassiveFold data from ${URL}"
    exit 1
fi

tar -xzvf "${TAR_FILE}" -C "${TARGET_DIR}"
if [ $? -ne 0 ]; then
    send_alert "ERROR: Failed to extract MassiveFold data in ${TAR_FILE}"
    exit 1
fi

mv "${TARGET_DIR}/${PHASE1_TARGET_ID}" "${TARGET_DIR}/target.decoys"

cd $TARGET_DIR

bash "run_phase2_${TARGET_ID}.sh"

send_alert "Phase 2 run for ${TARGET_ID} has now started!"
