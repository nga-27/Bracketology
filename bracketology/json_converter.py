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
from pathlib import Path
import os
import datetime 

import pandas as pd 

MAP_RANK_TO_INDEX = {
    "1": 0,
    "2": 14,
    "3": 8,
    "4": 4,
    "5": 6,
    "6": 10,
    "7": 12,
    "8": 2,
    "9": 3,
    "10": 13,
    "11": 11,
    "12": 7,
    "13": 5,
    "14": 9,
    "15": 15,
    "16": 1
}


def generate_json_bracket(bracket_csv_file: str,
                          json_schema_file: str,
                          attribute_dict: dict, 
                          heuristic_dict: dict) -> str:
    """generate_json_bracket

    Combine attributes, the bracket csv, and heuristics into a data-heavy json file

    Args:
        bracket_csv_file (str): file path
        json_schema_file (str): file path for the template json file
        attr_type_list (list, optional): list of attribute types. Defaults to None.
        attr_df_list (list, optional): list of attribute files. Defaults to None.
        hueristic_type_list (list, optional): list of heuristic types. Defaults to None.
        heur_df_list (list, optional): list of heuristic files. Defaults to None.

    Returns:
        Path: output file path for the generated json file
    """
    output_dir = Path("outputs").resolve()
    output_dir.mkdir(exist_ok=True)

    json_file_name = Path(output_dir / f'{bracket_csv_file.split(".")[0]}.json').resolve()
    schema_file = Path(f"schemas/{json_schema_file}").resolve()
    with open(schema_file, encoding='utf-8') as dataFile:
        data = json.loads(dataFile.read())

    now = datetime.datetime.now()

    bracket_csv = pd.read_csv(bracket_csv_file)
    bracket_columns = bracket_csv.columns
    bracket_rows = bracket_csv.shape[0]

    data["DateModified"] = now.strftime("%Y-%m-%d %H:%M")

    # Skip column 0, as it is the seeding number 
    for j in range(len(bracket_columns)-1):
        j += 1
        region = str(bracket_columns[j])

        for i in range(bracket_rows):
            data["Keys"].append(bracket_csv.values[i][j])
            data["Bracket"][bracket_csv.values[i][j]] = {
                "Region": region, 
                "RegionKey": str(j-1),
                "Seed": str(i+1),
                "Attributes": {}
            }
            

    if (len(bracket_columns) - 1) == 4:
        """ Standard NCAA bracketing of 4 regions """
        data["Matchups"] = {
            "SemiFinal1" : str(bracket_columns[1]) + " vs. " + str(bracket_columns[2]), 
            "SemiFinal2" : str(bracket_columns[3]) + " vs. " + str(bracket_columns[4])
        }

    ### Attribute addtions to the JSON file ###
    for attribute_name in attribute_dict:
        # Parse the df(s), store them in the json
        _df = attribute_dict[attribute_name]

        # bracketColumns SHOULD MATCH any attribute value!!!
        for i in range(len(bracket_columns)-1):
            i += 1
            for k in range(bracket_rows):
                data["Bracket"][bracket_csv.values[k][i]]["Attributes"][attribute_name] = \
                    _df.values[k][i]

    ### Heuristic additions to the JSON file ###
    for heuristic_name in heuristic_dict:
        data["Heuristics"]["Keys"] = []

        _df = heuristic_dict[heuristic_name]

        if (_df.shape[0] == 16):
            type_of_heur = "H2H_table"
        else:
            type_of_heur = "SQL_table"

        data["Heuristics"][heuristic_name] = {
            "file": f"{heuristic_name}.csv",
            "type": type_of_heur,
            "array": []
        }
        data["Heuristics"]["Keys"].append(heuristic_name)

        for i in range(_df.shape[0]):
            data["Heuristics"][heuristic_name]["array"].append(list(_df.values[i]))

    #print(data["Heuristics"]["randOnRank"]["array"][0][2])
    json_fp = json_file_name.open('w')
    json.dump(data, json_fp)

    print(f"JSON file creation {json_file_name}... done.")
    return json_file_name



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
            rank = data["Bracket"][team]["Seed"]
            index = MAP_RANK_TO_INDEX[rank]
            reg = int(data["Bracket"][team]["RegionKey"])
            brackets[reg][index] = team

    finalFour = []
    brackets.append(finalFour)
    #print(brackets)
    print("Create BracketLists... done.")

    return brackets
