from datetime import datetime
import json

import numpy as np
import matplotlib.pyplot as plt

from edge.comparer import ComparerManager

comparison_params_list = [
    {'iterations': 10, 'maximum_number_of_nodes': 200, 'euclidean': True},
    {'iterations': 10, 'maximum_number_of_nodes': 200, 'euclidean': False},
]


def compare_multiple_iterations():
    for i, params in enumerate(comparison_params_list):
        print('Comparison #%i: %s' % (i, params))

        comparer = ComparerManager(**params).run()

        print('Generating report...', end=' ')
        report_name = '../reports/%s.txt' % str(datetime.now()).replace(':', '-')

        with open(report_name, 'w') as f:
            json.dump(comparer.reports, f, indent=4)

        print('Done.\n')
        print('Interpreting report %s.' % report_name)

        nodes = np.array([e['nodes-in-graph'] for e in comparer.reports])
        costs = np.array([list(e['algorithms'].values()) for e in comparer.reports])

        increasing_node_order = np.argsort(nodes)
        nodes = nodes[increasing_node_order]
        costs = costs[increasing_node_order]

        print('Algorithms: %s' % ', '.join(comparer.reports[0]['algorithms'].keys()))
        print('Mean: %s, std: %s' % (costs.mean(axis=0), costs.std(axis=0)))

        for k in range(costs.shape[1]):
            plt.plot(nodes, costs[:, k].flatten())

        plt.legend(list(comparer.reports[0]['algorithms'].keys()))
        plt.show()

    print('Bye.')


if __name__ == '__main__':
    compare_multiple_iterations()
