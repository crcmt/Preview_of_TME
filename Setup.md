# Setup
All of the calculations and analyses are done in the iPython notebook. Most of the code is written in Python. There are also parts written in R in order to get data from GEO in a CEL file and process it to RNA-seq type data.
We highly recommend to install our python virtual environment to perform the analysis. Detailed instruction in “Preparation of the environment” section
## Environment Requirements 
* Python 3.10
  * For the required packages look into requirements.txt file
* R 4.0.0 or higher
  * For R packages look into install_R_packages.R file
* Jupyter notebook with its R and Python kernels
* WSL for Windows users only
## WSL installation (Essential for Windows users)
If you are a windows user at first you need to install WSL on your computer and if your operating system is unix based then simply skip this step.


Open the power shell in administrator mode and enter the command provided below after which restart your system.


    wsl --install
      
      
*This command enables the features necessary to run WSL and install the Ubuntu distribution of Linux.*


The first time you launch a newly installed Linux distribution, a console window will open and you'll be asked to wait for files to decompress and be stored on your machine. All future launches should take less than a second.


If you want to make changes during installation like changing default distribution from Ubuntu to another one look into the Microsofts tutorial and best practices on how to install WSL https://learn.microsoft.com/en-us/windows/wsl/install.


## Preparation of the environment
Please follow the instructions in the same order to not have any problems with installation.

***Installation of python using apt source***


    sudo apt-get update
    sudo apt-get install python3.10-venv python3.10-dev python3-pip
    python3.10 -m venv MFP_env


After completing all of the above steps use the command below to install jupyter notebook on your device. 
pip install notebook


**After the installation of the notebook please restart your device, enter the command below to start the jupyter notebook.
jupyter notebook**


After opening the notebook, complete all of the remaining steps using its terminal.


    source MFP_env/bin/activate
    cd MFP_env
    clone https://github.com/BostonGene/MFP
    cd MFP
    pip install --upgrade pip wheel --no-cache-dir
    pip install -r requirements.txt --no-cache-dir


***Installation of python using conda***


If you want to create a python environment via conda please follow the link below:


https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/installing-with-conda.html


***Install the jupyter kernel for your environment***


    python -m ipykernel install --user --name=MFP_env


**If your data is in CEL format you have to download R and all of the required packages.**


***Installation and preparation of R***


    sudo apt install r-base-core 
    Rscript -e "install.packages('IRkernel')"
    Rscript -e "IRkernel::installspec(user = FALSE)"
    Rscript -e 'install.packages("httr", repos="http://cran.rstudio.com/")' 
    Rscript -e 'install.packages("RJSONIO", repos="http://cran.rstudio.com/")' 
    sudo apt-get install libxml2-dev libcurl4-openssl-dev libssl-dev
    Rscript install_R_packages.R


