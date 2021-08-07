import pickle
import numpy as np
from pandas.core.algorithms import diff
from utils import avg, diff_sum, z_score, count, norm_vector
import sys

import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import seaborn as sn

plt.rcParams['font.size'] = 12

datasets = ['gene', 'ndcclasses', 'ndcsub', 'workplace', 'hs', 'ps', 'haggle', 'hospital', 'justice', 'wiki', 'babbuini', 'enron', 'EU', 'dblp96', 'history', 'geology']

def read(N):
    H_O = True
    PACS_OPT = True

    if H_O:
        path = 'results_ho'
    else:
        path = 'results_classic'

    d = {}

    datasets = ['gene', 'ndcclasses', 'ndcsub', 'workplace', 'hs', 'ps', 'haggle', 'hospital', 'justice', 'wiki', 'babbuini', 'enron', 'EU', 'dblp96', 'history', 'geology']

    for data in datasets:
        try:
            with open('{}/{}_{}.pickle'.format(path, data, N), 'rb') as handle:
                d[data] = pickle.load(handle)
                d[data]['score'] = norm_vector(diff_sum(d[data]['motifs'], d[data]['config_model']))
                #d[data]['score'] = norm_vector(z_score(d[data]['motifs'], d[data]['config_model']))
                #d[data]['score'] = count(d[data]['motifs'])
        except:
            pass

    scores = {}
    for k in d:
        scores[k] = list(d[k]['score'])

    if PACS_OPT:
        PACS = {}
        for n in range(10):
            try:
                with open('single_PACS/PACS{}_{}.pickle'.format(n, N), 'rb') as handle:
                    k = 'PACS{}'.format(n)
                    PACS[k] = pickle.load(handle)
                    PACS[k]['score'] = norm_vector(diff_sum(PACS[k]['motifs'], PACS[k]['config_model']))
                    #d[data]['score'] = norm_vector(z_score(d[data]['motifs'], d[data]['config_model']))
                    #d[data]['score'] = count(d[data]['motifs'])
            except:
                pass
        for k in PACS.keys():
            scores[k] = list(PACS[k]['score'])

    import pandas as pd
    #print(pd.DataFrame(scores).corr())

    bio = [0, 1, 2]
    socio = [3, 4, 5, 6,7, 8, 9, 10]
    tech = [11, 12]

    df = pd.DataFrame(scores, columns=list(scores.keys()))
    corr = df.corr()
    return corr

for i in range(10):
    datasets.append('PACS{}'.format(i))

tre = read(3)
quattro = read(4)

s1 = []
s2 = []

bio = [0, 1, 2]
socio = [3, 4, 5, 6,7, 8, 9, 10]
tech = [11, 12]

already = {}

for i in range(len(datasets)):
    for j in range(i+1, len(datasets)):
        a = datasets[i]
        b = datasets[j]

        color = 'blue'
        label = 'Different cluster'

        if (i in bio and j in bio) or (i in socio and j in socio) or (i in tech and j in tech) or (i > 12 and j > 12):
            color = 'red'
            label = 'Same cluster'

        try:
            if label not in already:
                plt.scatter(x = tre[a][b], y = quattro[a][b], color=color, s=20, label=label)
                already[label] = 1
            else:
                plt.scatter(x = tre[a][b], y = quattro[a][b], color=color, s=20)
        except:
            pass

X = np.linspace(-1,1,100)

plt.xlabel('Correlation with motifs of size 3')
plt.ylabel('Correlation with motifs of size 4')
plt.plot(X, X, color='black', linewidth=2.0)
sn.despine()
plt.tight_layout()
plt.legend(frameon=False)
plt.savefig("fig2b.pdf")