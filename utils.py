import random, math
import itertools
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

def motifs_ho_not_full(edges, N, TOT, visited):
    mapping, labeling = generate_motifs(N)

    T = {}
    graph = {}
    for e in edges:
        if len(e) >= N:
            continue

        T[tuple(sorted(e))] = 1

        for e_i in e:
            if e_i in graph:
                graph[e_i].append(e)
            else:
                graph[e_i] = [e]

    def count_motif(nodes):
        nodes = tuple(sorted(tuple(nodes)))
        p_nodes = power_set(nodes)
        
        motif = []
        for edge in p_nodes:
            if len(edge) >= 2:
                edge = tuple(sorted(list(edge)))
                if edge in T:
                    motif.append(edge)

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

    for e in edges:
        if len(e) == N - 1:
            nodes = list(e)
            
            for n in nodes:
                for e_i in graph[n]:
                    tmp = list(nodes)
                    tmp.extend(e_i)
                    tmp = list(set(tmp))
                    if len(tmp) == N and not (tuple(sorted(tmp)) in visited):
                        visited[tuple(sorted(tmp))] = 1
                        count_motif(tmp)

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
        #pickle.dump(D, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return out, visited


def motifs_standard(edges, N, TOT, visited):
    mapping, labeling = generate_motifs(N)

    graph = {}
    T = {}

    z = set()
    for e in edges:
        for n in e:
            z.add(n)

    for e in edges:
        if len(e) == 2:
            T[tuple(sorted(e))] = 1
            a, b = e
            if a in graph:
                graph[a].append(b)
            else:
                graph[a] = [b]

            if b in graph:
                graph[b].append(a)
            else:
                graph[b] = [a]

    def count_motif(nodes):
        nodes = tuple(sorted(tuple(nodes)))

        if nodes in visited:
            return

        p_nodes = power_set(nodes)
        
        motif = []
        for edge in p_nodes:
            edge = tuple(sorted(list(edge)))
            if edge in T:
                motif.append(edge)

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
        #pickle.dump(D, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return out

def motifs_ho_full(edges, N, TOT):
    mapping, labeling = generate_motifs(N)

    T = {}
    for e in edges:
        T[tuple(sorted(e))] = 1

    visited = {}

    def count_motif(nodes):
        nodes = tuple(sorted(tuple(nodes)))
        p_nodes = power_set(nodes)
        
        motif = []
        for edge in p_nodes:
            if len(edge) >= 2:
                edge = tuple(sorted(list(edge)))
                if edge in T:
                    motif.append(edge)

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

    for e in edges:
        if len(e) == N:
            #print(e)
            visited[e] = 1
            nodes = list(e)
            count_motif(nodes)

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
        #pickle.dump(D, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return out, visited

def diff_sum(original, null_models):
    u_null = avg(null_models)

    res = []
    for i in range(len(original)):
        res.append((original[i][1] - u_null[i]) / (original[i][1] + u_null[i] + 4))

    return res

def norm_vector(a):
    res = []
    M = 0
    for i in a:
        M += i**2
    M = math.sqrt(M)
    res = [i / M for i in a]
    return res

def count(a):
    res = []
    for i in a:
        res.append(i[1])
    return res

def count(edges):
    d = {}
    n = set()
    for i in range(2, 6):
        d[i] = 0
    for i in edges:
        try:
            d[len(i)] += 1
        except:
            pass
        finally:
            for j in i:
                n.add(j)
    print("& {} & {} & {} & {} & {} & {}".format(len(n), len(edges), d[2], d[3], d[4], d[5]))


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
    plt.savefig("distr/{}.pdf".format(title))

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
        z_scores.append((original[i][1] - u_null[i]) / (sigma_null[i] + 0.01))

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
    




