# 1. Evaluate metrics on test set
echo "sts test $1 $2"
python "methods/$1/$1.py" --ms -f "data/amrs/sts/test_sentences1_$2.txt" "data/amrs/sts/test_sentences2_$2.txt"
echo "sick test $1 $2"
python "methods/$1/$1.py" --ms -f "data/amrs/sick/TEST_sentences1_$2.txt" "data/amrs/sick/TEST_sentences2_$2.txt"
# 2. Print Correlations
python "experiments/semantic_consistency/stseval.py" -m $1 -p $2
python "experiments/semantic_consistency/sickeval.py" -m $1 -p $2