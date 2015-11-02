import abc
import numpy as np

import networkx as nx


class Algorithm(metaclass=abc.ABCMeta):
    def __init__(self, g):
        self.g = g
        self.hcc = None
        self.start = self.g.nodes()[0]

    def solve(self):
        raise NotImplementedError


class EdgeScore(Algorithm):
    def __init__(self, g):
        super().__init__(g)
        self.edge_scores = {}

    def solve(self):
        paths = nx.all_pairs_dijkstra_path(self.g)

        # Sum edge scores.
        for node, node_paths in paths.items():
            for neighbor, path in node_paths.items():
                path = iter(path)
                previous = next(path)

                for current in path:
                    self.score(previous, current)
                    previous = current

        self.hcc = nx.Graph()
        self.hcc.add_node(self.start)
        current = self.start

        available_nodes = set(self.g.nodes()) - {self.start}

        # Build hamiltonian circuit candidate.
        while self.hcc.number_of_nodes() < self.g.number_of_nodes():
            available_neighbors = available_nodes & self.edge_scores[current].keys()

            if available_neighbors:
                # Select edge with greatest betweenness (which appeared most in shortest-paths).
                next_in_path = max(available_neighbors, key=lambda p: self.edge_scores[current][p])
            else:
                # If none of the edges with :current as initial end-point were
                # present in any shortest-path, we pick the nearest-neighbor.
                available_neighbors = self.g[current].keys() & available_nodes
                next_in_path = min(available_neighbors, key=lambda p: self.g[current][p]['weight'])

            if not next_in_path:
                raise ValueError('No next node in path. Is g a k-complete graph?')

            self.hcc.add_edge(current, next_in_path, self.g[current][next_in_path])
            current = next_in_path

            available_nodes.remove(next_in_path)

        del available_nodes

        self.hcc.add_edge(next_in_path, self.start, self.g[next_in_path][self.start])

        return self.hcc

    def score(self, origin, target):
        if origin not in self.edge_scores:
            self.edge_scores[origin] = {}
        if target not in self.edge_scores[origin]:
            self.edge_scores[origin][target] = 0

        self.edge_scores[origin][target] += 1


class TwiceAround(Algorithm):
    def solve(self):
        self.hcc = nx.Graph()

        mst = nx.minimum_spanning_tree(self.g)
        path = np.array(list(nx.dfs_preorder_nodes(mst, self.start)))
        path = np.unique(path)
        path = list(np.append(path, [self.start]))

        path = iter(path)
        current = next(path)

        for next_in_path in path:
            self.hcc.add_edge(current, next_in_path, self.g[current][next_in_path])
            current = next_in_path

        return self.hcc


class NearestNeighbor(Algorithm):
    def solve(self):
        current = self.start

        nodes_available = set(self.g.nodes())
        nodes_available.remove(current)

        self.hcc = nx.Graph()

        while self.hcc.number_of_nodes() < self.g.number_of_nodes():
            neighbors_available = self.g[current].keys() & nodes_available

            nearest = min(neighbors_available, key=lambda n: self.g[current][n]['weight'])

            self.hcc.add_edge(current, nearest, self.g[current][nearest])
            current = nearest

            nodes_available.remove(current)

        self.hcc.add_edge(current, self.start, self.g[current][self.start])

        return self.hcc
