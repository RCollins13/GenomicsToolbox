#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022-Present Ryan L. Collins <rlcollins@g.harvard.edu> 
# and the Talkowski Laboratory
# Distributed under terms of the MIT license.

"""
Format an author list with numeric affiliations for a manuscript
"""


import csv
import pynumparser
import argparse


def load_affils(infile):
    """
    Load .tsv of affiliations and store as dictionary
    """

    with open(infile) as fin:
        affils = {akey : affil for akey, affil in csv.reader(fin, delimiter='\t')}
    
    return affils


def load_authors(authors_in, affils):
    """
    Load author list and remap old affiliations to new, ordered affiliations
    """

    authors = {}
    revised_affils = {}
    affil_map = {}
    nonnumeric_affils = set()

    with open(authors_in) as fin:
        for author, akeys_raw in csv.reader(fin, delimiter='\t'):

            # Map authors and affiliations
            new_akeys = []
            for akey in akeys_raw.split(','):
                if akey == '':
                    continue
                if akey in affil_map:
                    new_akeys.append(affil_map[akey])
                else:
                    if akey.isdigit():
                        new_akey = len(affil_map) + 1
                        affil_map[akey] = new_akey
                    else:
                        new_akey = akey
                        nonnumeric_affils.add(new_akey)
                    revised_affils[new_akey] = affils[akey]
                    new_akeys.append(new_akey)

            # Reformat affiliations
            nums = sorted([int(k) for k in new_akeys if str(k).isdigit()])
            not_nums = [str(k) for k in new_akeys if not str(k).isdigit()]
            authors[author] = ','.join([pynumparser.NumberSequence().encode(nums)] + not_nums)

    return authors, revised_affils


def print_authors(authors, plaintext_out=False):
    """
    Reformats and prints a dict of {author : affil} to stdout
    """

    n_authors = len(authors)

    k = 0
    for name, affstr in authors.items():
        k += 1
        if not plaintext_out:
            affstr = '<sup>' + affstr + '</sup>'
        if k < n_authors:
            print(name + affstr, end=', ')
        else:
            print(name + affstr)
    if plaintext_out:
        print('')
    else:
        print('<br />' * 2)


def print_affils(affils, plaintext_out=False, numeric_first=True):
    """
    Reformat affiliations into list of numbered strings and print to stdout
    """

    if numeric_first:
        for is_num in [True, False]:
            for i, aff in affils.items():
                if str(i).isdigit() == is_num:
                    print('. '.join([str(i), aff]), end='\n<br />')
    else:
        for i, aff in affils.items():
            print('. '.join([str(i), aff]), end='\n<br />')

    if plaintext_out:
        print('')
    else:
        print('<br />')


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('authors', help='.tsv of authors and affiliation keys')
    parser.add_argument('affiliations', help='.tsv of affiliation keys and affiliations')
    parser.add_argument('--plaintext-out', help='Do not format output as html',
                        action='store_true')
    args = parser.parse_args()

    # Load affiliations
    affils = load_affils(args.affiliations)

    # Load consortium authors and remap affiliations
    revised_authors, revised_affils = load_authors(args.authors, affils)

    # Print revised authors and affiliations
    print_authors(revised_authors, args.plaintext_out)
    print_affils(revised_affils, args.plaintext_out)


if __name__ == '__main__':
    main()

