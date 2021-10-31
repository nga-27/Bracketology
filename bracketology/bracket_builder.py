"""bracket_builder.py

    File to fill flatbrackets (i.e. lists) and generate a DAG bracket representation from the picked
    and flattened (lists) bracket.
"""

from graphviz import Digraph

def flat_bracket_creator(full_bracket: list) -> list:
    """flat_bracket_creator

    Function extends regions + final four to make listed locations for nodes

    Args:
        full_bracket (list): the building of a flat bracket

    Returns:
        list: full_bracket [updated]
    """
    for i in range(4):
        region = full_bracket[i]
        for _ in range(len(region)-1):
            region.append('b')

    # This will constitute the final four bracket.
    for _ in range(3):
        full_bracket[4].append('a')
    return full_bracket


def build_dag(bracket_list: list):
    """build_dag

    Final function that ultimately builds the directed, acyclic graph to represent the bracket.
    Assuming only 4 regions + 7 nodes for final four.  Final four assumes 0 vs. 1, 2 vs. 3 (array
    indices). Final step - takes a completed bracket and assembles it for graphing purposes.

    Args:
        bracket_list (list): bracket list object that has been added to from other functions
    """
    bracket = Digraph(format='png')
    bracket.attr('node', shape='rectangle', fixedsize='false', width='0.2')

    for i in range(4):
        # Building the 4 regions as specified by bracketList
        temp_region = bracket_list[i]

        for j in range(16):
            # All teams entered to start - no edges.  Random numbering convention
            node_key = "B" + str(i + 1) + str(10 + j)
            bracket.node(node_key, temp_region[j])
            #print(nodeKey)

        reduce_count = 16
        for j in range(16, len(temp_region)):
            # Advanced games per region - requires edges
            node_key = "B" + str(i + 1) + str(10 + j)
            bracket.node(node_key, temp_region[j])
            node_key2 = "B" + str(i + 1) + str(10 + j - reduce_count)
            node_key3 = "B" + str(i + 1) + str(10 + j - reduce_count + 1)
            bracket.edge(node_key2, node_key)
            bracket.edge(node_key3, node_key)
            reduce_count -= 1

    # Final four bracket
    for i in range(2):
        node_key = "B" + str(5) + str(10 + i)
        bracket.node(node_key, bracket_list[4][i])
        node_key2 = "B" + str(2 * i + 1) + str(10 + 30)
        node_key3 = "B" + str(2 * i + 2) + str(10 + 30)
        bracket.edge(node_key2, node_key)
        bracket.edge(node_key3, node_key)

    node_key = "B" + str(5) + str(12)
    bracket.node(node_key, bracket_list[4][2])
    node_key2 = "B" + str(5) + str(10)
    node_key3 = "B" + str(5) + str(11)
    bracket.edge(node_key2, node_key)
    bracket.edge(node_key3, node_key)

    bracket.render('outputs/NCAABracket', view=True)

    print('Bracket rendered. Function complete!')
