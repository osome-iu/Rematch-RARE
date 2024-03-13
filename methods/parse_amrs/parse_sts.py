import json
import codecs
import os
import argparse
import pandas as pd
import sys
from transition_amr_parser.parse import AMRParser

def sts2graph(args):
	in_data_path = args.indatapath
	out_data_path = args.outdatapath
	for split_type in ['test', 'train', 'test']:
		data = pd.read_csv(os.path.join(in_data_path,f'sts-{split_type}.csv'), sep = '\t', names = ['genre', 'subgenre', 'filename','year','score','sentence1','sentence2'], encoding = 'utf-8', quoting = 3, on_bad_lines=lambda x: x[:-2], engine = 'python')
		for model in ['AMR3-structbart-L-smpl', 'AMR3-joint-ontowiki-seed42']: 
			parser = AMRParser.from_pretrained(model)
			tokens1 = []
			tokens2 = []
			for i, row in list(data.iterrows()):
				sentence1 = row[f'sentence1']
				tokens1_, positions1 = parser.tokenize(sentence1)
				tokens1.append(tokens1_)
				sentence2 = row[f'sentence2']
				tokens2_, positions2 = parser.tokenize(sentence2)
				tokens2.append(tokens2_)

			annotations1, decoding_data1 = parser.parse_sentences(tokens1)
			with codecs.open(os.path.join(out_data_path, f'{split_type}_sentences1_{model}.txt'),  "w", "utf-8") as f1:
				for d1 in decoding_data1:
					amr1 = d1.get_amr().to_penman(jamr = False, isi = False)
					f1.write(amr1)
					f1.write("\n")

			annotations2, decoding_data2 = parser.parse_sentences(tokens2)
			with codecs.open(os.path.join(out_data_path ,f'{split_type}_sentences2_{model}.txt'),  "w", "utf-8") as f2:
				for d2 in decoding_data2:
					amr2 = d2.get_amr().to_penman(jamr = False, isi = False)
					f2.write(amr2)
					f2.write("\n")

if __name__== "__main__":
	parser=argparse.ArgumentParser(description = 'Parse Graphs')
	parser.add_argument('-ip','--indatapath', metavar = 'in data path', type = str, help = 'In Data Path', default = 'data/raw/stsbenchmark')
	parser.add_argument('-op','--outdatapath', metavar = 'out data path', type = str, help = 'Out Data Path', default = 'data/amrs/sts')
	args=parser.parse_args()
	sts2graph(args)