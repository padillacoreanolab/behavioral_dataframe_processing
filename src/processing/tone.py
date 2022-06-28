#!/usr/bin/env python3
"""
Functions for processing tone information from MED-PC's output

For more information on the MED-PC's programming language, Trans: 
- https://www.med-associates.com/wp-content/uploads/2017/01/DOC-003-R3.4-SOF-735-MED-PC-IV-PROGRAMMER%E2%80%99S-MANUAL.pdf
"""
from collections import defaultdict
import pandas as pd

def get_max_tone_number(tone_pd_series):
    """
    Gets the index, and the number for valid tones in MED-PC's outputted data.
    The recorded tones produce numbers that are divisible by 1000 after the recorded data.
    You can use the index to remove these unnecessary numbers by indexing until that number.

    Args:
        tone_pd_series: Pandas Series
            - A column from the dataframe that contains the data from MED-PC's output file
            - Usually created with dataframe_variable["(S)CSpresentation"]
    Returns:
        int, float
            - The index of the max tone number. This number can be used to index the tone_pd_series to remove unnecessary numbers.
            - The max tone number. This number can be used to verify whether or not the tone_pd_series had unnecessary numbers.
    """
    for index, num in enumerate(tone_pd_series):
        if num % 1000 == 0:
            return index, num
    return index, num

def get_valid_tones(tone_pd_series, drop_1000s=True, dropna=True):
    """
    Removes all unnecessary numbers from a Pandas Series of tone times extracted from MED-PC's dataframe.
    The unnecessary numbers are added after recorded tone times. These numbers are usually divisible by 1000. 
    NaNs are also added after that. So we will remove all tone times entries that meet either of these criterias.

    Args:
        tone_pd_series: Pandas Series
            - 
        dropna: bool
            - Whether or not you want to remove NaNs from tone_pd_series.
            - Usually a good idea because MED-PC adds NaNs to the tone time column.
    Returns: 
        Pandas series
            - The tone times with unnecessary numbers and NaNs removed
    """
    if dropna:
        tone_pd_series = tone_pd_series.dropna()
    if drop_1000s:
        # Getting the index of the tone time that is divisible by 1000
        max_tone_index, max_tone_number = get_max_tone_number(tone_pd_series=tone_pd_series)
        tone_pd_series = tone_pd_series[:max_tone_index]
    # Removing all numbers that are after the max tone
    return tone_pd_series

def get_first_port_entries_after_tone(tone_pd_series, port_entries_pd_series, port_exits_pd_series):
    """
    From an array of times of tones being played and subject's entries to a port, 
    finds the first entry immediately after every tone. 
    Makes a dataframe of tone times to first port entry times

    Args:
        tone_pd_series: Pandas Series
            - All the times the tone is being played
        port_entries_pd_series: Pandas Series
            - All the times that the port is being entered
    Returns: 
        Pandas DataFrame
            - A dataframe of tone times to first port entry times
    """
    # Creating a dictionary of index(current row number we're on) to current/next tone time and first port entry
    first_port_entry_dict = defaultdict(dict)
    for index, current_tone_time in tone_pd_series.items():
        # Using a counter so that we don't go through all the rows that include NaNs
        try:
            first_port_entry_dict[index]["current_tone_time"] = current_tone_time
            # Getting all the port entries that happened after the tone started
            # And then getting the first one of those port entries
            first_port_entry_after_tone = port_entries_pd_series[port_entries_pd_series >= current_tone_time].min()
            first_port_entry_dict[index]["first_port_entry_after_tone"] = first_port_entry_after_tone
            # Getting all the port exits that happened after the entery
            # And then getting the first one of those port exits
            port_exit_after_first_port_entry_after_tone = port_exits_pd_series[port_exits_pd_series > first_port_entry_after_tone].min()
            first_port_entry_dict[index]["port_exit_after_first_port_entry_after_tone"] = port_exit_after_first_port_entry_after_tone
        except:
            print("Look over value {} at index {}".format(current_tone_time, index))
    return pd.DataFrame.from_dict(first_port_entry_dict, orient="index")

def get_last_port_entries_before_tone(tone_pd_series, port_entries_pd_series, port_exits_pd_series):
    """
    From an array of times of tones being played and subject's entries to a port, 
    finds the first entry immediately after every tone. 
    Makes a dataframe of tone times to first port entry times

    Args:
        tone_pd_series: Pandas Series
            - All the times the tone is being played
        port_entries_pd_series: Pandas Series
            - All the times that the port is being entered
    Returns: 
        Pandas DataFrame
            - A dataframe of tone times to first port entry times
    """
    # Creating a dictionary of index(current row number we're on) to current/next tone time and first port entry
    last_port_entry_dict = defaultdict(dict)
    for index, current_tone_time in tone_pd_series.items():
        # Using a counter so that we don't go through all the rows that include NaNs
        try:
            last_port_entry_dict[index]["current_tone_time"] = current_tone_time
            # Getting all the port entries that happened after the tone started
            # And then getting the first one of those port entries
            last_port_entry_before_tone = port_entries_pd_series[port_entries_pd_series <= current_tone_time].max()
            last_port_entry_dict[index]["last_port_entry_before_tone"] = last_port_entry_before_tone
            # Getting all the port exits that happened after the entery
            # And then getting the first one of those port exits
            port_exit_after_last_port_entry_before_tone = port_exits_pd_series[port_exits_pd_series > last_port_entry_before_tone].min()
            last_port_entry_dict[index]["port_exit_after_last_port_entry_before_tone"] = port_exit_after_last_port_entry_before_tone
        except:
            print("Look over value {} at index {}".format(current_tone_time, index))
    return pd.DataFrame.from_dict(last_port_entry_dict, orient="index")

def get_concatted_first_porty_entry_after_tone_dataframe(concatted_medpc_df, tone_time_column="(S)CSpresentation", \
        port_entry_column="(P)Portentry", port_exit_column="(N)Portexit", subject_column="subject", date_column="date", \
        stop_with_error=False):
    """
    Creates dataframes of the time of the tone, and the first port entry after that tone.
    Along with the corresponding metadata of the path of the file, the date, and the subject.
    This is created from a dataframe that contains tone times, port entry times, and associated metadata.
    Which is usually from the extract.dataframe.get_medpc_dataframe_from_list_of_files function 

    Args:
        concatted_medpc_df: Pandas Dataframe 
            - Output of extract.dataframe.get_medpc_dataframe_from_list_of_files
            - Includes tone playing time, port entry time, subject, and date for each recording session
        tone_time_column: str
            - Name of the column of concatted_medpc_df that has the array port entry times
        port_entry_column: str
            - Name of the column of concatted_medpc_df that has the array port entry times
        subject_column: str
            - Name of the column of concatted_medpc_df that has the subject's ID
        date_column: str
            - Name of the column of concatted_medpc_df that has the date of the recording
        stop_with_error: bool
            - Flag to terminate the program when an error is raised.
            - Sometimes recordings can be for testing and don't include any valid tone times
    
    Returns: 
        Pandas Dataframe
            -
    """
    # List to combine all the Data Frames at the end
    all_first_port_entry_df = []
    for file_path in concatted_medpc_df["file_path"].unique():
        current_file_df = concatted_medpc_df[concatted_medpc_df["file_path"] == file_path]
        valid_tones = get_valid_tones(tone_pd_series=current_file_df[tone_time_column])
        # Sometimes the valid tones do not exist because it was a test recording
        if not valid_tones.empty:
            # All the first port entries for each tone            
            first_port_entry_df = get_first_port_entries_after_tone(tone_pd_series=valid_tones, \
                port_entries_pd_series=current_file_df[port_entry_column], port_exits_pd_series=current_file_df[port_exit_column])
            # Adding the metadata as columns
            first_port_entry_df["file_path"] = file_path
            # Making sure that there is only one date and subject for all the rows
            if len(current_file_df[date_column].unique()) == 1 and len(current_file_df[subject_column].unique()) == 1:
                # This assumes that all the date and subject keys are the same for the file
                first_port_entry_df[date_column] = current_file_df[date_column].unique()[0]
                first_port_entry_df[subject_column] = current_file_df[subject_column].unique()[0]
            elif stop_with_error:
                raise ValueError("More then one date or subject in {}".format(file_path))
            else:
                print("More then one date or subject in {}".format(file_path))
            all_first_port_entry_df.append(first_port_entry_df)
        elif valid_tones.empty and stop_with_error:
            raise ValueError("No valid tones for {}".format(file_path))
        else:
            print("No valid tones for {}".format(file_path))
    # Index repeats itself because it is concatenated with multiple dataframes
    return pd.concat(all_first_port_entry_df).reset_index(drop="True")

def get_concatted_last_porty_entry_before_tone_dataframe(concatted_medpc_df, tone_time_column="(S)CSpresentation", \
        port_entry_column="(P)Portentry", port_exit_column="(N)Portexit", subject_column="subject", date_column="date", \
        stop_with_error=False):
    """
    Creates dataframes of the time of the tone, and the first port entry after that tone.
    Along with the corresponding metadata of the path of the file, the date, and the subject.
    This is created from a dataframe that contains tone times, port entry times, and associated metadata.
    Which is usually from the extract.dataframe.get_medpc_dataframe_from_list_of_files function 

    Args:
        concatted_medpc_df: Pandas Dataframe 
            - Output of extract.dataframe.get_medpc_dataframe_from_list_of_files
            - Includes tone playing time, port entry time, subject, and date for each recording session
        tone_time_column: str
            - Name of the column of concatted_medpc_df that has the array port entry times
        port_entry_column: str
            - Name of the column of concatted_medpc_df that has the array port entry times
        subject_column: str
            - Name of the column of concatted_medpc_df that has the subject's ID
        date_column: str
            - Name of the column of concatted_medpc_df that has the date of the recording
        stop_with_error: bool
            - Flag to terminate the program when an error is raised.
            - Sometimes recordings can be for testing and don't include any valid tone times
    
    Returns: 
        Pandas Dataframe
            -
    """
    # List to combine all the Data Frames at the end
    all_last_port_entry_df = []
    for file_path in concatted_medpc_df["file_path"].unique():
        current_file_df = concatted_medpc_df[concatted_medpc_df["file_path"] == file_path]
        valid_tones = get_valid_tones(tone_pd_series=current_file_df[tone_time_column])
        # Sometimes the valid tones do not exist because it was a test recording
        if not valid_tones.empty:
            # All the first port entries for each tone            
            last_port_entry_df = get_last_port_entries_before_tone(tone_pd_series=valid_tones, \
                port_entries_pd_series=current_file_df[port_entry_column], port_exits_pd_series=current_file_df[port_exit_column])
            # Adding the metadata as columns
            last_port_entry_df["file_path"] = file_path
            # Making sure that there is only one date and subject for all the rows
            if len(current_file_df[date_column].unique()) == 1 and len(current_file_df[subject_column].unique()) == 1:
                # This assumes that all the date and subject keys are the same for the file
                last_port_entry_df[date_column] = current_file_df[date_column].unique()[0]
                last_port_entry_df[subject_column] = current_file_df[subject_column].unique()[0]
            elif stop_with_error:
                raise ValueError("More then one date or subject in {}".format(file_path))
            else:
                print("More then one date or subject in {}".format(file_path))
            all_last_port_entry_df.append(last_port_entry_df)
        elif valid_tones.empty and stop_with_error:
            raise ValueError("No valid tones for {}".format(file_path))
        else:
            print("No valid tones for {}".format(file_path))
    # Index repeats itself because it is concatenated with multiple dataframes
    return pd.concat(all_last_port_entry_df).reset_index(drop="True")

def main():
    """
    Main function that runs when the script is run
    """

if __name__ == '__main__': 
    main()
