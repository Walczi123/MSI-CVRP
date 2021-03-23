
from graph import Graph
from aco import ACO

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