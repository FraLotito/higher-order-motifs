from numpy import histogram_bin_edges
import numpy as np
from hypergraph import hypergraph
from utils import *
from loaders import *
import pickle
import math
import sys
import matplotlib.pyplot as plt
import seaborn as sn

def load(ds, a):
    attribute = a

    def mean_sex(a):
        return a.count('F')

    def different_classes(a):
        a = set(a)
        return len(a)

    N = 3
    res = {}
    res[0] = []
    res[1] = []
    res[2] = []
    res[3] = []

    name = ""

    if ds == 'hs':
        d = load_meta_hs(attribute)
        edges = load_high_school(N)
        name = 'HIGH SCHOOL'
    else:
        d = load_meta_ps(attribute)
        edges = load_primary_school(N)
        name = 'PRIMARY SCHOOL'
    E = {}

    for e in edges:
        E[tuple(sorted(e))] = 1

    for e in edges:
        if len(e) == 3:
            nodes = list(e)
            nodes = tuple(sorted(tuple(nodes)))
            p_nodes = power_set(nodes)
            unk = False

            v = []
            for n in nodes:
                try:
                    v.append(d[n])
                except:
                    unk = True
            
            if unk:
                continue
            
            c = 0
            fb_c = 0
            for edge in p_nodes:
                if len(edge) == 2 and tuple(sorted(edge)) in E:
                    c += 1
            
            if a == 'sex':
                res[c].append(mean_sex(v))
            else:
                res[c].append(different_classes(v))

    print("{} - Attribute = {}".format(name, attribute))

    R = []
    S = []
    for k in res:
        if len(res[k]) > 0 and k != 0:
            S.append(np.std(res[k]) / len(res[k]))
            R.append(np.mean(res[k]))
            #print('Dyadic edges: ', k, 'Entropy: ', res[k])
    return np.array(R), np.array(S)
        
hm, hs = load('hs', 'class')
pm, ps = load('ps', 'class')

hmf, hsf = load('hs', 'sex')
pmf, psf = load('ps', 'sex')

plt.ylim(0, 3)
plt.ylabel("Students")
plt.xticks(range(3), [])
plt.plot(hm, color='blue', label='Avg. classes High School')
plt.fill_between(range(len(hm)), hm-hs, hm+hs, alpha = 0.25, color='blue')
plt.plot(pm, color='cyan', label = 'Avg. classes Primary School')
plt.fill_between(range(len(pm)), pm-ps, pm+ps, alpha = 0.25, color='cyan')

plt.plot(hmf, color='orange', label='Avg. females High School')
plt.fill_between(range(len(hm)), hmf-hsf, hmf+hsf, alpha = 0.25, color='orange')
plt.plot(pmf, color='red', label = 'Avg. females Primary School')
plt.fill_between(range(len(pm)), pmf-psf, pmf+psf, alpha = 0.25, color='red')
plt.legend()
sn.despine()
plt.savefig("fig3c_pre.pdf")


"""
hm, hs = load('hs', 'class')
pm, ps = load('ps', 'class')

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))
axes[0].set_xticks(range(3)) 
axes[0].set_xticklabels([1,2,3])
axes[1].set_xticks(range(3)) 
axes[1].set_xticklabels([1,2,3])


axes[0].set_ylim(0, 3)
axes[0].set_title('Class')
axes[0].set_ylabel("Entropy")
axes[0].set_xlabel("Inner dyadic links")
axes[0].plot(hm, color='blue', label='High School')
axes[0].fill_between(range(len(hm)), hm-hs, hm+hs, alpha = 0.25, color='blue')
axes[0].plot(pm, color='orange', label = 'Primary School')
axes[0].fill_between(range(len(pm)), pm-ps, pm+ps, alpha = 0.25, color='orange')
axes[0].legend()

hm, hs = load('hs', 'sex')
pm, ps = load('ps', 'sex')

axes[1].set_ylim(0, 1.5)
axes[1].set_title('Sex')
axes[1].set_ylabel("Entropy")
axes[1].set_xlabel("Inner dyadic links")
axes[1].plot(hm, color='blue', label='High School')
axes[1].fill_between(range(len(hm)), hm-hs, hm+hs, alpha = 0.25, color='blue')
axes[1].plot(pm, color='orange', label = 'Primary School')
axes[1].fill_between(range(len(pm)), pm-ps, pm+ps, alpha = 0.25, color='orange')
axes[1].legend()

#axes[1].plot(x2, y2)
fig.tight_layout()
plt.show()
"""