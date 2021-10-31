"""DataFramer

    Imports *.csv files and creates formatted dataframes for use in algorithms
"""
from pathlib import Path
import os

import pandas as pd

def dataframe_importer(list_of_files: list) -> dict:
    """dataframe_importer

    Import numerical odds from various listed csv files

    Args:
        list_of_files (list): file names fitting the attribute template

    Returns:
        dict: key-values, where values are dataframes
    """
    MAX_REGION = 16
    df_dict = {}
    
    df_names = [os.path.basename(path).split(".")[0] for path in list_of_files]

    for i, file_name in enumerate(list_of_files):
        df_path = Path(f"attributes/{file_name}").resolve()
        _df = pd.read_csv(df_path)
        if (_df.shape[0] > MAX_REGION):
            removals = []
            for j in range(_df.shape[0]-MAX_REGION):
                removals.append(j+MAX_REGION)
            _df = _df.drop(removals)
        df_dict[df_names[i]] = _df
    
    print("Data imported for Attributes... done.")
    return df_dict


def heuristic_dataframe_importer(list_of_files: list) -> dict:
    """heuristic_dataframe_importer

    Import numerical odds (head-to-head) from various listed csv files

    Args:
        list_of_files (list): list of those files

    Returns:
        dict: dict of dataframes
    """
    df_dict = {}
    df_names = [os.path.basename(path).split('.')[0] for path in list_of_files]
    for i, file_name in enumerate(list_of_files):
        df_path = Path(f"heuristics/{file_name}").resolve()
        _df = pd.read_csv(df_path)

        ### For H2H_Table dataframes, drop the first column that holds the rank value ###
        if _df.shape[0] == 16:
            _df = _df.drop(columns=[_df.columns[0]])
        df_dict[df_names[i]] = _df

    print("Data imported for Heuristics... done.")
    return df_dict