import penman
import os
import numpy as np
from itertools import combinations
import math

@profile
def generate_matchups(args):
    all_graphs = penman.load(os.path.join(args.datapath,f'all_unwiki.txt'))
    N = len(all_graphs)
    # matchups_size = math.comb(N,2)
    # np.random.seed(0)
    # graphs1 = []
    # graphs2 = []
    # sample = np.random.choice([*range(matchups_size)], 500000) #500k sample
    # matchups = [m for i, m in enumerate(combinations([*range(N)], 2)) if i in sample]
    # graphs1 = [all_graphs[m[0]] for m in matchups]
    # graphs2 = [all_graphs[m[1]] for m in matchups]
    matchups = list(combinations([*range(N)], 2))
    sample = np.random.choice([*range(len(matchups))], 500000) #500k sample
    graphs1 = [all_graphs[matchups[ind][0]] for ind in sample]
    graphs2 = [all_graphs[matchups[ind][1]] for ind in sample]
    penman.dump(graphs1, os.path.join(args.datapath, f'all_unwiki_500k_1.txt'))
    penman.dump(graphs2, os.path.join(args.datapath, f'all_unwiki_500k_2.txt'))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate AMR Matchups for measuring time complexity")
    parser.add_argument('-dp','--datapath', metavar = 'data path', type = str, help = 'Data Path',default = 'data/processed/AMR3.0/')
    args = parser.parse_args()
    generate_matchups(args)