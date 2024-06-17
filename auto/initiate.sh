#!/bin/bash
#SBATCH -J AutoCASP
#SBATCH -p cpu
#SBATCH -c 2
#SBATCH --mem=8g
#SBATCH -w node01
#SBATCH -o /home/iu/casp16/auto/log/log_auto_%A.log

source /home/iu/.bashrc

python -u /home/iu/casp16/python/initiate_casp_auto.py
