#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <AF3 .ZIP directory>"
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "Directory $1 does not exist."
    exit 1
fi

cd $1

for zip_file in *.zip; do
    # Check if there are zip files to extract
    if [ -e "$zip_file" ]; then
        echo "Extracting $zip_file..."
        unzip -o "$zip_file" -d .
    else
        echo "No zip files found in $1"
        exit 0
    fi
done

for mmcif_file in *.cif; do
    echo "Processing $mmcif_file..."
    python /home/iu/casp16/python/af3_to_pdb.py "$mmcif_file"
done

pdb_count=$(ls *.pdb | wc -l)
echo "Complete: processed $pdb_count PDB files."
