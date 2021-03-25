from utils import generate_motifs, power_set, is_connected
from loaders import *

N = 3
CONT = 0

mapping, labeling = generate_motifs(N)

#edges = random_hypergraph(5, 6)
#print(edges)

#edges = load_gene_disease(N)
#edges = load_PACS(N)
edges = load_high_school(N)
#edges = load_example(N)

print("Edges ", len(edges))

z = set()
for e in edges:
    for n in e:
        z.add(n)

print("Nodes ", len(z))

#for e in edges:
#    print(e)

graph = {}
T = {}

for e in edges:
    e = list(sorted(e))
    T[tuple(e)] = 1

    for I in range(len(e)):
        for J in range(I+1, len(e)):
            i = e[I]
            j = e[J]

            #T[tuple(sorted([i,j]))] = 1

            if i in graph:
                graph[i].add(j)
            else:
                graph[i] = set([j])

            if j in graph:
                graph[j].add(i)
            else:
                graph[j] = set([i])

def count_motif(nodes):
    nodes = tuple(sorted(tuple(nodes)))
    p_nodes = power_set(nodes)
    
    motif = []
    for edge in p_nodes:
        if len(edge) >= 2:
            edge = tuple(sorted(list(edge)))
            if edge in T:
                motif.append(edge)
    
    conn = is_connected(motif, N)
    
    if not conn:
        return

    m = {}
    idx = 1
    for i in nodes:
        m[i] = idx
        idx += 1

    labeled_motif = []
    for e in motif:
        new_e = []
        for node in e:
            new_e.append(m[node])
        new_e = tuple(sorted(new_e))
        labeled_motif.append(new_e)
    labeled_motif = tuple(sorted(labeled_motif))

    if labeled_motif in labeling:
        labeling[labeled_motif] += 1

def graph_extend(sub, ext, v, n_sub):

    if len(sub) == N:
        count_motif(sub)
        return

    while len(ext) > 0:
        w = ext.pop()
        tmp = set(ext)

        for u in graph[w]:
            if u not in sub and u not in n_sub and u > v:
                tmp.add(u)

        new_sub = set(sub)
        new_sub.add(w)
        new_n_sub = set(n_sub).union(set(graph[w]))
        graph_extend(new_sub, tmp, v, new_n_sub)

c = 0
tot = len(graph.keys())
k = 0
for v in graph.keys():
    v_ext = set()
    for u in graph[v]:
        if u > v:
            v_ext.add(u)
    k += 1
    if k % 5 == 0:
        print(k, len(z))

    graph_extend(set([v]), v_ext, v, set(graph[v]))
    c += 1

out = []

for motif in mapping.keys():
    count = 0
    for label in mapping[motif]:
        count += labeling[label]

    if count > 0:
        out.append((count, motif))

out = list(sorted(out, reverse=True))

print("\n------- Motifs count -------\n")

for c, m in out:
    print("{} | {}".format(m, c))

print('\n')