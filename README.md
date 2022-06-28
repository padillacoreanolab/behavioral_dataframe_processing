# Behavioral Dataframe Processing

## Overview 
- This project helps extract and process MED-PC (https://www.med-associates.com/med-pc-v/) recording data. The overall goal is to train mice to associate a tone with a reward(sugary liquid). MED-PC records the times that the tones are played, when the mice enter/exit the port where the reward is dispensed, and the relevant metadata. The experiment is usually run with one subject for a recording that takes about a hour for multiple days. The data processing will calculate various metrics that displays or averages all the trials(each tone going off in a session and it's associated port entry/exit) for each recording session for all the subjects.

## Repository Organization
- [./jupyter_notebooks](./jupyter_notebooks)
    - Directory that has the Jupyter Notebooks to extract/process the MED-PC and the accompanying dataframes/plots that are created from it.
- [./results](./results)
    - Directory that has a record of previous iterations of the Jupyter Notebooks 
- [./src](./src)
    - Directory that has the Python source code used in the Jupyter Notebooks. All the original functions used in the notebooks will be imported from this.

## Steps To Take

### Step 0. Clone this repository 
- Check if you have the Git program on your computer. Do this on the Bash terminal(Linux), Powershell(Windows), and Terminal(Mac). In the terminal, type `git` then enter. 
    - If you don't have Git on your computer, install it following these instructions: https://git-scm.com/downloads
- Once you have Git, download the repository in a folder that you want to save it in
    - From the terminal: `git clone https://github.com/padillacoreanolab/med_pc_repo`
- NOTE: Every time you use this repo after cloning it, check for updates with: 
    - `cd {./path/to}/med_pc_repo`
    - `git pull origin main`

### Step 1. Create Conda Environment to Install Necessary Python libraries
- Check if you have Anaconda:
    - Use the `python` command in your terminal. If you have Anaconda, then it will say "Anaconda" somewhere in the output.
    - If you don't have Anaconda, follow the installation instructions on: https://www.anaconda.com/ 
- Create the Conda environment by following the instructions in: [./bin/conda_environments/doc/README.md](./bin/conda_environments/doc/README.md)
- This step only needs to be done once. Every subsquent time you want to run the analysis, you'll turn on the Conda environment with:
    - `conda deactivate`
    - `conda activate {./path/to}/med_pc_repo/bin/conda_environments/env/med_pc_env`

### Step 2. Turn on Jupyter Notebooks Program
- 1 Use the command `jupyter notebook --allow-root` in your terminal
- 1.1 If a browser window doesn't pop up with Jupyter notebooks, open up a browser window. Then copy and paste the URL given in the command line. It will be followed by `To access the notebook, open this file in a browser:` and `Or copy and paste one of these URLs:`
    - It should have a format similar to: `http://localhost:8888/?token=gsOH0vx373NRzHUmDzwX9TFzBf5Wx6czWIr1irV7ERKBLmlK`
- 2 Click on [./jupyter_notebooks](./jupyter_notebooks) in the Jupyter Notebooks GUI (Should be in the web browser)

### Step 3. Run each Data Processing/Analysis Jupyter Notebooks
- Follow the instructions to run the Jupyter Notebooks at [./jupyter_notebooks/README.MD](./jupyter_notebooks/README.MD)
- The dataframes and the plots should be saved in subdirectories in: (./jupyter_notebooks/proc)[./jupyter_notebooks/proc]

## Resources

### MED-PC Trans
- https://www.med-associates.com/wp-content/uploads/2017/01/DOC-003-R3.4-SOF-735-MED-PC-IV-PROGRAMMER%E2%80%99S-MANUAL.pdf

### Python library to extract data from MED-PC Recording Files
- https://github.com/cyf203/medpc2excel
- https://pypi.org/project/medpc2excel/
