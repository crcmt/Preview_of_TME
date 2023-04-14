# Molecular functional portrait analysis and Tumor microenvironment classification.

## Introduction
Tumor microenvironment (TME) plays a significant role in clinical outcomes and response to therapy. By exerting pro- and anti-tumorigenic actions, tumor-infiltrating immune cells can profoundly influence tumor progression as well as the success of anti-cancer therapies. In addition, cancer-associated fibroblasts (CAFs) as well as angiogenic signals from stromal cells have been shown to affect outcomes.
Based on a curated list of 29 functional gene expressions (shown on figure below) ssGSEA score the TME subtype classifications are done. Materials provided in this repository help to identify the TME subtype of an input sample (or you can use the example files in ![Cohorts](Cohorts) folder ). 

![image2020-11-4_18-20-47](https://user-images.githubusercontent.com/127855909/228009303-964b1147-0f42-4361-819b-bc22be9ccd97.png)

In BostonGene based on the analyses above we developed a way to create samples Molecular Functional Portrait which is a planetary schematic representation of integrated molecular and functional characteristics of a tumor and its microenvironment that depicts the prevalence of malignant and tumor microenvironment (TME) cell populations, and the activity of tumor promoting and suppressing processes. The portrait includes qualitative and quantitative descriptions of modules built based on the expression of BostonGene curated 29 gene expression signatures (reference manuscript and table), with the size of each module corresponding to the intensity of the normalized single-sample gene set enrichment analysis (GSEA) score, and the colors denoting pro- (red) or anti-cancer activity (blue).A short introduction to each TME subtype with its MFP portrait you can see in on figure below.

![image2020-11-4_18-12-26](https://user-images.githubusercontent.com/127855909/228009221-3fe09cc9-a30a-4d3f-aa4b-3641c6278f7e.png)


## Citation
This repository and all of its content are linked to “Integrated tumor exome and transcriptome analyses reveal conserved pan-cancer microenvironment subtypes predictive of response to immunotherapy” article. For the article look in the link below:

https://www.cell.com/cancer-cell/fulltext/S1535-6108(21)00222-1

For more information visit to BostonGene’s scientific portal using the following link: 

https://science.bostongene.com/tumor-portrait/ 


Please, when using the provided materials for research and publication make a reference to this repository and the article.

## Setup
If your environment is already set up according to the requirements in the description of  [Setup.md](Setup.md) file, you only just have to clone the github repository and start your analysis.
Copy the command below to clone our repository into your environment 


    git clone https://github.com/BostonGene/MFP.git


## Implementation overview
**Note: 
The analysis example is done for a cohort you must not try to do TME classification analyses for only one sample too.**


To make the analyses flow easier to understand we created a corresponding graph which is introduced below and helps to visually see every step of the analysis and its priority level.


The graph below introduces the whole analysis flow.

![MFP prediction flowchart](https://user-images.githubusercontent.com/127855909/228008558-4a7163ba-9c23-4107-b2f9-85d674b41499.jpg)


All the analyses are done in the [TME_Classification.ipynb](TME_Classification.ipynb) notebook which is separated into 2 main sections, 1 optional section introducing Data Preparation analyses and 1 additional section if the user wants to add their own reference cohort on which the classification will be done.



The pipeline consists of several nodes that correspond to each other where some of them are optional(depends on user choice):

* Data preparation (optional if you already have your expression matrix)
  * Data retrieval (and normalization if its from CEL files using R) 
  * Generation of a .tsv file containing gene expression values with the HUGO symbols (again is done if your data is retrieved from microarray chip)
* Quality Check (QC)
  * Batch detection
  * Outliers detection
  * Data distribution check for data quality
* Classification
  * Reading the expressions.tsv file to get the gene expression matrix of interested sample/samples
  * Getting the reference genes signatures expressions matrix (TCGA cohort is set by default you can change it to the path to your reference cohort)
  * Identifying the TME subtype of interested sample/samples by their ssGSEA score correspondence to reference cohorts ssGSEA scores
  * Giving an output .tsv file containing information about the sample/samples TME subtype
* Clusterization of a reference cohort (optional recommended using the default TCGA cohort)
  * Getting a reference cohort input
  * Detecting TME subtype for each sample by its ssGSEA score
  * Getting an output .tsv table that shows  a subtype of each sample in the reference cohort

**Note:
It is recommended to use the default TCGA cohort that is already processed so that the analyses would not have any problem.**


There is also **Methods_Description_-_Batch_correction.ipynb** notebook which is not necessary for classification analyses but it gives more information how the batch correction and outlier detection analyses were done in the article.




