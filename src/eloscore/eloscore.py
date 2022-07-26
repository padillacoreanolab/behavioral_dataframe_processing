#!/usr/bin/env python3
"""
"""
import re
from collections import defaultdict

def get_all_animal_ids(animal_string):
    """
    Converts a string that contains the ID of animals, and only gets the IDs. 
    This usually removes extra characters that were added. (i.e. "1.1 v 2.2" to ("1.1", "2.2"))

    Args:
        animal_string(str): This is the first param.

    Returns:
        tuple: Of IDs of animals as strings
    """
    # Splitting by space so that we have a list of just the words
    all_words = animal_string.split()
    # Removing all words that are not numbers
    all_numbers = [num for num in all_words if re.match(r'^-?\d+(?:\.\d+)$', num)]
    return tuple(all_numbers)

def calculate_elo_score(subject_elo_score, agent_elo_score, k_factor=20, score=1, number_of_decimals=None):
    """
    Calculates the Elo score of a given subject given it's original score, it's opponent, 
    the K-Factor, and whether or not it has won or not. 
    The calculation is based on: https://www.omnicalculator.com/sports/elo

    Args:
        subject_elo_score(float): The original Elo score for the subject
        agent_elo_score(float): The original Elo score for the agent
        k_factor(int): k-factor, or development coefficient. 
            - It usually takes values between 10 and 40, depending on player's strength 
        score(int): the actual outcome of the game. 
            - In chess, a win counts as 1 point, a draw is equal to 0.5, and a lose gives 0.
        number_of_decimals(int): Number of decimals to round to
        
    Returns:
        int: Updated Elo score of the subject
    """
    # Calculating the Elo score
    rating_difference = agent_elo_score - subject_elo_score
    expected_score = 1 / (1 + 10 ** (rating_difference / 400))
    new_elo_score = subject_elo_score + k_factor * (score - expected_score)
    # Rounding to `number_of_decimals`
    return round(new_elo_score, number_of_decimals)

def add_session_number_column(data_frame, indexes, session_number_column="session_number"):
    """
    Add a column to Pandas DataFrame that contains the session number. 
    This will only add session numbers to the rows specified by indexes. 
    You can fill in the empty cells with method: DataFrame.fillna(method='ffill')
    
    Args:
        data_frame(Pandas DataFrame): The DataFrame to add the session number column
        indexes(list): List of indexes for which rows to add the session numbers
        session_number_column(str): Name of the column to add
        
    Returns:
        Pandas DataFrame: DataFrame with the session numbers added
    """
    copy_data_frame = data_frame.copy()
    session_number = 1
    for index in indexes:
        copy_data_frame.at[index, session_number_column] = session_number
        session_number += 1
    return copy_data_frame

def update_elo_score(winner_id, loser_id, id_to_elo_score=None, default_elo_score=1000, \
    **calculate_elo_score_params):
    """
    Updates the Elo score in a dictionary that contains the ID of the subject as keys, 
    and the Elo score as the values. You can also adjust how the Elo score is calculated with 'calculate_elo_score_params'.
    
    Args:
        winner_id(str): ID of the winner
        loser_id(str): ID of the loser
        id_to_elo_score(dict): Dict that has the ID of the subjects as keys to the Elo Score as values
        default_elo_score(int): The default Elo score to be used if there is not elo score for the specified ID
        **calculate_elo_score_params(kwargs): Other params for the calculate_elo_score to change how the Elo score is calculated
        
    Returns:
        Dict: Dict that has the ID of the subjects as keys to the Elo Score as values
    """
    if id_to_elo_score is None:
        id_to_elo_score = defaultdict(lambda:default_elo_score)
    
    # Getting the current Elo Score
    current_winner_rating = id_to_elo_score[winner_id] 
    current_loser_rating = id_to_elo_score[loser_id] 
    
    # Calculating Elo score            
    id_to_elo_score[winner_id] = calculate_elo_score(subject_elo_score=current_winner_rating, \
        agent_elo_score=current_loser_rating, score=1, number_of_decimals=1, **calculate_elo_score_params)
    id_to_elo_score[loser_id] = calculate_elo_score(subject_elo_score=current_loser_rating, \
        agent_elo_score=current_winner_rating, score=0, number_of_decimals=1, **calculate_elo_score_params)

    return id_to_elo_score