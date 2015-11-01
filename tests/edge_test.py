from unittest import TestCase

from edge import EdgeScoreAlgorithm, GraphGenerator


class EdgeScoreAlgorithmTest(TestCase):
    def test_simple_graph(self):
        g = GraphGenerator(n=4).weighted_graph()
        solution = EdgeScoreAlgorithm(g).solve()

        self.assertIsNone(solution)

    def test_random_graph(self):
        g = GraphGenerator(n=10, m=30).weighted_graph()
        solution = EdgeScoreAlgorithm(g).solve()

        self.assertIsNotNone(solution)
