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
import enum
import json
from pathlib import Path
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
                          heuristic_dict: dict) -> Path:
    """generate_json_bracket

    Combine attributes, the bracket csv, and heuristics into a data-heavy json file

    Args:
        bracket_csv_file (str): file path
        json_schema_file (str): file path for the template json file
        attribute_dict (dict): dict of attribute content
        heuristic_dict (dict): dict of heuristic content

    Returns:
        Path: output file path for the generated json file
    """
    output_dir = Path("outputs").resolve()
    output_dir.mkdir(exist_ok=True)

    json_file_name = Path(output_dir / f'{bracket_csv_file.split(".")[0]}.json').resolve()
    data = json.load(Path(f"schemas/{json_schema_file}").resolve().open('r'))

    data["DateModified"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    bracket_csv = pd.read_csv(bracket_csv_file)

    # Skip column 0, as it is the seeding number
    for j in range(len(bracket_csv.columns)-1):
        j += 1
        region = str(bracket_csv.columns[j])

        for i in range(bracket_csv.shape[0]):
            data["Keys"].append(bracket_csv.values[i][j])
            data["Bracket"][bracket_csv.values[i][j]] = {
                "Region": region,
                "RegionKey": str(j-1),
                "Seed": str(i+1),
                "Attributes": {}
            }


    if (len(bracket_csv.columns) - 1) == 4:
        #  Standard NCAA bracketing of 4 regions
        data["Matchups"] = {
            "SemiFinal1" : str(bracket_csv.columns[1]) + " vs. " + str(bracket_csv.columns[2]),
            "SemiFinal2" : str(bracket_csv.columns[3]) + " vs. " + str(bracket_csv.columns[4])
        }

    ### Attribute additions to the JSON file ###
    for attribute_name in attribute_dict:
        # Parse the df(s), store them in the json
        _df = attribute_dict[attribute_name]

        # bracketColumns SHOULD MATCH any attribute value!!!
        for i in range(len(bracket_csv.columns)-1):
            i += 1
            for k in range(bracket_csv.shape[0]):
                data["Bracket"][bracket_csv.values[k][i]]["Attributes"][attribute_name] = \
                    _df.values[k][i]

    ### Heuristic additions to the JSON file ###
    for heuristic_name in heuristic_dict:
        data["Heuristics"]["Keys"] = []

        _df = heuristic_dict[heuristic_name]

        data["Heuristics"][heuristic_name] = {
            "file": f"{heuristic_name}.csv",
            "type": "H2H_table" if _df.shape[0] == 16 else "SQL_Table",
            "array": [],
            "table": {}
        }
        data["Heuristics"]["Keys"].append(heuristic_name)

        if data['Heuristics'][heuristic_name]['type'] == 'H2H_table':
            for i in range(_df.shape[0]):
                data["Heuristics"][heuristic_name]["array"].append(list(_df.values[i]))
        else:
            for i, team in enumerate(_df['Team']):
                data["Heuristics"][heuristic_name]["table"][team.strip()] = {
                    "round_1": _df['Round 1'][i],
                    "round_2": _df["Round 2"][i],
                    "round_3": _df["Round 3"][i],
                    "round_4": _df["Round 4"][i],
                    "round_5": _df["Round 5"][i],
                    "round_6": _df["Round 6"][i]
                }

    json.dump(data, json_file_name.open('w'))

    print(f"JSON file creation {json_file_name}... done.")
    return json_file_name



def convert_from_json_to_bracket_list(bracket_json: Path) -> list:
    """convert_from_json_bracket_list

    Imports the JSON file and exports teams in proper ranking order for analysis and bracket
    building

    Args:
        bracket_json (Path): path to newly generated bracket json file with loaded content

    Returns:
        list: new bracket object list
    """
    data = json.load(bracket_json.open('r'))

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

    final_four = []
    brackets.append(final_four)
    print("Create BracketLists... done.")
    return brackets
