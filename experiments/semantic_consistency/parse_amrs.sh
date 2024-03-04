#!/bin/bash
#SBATCH -A r00274
#SBATCH -J parse_amrs
#SBATCH -p gpu
#SBATCH -o parse_amrs_%j.txt
#SBATCH -e parse_amrs_%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=zoher.kachwala@gmail.com
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
#SBATCH --mem=24G
#SBATCH --time=3:00:00
errcho(){ >&2 echo $@; }
####################################################################
time python methods/parse_amrs/parse_sts.py
time python methods/parse_amrs/parse_sick.py