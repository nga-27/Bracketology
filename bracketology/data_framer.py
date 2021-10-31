"""DataFramer

    Imports *.csv files and creates formatted dataframes for use in algorithms
"""
from pathlib import Path

import pandas as pd

def dataframe_importer(list_of_files: list) -> list:
    """dataframe_importer

    Import numerical odds from various listed csv files

    Args:
        list_of_files (list): file names fitting the attribute template

    Returns:
        list: list of dataframes
    """
    MAX_REGION = 16
    list_of_dfs = []
    
    for file_name in list_of_files:
        df_path = Path(f"attributes/{file_name}").resolve()
        _df = pd.read_csv(df_path)
        if (_df.shape[0] > MAX_REGION):
            removals = []
            for j in range(_df.shape[0]-MAX_REGION):
                removals.append(j+MAX_REGION)
            _df = _df.drop(removals)
        list_of_dfs.append(_df)
    
    print("Data imported for Attributes... done.")
    return list_of_dfs


def heuristic_dataframe_importer(list_of_files: list) -> list:
    """heuristic_dataframe_importer

    Import numerical odds (head-to-head) from various listed csv files

    Args:
        list_of_files (list): list of those files

    Returns:
        list: list of dataframes
    """
    list_of_dfs = []
    for file_name in list_of_files:
        df_path = Path(f"heuristics/{file_name}").resolve()
        _df = pd.read_csv(df_path)

        ### For H2H_Table dataframes, drop the first column that holds the rank value ###
        if _df.shape[0] == 16:
            _df = _df.drop(columns=[_df.columns[0]])
        list_of_dfs.append(_df)

    print("Data imported for Heuristics... done.")
    return list_of_dfs