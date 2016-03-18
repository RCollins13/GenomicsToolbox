# ScriptToolbox
An expanding carpenter's belt of assorted genomics and bioinformatics utilities

**Contact:** Ryan Collins (rcollins@chgr.mgh.harvard.edu)

All code copyright (c) 2016 Ryan Collins and is distributed under terms of the MIT license.  

---  
## Table of Contents  
#### Examples  
- will be added soon  

#### Script documentation  
- [bidirectionalEnrichment.sh](https://github.com/RCollins13/ScriptToolbox#bidirectionalenrichmentsh)  
- [pairwiseEnrichment.sh](https://github.com/RCollins13/ScriptToolbox#pairwiseenrichmentsh)  

--- 

## bidirectionalEnrichment.sh  
Runs a bidirectional permutation-based enrichment tests for two gene sets by sampling from the universal set. "Bidirectional" is used to mean two independent permutation tests, which will differ proportionally to the size of each respective set:  
Test A: Probability of enrichment of set A in set B versus random chance (i.e. sets of size A are permuted and compared to set B)  
Test B: Probability of enrichment of set B in set A versus random chance (i.e. sets of size B are permuted and compared to set A)  

```
Usage: bidirectionalEnrichment.sh [-n PERMUTATIONS] LIST1 LIST2 REF_LIST
===============
LIST1               First gene list (required)
LIST2               Second gene list (required)
REF_LIST            List of all genes eligible for permutation (required)
-n PERMUTATIONS     Number of random permutations (default: 10,000)
-h                  Print this message
===============
```
**Usage Notes:**  
1a. Gene symbols in each list won't be sanity checked.  
1b. LIST1 and LIST2 don't even have to contain gene symbols; this script could theoretically be used to run an enrichment permutation between any two sets of strings.
2. Whitespace not permitted in elements of LIST1 and LIST2.  
3. Dev note/ToDo: merge with [pairwiseEnrichment.sh](https://github.com/RCollins13/ScriptToolbox#pairwiseenrichmentsh) with a toggled option for bidirectional or pairwise 

--- 

## pairwiseEnrichment.sh  
Runs a pairwise permutation-based enrichment test of two gene sets by sampling from the universal set. "Pairwise" is used to mean one single permutation test for both sets, which differs from [bidirectionalEnrichment.sh](https://github.com/RCollins13/ScriptToolbox#bidirectionalenrichmentsh): here, sets of both size A and size B are permuted and compared against each other, evaluating the empirical null of observing a number of shared items by both sets. However, probabilities for both tails of the null distribution are reported. 

```
Usage: pairwiseEnrichment.sh [-n PERMUTATIONS] LIST1 LIST2 REF_LIST
===============
LIST1               First gene list (required)
LIST2               Second gene list (required)
REF_LIST            List of all genes eligible for permutation (required)
-n PERMUTATIONS     Number of random permutations (default: 10,000)
-h                  Print this message
===============
```
**Usage Notes:**  
1a. Gene symbols in each list won't be sanity checked.  
1b. LIST1 and LIST2 don't even have to contain gene symbols; this script could theoretically be used to run an enrichment permutation between any two sets of strings.
2. Whitespace not permitted in elements of LIST1 and LIST2.  
3. Dev note/ToDo: merge with [bidirectionalEnrichment.sh](https://github.com/RCollins13/ScriptToolbox#bidirectionalenrichmentsh) with a toggled option for bidirectional or pairwise 
