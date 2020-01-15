"""
#############################################################################
#
#   engine.py
#
#   Generic picking class that is fed by configurable algorithms.
#
#
#   Version:    0.1.2, 01-15-20
#
#   nga-27
#
#   Version History:
#   -------------------------------------------------------------------------
#   0.0.1, 01-10-19:    Initial framework - PopulateBracket + MakePick
#   0.1.0, 01-20-19:    Version 1.0 released
#   0.1.1, 01-27-19:    Added round number for historical information
#   0.1.2, 01-15-20:    Pylint auto edits
#############################################################################
"""
import json

### ALGORITHM CHOICE(S) IMPORTS HERE ###
from .randOnRank import RandomOnRank
from .templateAlgo import TemplateName

###################################################################
##      USER-DEFINED IMPORT CONFIGURED HERE (and farther below)  ##
###################################################################
""" Import custom algorithm (if not 'templateAlgo' above) here as examples above """


###################################################################
##      DO NOT EDIT BELOW THIS SECTION!!! (Internal-use only)    ##
###################################################################
def PopulateBracket(flatBracket: list, jsonFile: str) -> list:
    """ Uses MakePick and algorithms below to fill in bracket with picks """

    with open(jsonFile, encoding='utf-8') as dataFile:
        data = json.loads(dataFile.read())

    roundVal = 1

    for i in range(4):
        nextGame = 16
        curGame = 0

        while (nextGame < 31):

            if curGame < 16:
                roundVal = 1
            elif curGame < 24:
                roundVal = 2
            elif curGame < 28:
                roundVal = 3
            else:
                roundVal = 4

            tA = flatBracket[i][curGame]
            tB = flatBracket[i][curGame+1]

            tC = MakePick(tA, tB, teamAFull=data["Bracket"][tA], teamBFull=data["Bracket"]
                          [tB], heuristic=data["Heuristics"], roundNum=roundVal)

            flatBracket[i][nextGame] = tC

            nextGame += 1
            curGame += 2

    """ Finish the final four part of the bracket """
    roundVal = 5
    tA = flatBracket[0][30]
    tB = flatBracket[1][30]
    tC = MakePick(tA, tB, teamAFull=data["Bracket"][tA], teamBFull=data["Bracket"]
                  [tB], heuristic=data["Heuristics"], roundNum=roundVal)
    flatBracket[4][0] = tC

    tA = flatBracket[2][30]
    tB = flatBracket[3][30]
    tC = MakePick(tA, tB, teamAFull=data["Bracket"][tA], teamBFull=data["Bracket"]
                  [tB], heuristic=data["Heuristics"], roundNum=roundVal)
    flatBracket[4][1] = tC

    roundVal = 6
    tA = flatBracket[4][0]
    tB = flatBracket[4][1]
    tC = MakePick(tA, tB, teamAFull=data["Bracket"][tA], teamBFull=data["Bracket"]
                  [tB], heuristic=data["Heuristics"], roundNum=roundVal)
    flatBracket[4][2] = tC

    return flatBracket


def MakePick(teamA: str, teamB: str, teamAFull=None, teamBFull=None, heuristic=None, roundNum: int = 0) -> str:
    """ 
        All inputs to this function are available for any configurable algorithm.
        "TeamXFull" variables refer to entire JSON object of team, including rank and attributes, 
        for customizable algorithm use.
    """

    ###################################################################
    ##      USER-DEFINED ALGO CONFIGURED BELOW                       ##
    ###################################################################
    winner = RandomOnRank(teamA, teamB, teamAFull, teamBFull, heuristic)
    #winner = TemplateName(teamA, teamB, teamAFull, teamBFull, heuristic, roundNum=roundNum)

    return winner
