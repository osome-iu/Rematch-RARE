import penman
import os
import numpy as np
from itertools import combinations

def generate_matchups(args):
    all_graphs = penman.load(os.path.join(args.datapath,f'all_unwiki.txt'))
    N = len(all_graphs)
    matchups = list(combinations([*range(N)], 2))
    np.random.seed(0)
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