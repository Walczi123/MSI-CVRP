


class MinMax (aco):

    def update_pheromone(self, solutions):
        coeffs = {e: 0 for (e, v) in self.graph.pheromones().items()}
        for solution in solutions:
            
            for path in (solution[0]):
                for i in range(len(path)-1):
                    e = (min(path[i], path[i+1]),
                         max(path[i], path[i+1]))
                    coeffs[e] += (self.th/solution[1])