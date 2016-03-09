#!/usr/bin/env python

# Copyright (c) 2016 Ryan Collins <rcollins@chgr.mgh.harvard.edu>
# Distributed under terms of the MIT license.

"""
Estimate original molecule sizes and coordinates from 10X linked-read WGS barcodes
"""

import argparse
from collections import defaultdict, Counter, namedtuple
import pysam

def get_gemcode_regions(ibam, dist):
    """
    Estimates molecule coordinates from colinear reads with overlapping 10X barcodes

    Parameters
    ----------
    ibam : pysam.AlignmentFile
        Input 10X bam
    dist
        Partitioning distance (bp) for separating reads with overlapping
        barcodes into independent fragments

    Yields
    ------
    region : namedtuple
        chr, start, end, barcode, readcount
    """

    #Open bamfile
    bam = pysam.AlignmentFile(ibam)

    #Create namedtuples for storing read coordinate and molecule info
    coords = namedtuple('coords', ['chr', 'pos'])
    molecule = namedtuple('molecule', ['chr', 'start', 'end', 'barcode', 'readcount'])

    #Create defaultdict for storing gemcode tuples
    #Key is gemcodes, value is coords namedtuple
    gemcodes = defaultdict(list)

    #Iterate over reads in bamfile
    for read in bam:
        #Save 10X barcode for read as gem
        gem = read.get_tag('RX')
        #If barcode has been seen previously and new read is either from different
        #contig or is colinear but beyond dist, write out old barcode as interval
        #before adding new read to list
        if gem in gemcodes and ( gemcodes[gem][-1].chr != read.reference_name or read.reference_start-gemcodes[gem][-1].pos < dist ):
            yield molecule(gemcodes[gem][1].chr, min([pos for chr, pos in gemcodes[gem]]), max([pos for chr, pos in gemcodes[gem]]), gem, len(gemcodes[gem]))
            gemcodes[read.get_tag('RX')] = coords(read.reference_name, read.reference_start)
        else:
            #Else just add read to preexisting dictionary 
            gemcodes[gem].append(coords(read.reference_name, read.reference_start))


