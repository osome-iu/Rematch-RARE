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
    predicted = np.load(os.path.join(data_path, f"test_unwiki_unoisy_rewire_{args.mode}_scores.npy"))
    corr = stats.spearmanr(predicted, ground_truth, nan_policy = 'omit')
    print(f"Correlation for noisy {args.mode} = {corr.correlation}")
    print(f'NaNs: {sum(np.isnan(predicted))}')

if __name__== "__main__":
	parser=argparse.ArgumentParser(description = 'Parse Graphs')
	parser.add_argument('-dp','--datapath', metavar = 'data path', type = str, help = 'Data Path', default = 'data/processed/AMR3.0/')
	parser.add_argument('-m','--mode', metavar = 'mode', type = str, help = 'If smatch/sembleu/rematch etc', default = 'rematch')
	args=parser.parse_args()
	structeval(args)