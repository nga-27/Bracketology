"""
#############################################################################
#
#   randOnRank
#
#   Default winner picking algorithm supplied: uses simple ratios of ranks + 
#   a random choice from python's random library
#
#
#   Version:    0.1.0, 01-12-19
#
#   Nick Amell
#
#   Version History:
#   -------------------------------------------------------------------------
#   0.1.0, 01-12-19:    Successful first implementation of random on rank
#############################################################################
"""
""" Default picking algorithm: 'randOnRank """
import random

def RandomOnRank(teamA: str, teamB: str, tAFull, tBFull, heuristic) -> str:
    """ Using a random number and fixed random template (heuristic), determine winner
        by mapping rank/seed to a random number spectrum. """

    tASeed = int(tAFull["Seed"])
    tBSeed = int(tBFull["Seed"])

    numLineA = heuristic["randOnRank"]["array"][tASeed-1][tBSeed-1]

    value = random.random()
    if (value <= numLineA):
        winner = teamA
    else:
        winner = teamB

    return winner