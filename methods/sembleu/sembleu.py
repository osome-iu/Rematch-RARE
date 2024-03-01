#!/usr/bin/env python3
import pandas as pd
import os, sys, json, time
from bleu_score import corpus_bleu, sentence_bleu, SmoothingFunction, NgramInst
from amr_graph import AMRGraph
import numpy as np
import amr

'''
Original script from: https://github.com/freesunshine0316/sembleu
Modified by Zoher Kachwala to conduct experiments from Rematch (https://github.com/Zoher15/Rematch-RARE)
'''

def read_amr(path):
    ids = []
    id_dict = {}
    amrs = []
    amr_str = ''
    for line in open(path,'r'):
        if line.startswith('#'):
            if line.startswith('# ::id'):
                id = line.strip().split()[2]
                ids.append(id)
                id_dict[id] = len(ids)-1
            continue
        line = line.strip()
        if line == '':
            if amr_str != '':
                amrs.append(amr_str.strip())
                amr_str = ''
        else:
            amr_str = amr_str + line + ' '

    if amr_str != '':
        amrs.append(amr_str.strip())
        amr_str = ''
    return amrs

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

def get_amr_ngrams(path, stat_save_path=None):
    data = []
    if stat_save_path:
        f = open(stat_save_path, 'w')
    for line in read_amr(path):
        try:
            amr = AMRGraph(line.strip())
        except AssertionError:
            print(line)
            assert False
        amr.revert_of_edges()
        ngrams = amr.extract_ngrams(3, multi_roots=True) # dict(list(tuple))
        data.append(NgramInst(ngram=ngrams, length=len(amr.edges)))
        if stat_save_path:
            print(len(amr), len(ngrams[1]), len(ngrams[2]), len(ngrams[3]), file=f)
    if stat_save_path:
        f.close()
    return data

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Smatch calculator")
    parser.add_argument(
        '-f',
        nargs=2,
        default=['/N/scratch/zkachwal/sts_data/test_sentences1_amrbart_unwiki.txt','/N/scratch/zkachwal/sts_data/test_sentences2_amrbart_unwiki.txt'],
        type=str,
        help=('Two files containing AMR pairs. '
              'AMRs in each file are separated by a single blank line'))
    parser.add_argument(
        '--ms',
        action='store_true',
        default=True,
        help=('Output multiple scores (one AMR pair a score) '
              'instead of a single document-level smatch score '
              '(Default: false)'))
    parser.add_argument(
        '-n',
        type=int,
        default=3,
        help=('number of n-grams/ length of random walks'))

    args = parser.parse_args()
    # print('loading ...')
    smoofunc = getattr(SmoothingFunction(), 'method3')
    weights = (1.0/args.n, )*args.n
    
    scores = []
    ref_sizes = []
    hyp_sizes = []
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

    if args.ms:
        f0 = open(args.f[0], 'r')
        f1 = open(args.f[1], 'r')
        for cur_amr1, cur_amr2 in generate_amr_lines(f0, f1):
            # starting time
            cur_time = time.time()
            try:
                amr1 = AMRGraph(cur_amr1.strip())
            except AssertionError:
                print(cur_amr1)
                assert False
            try:
                amr2 = AMRGraph(cur_amr2.strip())
            except AssertionError:
                print(cur_amr2)
                assert False
            amr1.revert_of_edges()
            amr2.revert_of_edges()
            ngrams1 = amr1.extract_ngrams(3, multi_roots=True) # dict(list(tuple))
            ngrams2 = amr2.extract_ngrams(3, multi_roots=True) # dict(list(tuple))
            hyp_i = NgramInst(ngram=ngrams1, length=len(amr1.edges))
            ref_i = NgramInst(ngram=ngrams2, length=len(amr2.edges))
            score = corpus_bleu([[ref_i]], [hyp_i], weights=weights, smoothing_function=smoofunc, auto_reweigh=True)
            # print(score)
            # stopping time
            runtime = time.time() - cur_time
            # recording data
            times.append(runtime)            
            scores.append(score)
            hyp_len = sum(list(map(len, list(hyp_i.ngram.values()))))
            hyp_sizes.append(hyp_len)
            ref_len = sum(list(map(len, list(ref_i.ngram.values()))))
            ref_sizes.append(ref_len)
            search_spaces.append(hyp_len*ref_len)
            # collecting triples
            amr1_ = amr.AMR.parse_AMR_line(cur_amr1)
            amr2_ = amr.AMR.parse_AMR_line(cur_amr2)
            (instance1, attributes1, relation1) = amr1_.get_triples()
            (instance2, attributes2, relation2) = amr2_.get_triples()
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
        f0.close()
        f1.close()
    else:
        hypothesis = get_amr_ngrams(args.f[0])
        references = [[r] for r in get_amr_ngrams(args.f[1])]
        # print(corpus_bleu(references, hypothesis, weights=weights, smoothing_function=smoofunc, auto_reweigh=True))
        scores.append(corpus_bleu(references, hypothesis, weights=weights, smoothing_function=smoofunc, auto_reweigh=True))
    df = pd.DataFrame({'scores':scores, 'time':times, 'ref_sizes': ref_sizes, 'hyp_sizes': hyp_sizes, 'search_spaces': search_spaces, 'instance1_count': instance1_count, 'instance2_count': instance2_count, 'attributes1_count': attributes1_count,'attributes2_count': attributes2_count, 'relation1_count': relation1_count, 'relation2_count': relation2_count, 'triples1_count': triples1_count, 'triples2_count': triples2_count, 'n':ns})
    name = f"{args.f[0].split('.txt')[0]}_sembleu_scores.npy"
    df_name = f"{args.f[0].split('.txt')[0]}_sembleu_data.csv"
    # print("\n".join(str(pr) for pr in scores))
    np.save(name, scores)
    df.to_csv(df_name, index = False)
