#!/bin/bash
#SBATCH -A r00274
#SBATCH -J parse_amrbart_amr
#SBATCH -p gpu
#SBATCH -o parse_amrbart_amr_%j.txt
#SBATCH -e parse_amrbart_amr_%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=zoher.kachwala@gmail.com
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
#SBATCH --mem=24G
#SBATCH --time=4:00:00
source /N/u/zkachwal/Carbonate/miniconda3/etc/profile.d/conda.sh
conda activate amrbart

export CUDA_VISIBLE_DEVICES=0

Dataset=examples

BasePath=/mnt/nfs-storage/data                    # change dir here
DataPath=$1/../$Dataset

ModelCate=AMRBART-large

MODEL=xfbai/AMRBART-large-finetuned-AMR3.0-AMRParsing-v2
ModelCache=$BasePath/.cache
DataCache=$DataPath/.cache/dump-amrparsing

lr=1e-5

OutputDir=$1/fine-tune/data_interface/
export HF_DATASETS_CACHE=$DataCache

if [ ! -d ${DataCache} ];then
  mkdir -p ${DataCache}
fi

for split in test train dev; do
    for num in 1 2; do
        cp -r data/processed/sts/$split\_sent$num.jsonl $1/fine-tune/data_interface/
        python -u $1/fine-tune/main.py \
            --data_dir . \
            --task "text2amr" \
            --test_file $split\_sent$num.jsonl \
            --output_dir $OutputDir \
            --cache_dir $ModelCache \
            --data_cache_dir $DataCache \
            --overwrite_cache True \
            --model_name_or_path $MODEL \
            --overwrite_output_dir \
            --unified_input True \
            --per_device_eval_batch_size 16 \
            --max_source_length 400 \
            --max_target_length 1024 \
            --val_max_target_length 1024 \
            --generation_max_length 1024 \
            --generation_num_beams 5 \
            --predict_with_generate \
            --smart_init False \
            --use_fast_tokenizer False \
            --logging_dir $OutputDir/logs \
            --seed 42 \
            --fp16 \
            --fp16_backend "auto" \
            --dataloader_num_workers 8 \
            --eval_dataloader_num_workers 2 \
            --include_inputs_for_metrics \
            --do_predict \
            --ddp_find_unused_parameters False \
            --report_to "tensorboard" \
            --dataloader_pin_memory True 2>&1 | tee $OutputDir/run.log
        mv $1/fine-tune/data_interface/val_outputs/test_generated_predictions_0.txt data/amrs/sts/$split\_sentences$num\_amrbart.txt
        python methods/preprocess_data/unwikify.py -f data/amrs/sts/$split\_sentences$num\_amrbart.txt
    done
done

export HF_DATASETS_CACHE=$DataCache

if [ ! -d ${DataCache} ];then
  mkdir -p ${DataCache}
fi

OutputDir=$1/fine-tune/data_interface/

for split in TEST TRAIN TRIAL; do
    for num in 1 2; do
        cp -r data/processed/sick/$split\_sent$num.jsonl $1/fine-tune/data_interface/
        python -u $1/fine-tune/main.py \
            --data_dir . \
            --task "text2amr" \
            --test_file $split\_sent$num.jsonl \
            --output_dir $OutputDir \
            --cache_dir $ModelCache \
            --data_cache_dir $DataCache \
            --overwrite_cache True \
            --model_name_or_path $MODEL \
            --overwrite_output_dir \
            --unified_input True \
            --per_device_eval_batch_size 16 \
            --max_source_length 400 \
            --max_target_length 1024 \
            --val_max_target_length 1024 \
            --generation_max_length 1024 \
            --generation_num_beams 5 \
            --predict_with_generate \
            --smart_init False \
            --use_fast_tokenizer False \
            --logging_dir $OutputDir/logs \
            --seed 42 \
            --fp16 \
            --fp16_backend "auto" \
            --dataloader_num_workers 8 \
            --eval_dataloader_num_workers 2 \
            --include_inputs_for_metrics \
            --do_predict \
            --ddp_find_unused_parameters False \
            --report_to "tensorboard" \
            --dataloader_pin_memory True 2>&1 | tee $OutputDir/run.log
        mv $1/fine-tune/data_interface/val_outputs/test_generated_predictions_0.txt data/amrs/sick/$split\_sentences$num\_amrbart.txt
        python methods/preprocess_data/unwikify.py -f data/amrs/sick/$split\_sentences$num\_amrbart.txt
    done
done