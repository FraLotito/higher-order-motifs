import csv, random, pandas as pd

from numpy import index_exp, nan

from utils import plot_dist_hyperedges, count

def load_facebook_hs():
    import pandas as pd
    res = {}

    d = pd.read_csv("DatasetHigherOrder/Facebook-known-pairs_data_2013.csv")
    for i in range(len(d)):
        a,b,c = list(map(int, d.iloc[i][0].split(' ')))
        if c == 1:
            res[(a,b)] = 1
            res[(b,a)] = 1
    return res

def load_friendship_hs():
    import pandas as pd
    res = {}

    d = pd.read_csv("DatasetHigherOrder/Friendship-network_data_2013.csv")
    for i in range(len(d)):
        a,b = list(map(int, d.iloc[i][0].split(' ')))
        res[(a,b)] = 1
    return res

def load_meta_hs(T = 'sex'):
    tsv_file = open("DatasetHigherOrder/meta_hs.txt")
    data = csv.reader(tsv_file, delimiter="\t")
    res = {}
    for i in data:
        a, b, c = i
        a = int(a)
        if T == 'sex' and c != 'Unknown':
            res[a] = c
        elif T == 'class':
            res[a] = b

    return res

def load_meta_ps(T = 'sex'):
    tsv_file = open("DatasetHigherOrder/metadata_ps.txt")
    data = csv.reader(tsv_file, delimiter="\t")
    res = {}
    for i in data:
        a, b, c = i
        a = int(a)
        if T == 'sex' and c != 'Unknown':
            res[a] = c
        elif T == 'class':
            res[a] = b

    return res


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
    #plot_dist_hyperedges(tot, "gene_disease")
    print(count(tot))
    return list(edges)

def pickle_PACS():
    import pandas as pd

    tb = pd.read_csv("DatasetHigherOrder/PACS.csv")

    tb = tb[['ArticleID', 'PACS', 'FullName']]

    papers = {}

    c = 0

    names = {}
    nidx = 0

    for _, row in tb.iterrows():
        idx = str(row['ArticleID'])
        a = str(row['PACS'])
        b = str(row['FullName'])

        if b in names:
            b = names[b]
        else:
            names[b] = nidx
            nidx += 1
            b = names[b]
        
        if idx in papers:
            papers[idx]['authors'].append(b)
        else:
            papers[idx] = {}
            papers[idx]['authors'] = [b]
            papers[idx]['PACS'] = a

        c+=1
        if c % 1000 == 0:
            print(c, tb.shape)

    import pickle
    pickle.dump(papers, open("PACS.pickle", "wb" ))

    #for k in papers:
    #    print(papers[k])

def load_PACS(N):
    import pickle, math

    papers = pickle.load(open("PACS.pickle", "rb" ))

    edges = []

    tot = []

    for k in papers:
        authors = papers[k]['authors']
        if len(authors) > 1 and len(authors) <= N:
            edges.append(tuple(sorted(authors)))
        tot.append(tuple(sorted(authors)))

    #plot_dist_hyperedges(tot, "PACS")
    print(len(edges))
    return edges

def load_PACS_single(N, S):
    import pickle

    papers = pickle.load(open("PACS.pickle", "rb" ))

    edges = []

    tot = []

    for k in papers:
        if int(papers[k]['PACS']) != S:
            continue
        authors = papers[k]['authors']
        if len(authors) > 1 and len(authors) <= N:
            edges.append(tuple(sorted(authors)))
        tot.append(tuple(sorted(authors)))

    ##plot_dist_hyperedges(tot, "PACS")
    print(count(tot))
    print(len(edges))
    return edges

def load_high_school_duplicates(N):
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
    
    edges = []
    
    for k in graph.keys():
        e_k = graph[k]
        G = nx.Graph(e_k, directed=False)
        c = list(nx.find_cliques(G))
        for i in c:
            i = tuple(sorted(i))

            if len(i) <= N:
                edges.append(i)

    #plot_dist_hyperedges(tot, "high_school")
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

    #plot_dist_hyperedges(tot, "high_school")
    print(count(tot))
    print(len(edges))
    return edges

def load_primary_school_duplicates(N):
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
    
    edges = []
    
    for k in graph.keys():
        e_k = graph[k]
        G = nx.Graph(e_k, directed=False)
        c = list(nx.find_cliques(G))
        for i in c:
            i = tuple(sorted(i))

            if len(i) <= N:
                edges.append(i)

    ##plot_dist_hyperedges(tot, "primary_school")
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

    ##plot_dist_hyperedges(tot, "primary_school")
    print(len(edges))
    print(count(tot))
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

    #plot_dist_hyperedges(tot, "conference")
    print(len(edges))
    print(count(tot))
    return edges

def load_conference_duplicates(N):
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
    
    tot = []
    edges = []
    
    for k in graph.keys():
        e_k = graph[k]
        G = nx.Graph(e_k, directed=False)
        c = list(nx.find_cliques(G))
        for i in c:
            i = tuple(sorted(i))

            if len(i) <= N:
                edges.append(i)

            tot.append(i)

    #plot_dist_hyperedges(tot, "conference")
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

    #plot_dist_hyperedges(tot, "workplace")
    print(len(edges))
    print(count(tot))
    return edges

def load_workplace_duplicates(N):
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
    
    tot = []
    edges = []
    
    for k in graph.keys():
        e_k = graph[k]
        G = nx.Graph(e_k, directed=False)
        c = list(nx.find_cliques(G))
        for i in c:
            i = tuple(sorted(i))

            if len(i) <= N:
                edges.append(i)

            tot.append(i)

    #plot_dist_hyperedges(tot, "workplace")
    print(len(edges))
    return edges

def load_hospital_duplicates(N):
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
    
    tot = []
    edges = []
    
    for k in graph.keys():
        e_k = graph[k]
        G = nx.Graph(e_k, directed=False)
        c = list(nx.find_cliques(G))
        for i in c:
            i = tuple(sorted(i))

            if len(i) <= N:
                edges.append(i)

            tot.append(i)

    #plot_dist_hyperedges(tot, "hospital")
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

    #plot_dist_hyperedges(tot, "hospital")
    print(len(edges))
    print(count(tot))
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
        paper, author, y = l
        y = int(y)

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

    #plot_dist_hyperedges(tot, "dblp")
    print(len(edges))
    print(count(tot))
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
        paper, author, y = l
        y = int(y)

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

    #plot_dist_hyperedges(tot, "history")
    print(len(edges))
    print(count(tot))
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
        paper, author, y = l
        y = int(y)

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

    #plot_dist_hyperedges(tot, "geology")
    print(len(edges))
    print(count(tot))
    return edges

def load_justice_ideo(N):
    dataset = "DatasetHigherOrder/justice.csv"
    ideo = "DatasetHigherOrder/justices_ideology.csv"
    
    df = pd.read_csv(dataset)
    df = df[['caseId', 'justiceName', 'vote', 'justice']]

    I = pd.read_csv(ideo)
    I = I[['spaethid', 'ideo']]
    
    cases = {}
    nodes = {}
    idx = 0
    dict_ideo = {}

    for _, row in df.iterrows():
        c, _, v, n = row['caseId'], row['justiceName'], row['vote'], row['justice']

        try:
            v = int(v) # valid vote
        except:
            continue # not voted

        n = int(n)

        if c in cases:
            if v in cases[c]:
                cases[c][v].append(n)
            else:
                cases[c][v] = [n]
        else:
            cases[c] = {}
            cases[c][v] = [n]
    for _, row in I.iterrows():
        ID, v = row[['spaethid', 'ideo']]
        try:
            ID = int(ID)
            v = float(v)
        except:
            continue
        dict_ideo[ID] = v


    tot = set()
    edges = set()

    for k in cases:
        for v in cases[k]:
            e = tuple(sorted(cases[k][v]))
            tot.add(e)
            if len(e) > 1 and len(e) <= N:
                edges.add(e)


    #plot_dist_hyperedges(tot, "justice")
    print(len(edges))
    return edges, dict_ideo

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


    #plot_dist_hyperedges(tot, "justice")
    print(len(edges))
    print(count(tot))
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

    ##plot_dist_hyperedges(tot, "babbuini")
    print(len(edges))
    print(count(tot))
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
    
    ##plot_dist_hyperedges(tot, "wiki")
    print(len(edges))
    print(count(tot))
    return edges

def load_NDC_substances(N):
    p = "DatasetHigherOrder/NDC-substances/"
    a = open(p + 'NDC-substances-nverts.txt')
    b = open(p + 'NDC-substances-simplices.txt')
    v = list(map(int, a.readlines()))
    s = list(map(int, b.readlines()))
    a.close()
    b.close()

    edges = set()
    tot = set()

    for i in v:
        cont = 0
        e = []
        while cont < i:
            e.append(s.pop(0))
            cont += 1
        e = tuple(sorted(e))
        if len(e) > 1 and len(e) <= N:
            edges.add(e)
        tot.add(e)

    #plot_dist_hyperedges(tot, "NDC_substances")
    print(len(edges))
    print(count(tot))
    return edges

def load_NDC_classes(N):
    p = "DatasetHigherOrder/NDC-classes/"
    a = open(p + 'NDC-classes-nverts.txt')
    b = open(p + 'NDC-classes-simplices.txt')
    v = list(map(int, a.readlines()))
    s = list(map(int, b.readlines()))
    a.close()
    b.close()

    edges = set()
    tot = set()

    for i in v:
        cont = 0
        e = []
        while cont < i:
            e.append(s.pop(0))
            cont += 1
        e = tuple(sorted(e))
        if len(e) > 1 and len(e) <= N:
            edges.add(e)
        tot.add(e)

    #plot_dist_hyperedges(tot, "NDC_classes")
    print(len(edges))
    print(count(tot))
    return edges

def load_eu(N):
    name = "email-Eu"
    p = "DatasetHigherOrder/{}/".format(name)
    a = open(p + '{}-nverts.txt'.format(name))
    b = open(p + '{}-simplices.txt'.format(name))
    v = list(map(int, a.readlines()))
    s = list(map(int, b.readlines()))
    a.close()
    b.close()

    edges = set()
    tot = set()

    for i in v:
        cont = 0
        e = []
        while cont < i:
            e.append(s.pop(0))
            cont += 1
        e = tuple(sorted(e))
        if len(e) > 1 and len(e) <= N:
            edges.add(e)
        tot.add(e)

    #plot_dist_hyperedges(tot, "{}".format(name))
    print(len(edges))
    print(count(tot))
    return edges

def load_enron(N):
    name = "email-Enron"
    p = "DatasetHigherOrder/{}/".format(name)
    a = open(p + '{}-nverts.txt'.format(name))
    b = open(p + '{}-simplices.txt'.format(name))
    v = list(map(int, a.readlines()))
    s = list(map(int, b.readlines()))
    a.close()
    b.close()

    edges = set()
    tot = set()

    for i in v:
        cont = 0
        e = []
        while cont < i:
            e.append(s.pop(0))
            cont += 1
        e = tuple(sorted(e))
        if len(e) > 1 and len(e) <= N:
            edges.add(e)
        tot.add(e)

    #plot_dist_hyperedges(tot, "{}".format(name))
    print(len(edges))
    print(count(tot))
    return edges




