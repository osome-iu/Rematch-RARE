import argparse
import os
import pandas as pd
import numpy as np
from scipy import stats

def stseval(args):
	for split_type in ['test']:#,'train','dev'
		data = pd.read_csv(os.path.join(args.datapath,f'sts-{split_type}.csv'), sep = '\t', names = ['genre', 'subgenre', 'filename','year','score','sentence1','sentence2'], encoding = 'utf-8', quoting = 3)
		ground_truth = data['score']
		# try:
		predicted = np.load(os.path.join(args.amrpath, f"{split_type}_sentences1_{args.parser}_{args.mode}_scores.npy"))
		corr = stats.spearmanr(predicted, ground_truth)
		print(f"Correlation for {split_type} {args.parser} {args.mode} = {corr.correlation}")
		# except:
		# 	print("Exception, nan detected")

if __name__== "__main__":
	parser=argparse.ArgumentParser(description = 'Parse Graphs')
	parser.add_argument('-dp','--datapath', metavar = 'data path', type = str, help = 'Data Path', default = 'data/raw/stsbenchmark/')
	parser.add_argument('-ap','--amrpath', metavar = 'amr path', type = str, help = 'Amr Path', default = 'data/amrs/sts/')
	parser.add_argument('-m','--mode', metavar = 'mode', type = str, help = 'If smatch/sembleu/rematch etc', default = 'rematch')
	parser.add_argument('-p','--parser', metavar = 'parser', type = str, help = 'If spring/amrbart etc', default = 'AMR3-joint-ontowiki-seed42')
	args=parser.parse_args()
	stseval(args)