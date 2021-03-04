class Graph:
    def __init__(self):
        self.vertices = None
        self.edges = None
        self.demand = None
        self.__feromones__ = None

    def feromones(self, x, y):
        return self.__feromones__(min(x, y), max(x, y))
