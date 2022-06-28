#!/usr/bin/env python3
"""
Functions for processing port information from MED-PC's output

For more information on the MED-PC's programming language, Trans: 
- https://www.med-associates.com/wp-content/uploads/2017/01/DOC-003-R3.4-SOF-735-MED-PC-IV-PROGRAMMER%E2%80%99S-MANUAL.pdf
"""
import numpy as np

def scale_time_to_whole_number(time, multiplier=100):
    """
    Function used to convert times that are floats into whole numbers by scaling it. i.e. from 71.36 to 7136
    This is used with pandas.DataFrame.apply/pandas.Series.apply to convert a column of float times to integer times.

    Args:
        time: float
            - The time in seconds that something is happening
    Returns: 
        int:
            - Converted whole number time
    """
    try:
        if np.isnan(time):
            return 0
        else:
            return int(time * multiplier)
    except:
        return 0

def get_all_port_entry_increments(port_entry_scaled, port_exit_scaled):
    """
    Gets all the numbers that are in the duration of the port entry and port exit times. 
    i.e. If the port entry was 7136 and port exit was 7142, we'd get [7136, 7137, 7138, 7139, 7140, 7141, 7142]
    This is done for all port entry and port exit times pairs between two Pandas Series

    Args:
        port_entry_scaled: Pandas Series
            - A column from a MED-PC Dataframe that has all the port entry times scaled
            (usually with the scale_time_to_whole_number function)
        port_exit_scaled: Pandas Series
            - A column from a MED-PC Dataframe that has all the port exit times scaled
            (usually with the scale_time_to_whole_number function)
    Returns: 
        Numpy array:
            - 1D Numpy Array of all the numbers that are in the duration of all the port entry and port exit times
    """
    all_port_entry_ranges = [np.arange(port_entry, port_exit+1) for port_entry, port_exit in zip(port_entry_scaled, port_exit_scaled)]
    return np.concatenate(all_port_entry_ranges)

def get_inside_port_mask(inside_port_numbers, max_time):
    """
    Gets a mask of all the times that the subject is inside the port. 
    First a range of number from 1 to the number for the max time is created.
    Then, a mask is created by seeing which numbers are within the inside port duration

    Args:
        max_time: int
            - The number that represents the largest number for the time. 
                - Usually this will be the number for the last tone played.  
            - We recommend adding 2001 if you are just using the number for the last tone played
                - This is because we are looking 20 seconds before and after. 
                - And 20 seconds becomes 2000 when scaled with our method.
        inside_port_numbers: Numpy Array
            - All the increments of of the duration that the subject is within the port
    Returns: 
        session_time_increments: Numpy Array
            - Range of number from 1 to max time 
        inside_port_mask: Numpy Array
            - The mask of True or False if the subject is in the port during the time of that index
    """
    if max_time is None:
        max_time = inside_port_numbers.max()
    session_time_increments = np.arange(1, max_time+1)
    inside_port_mask = np.isin(session_time_increments, inside_port_numbers)
    return session_time_increments, inside_port_mask

def get_inside_port_probability_averages_for_all_increments(tone_times, inside_port_mask, before_tone_duration=2000, after_tone_duration=2000):
    """
    Calculates the average probability that a subject is in the port between sessions. 
    This is calculated by seeing the ratio that a subject is in the port at a given time increment 
    that's the same time difference to the tone with all the other sessions. 
    i.e. The time increment of 10.01 seconds after the tone for all sessions.
    
    Args:
        tone_times: list or Pandas Series
            - An array of the times that the tone has played
        inside_port_mask: Numpy Array
            - The mask where the subject is in the port based on the index being the time increment
        before_tone_duration: int
            - The number of increments before the tone to be analyzed
        after_tone_duration: int
            - The number of increments after the tone to be analyzed
    Returns: 
        Numpy Array
            - The averages of the probabilities that the subject is inside the port for all increments
    """
    result = []
    for tone_start in tone_times:
        tone_start_int = int(tone_start)
        result.append(inside_port_mask[tone_start_int - before_tone_duration: tone_start_int + after_tone_duration])
    return np.stack(result).mean(axis=0)

def main():
    """
    Main function that runs when the script is run
    """

if __name__ == '__main__': 
    main()
