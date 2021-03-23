from data.tests import Tests
from data.graph import Graph
from algorithms.aco import ACO


g = Graph()
g.generateGraph("E-n22-k4.txt")
aco = ACO(graph=g, capacity_limit=g.capacity_limit, iterations=10)

T = Tests(instance=aco, n_repetition=3, name="t")
T.start()
