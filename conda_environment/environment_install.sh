#!/usr/bin/env bash

# Moving to the root directory of the Github repo
# Uncomment if using Linux or Mac
cd $(git rev-parse --show-toplevel)

# Creating the Conda environment
# Doing it in the root directory to simplify
conda create --prefix ./behavioral_processing_env python=3.9 --yes
# Turning on the Conda environment
conda activate ./behavioral_processing_env

# Installing the Python libraries
pip install medpc2excel
conda install -c conda-forge openpyxl --yes
conda install -c conda-forge notebook --yes
conda install -c conda-forge matplotlib --yes

# Running Jupyter Notebooks
jupyter notebook --allow-root