import argparse
import os
import pandas as pd
import numpy as np
from scipy import stats
import penman

def distance_diagonal(p):
    x, y = p
    return np.abs(x - y)/np.sqrt(2) 

def structeval(args):
    data_path = args.datapath
    ground_truth = np.load(os.path.join(data_path, f"test_noisy_scores_rewire.npy"))
    predicted_rematch = np.load(os.path.join(data_path, f"test_unwiki_unoisy_rewire_{args.mode}_scores.npy"))
    predicted_smatch = np.load(os.path.join(data_path, f"test_unwiki_unoisy_rewire_smatch_scores.npy"))
    rematch_zip = zip(predicted_rematch, ground_truth)
    smatch_zip = zip(predicted_smatch, ground_truth)
    rematch_dist = np.array(list(map(distance_diagonal, rematch_zip)))
    smatch_dist = np.array(list(map(distance_diagonal, smatch_zip)))
    diff_dist = rematch_dist - smatch_dist
    test_noisy = penman.load("/geode2/home/u110/zkachwal/BigRed3/Rematch-RARE/data/processed/AMR3.0/test_unwiki_noisy_rewire.txt")
    test_unoisy = penman.load("/geode2/home/u110/zkachwal/BigRed3/Rematch-RARE/data/processed/AMR3.0/test_unwiki_unoisy_rewire.txt")
    print("Zoher")    
    # corr = stats.spearmanr(predicted_rematch, ground_truth, nan_policy = 'omit')
    # print(f"Correlation for noisy {args.mode} = {corr.correlation}")
    # print(f'NaNs: {sum(np.isnan(predicted))}')

if __name__== "__main__":
	parser=argparse.ArgumentParser(description = 'Parse Graphs')
	parser.add_argument('-dp','--datapath', metavar = 'data path', type = str, help = 'Data Path', default = 'data/processed/AMR3.0/')
	parser.add_argument('-m','--mode', metavar = 'mode', type = str, help = 'If smatch/sembleu/rematch etc', default = 'rematch')
	args=parser.parse_args()
	structeval(args)