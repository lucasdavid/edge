def cost(g):
    """Return the cost of a given path or circuit represented by a nx.Graph object.

    :param g: the graph object which represents the path or circuit.
    :return: the float cost of transversing the path.
    """
    return sum((d['weight'] for _, _, d in g.edges(data=True)))
