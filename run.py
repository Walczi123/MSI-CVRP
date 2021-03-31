import os
from algorithms.aco_MinMax import ACO_MinMax
from algorithms.aco_Elite import ACO_Elite
from data.tests import Tests
from data.graph import Graph
from algorithms.aco import ACO
import glob
import time

NANTS = 25
ADDITIONALCARS = 2
DISTANCELIMIT = 1000
ITERATIONS = 10000  # 10000
NREPETITIONS = 30  # 30
NELITE = 3  # 3
SEED = 12020323  # 12020323
TMAX = 5  # 5


# ACO
aco = ACO(distance_limit=DISTANCELIMIT,
          iterations=ITERATIONS, n_ants=NANTS)
aco_name = "aco"
T_aco = Tests(instance=aco, n_repetition=NREPETITIONS,
              name=aco_name, seed=SEED)

# ACO_MINMAX
aco_minmax = ACO_MinMax(
    t_max=TMAX, distance_limit=DISTANCELIMIT, iterations=ITERATIONS, n_ants=NANTS)
aco_minmax_name = "aco_minmax"
T_aco_minmax = Tests(instance=aco_minmax, n_repetition=NREPETITIONS,
                     name=aco_minmax_name, seed=SEED)

# ACO_ELITE
aco_elite = ACO_Elite(
    n_elite=NELITE, distance_limit=DISTANCELIMIT, iterations=ITERATIONS, n_ants=NANTS)
aco_elite_name = "aco_elite"
T_aco_elite = Tests(instance=aco_elite, n_repetition=NREPETITIONS,
                    name=aco_elite_name, seed=SEED)

# ACO_GREEDY
aco_greedy = ACO(distance_limit=DISTANCELIMIT,
                 iterations=ITERATIONS, alfa=0, n_ants=NANTS)
aco_greedy_name = "aco_greedy"
T_aco_greedy = Tests(instance=aco_greedy, n_repetition=NREPETITIONS,
                     name=aco_greedy_name, seed=SEED)

start_time = time.time()
for file in glob.glob("./data/Benchmarks/*.vrp"):
    g = Graph()
    g.generateGraph(file)

    # ACO
    aco.capacity_limit = g.capacity_limit
    aco.cars_limit = g.car_min + ADDITIONALCARS
    T_aco.name = os.path.splitext(os.path.basename(file))[0] + "_" + aco_name
    T_aco.base_graph = g
    print(T_aco.name)
    T_aco.start()

    # ACO_GREEDY
    aco_greedy.capacity_limit = g.capacity_limit
    T_aco_greedy.name = os.path.splitext(os.path.basename(file))[
        0] + "_" + aco_greedy_name
    T_aco_greedy.base_graph = g
    print(T_aco_greedy.name)
    T_aco.start()

    # ACO_ELITE
    aco_elite.capacity_limit = g.capacity_limit
    T_aco_elite.base_graph = g
    T_aco_elite.name = os.path.splitext(os.path.basename(file))[
        0] + "_" + aco_elite_name
    print(T_aco_elite.name)
    T_aco_elite.start()

    # ACO_MINMAX
    g2 = Graph()
    g2.generateGraph(file, pheromones_start=TMAX)
    aco_minmax.capacity_limit = g.capacity_limit
    T_aco_minmax.base_graph = g
    T_aco_minmax.name = os.path.splitext(os.path.basename(file))[
        0] + "_" + aco_minmax_name
    print(T_aco_minmax.name)
    T_aco_minmax.start()

print("--- %s seconds ---" % (time.time() - start_time))
