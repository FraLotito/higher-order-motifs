from hypergraph import hypergraph
from utils import *
from loaders import *
import pickle

H_O = True
L_O = []

def count_motifs(edges, N, TOT):
    print(len(edges))
    mapping, labeling = generate_motifs(N)

    z = set()
    for e in edges:
        for n in e:
            z.add(n)

    graph = {}
    T = {}

    for e in edges:
        e = list(sorted(e))
        if H_O:
            T[tuple(e)] = 1

        for I in range(len(e)):
            for J in range(I+1, len(e)):
                i = e[I]
                j = e[J]

                if not H_O:
                    T[tuple(sorted([i,j]))] = 1

                if i in graph:
                    graph[i].add(j)
                else:
                    graph[i] = set([j])

                if j in graph:
                    graph[j].add(i)
                else:
                    graph[j] = set([i])
    global L_O
    L_O = list(T.keys())

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
    
    k = 0
    for v in graph.keys():
        v_ext = set()
        for u in graph[v]:
            if u > v:
                v_ext.add(u)
        k += 1
        if k % 5 == 0:
            print(k, len(z), TOT)

        graph_extend(set([v]), v_ext, v, set(graph[v]))
        c += 1

    out = []

    for motif in mapping.keys():
        count = 0
        for label in mapping[motif]:
            count += labeling[label]
            
        out.append((motif, count))

    out = list(sorted(out))

    D = {}
    for i in range(len(out)):
        D[i] = out[i][0]
    
    #with open('motifs_{}.pickle'.format(N), 'wb') as handle:
    #    pickle.dump(D, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return out

N = 3
results = []
output = {}

edges = load_primary_school(N)
m = count_motifs(edges, N, -1)
output['motifs'] = m

STEPS = len(edges)*10
ROUNDS = 10

for i in range(ROUNDS):
    if not H_O:
        e1 = hypergraph(edges)
    else:
        e1 = hypergraph(L_O)
    e1.MH(label='stub', n_steps=STEPS)
    m1 = count_motifs(e1.C, N, i)

    results.append(m1)

output['config_model'] = results
