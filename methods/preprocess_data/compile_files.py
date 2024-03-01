import penman
from penman.graph import Graph
import os

def compile_files(args):
    all_graphs = []
    for split in ['train','test','dev']:
        with open(os.path.join(args.datapath, f'{split}_unwiki.txt'), 'r') as file:
            all_graphs += [g for g in penman.loads(file)]
    with open(os.path.join(args.datapath, f'all_unwiki.txt'), 'w') as file:
        file.write(penman.dumps(all_graphs))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = "Remove wiki from AMRs")
    parser.add_argument('-dp','--datapath', metavar = 'data path', type = str, help = 'Data Path', default = 'data/processed/AMR3.0')
    args = parser.parse_args()
    compile_files(args)