from hypergraph import hypergraph
from utils import *
from loaders import *
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn

def load():
    N = 3
    res = {}
    res[0] = []
    res[1] = []
    res[2] = []
    res[3] = []

    

    E = {}

    edges, ideo = load_justice_ideo(N)

    NODES = set()
    ID_NODES = set()

    for k in ideo.keys():
        ID_NODES.add(k)

    for e in edges:
        E[tuple(sorted(e))] = 1
        for n in e:
            NODES.add(n)
    print(NODES)
    print(ID_NODES)
    print(NODES.intersection(ID_NODES))
    TOT = 0
    for e in edges:
        if len(e) == 3:
            TOT += 1
            nodes = list(e)
            nodes = tuple(sorted(tuple(nodes)))
            p_nodes = power_set(nodes)
            
            c = 0

            for edge in p_nodes:
                if len(edge) == 2 and tuple(sorted(edge)) in E:
                    c += 1
            try:
                values = [ideo[n] for n in nodes]
                res[c].append(np.std(values))
            except:
                print("OK")

    print(TOT)
            

    R = []
    S = []
    for k in res:
        if len(res[k]) != 0:
            R.append(np.mean(res[k]))
            S.append(np.std(res[k]) / len(res[k]))
    return np.array(R), np.array(S)

print(load())

"""
plt.ylim(0, 1.5)
plt.ylabel("Friendship")
plt.xticks(range(3), [])
plt.plot(r, color='orange', label='High School friendship')
plt.fill_between(range(len(r)), r-s, r+s, alpha = 0.25, color='orange')

r, s = load('fb')
plt.plot(r, color='blue', label='High School fb')
plt.fill_between(range(len(r)), r-s, r+s, alpha = 0.25, color='blue')
sn.despine()
plt.legend()
plt.savefig("fig3b_pre.pdf")
"""