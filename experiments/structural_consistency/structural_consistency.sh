#!/bin/bash
#SBATCH -A r00274
#SBATCH -J struct
#SBATCH -p general
#SBATCH -o struct_%j.txt
#SBATCH -e struct_%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=zoher.kachwala@gmail.com
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=128G
#SBATCH --time=12:00:00
# 1. Evaluate all metrics on RARE test
echo "test $1"
python "methods/$1/$1.py" --ms -f "data/processed/AMR3.0/test_unwiki_unoisy_rewire.txt" "data/processed/AMR3.0/test_unwiki_noisy_rewire.txt"
# 2. Print Correlations
python experiments/structural_consistency/structeval.py -m $1
