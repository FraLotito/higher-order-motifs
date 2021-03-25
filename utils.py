import random
import itertools
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

def plot_dist_hyperedges(edges, title):
    x = []
    for i in edges:
        if len(i) > 1 and len(i) < 20:
            x.append(len(i))

    M = max(x)

    ax = plt.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.title(title)
    plt.xlabel("Size S")
    plt.ylabel("P(S)")

    ax.hist(x, bins=np.arange(M + 1)+0.5, density=True, alpha=0.5, histtype='bar', ec='black')
    plt.savefig("{}.pdf".format(title))

def avg(motifs):
    result = []
    for i in range(len(motifs[0])):
        s = 0
        for j in range(len(motifs)):
            s += motifs[j][i][1]

        result.append(s / len(motifs))
    return result

def sigma(motifs):
    u = avg(motifs)

    result = []
    for i in range(len(motifs[0])):
        s = 0
        for j in range(len(motifs)):
            s += (motifs[j][i][1] - u[i])**2
        s /= len(motifs)
        s = s ** 0.5

        result.append(s)
    return result

def z_score(original, null_models):
    u_null = avg(null_models)
    sigma_null = sigma(null_models)

    z_scores = []
    for i in range(len(original)):
        if sigma_null[i] == 0:
            z_scores.append(0)
        else:
            z_scores.append((original[i] - u_null[i]) / sigma_null[i])

    return z_scores

def power_set(A): 
    subsets = []
    N = len(A)

    for mask in range(1<<N):
        subset = []

        for n in range(N):
            if ((mask>>n)&1) == 1:
                subset.append(A[n])

        subsets.append(subset)

    return subsets

def is_connected(edges, N):
    nodes = set()
    for e in edges:
        for n in e:
            nodes.add(n)

    if len(nodes) != N:
        return False

    visited = {}
    for i in nodes:
        visited[i] = False
    graph = {}
    for i in nodes:
        graph[i] = []
    
    for edge in edges:
        for i in range(len(edge)):
            for j in range(len(edge)):
                if edge[i] != edge[j]:
                    graph[edge[i]].append(edge[j])
                    graph[edge[j]].append(edge[i])
    
    q = []
    nodes = list(nodes)
    q.append(nodes[0])
    while len(q) != 0:
        v = q.pop(len(q) - 1)
        if not visited[v]:
            visited[v] = True
            for i in graph[v]:
                q.append(i)
    conn = True
    for i in nodes:
        if not visited[i]:
            conn = False
            break
    return conn

def relabel(edges, relabeling):
    res = []
    for edge in edges:
        new_edge = []
        for v in edge:
            new_edge.append(relabeling[v - 1])
        res.append(tuple(sorted(new_edge)))
    return sorted(res)

def generate_motifs(N):
    n = N
    assert n >= 2

    h = [i for i in range(1, n + 1)]
    A = []

    for r in range(n, 1, -1):
        A.extend(list(itertools.combinations(h, r)))

    B = power_set(A)

    C = []
    for i in range(len(B)):
        if is_connected(B[i], N):
            C.append(B[i])

    isom_classes = {}

    for i in C:
        edges = sorted(i)
        relabeling_list = list(itertools.permutations([j for j in range(1, n + 1)]))
        found = False
        for relabeling in relabeling_list:
            relabeling_i = relabel(edges, relabeling)
            #print(relabeling_i)
            if tuple(relabeling_i) in isom_classes:
                found = True
                break
        if not found:
            isom_classes[tuple(edges)] = 1

    mapping = {}
    labeling = {}

    for k in isom_classes.keys():
        mapping[k] = set()
        relabeling_list = list(itertools.permutations([j for j in range(1, n + 1)]))
        for relabeling in relabeling_list:
            relabeling_i = relabel(k, relabeling)
            labeling[tuple(sorted(relabeling_i))] = 0
            mapping[k].add(tuple(sorted(relabeling_i)))
    
    return mapping, labeling

#out = len(isom_classes.keys())
#print(out)



