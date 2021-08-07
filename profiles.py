import pickle
from numpy.core.fromnumeric import std

from pandas.core.algorithms import diff
from utils import avg, diff_sum, z_score, count, norm_vector

import matplotlib.pyplot as plt
import math

plt.rcParams['font.size'] = 14

N = 3
d = {}

def rotate(l, n):
    return l[n:] + l[:n]

def sorting(a):
    print(a)
    res = 0
    new_a = [list() for _ in range(len(a))]
    for i in range(len(a[0])):
        val = []
        for j in a:
            val.append(j[i])
        
        tmp = []
        for k in range(len(val)-1):
            for z in range(k+1, len(val)):
                tmp.append(val[k] - val[z])
        res = sum(tmp) / len(tmp)
        
        for j in range(len(a)):
            new_a[j].append((res, a[j][i]))

    for i in range(len(new_a)):
        new_a[i] = list(sorted(new_a[i]))
        new_a[i] = [j[1] for j in new_a[i]]
    return new_a

def array_mean(a):
    res = []
    std_dev = []

    for i in range(len(a[0])):
        val = []
        for j in a:
            val.append(j[i])
        res.append(sum(val) / len(val))
        std_dev.append(np.std(val) / len(a))
    return res, std_dev



datasets = ['gene', 'ndcclasses', 'ndcsub', 'workplace', 'ps', 'hs', 'hospital', 'justice', 'wiki', 'conference', 'babbuini', 'enron', 'EU', 'dblp', 'history', 'geology']

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
data['Socio'] = ['conference', 'workplace', 'hs', 'ps', 'hospital', 'justice', 'babbuini', 'wiki']
data['Tech'] = ['enron', 'EU']
data['Co-auth'] = ['dblp', 'history', 'geology']
data['Bio'] = ['gene', 'ndcclasses', 'ndcsub']

for i in range(10):
    data['Co-auth'].append("PACS{}".format(i))

print(data['Co-auth'])

# 2-edge, 3-edge
x_labels = ["2-0", "3-0", "0-1", "1-1", "2-1", "3-1"]
x_labels = ["   ", "   ", "   ", "   ", "   ", "   "]

"""
# plot cluster singoli
i = 0

for k in data.keys():
    fig, ax = plt.subplots()
    if N == 3:
        ax.set_xticks(range(len(x_labels)))
        ax.set_xticklabels(x_labels)
    ax.set_ylim(-1, 1)
    plt.title(k)
    tmp = []
    for p in data[k]:
        try:
            #ax.plot(d[p]['score'], label=p)
            tmp.append(d[p]['score'])
        except:
            pass
    tmp = sorting(tmp)
    for p in tmp:
        print(p)
        ax.plot(p)
    ax.legend()
    plt.show()
    #plt.savefig("profile_{}.pdf".format(k))
    i+=1
"""

uno = ['Socio', 'Tech', 'Co-auth', 'Bio']

# plot cluster singoli
i = 0
res = []
fig, ax = plt.subplots()
for k in data.keys():
    print(k)
    if N == 3:
        ax.set_xticks(range(len(x_labels)))
        ax.set_xticklabels(x_labels)
    if k not in uno:
        continue
    tmp = []
    print(len(data[k]))
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
    x = (array_mean(tmp), k)
    #print(x)
    res.append(x)

#tmp = sorting([i[0] for i in res])

colors = {}
colors['Bio'] = 'blue'
colors['Co-auth'] = 'purple'
colors['Socio'] = 'red'
colors['Tech'] = 'orange'
 
ax.set_ylim(-1, 1)
for i in range(len(res)):
    #print(res[i][0])
    V = res[i][0]
    L = res[i][1]
    M = np.array(rotate(V[0], 3))
    print(M, L)
    S = np.array(rotate(V[1], 3))
    ax.plot(M, label=L, color=colors[L])
    ax.fill_between(range(len(M)), M-S, M+S, alpha = 0.25, color=colors[L])
zeroes = [0 for _ in range(len(M))]
print(zeroes)
ax.plot(zeroes, color='black', linewidth=2)
#plt.ylabel("Δ")
#plt.xlabel("Motifs")

ax.legend(loc='best', frameon=False)

import seaborn as sn
sn.despine()
plt.tight_layout()
plt.savefig("fig1d.pdf")
#plt.show()
i+=1

