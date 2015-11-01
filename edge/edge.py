import networkx as nx


class EdgeScoreAlgorithm:
    def __init__(self, g):
        self.g = g
        self.edges_scores = {}

    def score(self, origin, target):
        if origin not in self.edges_scores:
            self.edges_scores[origin] = {}
        if target not in self.edges_scores[origin]:
            self.edges_scores[origin][target] = 0

        self.edges_scores[origin][target] += 1

    def solve(self):
        paths = nx.all_pairs_dijkstra_path(self.g)

        for node, node_paths in paths.items():
            for neighbor, path in node_paths.items():
                if node == neighbor:
                    continue

                previous = path[0]

                for i in range(1, len(path)):
                    current = path[i]

                    self.score(previous, current)
                    previous = current

        return self.edges_scores
