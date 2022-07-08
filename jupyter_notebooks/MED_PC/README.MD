# MED-PC Data Processing Notebooks

## Steps to take

1. Add MED-PC recording data to `./data/timestamp_dataframes` along with the `.MPC` script that you used to record that data. And then in `1_extracting_recording_data_and_metadata.ipynb`, make that cell that states: `all_med_pc_file = glob.glob("./data/timestamp_dataframes/*.txt")` into a Code block. 
- NOTE: Skip this step if you do not have any MED-PC Recording data 

2. Click on `01_extracting_recording_data_and_metadata.ipynb` and then run with `Kernel` > `Restart & Run All`

3. Click on `02_calculating_latencies.ipynb` and then run with `Kernel` > `Restart & Run All`

4. Click on `03_calculating_port_entry_precision.ipynb` and then run with `Kernel` > `Restart & Run All`

5. Analyze spreadsheets and plots created in `./proc`