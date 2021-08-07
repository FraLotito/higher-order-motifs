import pickle
import numpy as np
from pandas.core.algorithms import diff
from utils import avg, diff_sum, z_score, count, norm_vector
import sys

N = int(sys.argv[1])
assert(N == 3 or N == 4)
REVERSED = True

M = {}
with open('motifs_{}.pickle'.format(N), 'rb') as handle:
    M = pickle.load(handle)

datasets = ['gene', 'ndcclasses', 'ndcsub', 'DAWN', 'workplace', 'hs', 'ps', 'haggle', 'hospital', 'justice', 'congress', 'wiki', 'babbuini', 'enron', 'EU', 'dblp', 'history', 'geology', 'PACS']

socio = ['workplace', 'hs', 'ps', 'hospital', 'babbuini', 'justice', 'wiki', 'enron', 'EU', 'conference']
collab = ['dblp', 'history', 'geology', 'gene', 'ndcclasses', 'ndcsub']

def print_domain(a):
    dataset = []
    d = {}

    if a == 'BIO':
        dataset = bio
    elif a == 'VOTERS':
        dataset = voters
    elif a == 'TECH':
        dataset = tech
    elif a == 'SOCIO':
        dataset = socio
    else:
        dataset = collab
    
    print('\n ----- {} -----'.format(a))
    for data in dataset:
        try:
            with open('results_ho/{}_{}.pickle'.format(data, N), 'rb') as handle:
                d[data] = pickle.load(handle)
                k = d[data]['motifs']
                """
                for i in k:
                    if i[1] > 0:
                        print(i)
                """
                d[data]['score'] = norm_vector(diff_sum(d[data]['motifs'], d[data]['config_model']))
                #d[data]['score'] = norm_vector(z_score(d[data]['motifs'], d[data]['config_model']))
                #d[data]['score'] = count(d[data]['motifs'])
        except:
            pass
    
    if a != 'SOCIO':
        for n in range(10):
            try:
                with open('single_PACS/PACS{}_{}.pickle'.format(n, N), 'rb') as handle:
                    k = n
                    d[k] = pickle.load(handle)
                    d[k]['score'] = norm_vector(diff_sum(d[k]['motifs'], d[k]['config_model']))
                    
                    #d[k]['score'] = norm_vector(z_score(d[k]['motifs'], d[k]['config_model']))
                    #d[data]['score'] = count(d[data]['motifs'])
            except:
                pass

    scores = {}
    for k in d:
        scores[k] = list(d[k]['score'])

    average = {}
    for k in d:
        for i in range(len(d[k]['score'])):
            item = d[k]['score'][i]
            if i in average:
                average[i].append(item)
            else:
                average[i] = [item]

    for k in average:
        average[k] = sum(average[k]) / len(average[k])

    average = dict(sorted(average.items(), key=lambda item: round(item[1],2), reverse=REVERSED))
    cont = 0
    for k in average:
        if cont < 6:
            print(round(average[k],2), M[k])
            cont += 1
        else:
            break

def print_PACS():
    print('\n ----- PACS -----')
    d = {}
    for n in range(10):
        try:
            with open('single_PACS/PACS{}_{}.pickle'.format(n, N), 'rb') as handle:
                k = n
                d[k] = pickle.load(handle)
                d[k]['score'] = norm_vector(diff_sum(d[k]['motifs'], d[k]['config_model']))
                
                #d[k]['score'] = norm_vector(z_score(d[k]['motifs'], d[k]['config_model']))
                #d[data]['score'] = count(d[data]['motifs'])
        except:
            pass

    scores = {}
    for k in d:
        scores[k] = list(d[k]['score'])

    average = {}
    for k in d:
        for i in range(len(d[k]['score'])):
            item = d[k]['score'][i]
            if i in average:
                average[i].append(item)
            else:
                average[i] = [item]

    for k in average:
        average[k] = sum(average[k]) / len(average[k])

    average = dict(sorted(average.items(), key=lambda item: item[1], reverse=REVERSED))
    cont = 0
    for k in average:
        if cont < 6:
            print(round(average[k],2), M[k])
            cont += 1
        else:
            break

domains = ['SOCIO', 'COLLAB']
for d in domains:
    print_domain(d)
#print_PACS()
