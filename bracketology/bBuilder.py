"""
#############################################################################
#
#   bBuilder.py
#
#   File to fill flatbrackets (i.e. lists) and generate a DAG bracket representation
#   from the picked and flattened (lists) bracket.
#
#
#   Version:    0.1.0, 01-15-20
#
#   nga-27
#
#   Version History:
#   -------------------------------------------------------------------------
#   0.0.1, 01-12-18:    Flat bracket creator + DAG builder successful
#   0.1.0, 01-20-19:    Version 1.0 released
#   0.1.1, 01-15-20:    Pylint edits
#############################################################################
"""

from graphviz import Digraph


def FlatBracketCreator(fullBracket: list):
    """ Function extends regions + final four to make listed locations for nodes """

    for i in range(4):
        region = fullBracket[i]

        for _ in range(len(region)-1):
            region.append('b')

    # This will constitute the final four bracket.
    for _ in range(3):
        fullBracket[4].append('a')

    # print(fullBracket)
    return fullBracket


def BuildDAG(bracketList: list):
    """ Assuming only 4 regions + 7 nodes for final four.  Final four assumes 0 vs. 1, 2 vs. 3 (array indices) """
    """ Final step - takes a completed bracket and assembles it for graphing purposes """

    bracket = Digraph(format='png')
    bracket.attr('node', shape='rectangle', fixedsize='false', width='0.2')

    for i in range(4):
        """ Building the 4 regions as specified by bracketList """
        tRegion = bracketList[i]

        for j in range(16):
            """ all teams entered to start - no edges.  Random numbering convention """
            nodeKey = "B" + str(i+1) + str(10+j)
            bracket.node(nodeKey, tRegion[j])
            # print(nodeKey)

        reduceCount = 16
        for j in range(16, len(tRegion)):
            """ advanced games per region - requires edges """
            nodeKey = "B" + str(i+1) + str(10+j)
            bracket.node(nodeKey, tRegion[j])
            nodeKey2 = "B" + str(i+1) + str(10+j-reduceCount)
            nodeKey3 = "B" + str(i+1) + str(10+j-reduceCount+1)
            bracket.edge(nodeKey2, nodeKey)
            bracket.edge(nodeKey3, nodeKey)
            reduceCount -= 1

    """ Final four bracket """
    for i in range(2):
        nodeKey = "B" + str(5) + str(10+i)
        bracket.node(nodeKey, bracketList[4][i])
        nodeKey2 = "B" + str(2*i+1) + str(10+30)
        nodeKey3 = "B" + str(2*i+2) + str(10+30)
        bracket.edge(nodeKey2, nodeKey)
        bracket.edge(nodeKey3, nodeKey)

    nodeKey = "B" + str(5) + str(12)
    bracket.node(nodeKey, bracketList[4][2])
    nodeKey2 = "B" + str(5) + str(10)
    nodeKey3 = "B" + str(5) + str(11)
    bracket.edge(nodeKey2, nodeKey)
    bracket.edge(nodeKey3, nodeKey)

    bracket.render('outputs/NCAABracket', view=True)

    print('Bracket rendered.  makeBracket complete!')
