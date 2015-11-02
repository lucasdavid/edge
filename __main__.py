from datetime import datetime
import json

import numpy as np

import networkx as nx
import matplotlib.pyplot as plt

from edge import base, GraphGenerator, algorithms, graphics
from edge.comparer import ComparerManager


def display():
    g = GraphGenerator(n=10, m=50).weighted_graph()

    circuit = algorithms.EdgeScore(g).solve()
    print('Cost: %.2f' % base.cost(circuit))

    pos = nx.spring_layout(g)

    plt.subplot(121)
    plt.title('Original Graph')
    nx.draw(g, pos=pos, **graphics.default_style)
    edge_labels = dict([((u, v,), d['weight']) for u, v, d in g.edges(data=True)])
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)

    plt.subplot(122)
    plt.title('Hamiltonian Circuit Candidate')
    nx.draw(circuit, pos=pos, **graphics.solution_style)
    edge_labels = dict([((u, v,), d['weight']) for u, v, d in circuit.edges(data=True)])
    nx.draw_networkx_edge_labels(circuit, pos, edge_labels=edge_labels)

    plt.show()


def compare():
    comparer = ComparerManager(iterations=100, maximum_number_of_nodes=100).run()

    print('Generating report...', end=' ')

    report_name = 'reports/%s.txt' % str(datetime.now()).replace(':', '-')

    with open(report_name, 'w') as f:
        json.dump(comparer.reports, f, indent=4)

    print('Done.\n')
    return report_name


def interpret(report_name):
    print('Interpreting report %s.' % report_name)

    with open(report_name) as file:
        data = json.load(file)

    nodes = np.array([e['nodes-in-graph'] for e in data])
    costs = np.array([list(e['algorithms'].values()) for e in data])

    increasing_node_order = np.argsort(nodes)
    nodes = nodes[increasing_node_order]
    costs = costs[increasing_node_order]

    print('Mean: %s, std: %s' % (costs.mean(axis=0), costs.std(axis=0)))

    for i in range(costs.shape[1]):
        plt.plot(nodes, costs[:, i].flatten())

    plt.legend(list(data[0]['algorithms'].keys()))
    plt.show()

    print('Bye.')


if __name__ == '__main__':
    report = compare()
    interpret(report)
