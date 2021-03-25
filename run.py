from algorithms.aco_MinMax import ACO_MinMax
from algorithms.aco_Elite import ACO_Elite
from data.tests import Tests
from data.graph import Graph
from algorithms.aco import ACO


g1 = Graph()
g1.generateGraph("E-n22-k4.txt")
aco = ACO(graph=g1, cars_limit=5, capacity_limit=g1.capacity_limit,
          distance_limit=1000, iterations=100)
T_aco = Tests(instance=aco, n_repetition=10, name="aco_1", seed=12020323,
              graph=g1)
T_aco.start()
# aco.start()


g2 = Graph()
g2.generateGraph("E-n22-k4.txt", pheromones_start=5)
aco_minmax = ACO_MinMax(t_max=5, graph=g2, cars_limit=5,
                        capacity_limit=g2.capacity_limit, distance_limit=1000,
                        iterations=1000)
T_aco_minmax = Tests(instance=aco_minmax, n_repetition=10,
                     name="aco_minmax_1", seed=12020323,
                     graph=g2)
# T_aco_minmax.start()
# aco_minmax.start()


g3 = Graph()
g3.generateGraph("E-n22-k4.txt")
aco_elite = ACO_Elite(n_elite=5, graph=g3, cars_limit=6,
                      capacity_limit=g3.capacity_limit, distance_limit=1000,
                      iterations=1000)
T_aco_elite = Tests(instance=aco_elite, n_repetition=10,
                    name="aco_elite_1", seed=12020323,
                    graph=g3)
# T_aco_elite.start()
# aco_elite.start()
