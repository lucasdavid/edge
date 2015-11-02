from random import Random

import networkx as nx


class GraphGenerator:
    n, m = 10, 90
    min_edge_cost, max_edge_cost = 0, 100

    def __init__(self, **params):
        self.n = params.get('n', self.n)
        self.edge_weight_range = params.get('edge_weight_range', (10, 100))

    def weighted_graph(self):
        g = nx.complete_graph(self.n)
        r = Random()

        for origin, target in g.edges():
            g[origin][target]['weight'] = r.randint(*self.edge_weight_range)

        return g
