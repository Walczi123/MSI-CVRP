import os
from algorithms.aco_MinMax import ACO_MinMax
from algorithms.aco_Elite import ACO_Elite
from data.test import Test
from data.graph import Graph
from algorithms.aco import ACO
import multiprocessing
from glob import glob
import time

NANTS = 25
ADDITIONALCARS = 2
DISTANCELIMIT = 1000
ITERATIONS = 8000  # 10000
NREPETITIONS = 3  # 30
NELITE = 3  # 3
SEED = 12020330  # 12020323
TMAX = 5  # 5


def generate_instances():
    result = []
    for file in glob("./data/Benchmarks/*.vrp"):
        g = Graph()
        g.generateGraph(file)
        g2 = Graph()
        g2.generateGraph(file, pheromones_start=TMAX)

        for i in range(SEED, SEED+NREPETITIONS):
            # ACO
            aco = ACO(distance_limit=DISTANCELIMIT,
                      iterations=ITERATIONS, n_ants=NANTS)
            aco_name = "aco"
            T_aco = Test(instance=aco,
                         name=aco_name, seed=i)
            aco.capacity_limit = g.capacity_limit
            aco.cars_limit = g.car_min + ADDITIONALCARS
            T_aco.name = os.path.splitext(os.path.basename(file))[
                0] + "_" + aco_name
            T_aco.base_graph = g
            result.append(T_aco)

            # ACO_GREEDY
            aco_greedy = ACO(distance_limit=DISTANCELIMIT,
                             iterations=ITERATIONS, alfa=0, n_ants=NANTS)
            aco_greedy_name = "aco_greedy"
            T_aco_greedy = Test(instance=aco_greedy,
                                name=aco_greedy_name, seed=i)
            aco_greedy.capacity_limit = g.capacity_limit
            aco_greedy.cars_limit = g.car_min + ADDITIONALCARS
            T_aco_greedy.name = os.path.splitext(os.path.basename(file))[
                0] + "_" + aco_greedy_name
            T_aco_greedy.base_graph = g
            result.append(T_aco_greedy)

            # ACO_ELITE
            aco_elite = ACO_Elite(
                n_elite=NELITE, distance_limit=DISTANCELIMIT, iterations=ITERATIONS, n_ants=NANTS)
            aco_elite_name = "aco_elite"
            T_aco_elite = Test(instance=aco_elite,
                               name=aco_elite_name, seed=i)
            aco_elite.capacity_limit = g.capacity_limit
            aco_elite.cars_limit = g.car_min + ADDITIONALCARS
            T_aco_elite.base_graph = g
            T_aco_elite.name = os.path.splitext(os.path.basename(file))[
                0] + "_" + aco_elite_name
            result.append(T_aco_elite)

            # ACO_MINMAX
            aco_minmax = ACO_MinMax(
                t_max=TMAX, distance_limit=DISTANCELIMIT, iterations=ITERATIONS, n_ants=NANTS)
            aco_minmax_name = "aco_minmax"
            T_aco_minmax = Test(instance=aco_minmax,
                                name=aco_minmax_name, seed=i)

            aco_minmax.capacity_limit = g.capacity_limit
            aco_minmax.cars_limit = g.car_min + ADDITIONALCARS
            T_aco_minmax.base_graph = g
            T_aco_minmax.name = os.path.splitext(os.path.basename(file))[
                0] + "_" + aco_minmax_name
            result.append(T_aco_minmax)
    return result


def run_test(test):
    test.start()


def run_tests():
    iterable = generate_instances()
    start_time = time.time()

    p = multiprocessing.Pool()
    p.map_async(run_test, iterable)

    p.close()
    p.join()
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    run_tests()
