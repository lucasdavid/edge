from random import Random

import networkx as nx
import numpy as np
from scipy.spatial.distance import pdist


class GraphGenerator:
    n, m = 10, 90
    min_edge_cost, max_edge_cost = 0, 100

    def __init__(self, **params):
        self.n = params.get('n', self.n)
        self.edge_weight_range = params.get('edge_weight_range', (10, 100))
        self.vertices_pos_range = params.get('vertices_pos_range', (10, 100))

    def graph(self):
        g = nx.complete_graph(self.n)
        r = Random()

        for origin, target in g.edges():
            g[origin][target]['weight'] = r.randint(*self.edge_weight_range)

        return g

    def euclidean_graph(self):
        vertices = np.random.randint(*self.vertices_pos_range, size=(self.n, 3))
        vertices = pdist(vertices).tolist()

        g = nx.complete_graph(self.n)
        for i in range(0, self.n):
            for j in range(i+1, self.n):
                g.add_edge(i, j, weight=vertices.pop())

        return g
