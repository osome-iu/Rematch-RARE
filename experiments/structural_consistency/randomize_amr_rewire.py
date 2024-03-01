import penman
from penman.graph import Graph
import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
font = {'size':15}
matplotlib.rc('font', **font)

def get_graph_data(graph):
    graph_data = {'attributes': set(), 'relations': set()}
    # adding attributes data
    for attribute in graph.attributes():
        graph_data['attributes'].add((attribute.source, attribute.role, attribute.target))
        # we don't care about role_target because attributes roles are always associated with certain values. We don't want to randomize that. ':quant' will always be associated with a number.

    # adding relations data
    for relation in graph.edges():
        graph_data['relations'].add((relation.source, relation.role, relation.target))
    return graph_data

def is_connected(relations):
    graph = nx.Graph()
    graph.add_edges_from([(triple[0], triple[2]) for triple in relations])
    return nx.is_connected(graph)

def is_not_multiedge(relations):
    count = {}
    for triple in relations:
        source, _, target = triple
        edge = (source, target)
        if edge in count:
            count[edge] += 1
        else:
            count[edge] = 1
    max_val = max(list(count.values()))
    return max_val == 1

def is_acyclic_swap(node2height, source1, target1, source2, target2):
    return bool((node2height[source1] == node2height[source2] and source1 != source2) or 
                (node2height[target1] == node2height[target2] and target1 != target2) or 
                (node2height[source1] > node2height[source2] and node2height[source2] >= node2height[target1] and source2 != target1) or 
                (node2height[source2] > node2height[source1] and node2height[source1] >= node2height[target2] and source1 != target2))

# assign height, while also being lenient with cycles
def assign_height(graph):
    digraph = nx.DiGraph()
    digraph.add_edges_from([(edge.source, edge.target) for edge in graph.edges()])
    successors = {node: set() for node in digraph.nodes()}
    for source, target in digraph.out_edges():
        successors[source].add(target)
    postorder = list(nx.dfs_postorder_nodes(digraph))
    height = {node: 0 for node in digraph.nodes()}
    # initializing height 0
    for node in postorder:
        if successors[node]:
            successor_heights = []
            successor_successors = set()
            for s in successors[node]:
                # check if child is not a parent/grand-parent of the current node i.e. not a cyclic relationship.
                # 3% of amrs can have cycles https://github.com/amrisi/amr-guidelines/blob/master/amr.md#cycles
                if s != node and node not in successors[s]:
                    successor_heights.append(height[s])
                    successor_successors = successor_successors.union(successors[s])
            if successor_heights:
                max_height = max(successor_heights)
                height[node] = max_height + 1
                successors[node] = successors[node].union(successor_successors)
    return height

def swap_attribute(attribute1, graph, swapped_graph_data, original_graph_data, current_graph_data):
    attributes = [(attribute.source, attribute.role, attribute.target) for attribute in graph.attributes()]
    instances = [(instance.source, instance.role, instance.target) for instance in graph.instances()]
    relations = [(edge.source, edge.role, edge.target) for edge in graph.edges()]
    
    # shuffling order to randomize attributes
    np.random.seed(0)
    np.random.shuffle(attributes)
    # attribute 1
    source1, role1, target1 = attribute1
    # finding a candidate attribute
    for attribute2 in attributes:
        # attribute 2
        source2, role2, target2 = attribute2
        # new attribute1
        new_attribute1 = (source1, role2, target2)
        # new attribute2
        new_attribute2 = (source2, role1, target1)
        # collecting old and new
        old_attributes = (attribute1, attribute2)
        new_attributes = (new_attribute1, new_attribute2)
        
        updated_attributes = [attribute for attribute in attributes if attribute not in old_attributes] + list(new_attributes)

        # if source-role is not in original graph/current graph, and if source-target is not in original graph/current graph
        if (new_attribute1 not in original_graph_data['attributes'] and new_attribute2 not in original_graph_data['attributes']
            and new_attribute1 not in current_graph_data['attributes'] and new_attribute2 not in current_graph_data['attributes']):
             
            # counting swaps
            for old_attribute in old_attributes:
                # if the old attribute was not in swapped_graph_data already
                if old_attribute not in swapped_graph_data['attributes']:
                    swapped_graph_data['N_total'] += 1
                    swapped_graph_data['N_attributes'] += 1
                else:
                    swapped_graph_data['attributes'].remove(old_attribute)

            for new_attribute in new_attributes:
                swapped_graph_data['attributes'].add(new_attribute)

            # creating a new graph
            new_graph = Graph(updated_attributes + instances + relations)
            return new_graph, swapped_graph_data
    return graph, swapped_graph_data
  
def swap_relation(relation1, graph, swapped_graph_data, original_graph_data, current_graph_data):
    node2height = assign_height(graph)
    attributes = [(attribute.source, attribute.role, attribute.target) for attribute in graph.attributes()]
    instances = [(instance.source, instance.role, instance.target) for instance in graph.instances()]
    relations = [(edge.source, edge.role, edge.target) for edge in graph.edges()]

    # shuffling order to randomize relations
    np.random.seed(0)
    np.random.shuffle(relations)
    # relation 1
    source1, role1, target1 = relation1
    # finding a candidate relation
    for relation2 in relations:
        # relation 1
        source2, role2, target2 = relation2
        # new relation1
        new_relation1 = (source1, role1, target2)
        # new relation2
        new_relation2 = (source2, role2, target1)
        # collecting old and new
        old_relations = (relation1, relation2)
        new_relations = (new_relation1, new_relation2)
        updated_relations = [relation for relation in relations if relation not in old_relations] + list(new_relations)
        
        # if source-role is not in original graph or current graph, and if source-target is not in original graph or current graph and if swap is acyclic, if updated relations still create a connected graph and not multiedges
        if (new_relation1 not in original_graph_data['relations'] and new_relation2 not in original_graph_data['relations']
            and new_relation1 not in current_graph_data['relations'] and new_relation2 not in current_graph_data['relations']
            and is_acyclic_swap(node2height, source1, target1, source2, target2)
            and is_connected(updated_relations)
            and is_not_multiedge(updated_relations)):
            
            # counting swaps
            for old_relation in old_relations:
                '''
                There can be two scenarios. Either a triple was already modified and present in swapped or it is original.
                If it is original, then the changes made by swapping the source should be 2:
                1. breaking (source, _, target) +1
                2. breaking (_, role, target) +1
                But if it is not original, it could be one of two things:
                1. result of swapped target
                2. result of swapped source
                In both cases (source, _, target) would have been modified, so it would be present in swapped +0
                In case 1., even (_, role, target) would have been modified, so it would be present in swapped +0
                In case 2., only (source, role, _) would have been modified, so (_, role, target) would be a new change +1
                '''
                if old_relation not in swapped_graph_data['relations']:
                    swapped_graph_data['N_total'] += 1
                    swapped_graph_data['N_relations'] += 1
                else:
                    swapped_graph_data['relations'].remove(old_relation)
            # addings updates to swapped
            for new_relation in new_relations:
                swapped_graph_data['relations'].add(new_relation)
            
            # creating a new graph
            new_graph = Graph(attributes + instances + updated_relations)
            return new_graph, swapped_graph_data
    return graph, swapped_graph_data
    
def randomize_amrs(args):
    all_graphs = penman.load(os.path.join(args.datapath, f'all_unwiki.txt'))
    noisy_graphs = {'train':[], 'dev': [], 'test': []}
    unoisy_graphs = {'train':[], 'dev': [], 'test': []}
    noisy_labels = {'train':[], 'dev': [], 'test': []}
    noisy_scores = {'train':[], 'dev': [], 'test': []}
    np.random.seed(0)
    np.random.shuffle(all_graphs)
    train_bound = int(0.8 * len(all_graphs))
    dev_bound = train_bound + int(0.1 * len(all_graphs))  
    og_graphs = {'train': len(all_graphs[:train_bound]), 'dev': len(all_graphs[train_bound:dev_bound]), 'test': len(all_graphs[dev_bound:])}
    
    for i, graph in enumerate(all_graphs):
        if i < train_bound:
            mode = 'train'
        elif i < dev_bound:
            mode = 'dev'
        else:
            mode = 'test'
        attributes = [(attribute.source, attribute.role, attribute.target) for attribute in graph.attributes()]
        relations = [(edge.source, edge.role, edge.target) for edge in graph.edges()]
        original_attribute_set = set([(attribute.source, attribute.role, attribute.target) for attribute in graph.attributes()])
        original_relation_set = set([(edge.source, edge.role, edge.target) for edge in graph.edges()])
        # stores all the original data associated for the nodes
        original_graph_data = get_graph_data(graph)
        '''
        recording number of swaps made
        'N_total' : total swaps
        'source_attribute' : swapped (source, attribute.role, attribute.target) patterns
        'source_target' : swapped (source, _, target) patterns
        'source_role' : swapped (source, role, _) patterns
        'role_target' : swapped (source,)
        'targets': triples whose targets were swapped_graph_data
        '''
        swapped_graph_data = {'N_total':0, 'N_attributes':0, 'N_relations':0, 'attributes': set(), 'relations': set()}
        # we only want to swap attributes and relations
        triples2swap = attributes + relations
        possible_swaps = {'total': len(attributes) + len(relations), 'attributes': len(attributes), 'relations': len(relations)}
        np.random.seed(0)
        np.random.shuffle(triples2swap)
        original_metadata = graph.metadata.copy()
        original_graph = graph
        original_label = f'{i}_-1'
        original_score = 1
        original_graph.metadata['label'] = original_label
        original_graph.metadata['score'] = str(original_score)
        original_graph.metadata['swapped_data'] = str(swapped_graph_data)
        original_graph.metadata['possible_swaps'] = str(possible_swaps)
        
        # iterating over triples to swap
        for j, original_triple in enumerate(triples2swap):
            
            cur_swaps = swapped_graph_data['N_total']
            current_graph_data = get_graph_data(graph)
            # if original triple is still an unchanged attribute in the current_graph, rewire
            if original_triple in original_attribute_set:
                if original_triple in current_graph_data['attributes']:
                    graph, swapped_graph_data = swap_attribute(original_triple, graph, swapped_graph_data, original_graph_data, current_graph_data)
                        
            # if the original triple is a relation
            elif original_triple in original_relation_set:
                # check if triple is still unchanged relation in the current graph, rewire
                if original_triple in current_graph_data['relations']:
                    graph, swapped_graph_data = swap_relation(original_triple, graph, swapped_graph_data, original_graph_data, current_graph_data)

            # if new swaps, save the graph and score
            if swapped_graph_data['N_total'] > cur_swaps:
                numerator = float(possible_swaps['total'] - swapped_graph_data['N_total'])
                if numerator > 0:
                    score = numerator / possible_swaps['total']
                else:
                    score = numerator
                graph_label = f"{i}_{j}_{swapped_graph_data['N_total']}"
                graph.metadata = original_metadata.copy()
                graph.metadata['label'] = graph_label
                graph.metadata['score'] = str(score)
                graph.metadata['swapped_data'] = str(swapped_graph_data)
                graph.metadata['possible_swaps'] = str(possible_swaps)
                noisy_labels[mode].append(graph_label)
                noisy_scores[mode].append(score)
                noisy_graphs[mode].append(graph)
                unoisy_graphs[mode].append(original_graph)
        # adding self pair if changes made
        if swapped_graph_data['N_total'] > 0:
            # adding self pair
            noisy_labels[mode].append(original_label)
            noisy_scores[mode].append(original_score)
            noisy_graphs[mode].append(original_graph)
            unoisy_graphs[mode].append(original_graph)

    for mode in ['train', 'dev', 'test']:
        print(f"Graphs count {mode}: {len(noisy_graphs[mode])} pairs from {og_graphs[mode]} original graphs")
        penman.dump(noisy_graphs[mode], os.path.join(args.datapath, f'{mode}_unwiki_noisy_rewire.txt'))
        penman.dump(unoisy_graphs[mode], os.path.join(args.datapath, f'{mode}_unwiki_unoisy_rewire.txt'))
        np.save(os.path.join(args.datapath, f'{mode}_noisy_labels_rewire.npy'), noisy_labels[mode])
        np.save(os.path.join(args.datapath, f'{mode}_noisy_scores_rewire.npy'), noisy_scores[mode])
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AMR randomizer")
    parser.add_argument('-dp','--datapath', metavar = 'data path', type = str,help = 'Data Path',default = 'data/processed/AMR3.0/')
    args = parser.parse_args()
    randomize_amrs(args)