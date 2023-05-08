# Molecular functional portrait analysis and Tumor microenvironment classification.

## Introduction
Tumor microenvironment (TME) plays a significant role in clinical outcomes and response to antineoplastic therapy. By exerting pro-tumorigenic and anti-tumorigenic actions, tumor-infiltrating immune cells can profoundly influence tumor progression and affect the success of anti-cancer treatments. Cancer-associated fibroblasts (CAFs), as well as angiogenic signals from stromal cells, have also been shown to affect outcomes in cancer patients. 


BostonGene has compiled a curated list of 29 functional genes and  uses single-sample Gene Set Enrichment Analysis (ssGSEA) scores of their expression levels to classify a tumor sample into one of theTME subtypes (shown in Fig. 1 below) Materials provided in this repository will help to identify the TME subtype of an input sample (or you can use the example files in the Cohorts folder).

![image2020-11-4_18-20-47](https://user-images.githubusercontent.com/127855909/228009303-964b1147-0f42-4361-819b-bc22be9ccd97.png)

Using data on the gene expression profiles shown above, BostonGene developed a test that results in creating a Molecular Functional Portrait of a tumor sample.


Molecular Functional Portrait (MFP) is a schematic planetary representation of integrated molecular and functional characteristics of a tumor and its microenvironment that depicts the prevalence of malignant cells and TME cell populations, as well as the activity of tumor-promoting and tumor-suppressing processes. An MFP includes qualitative and quantitative descriptions of several modules built based on the expression patterns of BostonGene curated 29-gene signatures (reference manuscript and table). The size of each module corresponds to the intensity of the normalized single-sample gene set enrichment analysis (ssGSEA) score; the red color denotes pro-cancer processes, while blue color shows anti-cancer processes. Fig. 2 provides short descriptions of each TME subtype with its corresponding MFP portrait.


![image2020-11-4_18-12-26](https://user-images.githubusercontent.com/127855909/228009221-3fe09cc9-a30a-4d3f-aa4b-3641c6278f7e.png)


## Citation
If software, data, and/or website are used in your publication, please cite [Bagaev A et al. Conserved pan-cancer microenvironment subtypes predict response to immunotherapy. Cancer Cell. 2021 Jun 14;39(6):845-865](https://www.cell.com/cancer-cell/fulltext/S1535-6108(21)00222-1#articleInformation)
and make a reference to this repository.


For more information visit [BostonGene’s scientific portal](https://science.bostongene.com/tumor-portrait/)


## Setup
If your environment is already set up according to the requirements in the description of Setup.md file, clone the github repository to start your analysis.


Copy the command below to clone our repository into your environment 


    git clone https://github.com/BostonGene/MFP.git


## Implementation overview
**Note: The example analysis is performed for a cohort. Do not perform  TME classification analyses for one sample only.**


To make the analyses flow easier to understand we created a corresponding graph which is introduced below and helps to visually see every step of the analysis and its priority level.


The graph below introduces the whole analysis flow.

![MFP prediction flowchart](https://user-images.githubusercontent.com/127855909/228008558-4a7163ba-9c23-4107-b2f9-85d674b41499.jpg)


All the analyses are done in the [TME_Classification.ipynb](TME_Classification.ipynb) notebook which is separated into 2 main sections, 1 optional section introducing Data Preparation analyses and 1 additional section if the user wants to add their own reference cohort on which the classification will be done.



The pipeline consists of several nodes that correspond to each other where some of them are optional(depends on user choice):

* Data preparation (optional if you already have your expression matrix)
  * Data retrieval (and normalization if its from CEL files using R) 
  * Generation of a .tsv file containing gene expression values with genes identified by the HUGO symbols (for data retrieved from a microarray chip)
* Quality Check (QC)
  * Batch detection
  * Outliers detection
  * Data distribution check for data quality
* Classification
  * Reading the expressions.tsv file to get the gene expression matrix of the samples of interest
  * Getting the reference gene signatures expressions matrix (TCGA cohort is set by default and can be changed to the path to your reference cohort)
  * Identifying the TME subtype of the sample/samples of interest by comparing their ssGSEA score to the ssGSEA scores of the reference cohorts
  * Giving an output .tsv file with the sample/samples TME subtype
* Clusterization of a reference cohort (optional; we recommend using the default TCGA cohort)
  * Getting a reference cohort input
  * Identifying the TME subtype for each sample based on its ssGSEA score
  * Getting an output .tsv table with the sample subtypes in the reference cohort

**Note: It is recommended to use the default TCGA cohort that has already been processed to avoid possible problems during analysis.**


You can also access the **Methods_Description_-_Batch_correction.ipynb** notebook, which is not necessary for the classification analysis but provides additional information on how the batch correction and outlier detection analyses were done in the article.




