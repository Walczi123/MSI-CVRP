from graph import Graph
import numpy as np
import copy


class ACO:
    def __init__(self, iterations=1000, n_ants=25, graph=Graph(),
                 capacity_limit=6000, distance_limit=1000, seed=None,
                 alfa=2, beta=5, ro=0.2, th=80):  # seed=12023050
        self.iterations = iterations                # amount of iterations
        self.n_ants = n_ants                        # number of ants
        self.graph = copy.deepcopy(graph)           # graph information
        self.capacity_limit = capacity_limit        # capacity limit
        self.distance_limit = distance_limit        # distance limit
        self.best_solution = None                   # best solutionalfa
        self.alfa = alfa                            # alfa parameter
        self.beta = beta                            # beta parameter
        self.ro = (1 - ro)                          # ro parameter
        self.th = th                                # th parameter
        if seed != 0:
            np.random.seed(seed)                    # set seed

    def find_solution(self):
        solution = list()
        vertices = copy.deepcopy(self.graph.vertices)
        coeffs = {e: 0 for (e, v) in self.graph.feromones().items()}
        while(len(vertices) != 0):
            path = list()
            vertex = np.random.choice(vertices)
            capacity = self.capacity_limit - self.graph.demand[vertex]
            path.append(vertex)
            vertices.remove(vertex)
            last = vertex
            while(len(vertices) != 0):
                probabilities = [(self.graph.feromones(v, vertex)**self.alfa) *
                                 ((1/self.graph.edges(v, vertex))**self.beta)
                                 for v in vertices]
                sum = np.sum(probabilities)
                if sum == 0:
                    vertex = np.random.choice(vertices)
                else:
                    probabilities = probabilities/np.sum(probabilities)
                    vertex = np.random.choice(vertices, p=probabilities)
                capacity = capacity - self.graph.demand[vertex]
                if(capacity > 0):
                    path.append(vertex)
                    coeffs[min(last, vertex), max(last, vertex)] + self.th
                    vertices.remove(vertex)
                else:
                    break
            solution.append(path)
        return solution, coeffs

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

    def update_feromone(self, solutions):  # do poprawy
        # tmp = 0*
        # for s in solutions:
        #     for p in s[0]:

        # for (e, v) in self.graph.feromones().items():
        #     self.graph.set_feromones(
        #         {self.ro*v + (sume_z_e)})
        # for solution in solutions:
        #     self.graph.set_feromones(
        #         {e: (self.ro + self.th/solution[1]) * v
        #          for (e, v) in self.graph.feromones().items()})
        for solution in solutions:
            self.graph.set_feromones(
                {e: (self.ro + self.th/solution[1]) * v
                 for (e, v) in self.graph.feromones().items()})

    def run(self):
        for i in range(self.iterations):
            solutions = []
            coeffs = {e: 0 for (e, v) in self.graph.feromones().items()}
            for _ in range(self.n_ants):
                s, coeff = self.find_solution()
                solution = (s, self.rate_solution(s))
                solutions.append(solution)
                self.check_solution(solution)
                for (e, v) in coeff:
                    coeffs[e] = coeffs[e] + coeff[e]/solution[1]
            self.update_feromone(solutions, coeffs)
            print(str(i+1)+":\t"+str(int(self.best_solution[1])) +
                  "\t"+str(self.graph.optimal_value))
        return self.best_solution


if __name__ == "__main__":
    g = Graph()
    g.generateGraph("E-n22-k4.txt")
    aco = ACO(graph=g, capacity_limit=g.capacity_limit, iterations=50000)
    solution = aco.run()
