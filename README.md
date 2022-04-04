# Higher-order motif analysis in hypergraphs

This code implements the algorithms for higher-order motif analysis proposed in - here link -

## Abstract

A deluge of new data on social, technological and biological networked systems suggests that a
large number of interactions among system units are not limited to pairs, but rather involve a higher
number of nodes. To properly encode such higher-order interactions, richer mathematical frameworks such as hypergraphs are needed, where hyperlinks describe connections among an arbitrary
number of nodes. Here we introduce the concept of higher-order motifs, small connected subgraphs
where vertices may be linked by interactions of any order. We provide lower and upper bounds on
the number of higher-order motifs as a function of the motif size, and propose an efficient algorithm
to extract complete higher-order motif profiles from empirical data. We identify different families
of hypergraphs, characterized by distinct higher-order connectivity patterns at the local scale. We
also capture evidences of structural reinforcement, a mechanism that associates higher strengths of
higher-order interactions for the nodes that interact more at the pairwise level. Our work highlights the informative power of higher-order motifs, providing a first way to extract higher-order
fingerprints in hypergraphs at the network microscale.

<img src="https://github.com/FraLotito/higher-order-motifs/blob/master/cover.png" data-canonical-src="https://github.com/FraLotito/higher-order-motifs/blob/master/cover.png" width="700" height="300" />

## Datasets
Please download the datasets [here](https://drive.google.com/file/d/1uFaftX_hqjTiBt2SZ_6fbggYG9ySK3Ss/view?usp=sharing) and extract the archive inside the main directory.

## Code organization
* ```motifs.py``` contains the implementation of the baseline algorithm proposed in the paper
* ```motif2.py``` contains the implementation of the efficient algorithm proposed in the paper
* ```utils.py``` contains some useful functions
* ```loaders.py``` contains the loader for the datasets (see section above)
* ```hypergraph.py``` contains the implementation of a data structure for hypergraphs in Python and the configuration model for hypergraphs proposed by [Phil Chodrow](https://github.com/PhilChodrow)

## Acknowledgments
We thank [Phil Chodrow](https://github.com/PhilChodrow) for the code in the file ```hypergraph.py```



