from unittest import TestCase

from edge import algorithms, GraphGenerator


class EdgeScoreTest(TestCase):
    def test_simple_graph(self):
        g = GraphGenerator(n=4).graph()
        algorithms.EdgeScore(g).solve()

    def test_random_graph(self):
        g = GraphGenerator(n=10, m=30).graph()
        algorithms.EdgeScore(g).solve()


class TwiceAroundTest(TestCase):
    def test_simple_graph(self):
        g = GraphGenerator(n=4).graph()
        algorithms.TwiceAround(g).solve()


class NearestNeighborTest(TestCase):
    def test_simple_graph(self):
        g = GraphGenerator(n=4).graph()
        algorithms.NearestNeighbor(g).solve()
