from graph import Graph
import numpy as np
import copy


class ACO:
    def __init__(self, iterations=1000, n_ants=25, graph=Graph(),
                 capacity_limit=500, distance_limit=1000,
                 alfa=2, beta=5, sigm=3, ro=0.2, th=80):
        self.iterations = iterations            # amount of iterations
        self.n_ants = n_ants                    # number of ants
        self.graph = copy.deepcopy(graph)       # graph information
        self.capacity_limit = capacity_limit    # capacity limit
        self.distance_limit = distance_limit    # distance limit
        self.best_solution = None               # best solutionalfa
        self.alfa = alfa                        # alfa parameter
        self.beta = beta                        # beta parameter
        self.sigm = sigm                        # sigm parameter
        self.ro = (1 - ro)                        # ro parameter
        self.th = th                            # th parameter

    def find_solution(self):
        solution = list()
        vertices = copy.deepcopy(self.graph.vertices)
        while(len(vertices) != 0):
            path = list()
            vertex = np.random.choice(vertices)
            capacity = self.capacity_limit - self.graph.demand[vertex]
            path.append(vertex)
            vertices.remove(vertex)
            while(len(vertices) != 0):
                probabilities = [(self.graph.feromones[v, vertex]**self.alfa) *
                                 ((1/self.graph.edges[(v, vertex)])**self.beta)
                                 for v in vertices]
                probabilities = probabilities/np.sum(probabilities)
                vertex = np.random.choice(vertices, p=probabilities)
                capacity = capacity - self.graph.demand[vertex]
                if(capacity > 0):
                    path.append(vertex)
                    vertices.remove(vertex)
                else:
                    break
            solution.append(path)
        return solution

    def rate_solution(self, solution):
        s = 0
        for i in solution:
            a = 1
            for j in i:
                b = j
                s = s + self.edges[(min(a, b), max(a, b))]
                a = b
            b = 1
            s = s + self.edges[(min(a, b), max(a, b))]
        return s

    def check_solution(self, solutions):
        if self.best_solution is None or self.best_solution[1] > solution[1]:
            self.best_solution = solution

    def update_feromone(self, solutions):
        for solution in solutions:
            self.graph.feromones = {e: (self.ro + self.th/solution[0]) * v
                                    for (e, v) in self.graph.feromones.items()}

    def run(self):
        for _ in range(0, self.n):
            solutions = []
            for _ in self.n_ants:
                solution = self.find_solution()
                solutions.append(solution, self.rate_solution(solution))
                self.check_solution(solution)
            self.update_feromone(solutions)
        return self.best_solution


if __name__ == "__main__":
    aco = ACO()
    solution = aco.run()
    solution.print()
