from graph import Graph
import numpy as np
import math
import copy


class ACO:
    def __init__(self, iterations=1000, n_ants=25, graph=Graph(),
                 cars_limit =6, capacity_limit=6000, distance_limit=1000,  seed=None,
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
        if seed != 0:
            np.random.seed(seed)                    # set seed

    def find_solution(self):
        solution = list()
        vertices = copy.deepcopy(self.graph.vertices)
        cars_used = 0
        rate = 0
        while(len(vertices) != 0 and cars_used < self.cars_limit):
            path = list()
            vertex = np.random.choice(vertices)
            capacity = self.capacity_limit - self.graph.demand[vertex]
            distance =  self.graph.edges(1, vertex)
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
                capacity = capacity - self.graph.demand[vertex]

                a = path[len(path)-1]

                if((capacity > 0) and 
                    (distance + self.graph.edges(min(a, vertex), max(a, vertex)) + self.graph.edges(1, vertex) <= self.distance_limit)):
                    path.append(vertex)
                    vertices.remove(vertex)
                    distance += self.graph.edges(min(a, vertex), max(a, vertex))
                else:
                    break

            solution.append(path)
            cars_used += 1
            distance += self.graph.edges(1, path[len(path)-1])
            rate += distance
        if (cars_used  > self.cars_limit or len(vertices)>0): 
            return solution, -1
        return solution, rate

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

    def run(self):
        for i in range(self.iterations):
            solutions = []
            for _ in range(self.n_ants):
                solution = self.find_solution()
                if solution[1] > 0:
                    solutions.append(solution)
                    self.check_solution(solution)
            self.update_pheromone(solutions)
            print(str(i+1)+":\t"+str(int(self.best_solution[1])) +
                  "\t"+str(self.graph.optimal_value))
        print("best_solution", self.best_solution[0])
        return self.best_solution





class ACO_MinMax(ACO):

    def __init__(self, t_max = 5, **args):
        super().__init__(**args)
        self.k_ = ((self.n_ants -2) * (0.05 ** (1/float(self.n_ants)))) / 2*(1- (0.05 ** (1/float(self.n_ants))))
        self.t_max = t_max                                # tau max parameter
        # self.t_min = t_max/self.k_                        # tau min parameter
        self.t_min = 0.055

    def update_pheromone(self, solutions):
        coeffs = {e: 0 for (e, v) in self.graph.pheromones().items()}
        solution = self.best_solution
        for path in (solution[0]):
            for i in range(len(path)-1):
                e = (min(path[i], path[i+1]),
                        max(path[i], path[i+1]))
                coeffs[e] += (self.th/solution[1])
        
        self.graph.set_pheromones(
            {e: min(max(((1-self.ro) * v) + coeffs[e], self.t_min), self.t_max)
                for (e, v) in self.graph.pheromones().items()})




if __name__ == "__main__":
    t_max = 5
    g = Graph()
    g.generateGraph("E-n22-k4.txt", pheromones_start = t_max)
    aco = ACO_MinMax(t_max = 5, graph=g, cars_limit=5, capacity_limit=g.capacity_limit, distance_limit=1000, iterations=1000)
    # aco = ACO(graph=g, cars_limit=5, capacity_limit=g.capacity_limit, distance_limit=1000, iterations=1000)
    solution = aco.run()

# minMax:
# 1000:   376     375
# best_solution [[9, 7, 2, 3, 6, 8, 10], [14, 12, 5, 4, 11], [13, 16, 19, 21, 18], [17, 20, 22, 15]] dopiero w 974 iteracji

# zwykłe:
# 1000:   378     375
# best_solution [[9, 7, 2, 3, 6, 8, 10], [18, 21, 19, 16, 13], [22, 20, 17, 15], [11, 4, 5, 12, 14]]