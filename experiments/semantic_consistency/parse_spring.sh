#!/bin/bash
#SBATCH -A r00274
#SBATCH -J parse_spring_amr
#SBATCH -p gpu
#SBATCH -o parse_spring_amr_%j.txt
#SBATCH -e parse_spring_amr_%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=zoher.kachwala@gmail.com
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
#SBATCH --mem=24G
#SBATCH --time=4:00:00
for split in test train dev; do
    for num in 1 2; do
        python $1/bin/predict_amrs.py \
            --datasets data/processed/sts/$split\_sent$num\_spring*.txt \
            --gold-path data/processed/sts/$split\_sent$num\_spring.txt \
            --pred-path data/amrs/sts/$split\_sentences$num\_spring.txt  \
            --checkpoint $1/AMR3.parsing.pt \
            --beam-size 5 \
            --batch-size 200 \
            --device cuda \
            --penman-linearization --use-pointer-tokens
        python methods/preprocess_data/unwikify.py -f data/amrs/sts/$split\_sentences$num\_spring.txt
    done
done

for split in TEST TRAIN TRIAL; do
    for num in 1 2; do
        python $1/bin/predict_amrs.py \
            --datasets data/processed/sick/$split\_sent$num\_spring*.txt \
            --gold-path data/processed/sick/$split\_sent$num\_spring.txt \
            --pred-path data/amrs/sick/$split\_sentences$num\_spring.txt  \
            --checkpoint $1/AMR3.parsing.pt \
            --beam-size 5 \
            --batch-size 200 \
            --device cuda \
            --penman-linearization --use-pointer-tokens
        python methods/preprocess_data/unwikify.py -f data/amrs/sick/$split\_sentences$num\_spring.txt
    done
done

