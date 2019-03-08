"""
#############################################################################
#
#   DataFramer
#
#   Imports *.csv files and creates formatted dataframes for use in algorithms
#
#
#   Version:    0.1.0, 01-20-19
#
#   Nick Amell
#
#   Version History:
#   -------------------------------------------------------------------------
#   0.0.1, 12-16-18:    Initial Dataframe importing for attributes
#   0.0.2, 01-12-19:    Updated dataframe importing for attributes, added heuristics
#   0.1.0, 01-20-19:    Version 1.0 release
#############################################################################
"""
import pandas as pd 
import numpy as np 

def DataFrameLister(listOfFiles: list, listOfListsOfSheets: list=None):
    """ Currently not supporting a list of sheets 
            ASSUME .CSV for now
    """
    if not listOfFiles:
        return []

    MAX_REGION = 16

    listOfDFs = []
    for i in range(len(listOfFiles)):
        fName = "./attributes/" + listOfFiles[i]
        df = pd.read_csv(fName)
        if (df.shape[0] > MAX_REGION):
            removals = []
            for j in range(df.shape[0]-MAX_REGION):
                removals.append(j+MAX_REGION)
            df = df.drop(removals)
        listOfDFs.append(df)
    
    print("Data imported for Attributes... done.")
    return listOfDFs


def HeuristicDFLister(listOfFiles: list, listOfListOfSheets: list=None):
    """ Currently not supporting a list of sheets 
            ASSUME .CSV for now
    """
    if not listOfFiles:
        return []

    listOfDFs = []
    for i in range(len(listOfFiles)):
        fName = "./heuristics/" + listOfFiles[i]
        df = pd.read_csv(fName)

        ### For H2H_Table dataframes, drop the first column that holds the rank value ###
        if df.shape[0] == 16:
            df = df.drop(columns=[df.columns[0]])
        listOfDFs.append(df)

    print("Data imported for Heuristics... done.")
    return listOfDFs