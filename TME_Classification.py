#!/opt/TME_MFP_env/bin/python
# coding: utf-8

import warnings
warnings.filterwarnings("ignore")

import sys
import os
import argparse
import pandas as pd
import numpy as np
import seaborn as sns
import pathlib
import subprocess
import logging
import csv
import matplotlib.pyplot as plt
import umap
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook

plt.rcParams['pdf.fonttype'] = 'truetype'
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['figure.dpi'] = 120

from portraits.plotting import *
from portraits.mapping import get_gs_for_probes_from_3col,get_expressions_for_gs
from portraits.utils import read_gene_sets, ssgsea_formula, median_scale
from portraits.classification import KNeighborsClusterClassifier
from portraits.clustering import clustering_profile_metrics, clustering_profile_metrics_plot,clustering_select_best_tr

# Args

p = argparse.ArgumentParser()
p.add_argument('expression_file')
p.add_argument('-v', '--verbose', action='count', default=0)
args = p.parse_args()

# Constants

EXPRESSION_MATRIX = args.expression_file
EXPRESSION_MATRIX_SCALING_SERIES = 'Cohorts/fix_scaling/tcga/subset_10s_tcga.tsv'
TCGA_SIGNATURES = 'Cohorts/Pan_TCGA/signatures.tsv'
TCGA_COHORTS_ANNOTATION = 'Cohorts/Pan_TCGA/annotation.tsv'
CLASSIFIED_SAMPLES = 'classified_samples.tsv'
GENE_SIGNATURES = 'signatures/gene_signatures.gmt'

# Func

def log2_(df_):
    if args.verbose > 0:
        print('Performing log2+1 transformation')
    return df_.transform(lambda x: np.log2(1+x))

# TME classification

# The classification section determines each sample subtype against the
# reference TCGA cohort. The TCGA cohort was split into clusters using
# KNeighborsClusterClassifier. The resulting clusters are stored as a MODEL
# variable, with each cluster belonging to a different subtype. Then the
# samples EXPRESSION_MATRIX and GENE_SIGNATURES files are read and passed to
# the ssgsea_formula function to determine each signature (columns) score for
# every sample (rows).

# Load Reference Cohort with known TME labels and gene expression values

TCGA_signature_scores_scaled = pd.read_csv(TCGA_SIGNATURES, sep='\t', index_col=0).T  # Signatures in rows

if args.verbose > 0:
    print(f'Reference annotation provided for {len(TCGA_signature_scores_scaled)} samples')

TCGA_annotation = pd.read_csv(TCGA_COHORTS_ANNOTATION, sep='\t', index_col=0)  # Contains MFP cluster labels in MFP column

# Fit the model
MODEL = KNeighborsClusterClassifier(norm=False, scale=False, clip=2, k=35).fit(TCGA_signature_scores_scaled, TCGA_annotation.MFP)

# Read signatures
gene_signatures = read_gene_sets(GENE_SIGNATURES) # GMT format like in MSIGdb

if args.verbose > 0:
    print(f'Loaded {len(gene_signatures)} signatures')

# Read expressions
gene_expressions = pd.read_csv(EXPRESSION_MATRIX, sep='\t', index_col=0)  # log2+1 transformed; Genes should appear to be in rows

if args.verbose > 0:
    print(f'Classifying cohort, N={len(gene_expressions)} samples')

if gene_expressions.max().max() > 35:
    gene_expressions = log2_(gene_expressions)

# Classify the input cohort and give the output .tsv file with the TME subtype for each sample

# The codeblock establishes to which subtype each sample belongs and then
# prints out the number of samples that have the given subtype. The
# CLASSIFIED_SAMPLES file is given as an output. It lists the subtypes of all
# analyzed samples.

# Calc signature scores
signature_scores = ssgsea_formula(gene_expressions, gene_signatures)

# Scale signatures
signature_scores_scaled = median_scale(signature_scores)

data_ = signature_scores_scaled[MODEL.X.columns]

# Predict clusters
classified_samples = MODEL.predict(data_).rename('TME')

if args.verbose > 0:

    #Output the predicted clusters
    print('Predicted labels count:')
    print(classified_samples.value_counts())

# Output the classified samples table
classified_samples.to_csv(CLASSIFIED_SAMPLES, sep='\t', index=True)
