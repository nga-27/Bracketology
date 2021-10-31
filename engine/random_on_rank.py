"""rand_on_rank

    Default winner picking algorithm supplied: uses simple ratios of ranks + 
    a random choice from python's random library. Default picking algorithm.
"""
import random

def random_on_rank(team_a: dict, team_b: dict, heuristic) -> str:
    """random_on_rank
    
    Using a random number and fixed random template (heuristic), determine winner by mapping
    rank/seed to a random number spectrum.
    
    Args:
        team_a (dict): sub content of the large json object revolving around one of the 2 teams
        team_b (dict): sub content of the large json object revolving around the other of the 2
                       teams
        heuristic (dict): data to feed the chosen algorithm below

    Returns:
        str: team name of the winner
    """
    team_a_name = list(team_a.keys())[0]
    team_b_name = list(team_b.keys())[0]
    team_a_seed = int(team_a[team_a_name]["Seed"])
    team_b_seed = int(team_b[team_b_name]["Seed"])

    number_line_a = heuristic["randOnRank"]["array"][team_a_seed-1][team_b_seed-1]

    value = random.random()
    if (value <= number_line_a):
        winner = team_a_name
    else:
        winner = team_b_name

    return winner