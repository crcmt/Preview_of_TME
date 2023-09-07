#!/usr/bin/env ipython
# coding: utf-8

import warnings
warnings.filterwarnings("ignore")

get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', 'IPCompleter.use_jedi = False')

import sys
import os
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
from IPython.display import SVG
from tqdm import tqdm_notebook

get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'png'")
plt.rcParams['pdf.fonttype'] = 'truetype'
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['figure.dpi'] = 120

from portraits.plotting import *
from portraits.mapping import get_gs_for_probes_from_3col,get_expressions_for_gs
from portraits.utils import read_gene_sets, ssgsea_formula, median_scale
from portraits.classification import KNeighborsClusterClassifier
from portraits.clustering import clustering_profile_metrics, clustering_profile_metrics_plot,clustering_select_best_tr

get_ipython().run_line_magic('load_ext', 'rpy2.ipython')

# Constants

EXPRESSION_MATRIX = sys.argv[1]
#EXPRESSION_MATRIX = 'subset_1s_tcga.tsv'

TCGA_SIGNATURES = 'Cohorts/Pan_TCGA/signatures.tsv'
TCGA_COHORTS_ANNOTATION = 'Cohorts/Pan_TCGA/annotation.tsv'
CLASSIFIED_SAMPLES = 'classified_samples.tsv'
GENE_SIGNATURES = 'signatures/gene_signatures.gmt'

annotated_expression = pd.read_csv(EXPRESSION_MATRIX, sep='\t', index_col=0)
annotated_expression.head(n=20)

# check if expression matrix is normalized if not log2 transform it.

if all(0<=sample<=18 for sample in annotated_expression.mean()):
    print(annotated_expression.head())
else:
    #annotated_expression = pd.log2(1+annotated_expression)
    annotated_expression = annotated_expression.transform(lambda x: np.log2(1+x))
    print(annotated_expression.head())

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
print(f'Reference signatures provided for {len(TCGA_signature_scores_scaled)} samples')

TCGA_annotation = pd.read_csv(TCGA_COHORTS_ANNOTATION, sep='\t', index_col=0)  # Contains MFP cluster labels in MFP column
print(f'Reference annotation provided for {len(TCGA_signature_scores_scaled)} samples')

# Fit the model
MODEL = KNeighborsClusterClassifier(norm=False, scale=False, clip=2, k=35).fit(TCGA_signature_scores_scaled, TCGA_annotation.MFP)

# Read signatures
gene_signatures = read_gene_sets(GENE_SIGNATURES) # GMT format like in MSIGdb

print(f'Loaded {len(gene_signatures)} signatures')

# Read expressions
gene_expressions = pd.read_csv(EXPRESSION_MATRIX, sep='\t', index_col=0)  # log2+1 transformed; Genes should appear to be in rows

print(f'Classifying cohort, N={len(gene_expressions)} samples')

if gene_expressions.max().max() > 35:
    print('Performing log2+1 transformation')
    gene_expressions = np.log2(1+gene_expressions)
    
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

#Output the predicted clusters
print('Predicted labels count:')
print(classified_samples.value_counts())

# Output the classified samples table
classified_samples.to_csv(CLASSIFIED_SAMPLES, sep='\t', index=True)
