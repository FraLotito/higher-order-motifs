import pickle
from numpy.core.fromnumeric import std

from pandas.core.algorithms import diff
from utils import avg, diff_sum, z_score, count, norm_vector

import matplotlib.pyplot as plt
import math

plt.rcParams['font.size'] = 18

N = 4
d = {}

def rotate(l, n):
    return l[n:] + l[:n]

def array_mean(a):
    res = []
    std_dev = []

    for i in range(len(a[0])):
        val = []
        for j in a:
            val.append(j[i])
        res.append(sum(val) / len(val))
        std_dev.append(np.std(val) / (len(a)))
    return (res, std_dev)



datasets = ['gene', 'ndcclasses', 'ndcsub', 'workplace', 'hs', 'ps', 'hospital', 'justice', 'conference', 'wiki', 'babbuini', 'enron', 'EU', 'dblp', 'history', 'geology']

for data in datasets:
    try:
        with open('results_ho/{}_{}.pickle'.format(data, N), 'rb') as handle:
            d[data] = pickle.load(handle)
            d[data]['score'] = norm_vector(diff_sum(d[data]['motifs'], d[data]['config_model']))
            #d[data]['score'] = norm_vector(z_score(d[data]['motifs'], d[data]['config_model']))
            #d[data]['score'] = count(d[data]['motifs'])
    except:
        pass

scores = {}
for k in d:
    scores[k] = list(d[k]['score'])

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

print(scores.keys())

import numpy as np
import matplotlib.pyplot as plt

data = {}
data['Socio'] = ['workplace', 'hs', 'ps', 'conference', 'hospital', 'justice', 'babbuini', 'wiki']
data['Tech'] = ['enron', 'EU']
data['Co-auth'] = ['dblp', 'history', 'geology']
data['Bio'] = ['gene', 'ndcclasses', 'ndcsub']

for i in range(10):
    data['Co-auth'].append("PACS{}".format(i))

# 2-edge, 3-edge
x_labels = ["2-0", "3-0", "0-1", "1-1", "2-1", "3-1"]


uno = ['Socio', 'Tech', 'Co-auth', 'Bio']

# plot cluster singoli
i = 0
res = []
fig, ax = plt.subplots()
for k in ['Socio', 'Tech']:
    if N == 3:
        ax.set_xticks(range(len(x_labels)))
        ax.set_xticklabels(x_labels)

    tmp = []
    for p in data[k]:
        try:
            #ax.plot(d[p]['score'], label=p)
            tmp.append(d[p]['score'])
        except:
            pass

x = array_mean(tmp)
#print(x)
res.append(x)

for k in ['Bio', 'Co-auth']:
    if N == 3:
        ax.set_xticks(range(len(x_labels)))
        ax.set_xticklabels(x_labels)

    tmp = []
    for p in data[k]:
        try:
            #ax.plot(d[p]['score'], label=p)
            tmp.append(d[p]['score'])
        except:
            pass
        try:
            tmp.append(PACS[p]['score'])
        except:
            pass
print(len(tmp))
x = array_mean(tmp)
#print(x)
res.append(x)

differences = [res[0][0][i] - res[1][0][i] for i in range(len(res[0][0]))]
idx = np.argsort(differences)
res[0] = ((np.array(res[0][0])[idx], np.array(res[0][1])[idx]), 'Socio')
res[1] = ((np.array(res[1][0])[idx], np.array(res[1][1])[idx]), 'Bio')

colors = {}
colors['Bio'] = 'blue'
colors['Co-auth'] = 'purple'
colors['Socio'] = 'red'
colors['Tech'] = 'orange'
 
ax.set_ylim(-0.4, 0.4)
for i in range(len(res)):
    #print(res[i][0])
    V = res[i][0]
    L = res[i][1]
    M = V[0]
    S = V[1]
    if L == 'Socio':
        L1 = 'Socio / Tech'
    else:
        L1 = 'Bio / Co-auth'
    ax.plot(M, label=L1, color=colors[L])
    ax.fill_between(range(len(M)), M-S, M+S, alpha = 0.25, color=colors[L])
zeroes = [0 for _ in range(len(M))]
ax.plot(zeroes, color='black', linewidth=2)

ax.legend(loc='best', frameon=False)
plt.ylabel("Δ")
plt.xlabel("Motifs")

import seaborn as sn
sn.despine()
plt.tight_layout()
#plt.show()
plt.savefig("fig2b.pdf")
i+=1

