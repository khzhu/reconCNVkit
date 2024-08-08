#!/usr/bin/env python3

import pandas as pd
import argparse

def get_options():
    parser = argparse.ArgumentParser(description="Filter CNV ratios by gene names.")
    parser.add_argument("--ratio-file", "-r", required=False,
                        dest="ratio_file", default=None,
                        help="A tab-delimited text file contains the log2(FC) of bins from paired tumor and normal samples.")
    parser.add_argument("--seg-file", "-s", required=False,
                        dest="seg_file", default=None,
                        help="A tab-delimited text file contains the log2(FC) of segments from paired tumor and normal samples.")
    parser.add_argument("--gene_list", "-g", required=False,
                    dest="gene_list", 
                    default="~/projects/reconCNV/data/gene_list.txt",
                    help="A tab-delimited text file contains a list of targeted genes")
    parser.add_argument('--version', action='version', version='%(prog)s v1.0.0')
    return parser.parse_args()

def main():
    options = get_options()
    global gene_list
    gene_list = pd.read_csv(options.gene_list, sep="\t")
    if options.ratio_file != None:
        # filter copy number log2 ratio file
        cnr_df = pd.read_csv(options.ratio_file, sep="\t", low_memory=False)
        cnr_df = cnr_df.loc[(cnr_df['gene']).isin(gene_list['gene_name'])]
        cnr_df.to_csv(options.ratio_file.replace(".cnr",".filtered.cnr"), index=False, sep="\t")
    
    if (options.seg_file != None):
        #filter copy number log2 segment file
        cns_df = pd.read_csv(options.seg_file, sep="\t", low_memory=False)
        cns_df = cns_df.loc[(cns_df['gene']).isin(gene_list['gene_name'])]
        cns_df.dropna(subset=['cn1', 'cn2'], inplace=True)
        cns_df['cn1'] = cns_df['cn1'].astype(int)
        cns_df['cn2'] = cns_df['cn2'].astype(int)
        cns_df.to_csv(options.seg_file.replace(".cns",".filtered.cns"), index=False, sep="\t")

if __name__ == "__main__":
    main()

