#!/bin/bash
#Copyright (c) 2016 Ryan Collins <rcollins@chgr.mgh.harvard.edu>
#Distributed under terms of the MIT license

#Script to perform a pairwise enrichment test for a pair of gene lists
#Bidirectional performs one test:
# 1) Probability of observed overlap of set A and set B versus random chance

#Usage
usage(){
cat <<EOF

Script to perform pairwise permutation-based enrichment test of two gene sets

Usage: pairwiseEnrichment.sh [-n PERMUTATIONS] LIST1 LIST2 REF_LIST
===============
LIST1               First gene list (required)
LIST2               Second gene list (required)
REF_LIST            List of all genes eligible for permutation (required)
-n PERMUTATIONS     Number of random permutations (default: 10,000)
-h                  Print this message
===============

EOF
}

#Read arguments
nperm=10000
while getopts ":n:h" opt; do
  case "$opt" in
    n)
      nperm=$OPTARG
      ;;
    h)
      usage
      exit 0
      ;;
  esac
done
shift $(( OPTIND - 1))
l1=$1 #first gene list
l2=$2 #second gene list
ref=$3 #reference gene list

#Check positional arguments
if [ -z ${l1} ] || [ -z ${l2} ] || [ -z ${ref} ]; then
  usage
  exit 0
fi

#Create temporary files
l1p=`mktemp` #file to hold random permutation set size of l1
l2p=`mktemp` #file to hold random permutation set size of l2
povr=`mktemp` #file to track number of overlapping elements from l1p and l2p

#Determine count of genes in l1, l2, and intersection of l1 and l2
l1c=$( cat ${l1} | wc -l )
l2c=$( cat ${l2} | wc -l )
ovr=$( fgrep -wf ${l1} ${l2} | wc -l )

#Run permutations
for p in $( seq 1 ${nperm} ); do
  sort -R ${ref} | head -n ${l1c} > ${l1p}
  sort -R ${ref} | head -n ${l2c} > ${l2p}
  fgrep -wf ${l1p} ${l2p} | wc -l >> ${povr}
done

#Write results
cat <<EOF
+---------------------+
| PERMUTATION SUMMARY |
+---------------------+
Genes in LIST1: ${l1c}
Genes in LIST2: ${l2c}
Genes in REF_LIST: $( cat ${ref} | wc -l )

${ovr} genes appeared in LIST1 and LIST2
More overlap than $( awk -v ovr=${ovr} '{ if ($1<ovr) print $0 }' ${povr} | wc -l ) / ${nperm} random permutations
Probability of observing a result equally or more significant, by ${nperm}-fold random permutation:
p=$( echo "scale=10;($( awk -v ovr=${ovr} '{ if ($1>=ovr) print $0 }' ${povr} | wc -l )+1)/(${nperm}+1)" | bc )

Less overlap than $( awk -v ovr=${ovr} '{ if ($1>ovr) print $0 }' ${povr} | wc -l ) / ${nperm} random permutations
Probability of observing a result equally or more significant, by ${nperm}-fold random permutation:
p=$( echo "scale=10;($( awk -v ovr=${ovr} '{ if ($1<ovr) print $0 }' ${povr} | wc -l )+1)/(${nperm}+1)" | bc )

EOF

#Clean up
rm -f ${l1p} ${l2p} ${povr}
