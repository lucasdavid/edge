from unittest import TestCase

from edge.generator import GraphGenerator


class GraphGeneratorTest(TestCase):
    def test_graph(self):
        expected = 4

        g = GraphGenerator(n=expected).graph()
        self.assertEqual(g.number_of_nodes(), expected)

    def test_euclidean_graph(self):
        expected = 4

        g = GraphGenerator(n=expected).euclidean_graph()
        self.assertEqual(g.number_of_nodes(), expected)
