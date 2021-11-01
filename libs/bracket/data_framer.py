"""DataFramer

    Imports *.csv files and creates formatted dataframes for use in algorithms
"""
from pathlib import Path
import json

import pandas as pd


def import_configuration(config_path: Path) -> dict:
    """import_configuration

    Function that pulls in the config.json file or config_example if config is not present

    Args:
        config_path (Path): config file path that is user-defined

    Returns:
        dict: config data object
    """
    if not config_path.exists():
        config_path = Path("config/config_example.json").resolve()
    config_data = json.load(config_path.open('r'))
    return config_data


def dataframe_importer(config_data: dict) -> dict:
    """dataframe_importer

    Import numerical odds from various listed csv files

    Args:
        list_of_files (list): file names fitting the attribute template

    Returns:
        dict: key-values, where values are dataframes
    """
    MAX_REGION = 16 # pylint: disable=invalid-name
    df_dict = {}

    df_names = [attribute['name'] for attribute in config_data.get("attributes", [])]

    for i, file_obj in enumerate(config_data.get("attributes", [])):
        df_path = Path(file_obj['path']).resolve()
        _df = pd.read_csv(df_path)
        if _df.shape[0] > MAX_REGION:
            removals = []
            for j in range(_df.shape[0] - MAX_REGION):
                removals.append(j + MAX_REGION)
            _df = _df.drop(removals)
        df_dict[df_names[i]] = _df

    print("Data imported for Attributes... done.")
    return df_dict


def heuristic_dataframe_importer(config_data: dict) -> dict:
    """heuristic_dataframe_importer

    Import numerical odds (head-to-head) from various listed csv files

    Args:
        list_of_files (list): list of those files

    Returns:
        dict: dict of dataframes
    """
    df_dict = {}
    df_names = [heuristic['name'] for heuristic in config_data.get("heuristics", [])]
    for i, file_obj in enumerate(config_data.get("heuristics", [])):
        df_path = Path(file_obj['path']).resolve()
        _df = pd.read_csv(df_path)

        ### For H2H_Table dataframes, drop the first column that holds the rank value ###
        if _df.shape[0] == 16:
            _df = _df.drop(columns=[_df.columns[0]])
        df_dict[df_names[i]] = _df

    print("Data imported for Heuristics... done.")
    return df_dict
