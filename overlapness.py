from hypergraph import hypergraph
from utils import *
from loaders import *
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import math
import scipy.special

plt.rcParams['font.size'] = 16

opt = 'edges_num'

def edges_num(edges):
    return len(edges)

def mean_edge_size(edges):
    v = [len(e) for e in edges]
    return np.mean(v)

def participation(edges, N):
    d = {}
    for i in range(2, N+1):
        d[i] = 0
    for e in edges:
        d[len(e)] += 1
    c = 1
    tot = 0
    for k in d:
        tot += d[k]
    for i in range(2, N+1):
        c -= (d[i] / tot)**2
    return c


def mean_overlap(edges):
    #overlapping coefficient
    if len(edges) > 1:
        o = 0
        den = 0
        for i in range(len(edges)):
            for j in range(i+1, len(edges)):
                a = set(edges[i])
                b = set(edges[j])
                o += len(a.intersection(b))
                den += 1
        return o / den
    else:
        return math.nan

def average(a):
    res = []
    for j in range(len(a[0])):
        tmp = []
        for i in range(len(a)):
            v = a[i][j]
            if not math.isnan(v):
                tmp.append(v)
        res.append(np.mean(tmp))
    return np.array(res)

def overlap(edges):
    #overlapping coefficient
    o = 0
    for i in range(len(edges)):
        for j in range(i+1, len(edges)):
            a = set(edges[i])
            b = set(edges[j])
            o += (len(a.intersection(b)) / min(len(a), len(b)))
    return o

def overlap_min(edges):
    #overlapping coefficient
    o = 0
    for i in range(len(edges)):
        for j in range(i+1, len(edges)):
            a = set(edges[i])
            b = set(edges[j])
            print(a, b)
            o += len(a.intersection(b))
    return o

def overlap2(edges):
    #overlapping coefficient
    o = 0
    for i in range(len(edges)):
        for j in range(i+1, len(edges)):
            a = set(edges[i])
            b = set(edges[j])
            if len(a) > 2 and len(b) > 2:
                o += (len(a.intersection(b)) / min(len(a), len(b)))
    return o

def load(a, N):
    print(a, N)
    if a == 'conference':
        d = load_conference(N)
    elif a == 'hs':
        d = load_high_school(N)
    elif a == 'ps':
        d = load_primary_school(N)
    elif a == 'haggle':
        d = load_haggle(N)
    elif a == 'hospital':
        d = load_hospital(N)
    elif a == 'justice':
        d = load_justice(N)
    elif a == 'babbuini':
        d = load_babbuini(N)
    elif a == 'wiki':
        d = load_wiki(N)
    elif a == 'workplace':
        d = load_workplace(N)
    elif a == 'gene':
        d = load_gene_disease(N)
    elif a == 'ndcclasses':
        d = load_NDC_classes(N)
    elif a == 'ndcsub':
        d = load_NDC_substances(N)
    elif a == 'enron':
        d = load_enron(N)
    elif a == 'eu':
        d = load_eu(N)
    elif a == 'PACS':
        d = load_PACS(N)
    elif a == 'dblp':
        d = load_DBLP(N)
    elif a == 'history':
        d = load_history(N)
    elif a == 'geology':
        d = load_geology(N)
    E = {}
    for e in d:
        E[tuple(sorted(e))] = 1

    res = []
    count = 0

    for e in d:
        if len(e) == N:
            count += 1
            subgraph = []
            nodes = list(e)
            nodes = tuple(sorted(tuple(nodes)))
            p_nodes = power_set(nodes)

            for edge in p_nodes:
                if tuple(sorted(edge)) in E:
                    subgraph.append(edge)

            if len(subgraph) <= 1:
                continue

            if opt == 'overlap':
                res.append(overlap(subgraph))
            elif opt == 'mean_edge_size':
                res.append(mean_edge_size(subgraph))
            elif opt == 'overlap2':
                res.append(overlap2(subgraph))
            elif opt == 'overlap_min':
                res.append(overlap_min(subgraph))
            elif opt == 'edges_num':
                res.append(edges_num(subgraph))
            elif opt == 'mean_overlap':
                res.append(mean_overlap(subgraph))
            elif opt == 'participation':
                res.append(participation(subgraph, N))
    print(count)
    return np.mean(res), np.std(res) / math.sqrt(len(res))

"""
a1 = []
a2 = []

for data in ['conference', 'workplace', 'hs', 'ps', 'haggle', 'justice', 'hospital', 'babbuini', 'enron', 'wiki', 'eu']:
    m = []
    std = []
    for i in range(3, 8):
        r, s = load(data, i)
        m.append(r)
        std.append(s)

    a1.append(m)
    a2.append(std)

with open('dump_{}_a.pkl'.format(opt), 'wb') as f:
    pickle.dump((a1, a2), f)

print(a1)



b1 = []
b2 = []

for data in ['gene', 'ndcclasses', 'ndcsub', 'PACS', 'dblp', 'geology', 'history']:
    m = []
    std = []
    for i in range(3, 8):
        r, s = load(data, i)
        m.append(r)
        std.append(s)
    b1.append(m)
    b2.append(std)

with open('dump_{}_b.pkl'.format(opt), 'wb') as f:
    pickle.dump((b1, b2), f)

print(b1)
"""


a = pickle.load(open("dump_{}_a.pkl".format(opt), "rb"))
a = (average(a[0]), average(a[1]))

b = pickle.load(open("dump_{}_b.pkl".format(opt), "rb"))
b = (average(b[0]), average(b[1]))

print(b[0])

if opt == 'mean_edge_size':
    v = 'Mean size of nested edges'
else:
    v = 'Number of nested edges'

plt.xticks(range(len(a[0])), range(3, 8))
plt.ylabel("{}".format(v))
plt.xlabel("Hyperedge size")
#plt.ylim((0, 8))
plt.plot(a[0], label='Socio / Tech')
plt.plot(b[0], label='Bio / Co-auth')
print(a[1])
plt.fill_between(range(len(a[0])), a[0] + a[1], a[0] - a[1], alpha = 0.25)
plt.fill_between(range(len(b[0])), b[0] + b[1], b[0] - b[1], alpha = 0.25)


plt.legend(frameon=False)
sn.despine()
plt.tight_layout()

plt.savefig("{}.pdf".format(opt))

