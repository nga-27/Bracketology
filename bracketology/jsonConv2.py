"""
#############################################################################
#
#   JSON Converter
#
#   JSON file: stores relevant attribute, heuristic, and bracket info
#
#
#   Version:    0.1.0, 01-20-19
#
#   Nick Amell
#
#   Version History:
#   -------------------------------------------------------------------------
#   0.0.1, 12-16-18:    Initial JSON parsing/formatting w/ attributes
#   0.0.2, 01-12-19:    Modified to handle new JSON format + heuristics
#   0.1.0, 01-20-19:    Version 1.0 release
#############################################################################
"""
import json
from pprint import pprint
import copy
import os
import pandas as pd 
import numpy as np 
import datetime 

def ConvertToJSON2(bracketCSVFile: str, jsonSchemaFile: str, attrTypeList: list=None, attrListOfDFs: list=None, 
    huerTypeList: list=None, heurListOfDFs: list=None):

    jsonName = "outputs/" + bracketCSVFile.split(".")[0] + ".json"
    jsonSchemaFile = "schemas/" + jsonSchemaFile
    with open(jsonSchemaFile, encoding='utf-8') as dataFile:
        data = json.loads(dataFile.read())

    now = datetime.datetime.now()

    bracketCSV = pd.read_csv(bracketCSVFile)
    bracketColumns = bracketCSV.columns
    bracketNumRows = bracketCSV.shape[0]

    data["DateModified"] = now.strftime("%Y-%m-%d %H:%M")

    # Skip column 0, as it is the seeding number 
    for j in range(len(bracketColumns)-1):
        j += 1
        region = str(bracketColumns[j])

        for i in range(bracketNumRows):
            data["Keys"].append(bracketCSV.values[i][j])
            data["Bracket"][bracketCSV.values[i][j]] = {
                                            "Region": region, 
                                            "RegionKey": str(j-1),
                                            "Seed": str(i+1),
                                            "Attributes": 
                                                {}
                                        }
            

    if (len(bracketColumns) - 1) == 4:
        """ Standard NCAA bracketing of 4 regions """
        data["Matchups"] = {
            "SemiFinal1" : str(bracketColumns[1]) + " vs. " + str(bracketColumns[2]), 
            "SemiFinal2" : str(bracketColumns[3]) + " vs. " + str(bracketColumns[4])
        }

    ### Attribute addtions to the JSON file ###
    if (attrTypeList is not None) and (attrListOfDFs is not None):
        if len(attrListOfDFs) == len(attrTypeList):
            """ parse the df(s), store them in the json """
            for j in range(len(attrTypeList)):
                attrItem = attrTypeList[j]
                df = attrListOfDFs[j]
                

                """ bracketColumns SHOULD MATCH any attribute value!!! """
                for i in range(len(bracketColumns)-1):
                    i += 1

                    for k in range(bracketNumRows):
                        data["Bracket"][bracketCSV.values[k][i]]["Attributes"][attrItem] = df.values[k][i]

    ### Heuristic additions to the JSON file ###
    if (huerTypeList is not None) and (heurListOfDFs is not None):
        if len(huerTypeList) == len(heurListOfDFs):
            data["Heuristics"]["Keys"] = []

            for j in range(len(huerTypeList)):
                heurItem = huerTypeList[j]
                df = heurListOfDFs[j]
                heurName = heurItem.split(".")[0]

                if (df.shape[0] == 16):
                    typeOfHeur = "H2H_table"
                else:
                    typeOfHeur = "SQL_table"

                data["Heuristics"][heurName] = {
                    "file": heurItem,
                    "type": typeOfHeur,
                    "array": []
                }
                data["Heuristics"]["Keys"].append(heurName)

                for i in range(df.shape[0]):
                    data["Heuristics"][heurName]["array"].append(list(df.values[i]))

    #print(data["Heuristics"]["randOnRank"]["array"][0][2])
    
    with open(jsonName, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    print("JSON file creation " + str(jsonName) + "... done.")
    return jsonName



def ConvertToBracketLists2(jsonFile: str) -> list:
    """ Imports the JSON file and exports teams in proper ranking order for analysis and bracket building """

    with open(jsonFile, encoding='utf-8') as dataFile:
        data = json.loads(dataFile.read())

    """
    length = 0
    if 'Matchups' not in data["Bracket"]["Regions"]:
        length = len(data["Bracket"]["Regions"])
    else:
        length = len(data["Bracket"]["Regions"]) - 2
    """

    brackets = []
    for i in range(4):
        region = []
        for j in range(16):
            region.append('')
        brackets.append(region)


    for i in range(4):
        for j in range(16):

            team = data["Keys"][i * 16 + j]
            rank = int(data["Bracket"][team]["Seed"])
            index = MapRankToIndex(rank)
            reg = int(data["Bracket"][team]["RegionKey"])
            brackets[reg][index] = team
        


    finalFour = []
    brackets.append(finalFour)
    #print(brackets)
    print("Create BracketLists... done.")

    return brackets


def MapRankToIndex(rank: int) -> int:
    if rank == 1:
        return 0
    elif rank == 2:
        return 14
    elif rank == 3:
        return 8
    elif rank == 4:
        return 4
    elif rank == 5:
        return 6
    elif rank == 6:
        return 10
    elif rank == 7:
        return 12
    elif rank == 8:
        return 2
    elif rank == 9:
        return 3
    elif rank == 10:
        return 13
    elif rank == 11:
        return 11
    elif rank == 12:
        return 7
    elif rank == 13:
        return 5
    elif rank == 14:
        return 9
    elif rank == 15:
        return 15
    elif rank == 16:
        return 1
