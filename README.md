# ScriptToolbox
Toolbox of various utility genomics scripts

**Contact:** Ryan Collins (rcollins@chgr.mgh.harvard.edu)

All code copyright (c) 2016 Ryan Collins and is distributed under terms of the MIT license.

## genesetEnrichment.sh  
Runs a permutation-based statistical enrichment test between two gene sets by sampling from the universal set.
```
Usage: genesetEnrichment.sh [-n PERMUTATIONS] LIST1 LIST2 REF_LIST
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
1b. Gene lists don't even have to be gene symbols, so this script can be used to run an enrichment permutation between any two sets of strings.
