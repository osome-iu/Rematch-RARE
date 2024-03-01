# 1. move AMR Annotation 3.0 to the raw folder
cp $1/amr_annotation_3.0_LDC2020T02.tgz data/raw/
# 2. unzip AMR Annotation 3.0
tar -xvzf data/raw/amr_annotation_3.0_LDC2020T02.tgz -C data/raw/
# 3. merge files (script from https://github.com/IBM/transition-amr-parser)
python methods/preprocess_data/merge_files.py data/raw/amr_annotation_3.0/data/amrs/split/ data/processed/AMR3.0/
# 4. delete the raw data and tar file
rm data/raw/amr_annotation_3.0_LDC2020T02.tgz
rm -rf data/raw/amr_annotation_3.0/
# 5. remove wiki edges
python methods/preprocess_data/unwikify.py -f data/processed/AMR3.0/train.txt
python methods/preprocess_data/unwikify.py -f data/processed/AMR3.0/test.txt
python methods/preprocess_data/unwikify.py -f data/processed/AMR3.0/dev.txt
# 6. merge all files
python methods/preprocess_data/compile_files.py