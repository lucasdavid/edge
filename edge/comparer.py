import multiprocessing
import threading
import time

from edge import base, generator, algorithms


class ComparerManager:
    edge_weight_range = (10, 100)
    number_of_concurrent_graphs = multiprocessing.cpu_count()
    algorithms = {
        algorithms.NearestNeighbor,
        algorithms.EdgeScore,
        algorithms.TwiceAround,
    }

    def __init__(self, iterations=10, maximum_number_of_nodes=100, number_of_workers=None, euclidean=True):
        self.maximum_number_of_nodes = maximum_number_of_nodes
        self.use_euclidean_graphs = True
        self.iterations = iterations
        self.workers = None
        self.number_of_workers = number_of_workers or multiprocessing.cpu_count()
        self.running = False
        self.cv = threading.Condition()

        self.graphs = []
        self.graphs_generated = 0
        self.graph_generator = generator.GraphGenerator(edge_weight_range=self.edge_weight_range)

        self.reports = []

    def run(self):
        print('Edge Score comparer has started.\n')

        self.running = True
        self.start_workers()

        try:
            while len(self.reports) < self.iterations:
                with self.cv:
                    if self.graphs_generated < self.iterations and len(self.graphs) < self.number_of_concurrent_graphs:
                        self.generate_random_graphs(min(
                            self.iterations - self.graphs_generated,
                            self.number_of_concurrent_graphs - len(self.graphs)))
                        self.cv.notify()

                time.sleep(.1)

        except KeyboardInterrupt:
            pass

        self.dispose()

        return self

    def start_workers(self):
        if not self.workers:
            self.workers = [ComparerWorker(worker_id=i, manager=self) for i in range(self.number_of_workers)]

        for w in self.workers:
            w.start()

    def stop_workers(self):
        print('Stopping workers...', end=' ')
        self.running = False

        with self.cv:
            self.cv.notify_all()

        for w in self.workers:
            w.join()

        print('Done.')

    def dispose(self):
        self.stop_workers()

    def generate_random_graphs(self, count):
        with self.cv:
            for _ in range(count):
                self.graph_generator.n = max(
                    4,
                    int(self.graphs_generated / self.iterations * self.maximum_number_of_nodes))

                g = self.graph_generator.euclidean_graph() \
                    if self.use_euclidean_graphs \
                    else self.graph_generator.graph()

                self.graphs.append((self.graphs_generated, g))
                self.graphs_generated += 1

            self.cv.notify_all()


class ComparerWorker(threading.Thread):
    def __init__(self, worker_id, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.worker_id = worker_id
        self.manager = manager

    def run(self):
        while True:
            with self.manager.cv:
                self.manager.cv.wait_for(lambda: self.manager.graphs or not self.manager.running)

                if not self.manager.running:
                    return

                i, graph = self.manager.graphs.pop()

            print('Worker #%i is processing graph #%i.' % (self.worker_id, i))

            report = {
                'worker-id': self.worker_id,
                'nodes-in-graph': graph.number_of_nodes(),
                'algorithms': {},
            }

            for algorithm in self.manager.algorithms:
                circuit = algorithm(graph).solve()
                cost = base.cost(circuit)

                report['algorithms'][algorithm.__name__] = cost

            self.manager.reports.append(report)
