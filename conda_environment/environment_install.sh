#!/usr/bin/env bash

# Moving to the root directory of the Github repo
cd $(git rev-parse --show-toplevel)

# Turning off the Conda Environment 
# so that you don't add anything onto an existing environment
conda deactivate

# Creating the Conda environment
# Doing it in the root directory to simplify
conda create --prefix ./behavioral_processing_env python=3.9 --yes
# Turning on the Conda environment
conda activate ./behavioral_processing_env

# Installing general data processing libraries
conda install -c conda-forge notebook --yes
conda install -c conda-forge pandas --yes
conda install -c conda-forge openpyxl --yes
conda install -c conda-forge matplotlib --yes

# Installing libraries for MED-PC data processing
pip install medpc2excel 
conda install -c conda-forge moviepy --yes
conda install -c conda-forge xlrd --yes
conda install -c conda-forge matplotlib-label-lines --yes
