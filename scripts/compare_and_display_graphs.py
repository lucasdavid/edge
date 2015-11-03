import networkx as nx
import matplotlib.pyplot as plt

from edge import algorithms, graphics, base, generator


def compare_algorithms_one_iteration():
    g = generator.GraphGenerator(n=5).euclidean_graph()

    pos = nx.spring_layout(g)

    plt.subplot(221)
    plt.title('Original Graph')
    nx.draw(g, pos=pos, **graphics.default_style)
    edge_labels = dict([((u, v,), '%.1f' % d['weight']) for u, v, d in g.edges(data=True)])
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)

    for i, algorithm in enumerate((algorithms.NearestNeighbor, algorithms.TwiceAround, algorithms.EdgeScore)):
        solution = algorithm(g).solve()
        plt.subplot(222 + i)
        plt.title('%s, c: %.2f' % (algorithm.__name__, base.cost(solution)))
        nx.draw(solution, pos=pos, **graphics.solution_style)
        edge_labels = dict([((u, v,), '%.1f' % d['weight']) for u, v, d in solution.edges(data=True)])
        nx.draw_networkx_edge_labels(solution, pos, edge_labels=edge_labels)

    plt.show()

if __name__ == '__main__':
    compare_algorithms_one_iteration()
