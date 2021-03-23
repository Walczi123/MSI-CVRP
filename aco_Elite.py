
from graph import Graph
from aco import ACO

class ACO_Elite(ACO):

    def __init__(self, n_elite = 3, **args):
        super().__init__(**args)
        self.n_elite = n_elite              #elite ants number parameter

    def update_pheromone(self, solutions):
        solutions.sort(key = lambda x: x[1])
        coeffs = {e: 0 for (e, v) in self.graph.pheromones().items()}
        for i in range(self.n_elite):
            for path in (solutions[i][0]):
                for i in range(len(path)-1):
                    e = (min(path[i], path[i+1]),
                            max(path[i], path[i+1]))
                    coeffs[e] += (self.th/solutions[i][1])

        self.graph.set_pheromones(
            {e: ((1-self.ro) * v) + coeffs[e]
                for (e, v) in self.graph.pheromones().items()})


if __name__ == "__main__":
    t_max = 5
    g = Graph()
    g.generateGraph("E-n22-k4.txt")
    aco = ACO_Elite(n_elite = 5, graph=g, cars_limit=6, capacity_limit=g.capacity_limit, distance_limit=1000, iterations=1000)
    # aco = ACO(graph=g, cars_limit=5, capacity_limit=g.capacity_limit, distance_limit=1000, iterations=1000)
    solution = aco.run()