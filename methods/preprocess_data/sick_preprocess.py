import json
import codecs
import os
import networkx as nx
import argparse
import pandas as pd
import sys

def sick_preprocess(args):
	in_data_path = args.indatapath
	out_data_path = args.outdatapath
	full_data = pd.read_csv(os.path.join(in_data_path, f'SICK.txt'), sep = '\t', encoding = 'utf-8', quoting = 3)
	for split_type in ['TRAIN', 'TEST', 'TRIAL']:
		data = full_data.loc[full_data['SemEval_set'] == split_type]
		sent1_jsonl = []
		sent2_jsonl = []
		for i, row in list(data.iterrows()):
			sentence1 = row[f'sentence_A']
			sentence2 = row[f'sentence_B']
			sent1_jsonl.append({"sent": sentence1, "amr":""})
			sent2_jsonl.append({"sent": sentence2, "amr":""})
	
		with codecs.open(os.path.join(out_data_path, f'{split_type}_sent1.jsonl'),  "w", "utf-8") as f1:
			for data in sent1_jsonl:
				json.dump(data, f1)
				f1.write("\n")

		with codecs.open(os.path.join(out_data_path ,f'{split_type}_sent2.jsonl'),  "w", "utf-8") as f2:
			for data in sent2_jsonl:
				json.dump(data, f2)
				f2.write("\n")

		with codecs.open(os.path.join(out_data_path ,f'{split_type}_sent1_spring.txt'),  "w", "utf-8") as f1:
			for data in sent1_jsonl:
				f1.write(f"# ::snt {data['sent']}")
				f1.write("\n")
				f1.write("()")
				f1.write("\n\n")

		with codecs.open(os.path.join(out_data_path ,f'{split_type}_sent2_spring.txt'),  "w", "utf-8") as f2:
			for data in sent2_jsonl:
				f2.write(f"# ::snt {data['sent']}")
				f2.write("\n")
				f2.write("()")
				f2.write("\n\n")

if __name__== "__main__":
	parser=argparse.ArgumentParser(description = 'Parse Graphs')
	parser.add_argument('-ip','--indatapath', metavar = 'in data path', type = str, help = 'In Data Path', default = 'data/raw/SICK')
	parser.add_argument('-op','--outdatapath', metavar = 'out data path', type = str, help = 'Out Data Path', default = 'data/processed/sick')
	args=parser.parse_args()
	sick_preprocess(args)