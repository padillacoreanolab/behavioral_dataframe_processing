# Refactoring and Documentation Project

## Daily Notes

2022, December 5th
- Updated repo README.md with formatting and description 
- Finished reading: https://towardsdatascience.com/how-to-refactor-a-jupyter-notebook-ed531b6a17
    - Suggestions: 
        1. Run notebook from start to end and ensure everything works.
        2. Make a copy of the original notebook.
        3. Convert Jupyter notebook into a plain Python file.
        4. Remove print statements, e.g. print(...), df.head(), df.plot(...)
        5. Code Smells
            - https://github.com/davified/clean-code-ml
        6. Define refactoring boundary and add a characterisation test.
- Started refactoring: results/2022_12_05_nb_refactoring/pilot_3/pilot_3_tube_test_processing.py
    - Using pylint with the Python script version of the Jupyter Notebook
    - Changed `sheet_name_to_everything[key]` to `value` for all instances when iterating through the dictionary

## Things TODO
- [] Make a notebook to process one sheet at at time
    - Then create a notebook to process more than one sheet at a time
- [] Run Pylint with src code