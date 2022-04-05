# Higher-order motif analysis in hypergraphs

This code implements the algorithms for higher-order motif analysis proposed in [https://www.nature.com/articles/s42005-022-00858-7](https://www.nature.com/articles/s42005-022-00858-7)

## Abstract

A deluge of new data on real-world networks suggests that interactions among system units are not limited to pairs, but often involve a higher number of nodes. To properly encode higher-order interactions, richer mathematical frameworks such as hypergraphs are needed, where hyperedges describe interactions among an arbitrary number of nodes. Here we systematically investigate higher-order motifs, defined as small connected subgraphs in which vertices may be linked by interactions of any order, and propose an efficient algorithm to extract complete higher-order motif profiles from empirical data. We identify different families of hypergraphs, characterized by distinct higher-order connectivity patterns at the local scale. We also propose a set of measures to study the nested structure of hyperedges and provide evidences of structural reinforcement, a mechanism that associates higher strengths of higher-order interactions for the nodes that interact more at the pairwise level. Our work highlights the informative power of higher-order motifs, providing a principled way to extract higher-order fingerprints in hypergraphs at the network microscale.

<img src="https://github.com/FraLotito/higher-order-motifs/blob/master/cover.png" data-canonical-src="https://github.com/FraLotito/higher-order-motifs/blob/master/cover.png" width="700" height="300" />

## Code organization
* ```motifs.py``` contains the implementation of the baseline algorithm proposed in the paper
* ```motif2.py``` contains the implementation of the efficient algorithm proposed in the paper
* ```utils.py``` contains some useful functions
* ```loaders.py``` contains the loader for the datasets (see section below)
* ```hypergraph.py``` contains the implementation of a data structure for hypergraphs in Python and the configuration model for hypergraphs proposed by [Phil Chodrow](https://github.com/PhilChodrow)

## Datasets
Please download the datasets [here](https://drive.google.com/file/d/1uFaftX_hqjTiBt2SZ_6fbggYG9ySK3Ss/view?usp=sharing) and extract the archive inside the main directory.

## How to use custom datasets
If you wish to perform higher-order motif analysis on your own datasets, you should implement a custom ```loader``` function. This function should return a set of tuples. Each tuple represents an hyperedge, and will contain the ids of the nodes involved in a group interactions.  

## How to perform higher-order motif analysis
If you wish to experiment with the code, you can run analysis setting up the parameter ```N``` in the code, which specifies the order of the motifs to use for the analysis. At the moment, the only feasible orders are ```N=3``` and ```N=4```. The parameter ```ROUNDS``` specifies the number of samples from the configuration model. Keep in mind that ```ROUNDS``` can heavily affect the performance. A value between 10 and 20 already gives reliable results.

## Acknowledgments
We thank [Phil Chodrow](https://github.com/PhilChodrow) for the code in the file ```hypergraph.py```



