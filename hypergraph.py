'''
An object of class hypergraph is a list of tuples on a specified node set, which can be implicit. 
It is equipped with methods for computing hypergraph moments of interest and running Markov Chain Monte Carlo. 
'''

from networkx.classes.function import nodes
from utils import relabel
import numpy as np
import networkx as nx
from collections import Counter 
from itertools import accumulate
from bisect import bisect
import random
import itertools
from scipy.special import binom
import random

class hypergraph:
    
    def __init__(self, C, n_nodes = None, node_labels = None):
        
        
        self.C = [tuple(sorted(f)) for f in C] # edge list
        
        self.nodes = list(set([v for f in self.C for v in f])) # node list
        self.n = len(self.nodes) # number of nodes

        # optional node labels -- not really used for anything at the moment
        if node_labels is not None:
            self.node_labels = node_labels
        
        # number of edges
        self.m = len(self.C)
             
        # node degree vector
        D = {}
        for i in self.nodes:
            D[i] = 0

        for f in self.C:
            for v in f:
                D[v] += 1
        
        self.D = D
        
        # edge dimension sequence
        K = np.array([len(f) for f in self.C])
        self.K = K
        
        # bookkeeping for Monte Carlo
        self.MH_rounds = 0
        self.MH_steps = 0
        self.acceptance_rate = 0 
                
    def node_degrees(self, by_dimension = False):
        '''
        Return a np.array() of node degrees. If by_dimension, return a 2d np.array() 
        in which each entry gives the number of edges of each dimension incident upon the given node. 
        '''
        if not by_dimension:
            return(self.D)
        else:
            D = np.zeros((len(self.D), max(self.K)))
            for f in self.C:
                for v in f:
                    D[v, len(f)-1] += 1
            return(D)
        
    def edge_dimensions(self):
        '''
        Return an np.array() of edge dimensions. 
        '''
        return(self.K)
    
    def node_dimension_matrix(self):
        '''
        Return a matrix in which the i,j entry gives the number of dimension j edges incident on node i. 
        '''
        A = np.zeros((self.n, max([len(f) for f in self.C])+1))
        for f in self.C:
            for v in f:
                A[v, len(f)] += 1
        return(A)
    
    
    def line_graph(self):
        '''
        Return a networkx Graph() in which each node corresponds to a hyperedge 
        and two nodes are linked if the corresponding edges intersect in the primal hypergraph. 
        '''
        H = nx.Graph()

        counts = Counter(self.C)
        d = {v : counts[v] for v in counts}

        H.add_nodes_from(d.keys())
        nx.set_node_attributes(H, values = d, name = 'm')
        
        node_list = list(H.nodes())
        n_nodes = len(node_list)
        for u in range(n_nodes):
            for v in range(u+1, n_nodes):
                j = len(set(node_list[u]).intersection(set(node_list[v])))
                if j > 0:
                    H.add_edge(node_list[u],node_list[v], weight = j)
        return(H)
    
    def get_edges(self, node):
        '''
        Return a list of edges incident upon a specified node. 
        '''
        return([f for f in self.C if node in f])
    
    def remove_degeneracy(self, verbose = True):
        '''
        Use pairwise reshuffles to remove degenerate edges, as may be generated in stub-matching. 
        '''
        m_degenerate = self.check_degeneracy()
        while self.check_degeneracy() > 0:
            for i in range(len(self.C)):
                while is_degenerate(self.C[i]):
                    j = np.random.choice(range(len(self.C)))
                    f1, f2 = self.C[i], self.C[j]
                    self.C[i], self.C[j] = pairwise_reshuffle(f1, f2, True)
        if verbose:
            print(str(m_degenerate) + ' degeneracies removed, ' + str(self.check_degeneracy()) + ' remain.')
    
    def MH(self, n_steps = 1000, verbose = True, label = 'edge', n_clash = 1, detailed = False, **kwargs):
        '''
        Conduct Markov Chain Monte Carlo in order to approximately sample from the space of appropriately-labeled graphs. 
        n_steps: number of steps to perform
        verbose: if True, print a finishing message with descriptive summaries of the algorithm run. 
        label: the label space to use. Can take values in ['vertex' , 'stub', 'edge']. 
        n_clash: the number of clashes permitted when updating the edge counts in vertex-labeled MH. n_clash = 0 will be exact but very slow. n_clash >= 2 may lead to performance gains at the cost of decreased accuracy. 
        detailed: if True, preserve the number of edges of given dimension incident to each node
        **kwargs: additional arguments passed to sample_fun
        '''
        if (label == 'edge') or (label == 'stub'):
            self.stub_edge_MH(n_steps = n_steps, verbose = verbose, label = label, detailed = detailed, **kwargs)
        elif label == 'vertex':
            self.vertex_labeled_MH(n_steps = n_steps, verbose = verbose, n_clash = n_clash, detailed = detailed, **kwargs)
        else:
            print('not implemented')
    
    def stub_edge_MH(self, n_steps = 1000, verbose = True, label = 'edge',  detailed = False, message = True, **kwargs):
        '''
        See description of self.MH()
        '''
        
        C_new = [list(c) for c in self.C]
        m = len(C_new)
        
        proposal = proposal_generator(m, detailed)

        def MH_step(label = 'edge'):
            i, j, f1, f2, g1, g2 = proposal(C_new)
            C_new[i] = sorted(g1)
            C_new[j] = sorted(g2)
        
        n = 0
        n_rejected = 0
        
        while n < n_steps:
            MH_step()
            n += 1
            
        self.C = [tuple(sorted(f)) for f in C_new]
        self.MH_steps += n
        self.MH_rounds += 1
        
        if message: 
            print(str(n_steps) + ' steps completed.')
    
    def vertex_labeled_MH(self, n_steps = 10000, sample_every = 500, sample_fun = None, verbose = False, n_clash = 0, message = True, detailed = False, **kwargs):
        '''
        See description of self.MH()
        '''
        
        rand = np.random.rand
        randint = np.random.randint
                
        k = 0
        done = False
        c = Counter(self.C)
        
        epoch_num = 0
        n_rejected = 0
        
        m = sum(c.values())

        while not done:
            # initialize epoch
            
            l = list(c.elements())
            
            add = []
            remove = []
            
            end_epoch = False
            num_clash = 0
            
            epoch_num += 1
            
            # within each epoch
            
            k_rand = 20000       # generate many random numbers at a time
            
            k_ = 0
            IJ = randint(0, m, k_rand)
            A = rand(k_rand)
            while True:
                if k_ >= k_rand/2.0:
                    IJ = randint(0, m, k_rand)
                    A  = rand(k_rand)
                    k_ = 0
                i,j = (IJ[k_],IJ[k_+1])
                k_ += 2
                
                f1, f2 = l[i], l[j]
                while f1 == f2:
                    i,j = (IJ[k_],IJ[k_+1])
                    k_ += 2
                    f1, f2 = l[i], l[j]
                if detailed:
                    while len(f1) != len(f2):
                        i,j = (IJ[k_],IJ[k_+1])
                        k_ += 2
                        f1, f2 = l[i], l[j]
                        while f1 == f2:
                            i,j = (IJ[k_],IJ[k_+1])
                            k_ += 2
                            f1, f2 = l[i], l[j]
                            
                inter = 2**(-len((set(f1).intersection(set(f2)))))
                if A[k_] > inter /(c[f1] * c[f2]):
                    n_rejected += 1
                    k += 1
                else: # if proposal was accepted
                    g1, g2 = pairwise_reshuffle(f1, f2, True)    
                    num_clash += remove.count(f1) + remove.count(f2)
                    if (num_clash >= n_clash) & (n_clash >=1):
                        break
                    else:
                        remove.append(f1)
                        remove.append(f2)
                        add.append(g1)
                        add.append(g2)
                        k += 1
                    if n_clash == 0:
                        break
                
            add = Counter(add)
            add.subtract(Counter(remove))
            
            c.update(add) 
            done = k - n_rejected>=n_steps
        if message:
            print(str(epoch_num) + ' epochs completed, ' + str(k - n_rejected) + ' steps taken, ' + str(n_rejected) + ' steps rejected.')
        self.C = [tuple(sorted(f)) for f in list(c.elements())]
        self.MH_steps += k - n_rejected
        self.MH_rounds += 1
        self.acceptance_rate = (1.0*(k - n_rejected)) / (k)
        
    
    def check_degeneracy(self):
        '''
        Find the number of degeneracies in self.C
        '''
        return np.sum([is_degenerate(f) for f in self.C])        
    def choose_nodes(self, n_samples, choice_function = 'uniform'):
        '''
        Utility function for choosing pairs of nodes from self.C, used in assortativity calculations. 
        '''
        D = self.node_degrees()
 
        def uniform(x):
            i = np.random.randint(len(x))
            j = i
            while i == j:
                j = np.random.randint(len(x))
            return(np.array([x[i],x[j]]))
        
        def top_2(x):
            ind = np.argpartition(D[x,], -2)[-2:]
            y = np.array(x)[ind]
            random.shuffle(y)
            return(y)
        
        def top_bottom(x):
            top = np.argmax(D[x,])
            bottom = np.argmin(D[x,])
            y = np.array(x)[[bottom, top]]
            random.shuffle(y)
            return(y)
        
        choice_functions = {
            'uniform': uniform,
            'top_2' : top_2,
            'top_bottom' : top_bottom, 
            'NA' : uniform
        }
        
        n = 0
        v = []
        while True:
            edge = self.C[np.random.randint(self.m)]
            if len(edge) < 2:
                continue
            x = choice_functions[choice_function](edge)
            v.append(x)
            n+=1
            if n > n_samples:
                break
        return(v)
            
    def assortativity(self, n_samples = 10, choice_function = 'uniform', method = 'pearson'):
        '''
        Compute the approximate degree assortativity of a hypergraph using the specified choice_function and method in ['spearman', 'pearson']
        '''
        D = self.node_degrees()
        arr = np.array(self.choose_nodes(n_samples, choice_function))
        arr = D[arr]
        
        if method == 'spearman':
            order = np.argsort(arr, axis = 0)
            arr = np.argsort(order, axis = 0)
        elif method == 'pearson':
            arr = arr - 1
            
        return(np.corrcoef(arr.T))[0,1]

    def shuffle_edges(self, p):
        nodes = self.nodes
        sub_nodes = list(nodes)[:int(len(nodes)*p/100)]
        relabel = list(sub_nodes)
        random.shuffle(relabel)
        rel = {}
        for i in range(len(sub_nodes)):
            rel[sub_nodes[i]] = relabel[i]
        
        res = []
        for e in self.C:
            if len(e) >= 3:
                res.append(e)
            else:
                E = []
                for n in e:
                    if n in rel:
                        E.append(rel[n])
                    else:
                        E.append(n)
                E = tuple(sorted(E))
                res.append(E)
        return res
        
is_degenerate = lambda x: len(set(x)) < len(x)

def proposal_generator(m, detailed = False):
    '''
    Propose a transition in stub- and edge-labeled MH. 
    '''
    def proposal(edge_list):
        i,j = np.random.randint(0,m,2)
        f1, f2 = edge_list[i], edge_list[j]
        if detailed: 
            while len(f1) != len(f2):
                i,j = np.random.randint(0,m,2)
                f1, f2 = edge_list[i], edge_list[j]
        g1, g2 = pairwise_reshuffle(f1, f2, True)
        return(i, j, f1, f2, g1, g2)
    return(proposal)

def pairwise_reshuffle(f1, f2, preserve_dimensions = True):
    '''
    Randomly reshuffle the nodes of two edges while preserving their sizes.
    '''
    
    f = list(f1) + list(f2)
    s = set(f)
    
    intersection = set(f1).intersection(set(f2))
    ix = list(intersection)
    
    g1 = ix.copy()
    g2 = ix.copy()
    
    for v in ix:
        f.remove(v)
        f.remove(v)
    
    for v in f:
        if (len(g1) < len(f1)) & (len(g2) < len(f2)):
            if np.random.rand() < .5:
                g1.append(v)
            else:
                g2.append(v)
        elif len(g1) < len(f1):
            g1.append(v)
        elif len(g2) < len(f2):
            g2.append(v)
    if len(g1) != len(f1):
        print('oops')
        print(f1, f2, g1, g2)
    return (tuple(sorted(g1)), tuple(sorted(g2)))
     
def projected_graph(C, weighted = False, as_hyper = False, multi = True):
    '''
    Compute the projected (clique) graph corresponding to a given hypergraph. Can be slow when many high-dimensional edges are present. 
    '''
    if not as_hyper:
        if multi:
            G = nx.MultiGraph()
        else:
            G = nx.Graph()
        G.add_nodes_from(C.nodes)
        for f in C.C:
            if weighted:
                if len(f) >= 2:
                    G.add_edges_from(itertools.combinations(f, 2), weight = 1.0/(len(f) - 1))
            else :
                G.add_edges_from(itertools.combinations(f, 2))
        return(G)
    else:
        G = [f for F in C.C for f in itertools.combinations(F, 2)]
        return(hypergraph(G, n_nodes = len(C.nodes)))