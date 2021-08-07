from hypergraph import hypergraph
from utils import *
from loaders import *
import pickle

def motifs_order_3(edges, TOT):
    N = 3
    full, visited = motifs_ho_full(edges, N, TOT)
    standard = motifs_standard(edges, N, TOT, visited)

    res = []
    for i in range(len(full)):
        res.append((full[i][0], max(full[i][1], standard[i][1])))

    return res

def motifs_order_4(edges, TOT):
    N = 4
    full, visited = motifs_ho_full(edges, N, TOT)
    not_full, visited = motifs_ho_not_full(edges, N, TOT, visited)
    standard = motifs_standard(edges, N, TOT, visited)

    res = []
    for i in range(len(full)):
        res.append((full[i][0], max([full[i][1], not_full[i][1], standard[i][1]])))

    return res

N = 3

edges = load_conference(N)

output = {}

if N == 3:
    output['motifs'] = motifs_order_3(edges, -1)
elif N == 4:
    output['motifs'] = motifs_order_4(edges, -1)

#for c in output['motifs']:
#    if c[1] > 0:
#        print(c)

STEPS = len(edges)*10

results = []

for i in range(10):
    e1 = hypergraph(edges)
    e1.MH(label='stub', n_steps=STEPS)
    if N == 3:
        m1 = motifs_order_3(e1.C, i)
    elif N == 4:
        m1 = motifs_order_4(e1.C, i)

    #null_model = e1.shuffle_edges(100)
    #m1 = count_motifs(null_model, N)
    results.append(m1)

output['config_model'] = results

with open('results_ho/conference_{}.pickle'.format(N), 'wb') as handle:
    pickle.dump(output, handle, protocol=pickle.HIGHEST_PROTOCOL)
