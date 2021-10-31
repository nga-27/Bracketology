"""engine.py

    Generic picking class that is fed by configurable algorithms.
"""
import json
from pathlib import Path

### ALGORITHM CHOICE(S) IMPORTS HERE ###
from config.default import random_on_rank
# from .template_algorithm import template_name

########################################################################################
##          USER-DEFINED IMPORT CONFIGURED HERE (and farther below)                   ##
## Import custom algorithm (if not 'template_algorithm' above) here as examples above ##
########################################################################################


###################################################################
##      DO NOT EDIT BELOW THIS SECTION!!! (Internal-use only)    ##
###################################################################
def populate_bracket(flat_bracket: list, json_file: Path) -> list:
    """populate_bracket

    Uses MakePick and algorithms below to fill in bracket with picks

    Args:
        flat_bracket (list): bracket object represented as a "flat" list
        json_file (Path): data-loaded json file for the bracket

    Returns:
        list: filled out bracket with picked winners, etc.
    """
    data = json.load(json_file.open('r'))
    round_val = 1

    for i in range(4):
        next_game = 16
        cur_game = 0
        while next_game < 31:
            if cur_game < 16:
                round_val = 1
            elif cur_game < 24:
                round_val = 2
            elif cur_game < 28:
                round_val = 3
            else:
                round_val = 4

            team_a = flat_bracket[i][cur_game]
            team_b = flat_bracket[i][cur_game+1]
            team_c = make_pick(
                {team_a: data["Bracket"][team_a]},
                {team_b: data["Bracket"][team_b]},
                heuristic=data["Heuristics"],
                round_num=round_val
            )
            flat_bracket[i][next_game] = team_c
            next_game += 1
            cur_game += 2

    # Finish the final four part of the bracket
    round_val = 5
    team_a = flat_bracket[0][30]
    team_b = flat_bracket[1][30]
    team_c = make_pick(
        {team_a: data["Bracket"][team_a]},
        {team_b: data["Bracket"][team_b]},
        heuristic=data["Heuristics"],
        round_num=round_val
    )
    flat_bracket[4][0] = team_c

    team_a = flat_bracket[2][30]
    team_b = flat_bracket[3][30]
    team_c = make_pick(
        {team_a: data["Bracket"][team_a]},
        {team_b: data["Bracket"][team_b]},
        heuristic=data["Heuristics"],
        round_num=round_val
    )
    flat_bracket[4][1] = team_c

    round_val = 6
    team_a = flat_bracket[4][0]
    team_b = flat_bracket[4][1]
    team_c = make_pick(
        {team_a: data["Bracket"][team_a]},
        {team_b: data["Bracket"][team_b]},
        heuristic=data["Heuristics"],
        round_num=round_val
    )
    flat_bracket[4][2] = team_c

    return flat_bracket


def make_pick(team_a: dict, team_b: dict, heuristic: dict, round_num: int = 0) -> str:
    """make_pick

    At its core, this uses the heuristic and algorithm chosen to make the winner pick of a game.
    All inputs to this function are available for any configurable algorithm. "TeamXFull" variables
    refer to entire JSON object of team, including rank and attributes, for customizable algorithm
    use.

    Args:
        team_a (dict): sub content of the large json object revolving around one of the 2 teams
        team_b (dict): sub content of the large json object revolving around the other of the 2
                       teams
        heuristic (dict): data to feed the chosen algorithm below
        round_num (int, optional): for algorithms that require round number for information

    Returns:
        str: team name of the winner
    """
    ###################################################################
    ##      USER-DEFINED ALGO CONFIGURED BELOW                       ##
    ###################################################################
    winner = ""
    if round_num < 15:
        # There should never be more than 6? rounds. Only for compilation/pylint
        winner = random_on_rank(team_a, team_b, heuristic)
    #winner = template_name(team_a, team_b, heuristic, round_num=round_num)

    return winner
