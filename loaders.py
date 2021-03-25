import csv, random, pandas as pd
from networkx.generators import directed

from numpy import index_exp, nan

from utils import plot_dist_hyperedges

def load_example(N):
    e = [(1,2,3), (2,4), (2,3), (2,5,6), (4,6), (1,2,3,7)]
    edges = []
    for i in e:
        if len(i) <= N:
            edges.append(i)
    return edges

def random_hypergraph(N, E):
    graph = []
    for _ in range(E):
        s = random.randint(2, 3)
        graph.append(tuple(sorted(random.sample([i for i in range(1, N+1)], s))))

    graph = list(set(graph))
    return graph

def load_gene_disease(N):
    name2id_gene = {}
    id_gene2name = {}

    diseases = {}
    idxG = 0

    tsv_file = open("DatasetHigherOrder/curated_gene_disease_associations.tsv")
    data = csv.reader(tsv_file, delimiter="\t")

    c = 0
    
    for row in data:
        c += 1
        if c == 1:
            continue
        gene = int(row[0])
        dis = row[4]
        if gene in name2id_gene:
            gene = name2id_gene[gene]
        else:
            name2id_gene[gene] = idxG
            id_gene2name[idxG] = gene
            gene = name2id_gene[gene]
            idxG += 1

        if dis in diseases:
            diseases[dis].append(gene)
        else:
            diseases[dis] = [gene]

    edges = set()
    tot = []

    discarded_1 = 0
    discarded = 0

    for d in diseases.keys():
        if len(diseases[d]) > 1 and len(diseases[d]) <= N:
            edges.add(tuple(sorted(diseases[d])))
        elif len(diseases[d]) == 1:
            discarded_1 += 1
        else:
            discarded += 1
        
        tot.append(diseases[d])

    tsv_file.close()
    plot_dist_hyperedges(tot, "gene_disease")
    print(len(edges))
    return list(edges)

def pickle_PACS():
    import pandas as pd
    edges = set()

    tb = pd.read_csv("DatasetHigherOrder/PACS.csv")

    tb = tb[['ArticleID', 'AuthorDAIS']]

    papers = {}

    c = 0

    for _, row in tb.iterrows():
        idx = str(row['ArticleID'])
        a = row['AuthorDAIS']
        
        if idx in papers:
            papers[idx].append(a)
        else:
            papers[idx] = [a]

        c+=1
        if c % 1000 == 0:
            print(c)

    import pickle
    pickle.dump(papers, open("PACS.pickle", "wb" ))

    #for k in papers:
    #    print(papers[k])

def load_PACS(N):
    import pickle, math

    papers = pickle.load(open("PACS.pickle", "rb" ))

    edges = []

    A = {}
    idx = 0

    tot = []

    for k in papers:
        if len(papers[k]) > 1 and len(papers[k]) <= N:
            authors = []
            nan = False
            for i in papers[k]:
                if math.isnan(i):
                    nan = True
                    break
                if i in A:
                    i = A[i]
                else:
                    i = idx
                    A[i] = idx
                    idx += 1

                authors.append(i)

            if not nan:
                edges.append(tuple(authors))


    for k in papers:
        nan = False
        for i in papers[k]:
            if math.isnan(i):
                nan = True
                break
        if not nan:
            tot.append(papers[k])

    plot_dist_hyperedges(tot, "PACS")
    print(len(edges))
    return edges

def load_high_school(N):
    import networkx as nx
    dataset = "DatasetHigherOrder/High-School_data_2013.csv"

    fopen = open(dataset, 'r')
    lines = fopen.readlines()

    graph = {}
    for l in lines:
        t, a, b, c, d = l.split()
        t = int(t) - 1385982020
        a = int(a)
        b = int(b)
        if t in graph:
            graph[t].append((a,b))
        else:
            graph[t] = [(a,b)]

    fopen.close()
    
    tot = set()
    edges = set()
    
    for k in graph.keys():
        e_k = graph[k]
        G = nx.Graph(e_k, directed=False)
        c = list(nx.find_cliques(G))
        for i in c:
            i = tuple(sorted(i))

            if len(i) <= N:
                edges.add(i)

            tot.add(i)

    plot_dist_hyperedges(tot, "high_school")
    print(len(edges))
    return edges

def load_primary_school(N):
    import networkx as nx
    dataset = "DatasetHigherOrder/primaryschool.csv"

    fopen = open(dataset, 'r')
    lines = fopen.readlines()

    graph = {}
    for l in lines:
        t, a, b, c, d = l.split()
        t = int(t) - 31220
        a = int(a)
        b = int(b)
        if t in graph:
            graph[t].append((a,b))
        else:
            graph[t] = [(a,b)]

    fopen.close()
    
    tot = set()
    edges = set()
    
    for k in graph.keys():
        e_k = graph[k]
        G = nx.Graph(e_k, directed=False)
        c = list(nx.find_cliques(G))
        for i in c:
            i = tuple(sorted(i))

            if len(i) <= N:
                edges.add(i)

            tot.add(i)

    plot_dist_hyperedges(tot, "primary_school")
    print(len(edges))
    return edges

def load_conference(N):
    import networkx as nx
    dataset = "DatasetHigherOrder/conference.dat"

    fopen = open(dataset, 'r')
    lines = fopen.readlines()

    graph = {}
    for l in lines:
        t, a, b = l.split()
        t = int(t) - 32520
        a = int(a)
        b = int(b)
        if t in graph:
            graph[t].append((a,b))
        else:
            graph[t] = [(a,b)]

    fopen.close()
    
    tot = set()
    edges = set()
    
    for k in graph.keys():
        e_k = graph[k]
        G = nx.Graph(e_k, directed=False)
        c = list(nx.find_cliques(G))
        for i in c:
            i = tuple(sorted(i))

            if len(i) <= N:
                edges.add(i)

            tot.add(i)

    plot_dist_hyperedges(tot, "conference")
    print(len(edges))
    return edges

def load_workplace(N):
    import networkx as nx
    dataset = "DatasetHigherOrder/workspace.dat"

    fopen = open(dataset, 'r')
    lines = fopen.readlines()

    graph = {}
    for l in lines:
        t, a, b = l.split()
        t = int(t) - 28820
        a = int(a)
        b = int(b)
        if t in graph:
            graph[t].append((a,b))
        else:
            graph[t] = [(a,b)]

    fopen.close()
    
    tot = set()
    edges = set()
    
    for k in graph.keys():
        e_k = graph[k]
        G = nx.Graph(e_k, directed=False)
        c = list(nx.find_cliques(G))
        for i in c:
            i = tuple(sorted(i))

            if len(i) <= N:
                edges.add(i)

            tot.add(i)

    plot_dist_hyperedges(tot, "workplace")
    print(len(edges))
    return edges

def load_hospital(N):
    import networkx as nx
    dataset = "DatasetHigherOrder/hospital.dat"

    fopen = open(dataset, 'r')
    lines = fopen.readlines()

    graph = {}
    for l in lines:
        t, a, b, c, d = l.split()
        t = int(t) - 140
        a = int(a)
        b = int(b)
        if t in graph:
            graph[t].append((a,b))
        else:
            graph[t] = [(a,b)]

    fopen.close()
    
    tot = set()
    edges = set()
    
    for k in graph.keys():
        e_k = graph[k]
        G = nx.Graph(e_k, directed=False)
        c = list(nx.find_cliques(G))
        for i in c:
            i = tuple(sorted(i))

            if len(i) <= N:
                edges.add(i)

            tot.add(i)

    plot_dist_hyperedges(tot, "hospital")
    print(len(edges))
    return edges

def load_DBLP(N):
    dataset = "DatasetHigherOrder/dblp.csv"

    fopen = open(dataset, 'r')
    lines = fopen.readlines()

    graph = {}

    for i in range(len(lines)):
        if i == 0:
            continue

        l = lines[i]
        l = l.split(',')
        paper, author, _ = l
        if paper in graph:
            graph[paper].append(author)
        else:
            graph[paper] = [author]
    
    fopen.close()

    edges = set()
    tot = set()
    for k in graph:
        p = tuple(sorted(graph[k]))
        tot.add(p)
        if len(p) > 1 and len(p) <= N:
            edges.add(p)

    plot_dist_hyperedges(tot, "dblp")
    print(len(edges))
    return edges

def load_history(N):
    dataset = "DatasetHigherOrder/history.csv"

    fopen = open(dataset, 'r')
    lines = fopen.readlines()

    graph = {}

    for i in range(len(lines)):
        if i == 0:
            continue

        l = lines[i]
        l = l.split(',')
        paper, author, _ = l
        if paper in graph:
            graph[paper].append(author)
        else:
            graph[paper] = [author]

    fopen.close()

    edges = set()
    tot = set()
    for k in graph:
        p = tuple(sorted(graph[k]))
        tot.add(p)
        if len(p) > 1 and len(p) <= N:
            edges.add(p)

    plot_dist_hyperedges(tot, "history")
    print(len(edges))
    return edges

def load_geology(N):
    dataset = "DatasetHigherOrder/geology.csv"

    fopen = open(dataset, 'r')
    lines = fopen.readlines()

    graph = {}

    for i in range(len(lines)):
        if i == 0:
            continue

        l = lines[i]
        l = l.split(',')
        paper, author, _ = l
        if paper in graph:
            graph[paper].append(author)
        else:
            graph[paper] = [author]

    fopen.close()

    edges = set()
    tot = set()
    for k in graph:
        p = tuple(sorted(graph[k]))
        tot.add(p)
        if len(p) > 1 and len(p) <= N:
            edges.add(p)

    plot_dist_hyperedges(tot, "geology")
    print(len(edges))
    return edges

def load_justice(N):
    dataset = "DatasetHigherOrder/justice.csv"
    
    df = pd.read_csv(dataset)
    df = df[['caseId', 'justiceName', 'vote']]
    
    cases = {}
    nodes = {}
    idx = 0

    for _, row in df.iterrows():
        c, n, v = row['caseId'], row['justiceName'], row['vote']

        try:
            v = int(v) # valid vote
        except:
            continue # not voted

        if n in nodes:
            n = nodes[n]
        else:
            nodes[n] = idx
            idx += 1
            n = nodes[n]

        if c in cases:
            if v in cases[c]:
                cases[c][v].append(n)
            else:
                cases[c][v] = [n]
        else:
            cases[c] = {}
            cases[c][v] = [n]

    tot = set()
    edges = set()

    for k in cases:
        for v in cases[k]:
            e = tuple(sorted(cases[k][v]))
            tot.add(e)
            if len(e) > 1 and len(e) <= N:
                edges.add(e)


    plot_dist_hyperedges(tot, "justice")
    print(len(edges))
    return edges

def load_copenaghen(N):
    import networkx as nx
    dataset = "DatasetHigherOrder/copenaghen.csv"

    fopen = open(dataset, 'r')
    lines = fopen.readlines()

    graph = {}
    cont = 0
    for l in lines:
        if cont == 0:
            cont += 1
            continue

        a, b, t, _ = l.split(',')
        t = int(t)
        a = int(a)
        b = int(b)
        if t in graph:
            graph[t].append((a,b))
        else:
            graph[t] = [(a,b)]

    fopen.close()
    
    tot = set()
    edges = set()
    
    for k in graph.keys():
        e_k = graph[k]
        G = nx.Graph(e_k, directed=False)
        c = list(nx.find_cliques(G))
        for i in c:
            i = tuple(sorted(i))

            if len(i) <= N:
                edges.add(i)

            tot.add(i)

    plot_dist_hyperedges(tot, "copenaghen")
    print(len(edges))
    return edges

def load_haggle(N):
    import networkx as nx
    dataset = "DatasetHigherOrder/haggle.csv"

    fopen = open(dataset, 'r')
    lines = fopen.readlines()

    graph = {}
    cont = 0
    for l in lines:
        if cont == 0:
            cont += 1
            continue

        a, b, _, t= l.split(',')
        t = int(t)
        a = int(a)
        b = int(b)
        if t in graph:
            graph[t].append((a,b))
        else:
            graph[t] = [(a,b)]

    fopen.close()
    
    tot = set()
    edges = set()
    
    for k in graph.keys():
        e_k = graph[k]
        G = nx.Graph(e_k, directed=False)
        c = list(nx.find_cliques(G))
        for i in c:
            i = tuple(sorted(i))

            if len(i) <= N:
                edges.add(i)

            tot.add(i)

    plot_dist_hyperedges(tot, "haggle")
    print(len(edges))
    return edges

def load_babbuini(N):
    import gzip
    import networkx as nx

    f = gzip.open("DatasetHigherOrder/babbuini.txt", 'rb')
    lines = f.readlines()

    graph = {}
    names = {}
    idx = 0

    cont = 0
    for l in lines:
        if cont == 0:
            cont = 1
            continue

        l = l.split()

        t, a, b, _, _ = l

        t = int(t)

        if a in names:
            a = names[a]
        else:
            names[a] = idx
            a = idx
            idx += 1

        if b in names:
            b = names[b]
        else:
            names[b] = idx
            b = idx
            idx += 1
        
        if t in graph:
            graph[t].append((a,b))
        else:
            graph[t] = [(a,b)]
    
    tot = set()
    edges = set()
    
    for k in graph.keys():
        e_k = graph[k]
        G = nx.Graph(e_k, directed=False)
        c = list(nx.find_cliques(G))
        for i in c:
            i = tuple(sorted(i))

            if len(i) <= N:
                edges.add(i)

            tot.add(i)

    plot_dist_hyperedges(tot, "babbuini")
    print(len(edges))
    return edges

def load_wiki(N):
    fopen = open("DatasetHigherOrder/wiki.txt", 'r')
    lines = fopen.readlines()

    edges = set()
    tot = set()
    votes = {}

    for l in lines:
        l = l.split()

        if len(l) == 0:
            for k in votes:
                e = tuple(sorted(votes[k]))
                tot.add(e)
                if len(e) > 1 and len(e) <= N:
                    edges.add(e)
            votes = {}
            continue
        
        if l[0] != 'V':
            continue

        _, vote, u_id, _, _, _ = l
        if vote in votes:
            votes[vote].append(u_id)
        else:
            votes[vote] = [u_id]
    
    plot_dist_hyperedges(tot, "wiki")
    print(len(edges))
    return edges

    
#pickle_PACS()
#load_gene_disease(4)
#pickle_high_school()
#load_conference(4)