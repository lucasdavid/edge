from random import Random

import networkx as nx


class GraphGenerator:
    n, m = 10, 90
    min_edge_cost, max_edge_cost = 0, 100

    def __init__(self, **params):
        self.n = params.get('n', self.n)
        self.m = params.get('m', self.m)
        self.min_edge_cost = params.get('min_edge_cost', self.min_edge_cost)
        self.max_edge_cost = params.get('max_edge_cost', self.max_edge_cost)

    def weighted_graph(self):
        g = nx.gnm_random_graph(self.n, self.m)
        r = Random()

        for origin, target in g.edges():
            g[origin][target]['weight'] = r.randint(self.min_edge_cost, self.max_edge_cost)

        return g
