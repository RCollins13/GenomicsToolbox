#!/bin/bash

#Script to perform paired gene list enrichment tests by permutation

#Usage
usage(){
cat <<EOF

Script to perform permutation-based paired gene set enrichments

Usage: genesetEnrichment.sh [-n PERMUTATIONS] LIST1 LIST2 REF_LIST
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
l1p=`mktemp` #file to hold intersection outcomes from random permutation of l1 in l2
l2p=`mktemp` #file to hold intersection outcomes from random permutation of l2 in l1

#Determine count of genes in l1, l2, and intersection of l1 and l2
l1c=$( cat ${l1} | wc -l )
l2c=$( cat ${l2} | wc -l )
ovr=$( fgrep -wf ${l1} ${l2} | wc -l )

#Run permutations
for p in $( seq 1 ${nperm} ); do
  sort -R ${ref} | head -n ${l1c} | fgrep -wf - ${l2} | wc -l >> ${l1p}
  sort -R ${ref} | head -n ${l2c} | fgrep -wf - ${l1} | wc -l >> ${l2p}
done

#Write results
cat <<EOF
+---------------------+
| PERMUTATION SUMMARY |
+---------------------+
Genes in LIST1: ${l1c}
Genes in LIST2: ${l2c}
Genes in REF_LIST: $( cat ${ref} | wc -l )

${ovr} / ${l1c} genes in LIST1 appeared in LIST2
Greater overlap than $( awk -v ovr=${ovr} '{ if ($1<ovr) print $0 }' ${l1p} | wc -l ) / ${nperm} random permutations
p=$( echo "scale=10;($( awk -v ovr=${ovr} '{ if ($1>=ovr) print $0 }' ${l1p} | wc -l )+1)/(${nperm}+1)" | bc )

${ovr} / ${l2c} genes in LIST2 appeared in LIST1
Greater overlap than $( awk -v ovr=${ovr} '{ if ($1<ovr) print $0 }' ${l2p} | wc -l ) / ${nperm} random permutations
p=$( echo "scale=10;($( awk -v ovr=${ovr} '{ if ($1>=ovr) print $0 }' ${l2p} | wc -l )+1)/(${nperm}+1)" | bc )

EOF

#Clean up
rm -f ${l1p} ${l2p}