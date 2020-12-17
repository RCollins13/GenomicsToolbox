# Genomics Toolbox
A slowly expanding carpenter's belt of assorted genomics and bioinformatics utilities

**Contact:** Ryan Collins (rlcollins@g.harvard.edu)

All code copyright (c) 2016-present Ryan Collins and is distributed under terms of the MIT license.  

---  
## Table of Contents  
#### Script documentation  
- [bidirectionalEnrichment.sh](https://github.com/RCollins13/ScriptToolbox#bidirectionalenrichmentsh)  
- [evenSplitter.R](https://github.com/RCollins13/ScriptToolbox#evensplitterr)
- [formatContributions.py](https://github.com/RCollins13/ScriptToolbox#formatcontributionspy)
- [pairwiseEnrichment.sh](https://github.com/RCollins13/ScriptToolbox#pairwiseenrichmentsh)  

#### Examples  
- Will be added eventually  
--- 

## bidirectionalEnrichment.sh  
Runs a bidirectional permutation-based enrichment tests for two gene sets by sampling from a universal set.  

"Bidirectional" is used to mean two separate permutation tests, which will differ proportionally to the size of each respective set:  

*  **Test A:** Probability of enrichment of set A in set B versus random chance (i.e. sets of size A are permuted and compared to set B)  
*  **Test B:** Probability of enrichment of set B in set A versus random chance (i.e. sets of size B are permuted and compared to set A)  

```
Usage: bidirectionalEnrichment.sh [-n PERMUTATIONS] LIST1 LIST2 REF_LIST

Arguments and options:
	LIST1               First gene list (required)
	LIST2               Second gene list (required)
	REF_LIST            List of all genes eligible for permutation (required)
	-n PERMUTATIONS     Number of random permutations (default: 10,000)
	-h                  Print this message
```
**Usage Notes:**  
1. Gene symbols in each list won't be sanity checked.  
2. `LIST1` and `LIST2` don't even have to contain gene symbols; this script could theoretically be used to run an enrichment permutation between any two sets of strings.
3. Whitespace not permitted in elements of `LIST1` and `LIST2`.  

_Dev note/ToDo_: merge with [pairwiseEnrichment.sh](https://github.com/RCollins13/ScriptToolbox#pairwiseenrichmentsh) with a toggled option for bidirectional or pairwise 

--- 

## evenSplitter.R  
Uniformly partition an input file of arbitrary size according to various dimensions and parameters.    

```
Usage: evenSplitter.R [options] INFILE PREFIX

Options:
	-L INTEGER, --targetLines=INTEGER
		target lines per split [default: NULL]
	-S INTEGER, --targetSplits=INTEGER
		target splits [default: NULL]
	--shuffle
		randomly shuffle lines in input file before splitting [default: FALSE]
	-q, --quiet
		suppress output messages [default: FALSE]
	-h, --help
		Show this help message and exit
```
**Usage Notes:**  
1. Must specify either `--targetLines` or `--targetSplits`, but not both.
2. If `--targetLines` is specified, optimal number of partitions will be automatically determined.  
3. If `--targetSplits` is specified, optimal number of lines per partition will be automatically determined.  

--- 

## formatContributions.py  
Format an author contributions statement for a manuscript.  

Expects a .tsv of authors (rows) by contribution categories (columns) as input, and will generate a plain text string of formatted author contributions as output.

```
usage: formatContributions.py [-h] [-i IGNORE_FIRST_N] [-c INITIALS_COLUMN]
                              [-o OUTFILE]
                              tsv_in

positional arguments:
  tsv_in                Input author contribution matrix, as .tsv

optional arguments:
  -h, --help            show this help message and exit
  -i IGNORE_FIRST_N, --ignore-first-n IGNORE_FIRST_N
                        Number of leading columns to ignore
  -c INITIALS_COLUMN, --initials-column INITIALS_COLUMN
                        Specify column number corresponding to author
                        initials. [default: create initials from first three
                        columns]
  -s, --sort-contribution-categories
                        Alphabetically sort contribution categories. [default:
                        False]
  -o OUTFILE, --outfile OUTFILE
                        Path to output file. [default: stdout]
```

**Usage Notes:**  
1. Input .tsv expects first four columns to be first name, middle initial, last name, and initials, but this can be changed with `--ignore-first-n`.  
2. Designed with the [CRediT Taxonomy](http://credit.niso.org/) in mind, but can be adapted to other formats.  

--- 

## pairwiseEnrichment.sh  
Runs a pairwise permutation-based enrichment test of two gene sets by sampling from the universal set.  

"Pairwise" is used to mean one single permutation test for both sets, which differs from [bidirectionalEnrichment.sh](https://github.com/RCollins13/ScriptToolbox#bidirectionalenrichmentsh): here, sets of both size A and size B are permuted and compared against each other, evaluating the empirical null of observing a number of shared items by both sets. However, probabilities for both tails of the null distribution are reported.  

```
Usage: pairwiseEnrichment.sh [-n PERMUTATIONS] LIST1 LIST2 REF_LIST

Arguments and options:
	LIST1               First gene list (required)
	LIST2               Second gene list (required)
	REF_LIST            List of all genes eligible for permutation (required)
	-n PERMUTATIONS     Number of random permutations (default: 10,000)
	-h                  Print this message
```
**Usage Notes:**  
1. Gene symbols in each list won't be sanity checked.  
2. `LIST1` and `LIST2` don't even have to contain gene symbols; this script could theoretically be used to run an enrichment permutation between any two sets of strings.
3. Whitespace not permitted in elements of `LIST1` and `LIST2`.  

_Dev note/ToDo_: merge with [bidirectionalEnrichment.sh](https://github.com/RCollins13/ScriptToolbox#bidirectionalenrichmentsh) with a toggled option for bidirectional or pairwise 

### Terms of Use &amp; Referencing this Library 
No formal citation is required to use anything in this library: as mentioned above, all code is released under the terms of the M.I.T. license.     

#### About Me
I'm Ryan, and I'm currently working towards a Ph.D. in human genomics. If you want to learn more about me or my research, you can [visit my website](http://ryanlcollins.com) or [follow me on Twitter (@ryanlcollins13)](https://twitter.com/ryanlcollins13).
  