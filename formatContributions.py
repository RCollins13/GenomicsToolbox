#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Ryan L. Collins <rlcollins@g.harvard.edu> 
# Distributed under terms of the MIT license.

"""
Format author contributions statement for a manuscript

Input: .tsv of authors (rows) by contribution categories (columns)
       Input .tsv expects first four columns to be first name, middle initial, 
       last name, and initials, but this can be changed with --ignore-first-n

Output: plain text string of formatted author contributions
"""


import argparse
from sys import stdout


def make_contribs_dict(tsv_in, ignore=4, initials_col=None):
    """
    Convert input author contributions .tsv to dict mapping contribution 
    categories to author initials
    """

    with open(tsv_in) as f:

        # Read first line of tsv_in to get contribution categories
        categs = f.readline().rstrip().split('\t')[ignore:]
        contrib_dict = {categ : [] for categ in categs}

        # Read remaining lines assuming one row per author
        for line in f:
            
            line_vals = line.rstrip().split('\t')

            # Automatically format initials unless initial column is specified
            if initials_col is None:
                initials = ''.join(['{}.'.format(x[0]) for x in line_vals[0:3] if x != ''])
            else:
                initials = line_vals[initials_col-1]

            for categ, indicator in zip(categs, [x != '' for x in line_vals[ignore:]]):
                if indicator:
                    contrib_dict[categ].append(initials)

    return contrib_dict


def main():
    # Parse command-line arguments and options
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('tsv_in', help='Input author contribution matrix, as .tsv')
    parser.add_argument('-i', '--ignore-first-n', type=int, default=4,
                        help='Number of leading columns to ignore')
    parser.add_argument('-c', '--initials-column', type=int, default=None,
                        help='Specify column number corresponding to author initials. ' +
                        '[default: create initials from first three columns]')
    parser.add_argument('-o', '--outfile', help='Path to output file. [default: ' +
                        'stdout]', default='stdout')
    args = parser.parse_args()

    # Open connection to outfile
    if args.outfile in '- stdout'.split():
        outfile = stdout
    else:
        outfile = open(args.outfile, 'w')

    # Load contributions matrix
    contribs = make_contribs_dict(args.tsv_in, args.ignore_first_n, 
                                  args.initials_column)

    # Write to outfile
    for categ, initials in contribs.items():
        outfile.write('{}: {}; '.format(categ, ', '.join(initials)))
    outfile.write('\n')
    outfile.close()


if __name__ == '__main__':
    main()