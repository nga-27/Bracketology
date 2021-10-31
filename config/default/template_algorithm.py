"""template_algorithm.py

    Generic template for users to create their own picking algorithms. Use this to build custom
    picking algorithm. Use 'randOnRank.py' as a further example as to how to properly construct a
    picking algorithm.

    Change 'template_name' to whatever the user wants to name the algorithm.
    Import the file into the 'engine.py' file as the 'randOnRank.py' file was imported and utilized.

"""

def template_name(team_a: dict, team_b: dict, heuristic, round_num: int) -> str:
    """template_name

    Generic template for algorithms. Below details how to use various aspects of the input field
    variables.

    Args:
        team_a (dict): sub content of the large json object revolving around one of the 2 teams
        team_b (dict): sub content of the large json object revolving around the other of the 2
                       teams
        heuristic (dict): data to feed the chosen algorithm below
        round_num (int, optional): for algorithms that require round number for information

    Returns:
        str: team name of the winner
    """

    # 'team_a_seed' and 'team_b_seed' are an integer of the team's seed.
    team_a_name = list(team_a.keys())[0]
    team_b_name = list(team_b.keys())[0]
    team_a_seed = int(team_a[team_a_name]["Seed"])
    team_b_seed = int(team_b[team_b_name]["Seed"])

    # 'team_a' and 'team_b' return all fields stored in 'Attributes'. Any user-supplied data from
    # attribute fields will be returned for each team and stored as these two variables.

    # 'heuristic' field returns any user-supplied heuristics. Such heuristics can include data
    # metrics that can help an algorithm make a pick decision.

    ### DEFAULT FOR COMPILATION ###
    print(f"round: {round_num}")
    print(f"heuristic: {heuristic}")
    if team_a_seed <= team_b_seed:
        winner = team_a_name
    else:
        winner = team_b_name

    return winner
