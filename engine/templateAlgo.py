"""
#############################################################################
#
#   templateAlgo.py
#
#   Generic template for users to create their own picking algorithms. Use this
#   to build custom picking algorithm. Use 'randOnRank.py' as a further example
#   as to how to properly construct a picking algorithm.
#
#   Change 'TemplateName' to whatever the user wants to name the algorithm. 
#   Import the file into the 'engine.py' file as the 'randOnRank.py' file was
#   imported and utilized.
#
#   Version:    0.0.2, 01-27-19
#
#   Nick Amell
#
#   Version History:
#   -------------------------------------------------------------------------
#   0.0.1, 01-20-19:    Initial framework for template. 
#   0.0.2, 01-27-19:    Added roundNum field (added optional functionality)
#############################################################################
"""

def TemplateName(teamA: str, teamB: str, tAFull, tBFull, heuristic, roundNum: int) -> str:
    """ Generic template for algorithms. Below details how to use various aspects of the
        input field variables. """

    """ 'tASeed' and 'tBSeed' are an integer of the team's seed. """
    tASeed = int(tAFull["Seed"])
    tBSeed = int(tBFull["Seed"])

    """ 'tAFull' and 'tBFull' return all fields stored in 'Attributes'. Any user-supplied
        data from attribute fields will be returned for each team and stored as these
        two variables. """
    
    """ 'heuristic' field returns any user-supplied heuristics. Such heuristics can
        include data metrics that can help an algorithm make a pick decision. """

    ### DEFAULT FOR COMPILATION ###
    if (tASeed <= tBSeed):
        winner = teamA
    else:
        winner = teamB    

    return winner