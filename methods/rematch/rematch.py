#!/usr/bin/env python
import numpy as np
import pandas as pd
from collections import Counter
import time
import amr
import networkx as nx
import itertools
import json

def normalize(item):
    """
    lowercase and remove quote signifiers from items that are about to be compared
    """
    return item.lower().rstrip('_')

def generate_amr_lines(f1, f2):
    """
    Read one AMR line at a time from each file handle
    :param f1: file handle (or any iterable of strings) to read AMR 1 lines from
    :param f2: file handle (or any iterable of strings) to read AMR 2 lines from
    :return: generator of cur_amr1, cur_amr2 pairs: one-line AMR strings
    """
    while True:
        cur_amr1 = amr.AMR.get_amr_line(f1)
        cur_amr2 = amr.AMR.get_amr_line(f2)
        if not cur_amr1 and not cur_amr2:
            pass
        elif not cur_amr1:
            print("Error: File 1 has less AMRs than file 2")
            print("Ignoring remaining AMRs")
        elif not cur_amr2:
            print("Error: File 2 has less AMRs than file 1")
            print("Ignoring remaining AMRs")
        else:
            yield cur_amr1, cur_amr2
            continue
        break

def generate_attribute_motifs(attribute, instance):
    # format : {'a0':[('color','red'),('quant','1')]}
    # initializing attribute dict with list values using keys from instances
    attribute_motifs = {inst[1]: [] for inst in instance}
    # collecting attribute motifs for canonical keys
    for attr in attribute:
        attribute_motifs[attr[1]].append(tuple([normalize(attr[0]), normalize(attr[2])]))
    # sorting by str to maintain ordered partions of attributes
    sorted_attribute_motifs = {attr: sorted(attribute_motifs[attr], key = str) for attr in attribute_motifs}
    return sorted_attribute_motifs

def generate_instance_motifs(instance, attribute_motifs, pb2va):
    # format : {'a0':['car',('mode','red'),('quant','1')]}
    # collecting instance motifs for canonical keys
    # no need to sort as attributes are already sorted
    instance_motifs = {inst[1]: [] for inst in instance}
    for inst in instance:
        label = normalize(inst[2])
        if label in pb2va:
            # if label in verbatlas changing from propbank to va label
            label = pb2va[label]['label']
        if len(attribute_motifs[inst[1]]) > 0:
            for attribute_motif in attribute_motifs[inst[1]]:
                instance_motifs[inst[1]].append(tuple([label, attribute_motif]))
        else:
            instance_motifs[inst[1]].append(tuple([label]))
    return instance_motifs

def generate_relation_motifs(relation, instance_motifs, pb_nodes):
    # format : {'a0':['car',('mode','red'),('quant','1')]}
    # collecting instance motifs for canonical keys
    # no need to sort as attributes are already sorted
    relation_motifs = {(rel[1], rel[2]):[] for rel in relation}
    for rel in relation:
        rel_label = rel[0]
        source = rel[1]
        target = rel[2]
        # if source in pb_nodes:
        source_motifs = instance_motifs[source]
        target_motifs = instance_motifs[target]
        for inst1 in source_motifs:
            for inst2 in target_motifs:
                relation_motifs[(source, target)].append(tuple([inst1, rel_label, inst2]))
    return relation_motifs

def flatten(l):
    return [item for sublist in l for item in sublist]

def generate_amr_motifs(attributes, instance, relation, pb, pb2va):
    # remove 'top' from attributes
    attributes = [attr for attr in attributes if attr[2] != 'top']
    # collecting ordered attribute motifs
    attribute_motifs = generate_attribute_motifs(attributes, instance)
    # collecting ordered instance motifs
    pb_nodes = set([inst[1] for inst in instance if inst[2] in pb])
    instance_motifs = generate_instance_motifs(instance, attribute_motifs, pb2va)
    # collecting relation motifs
    relation_motifs = generate_relation_motifs(relation, instance_motifs, pb_nodes)
    # collecting all motifs
    motifs = flatten(attribute_motifs.values()) + flatten(instance_motifs.values()) + flatten(relation_motifs.values())
    # typecasting motifs to str
    motifs = list(map(str, motifs))
    return motifs

def get_amr_match(cur_amr1, cur_amr2, pb, pb2va, sent_num):
    amr_pair = []
    for i, cur_amr in (1, cur_amr1), (2, cur_amr2):
        try:
            amr_pair.append(amr.AMR.parse_AMR_line(cur_amr))
        except Exception as e:
            print("Error in parsing amr %d: %s" % (i, cur_amr))
            print("Please check if the AMR is ill-formatted. Ignoring remaining AMRs")
            print("Error message: %s" % e)
    amr1, amr2 = amr_pair
    prefix1 = "a"
    prefix2 = "b"
    # Rename node to "a1", "a2", .etc
    amr1.rename_node(prefix1)
    # Renaming node to "b1", "b2", .etc
    amr2.rename_node(prefix2)
    (instance1, attributes1, relation1) = amr1.get_triples()
    (instance2, attributes2, relation2) = amr2.get_triples()

    # starting time
    cur_time = time.time()
    motifs1 = generate_amr_motifs(attributes1, instance1, relation1, pb, pb2va)
    motifs2 = generate_amr_motifs(attributes2, instance2, relation2, pb, pb2va)

    # taking intersection and union of motifs from both AMRs
    intersect_motifs = set(motifs1).intersection(set(motifs2))
    union_motifs = set(motifs1).union(set(motifs2))

    search_space = len(motifs1) * len(motifs2)
    numerator = len(intersect_motifs)
    denominator = len(union_motifs)
    runtime = time.time() - cur_time
    return numerator, denominator, instance1, instance2, attributes1, attributes2, relation1, relation2, search_space, runtime

def score_amr_pairs(f1, f2, pb, pb2va, multiscore):
    """
    Score one pair of AMR lines at a time from each file handle
    :param f1: file handle (or any iterable of strings) to read AMR 1 lines from
    :param f2: file handle (or any iterable of strings) to read AMR 2 lines from
    :param max_depth: max depth upto which semantic graphs are mined to
    :return: generator of cur_amr1, cur_amr2 pairs: one-line AMR strings
    """
    # Read amr pairs from two files
    total_numerator = 0
    total_denominator = 0
    for sent_num, (cur_amr1, cur_amr2) in enumerate(generate_amr_lines(f1, f2), start=1):
        numerator, denominator, instance1, instance2, attributes1, attributes2, relation1, relation2, search_space, runtime = get_amr_match(cur_amr1, cur_amr2, pb, pb2va, sent_num)
        total_numerator += numerator
        total_denominator += denominator
        if multiscore:
            if numerator:
                score = numerator/denominator
            else:
                score = 0
            yield score, instance1, instance2, attributes1, attributes2, relation1, relation2, search_space, runtime
    if not multiscore:
        score = total_numerator/total_denominator
        yield  score, None, None, None, None, None, None, None, None

def main(args):
    """
    Main function of rematch score calculation
    """
    with open(args.pb, 'r') as f:
        pb = set([frame.strip() for frame in f.readlines()])
    with open(args.va, 'r') as f:
        pb2va = json.load(f)
    scores = []
    instance1_count = []
    instance2_count = []
    attributes1_count = []
    attributes2_count = []
    relation1_count = []
    relation2_count = []
    triples1_count = []
    triples2_count = []
    search_spaces = []
    times = []
    ns = []
    f0 = open(args.f[0], 'r')
    f1 = open(args.f[1], 'r')
    suffix = ""
    for score, instance1, instance2, attributes1, attributes2, relation1, relation2, search_space, runtime in score_amr_pairs(f0, f1, pb, pb2va, args.ms):
        scores.append(score)
        times.append(runtime)
        search_spaces.append(search_space)
        instance1_count.append(len(instance1))
        instance2_count.append(len(instance2))
        attributes1_count.append(len(attributes1))
        attributes2_count.append(len(attributes2))
        relation1_count.append(len(relation1))
        relation2_count.append(len(relation2))
        t1 = len(instance1) + len(attributes1) + len(relation1)
        t2 = len(instance2) + len(attributes2) + len(relation2)
        triples1_count.append(t1)
        triples2_count.append(t2)
        ns.append((t1 + t2)/2)
        if not args.ms:
            print(f"Overlap score: {score}")
    f0.close()
    f1.close()
    df = pd.DataFrame({'scores':scores, 'time':times, 'search_spaces': search_spaces, 'instance1_count': instance1_count, 'instance2_count': instance2_count, 'attributes1_count': attributes1_count,'attributes2_count': attributes2_count, 'relation1_count': relation1_count, 'relation2_count': relation2_count, 'triples1_count': triples1_count, 'triples2_count': triples2_count, 'n':ns})
    name = f"{args.f[0].split('.txt')[0]}_rematch{suffix}_scores.npy"
    df_name = f"{args.f[0].split('.txt')[0]}_rematch{suffix}_data.csv"
    # print("\n".join(str(pr) for pr in scores))
    np.save(name, scores)
    df.to_csv(df_name, index = False)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Jaccard Match")
    parser.add_argument(
        '-f',
        nargs=2,
        default=['/N/scratch/zkachwal/amr3_data/all_gold_unwiki_500k_1.txt', '/N/scratch/zkachwal/amr3_data/all_gold_unwiki_500k_2.txt'],
        type=str,
        help=('Two files containing AMR pairs. '
              'AMRs in each file are separated by a single blank line'))
    parser.add_argument(
        '--ms',
        action='store_true',
        default=False,
        help=('Output multiple scores (one AMR pair a score) '
              'instead of a single document-level smatch score '
              '(Default: false)'))
    parser.add_argument(
        '--pb',
        default='/N/scratch/zkachwal/propbank-frames.txt',
        help=('Path to file containing Propbank frames'))
    parser.add_argument(
        '--va',
        default='/N/scratch/zkachwal/VerbAtlas/pb2va.json',
        help=('Path to file containing Verbatlas mappings'))
    args = parser.parse_args()
    main(args)