# 1. Run a metric on the time testbed
python "methods/$1/$1.py" --ms -f "data/processed/AMR3.0/all_unwiki_500k_1.txt" "data/processed/AMR3.0/all_unwiki_500k_2.txt"
# 2. sum the time
python experiments/efficiency/sum_time.py -m $1