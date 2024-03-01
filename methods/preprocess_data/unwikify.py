import penman
from penman.graph import Graph

def unwikify(args):
    with open(args.file, 'r') as file:
        old_graphs = penman.loads(file)
        new_graphs = []
        for g in old_graphs:
            new_triples = []
            for triple in g.triples:
                if triple[1] != ':wiki':
                    new_triples.append(triple)
            new_g = Graph(new_triples)
            new_g.metadata = g.metadata
            new_graphs.append(new_g)
    with open(args.file.replace('.txt','_unwiki.txt'), 'w') as file:
        file.write(penman.dumps(new_graphs))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = "Remove wiki from AMRs")
    parser.add_argument('-f','--file', metavar = 'data path', type = str, help = 'Data Path')
    args = parser.parse_args()
    unwikify(args)