from hypergraph import hypergraph
from utils import *
from loaders import *
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import math

plt.rcParams['font.size'] = 16


def load(a):
    N = 3
    res = {}
    res[0] = []
    res[1] = []
    res[2] = []
    res[3] = []

    if a == 'fb':
        fb = load_facebook_hs()
    else:
        fb = load_friendship_hs()

    E = {}

    edges = load_high_school(N)
    for e in edges:
        E[tuple(sorted(e))] = 1

    for e in edges:
        if len(e) == 3:
            nodes = list(e)
            nodes = tuple(sorted(tuple(nodes)))
            p_nodes = power_set(nodes)
            
            c = 0
            fb_c = 0
            for edge in p_nodes:
                if len(edge) == 2 and tuple(sorted(edge)) in E:
                    c += 1
                x = tuple(sorted(edge))
                if len(edge) == 2 and x in fb:
                    fb_c += 1
                if len(edge) == 2 and tuple(reversed(list(x))) in fb:
                    fb_c += 1
            if c == 0:
                print("OK")
            res[c].append(fb_c)

    R = []
    S = []
    for k in res:
        if len(res[k]) != 0:
            R.append(np.mean(res[k]))
            S.append(np.std(res[k]) / len(res[k]))
    return np.array(R), np.array(S)

r, s = load('friends')
        
plt.ylim(0, 1.5)
plt.ylabel("Friends in group interactions")
plt.xticks(range(3), [])
plt.plot(r, color='orange', label='High School friendship')
plt.fill_between(range(len(r)), r-s, r+s, alpha = 0.25, color='orange')
sn.despine()


r, s = load('fb')
plt.plot(r, color='blue', label='High School fb')
plt.fill_between(range(len(r)), r-s, r+s, alpha = 0.25, color='blue')
plt.legend(frameon=False)
plt.tight_layout()

plt.savefig("fig3b_pre.pdf")