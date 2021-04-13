from data.graph import Graph
import numpy as np
import copy


class ACO:
    def __init__(self, iterations=1000, n_ants=25, graph=Graph(),
                 cars_limit=15, capacity_limit=6000, distance_limit=1000, seed=None,
                 alfa=2, beta=5, ro=0.2, th=80):  # seed=12023050
        self.iterations = iterations                # amount of iterations
        self.n_ants = n_ants                        # number of ants
        self.graph = copy.deepcopy(graph)           # graph information
        self.cars_limit = cars_limit                # cars limit
        self.capacity_limit = capacity_limit        # capacity limit
        self.distance_limit = distance_limit        # distance limit
        self.best_solution = None                   # best solutionalfa
        self.alfa = alfa                            # alfa parameter
        self.beta = beta                            # beta parameter
        self.ro = ro                                # ro parameter
        self.th = th                                # th parameter
        if seed is not None:
            np.random.seed(seed)                    # set seed

    def reset(self, base_graph):
        self.graph = copy.deepcopy(base_graph)      # graph information
        self.best_solution = None                   # best solutionalfa

    def hypothesis_road_lenght(self, solution):
        s_all = 0
        l_roads = list()
        for i in solution:
            s = 0
            a = 1
            for j in i:
                b = j
                s = s + self.graph.edges(min(a, b), max(a, b))
                a = b
            b = 1
            s = s + self.graph.edges(min(a, b), max(a, b))
            l_roads.append(s)
            s_all = s_all + s
        result = 0
        avg = float(s_all) / len(l_roads)
        for l_road in l_roads:
            result = abs(l_road - avg)
        return result

    def find_solution(self):
        solution = list()
        vertices = copy.deepcopy(self.graph.vertices)
        cars_used = 0
        rate = 0
        back_capacity = 0
        while(len(vertices) != 0 and cars_used < self.cars_limit):
            path = list()
            vertex = np.random.choice(vertices)
            capacity = self.capacity_limit - self.graph.demand[vertex]
            distance = self.graph.edges(1, vertex)
            path.append(vertex)
            vertices.remove(vertex)
            while(len(vertices) != 0):
                probabilities = [(self.graph.pheromones(v, vertex)**self.alfa) *
                                 ((1/self.graph.edges(v, vertex))**self.beta)
                                 for v in vertices]
                sum = np.sum(probabilities)
                if sum == 0:
                    vertex = np.random.choice(vertices)
                else:
                    probabilities = probabilities/np.sum(probabilities)
                    vertex = np.random.choice(vertices, p=probabilities)
                c = capacity - self.graph.demand[vertex]

                a = path[len(path)-1]

                if((c > 0) and
                        (distance + self.graph.edges(min(a, vertex), max(a, vertex)) + self.graph.edges(1, vertex) <= self.distance_limit)):
                    path.append(vertex)
                    vertices.remove(vertex)
                    distance += self.graph.edges(min(a, vertex),
                                                 max(a, vertex))
                    capacity = capacity - self.graph.demand[vertex]
                else:
                    break

            back_capacity += capacity
            solution.append(path)
            cars_used += 1
            distance += self.graph.edges(1, path[len(path)-1])
            rate += distance
        if (cars_used > self.cars_limit or len(vertices) > 0):
            return solution, -1, -1
        return solution, rate, back_capacity

    def rate_solution(self, solution):
        s = 0
        for i in solution:
            a = 1
            for j in i:
                b = j
                s = s + self.graph.edges(min(a, b), max(a, b))
                a = b
            b = 1
            s = s + self.graph.edges(min(a, b), max(a, b))
        return s

    def check_solution(self, solution):
        if self.best_solution is None or self.best_solution[1] > solution[1]:
            self.best_solution = solution

    def update_pheromone(self, solutions):
        coeffs = {e: 0 for (e, v) in self.graph.pheromones().items()}
        for solution in solutions:
            for path in (solution[0]):
                for i in range(len(path)-1):
                    e = (min(path[i], path[i+1]),
                         max(path[i], path[i+1]))
                    coeffs[e] += (self.th/solution[1])

        self.graph.set_pheromones(
            {e: ((1-self.ro)*v) + coeffs[e]
                for (e, v) in self.graph.pheromones().items()})

    def add_to_result(self, result: list, iteration, r):
        if len(result) == 0:
            result.append((iteration, r))
        else:
            _, last = result[-1]
            if last[1] != r[1] or last[2] != r[2] or last[3] != r[3]:
                result.append((iteration, r))

    def run(self):
        result = list()
        for i in range(self.iterations):
            solutions = []
            for _ in range(self.n_ants):
                s, rate, back_capacity = self.find_solution()
                solution = (
                    s, rate, self.hypothesis_road_lenght(s), back_capacity)
                if solution[1] > 0:
                    solutions.append(solution)
                    self.check_solution(solution)
            self.update_pheromone(solutions)
            print(str(i+1)+":\t"+str(int(self.best_solution[1])) +
                  "\t"+str(self.graph.optimal_value) +
                  "\t"+str(self.best_solution[2]) +
                  "\t"+str(self.best_solution[3]))
            self.add_to_result(result=result, iteration=i +
                               1, r=self.best_solution)
            # result.append((i+1, self.best_solution))
        print("best solution "+str(self.best_solution))
        result.append(self.best_solution)
        result.append(self.graph.optimal_value)
        return result

    def start(self):
        self.run()


NANTS = 25
ADDITIONALCARS = 2
DISTANCELIMIT = 1000
ITERATIONS = 10  # 10000
NREPETITIONS = 2  # 30
NELITE = 3  # 3
SEED = 12020322  # 12020323
TMAX = 5  # 5

if __name__ == "__main__":
    # g = Graph()
    # g.generateGraph("M-n101-k10.vrp")
    # aco = ACO(graph=g, cars_limit=g.car_min+2, capacity_limit=g.capacity_limit,
    #           distance_limit=1000, iterations=10)
    # aco.start()

    # ACO
    g = Graph()
    g.generateGraph("M-n101-k10.vrp")
    aco = ACO(distance_limit=DISTANCELIMIT,
              iterations=ITERATIONS, n_ants=NANTS)
    aco_name = "aco"
    aco.capacity_limit = g.capacity_limit
    aco.cars_limit = g.car_min + ADDITIONALCARS
    aco.reset(g)
    aco.start()
