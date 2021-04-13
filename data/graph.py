import re
import numpy as np


class Graph:
    def __init__(self):
        self.vertices = None
        self.__edges__ = None
        self.demand = None
        self.__pheromones__ = None
        self.capacity_limit = None
        self.optimal_value = None
        self.car_min = None

    def pheromones(self, x=None, y=None):
        if x is None and y is None:
            return self.__pheromones__
        return self.__pheromones__[min(x, y), max(x, y)]

    def set_pheromones(self, value):
        self.__pheromones__ = value

    def edges(self, x, y):
        return self.__edges__[min(x, y), max(x, y)]

    def getData(self, fileName):
        f = open(fileName, "r")
        content = f.read()
        self.optimal_value = re.search(
            "Optimal value: (\d+)", content, re.MULTILINE)
        if(self.optimal_value is not None):
            self.optimal_value = self.optimal_value.group(1)
        else:
            self.optimal_value = re.search(
                "Best value: (\d+)", content, re.MULTILINE)
            if(self.optimal_value is not None):
                self.optimal_value = self.optimal_value.group(1)

        self.car_min = re.search(
            "Min no of trucks: (\d+)", content, re.MULTILINE)
        if(self.car_min is not None):
            self.car_min = self.car_min.group(1)
        else:
            self.car_min = re.search(
                "No of trucks: (\d+)", content, re.MULTILINE)
            if(self.car_min is not None):
                self.car_min = self.car_min.group(1)

        self.capacity_limit = re.search("^CAPACITY : (\d+)$",
                                        content, re.MULTILINE).group(1)
        graph = re.findall(r"^(\d+) (\d+) (\d+)$", content, re.MULTILINE)
        self.demand = re.findall(r"^(\d+) (\d+)$", content, re.MULTILINE)
        graph = {int(a): (int(b), int(c)) for a, b, c in graph}
        self.demand = {int(a): int(b) for a, b in self.demand}
        self.capacity_limit = int(self.capacity_limit)
        self.optimal_value = int(self.optimal_value)
        self.car_min = int(self.car_min)
        return graph

    def check_zero(self, x):
        if x > 0:
            return x
        return 0.000000000000000001

    def generateGraph(self, fileName, pheromones_start=1):
        graph = self.getData(fileName)
        self.vertices = list(graph.keys())
        self.vertices.remove(1)

        self.__edges__ = {(min(a, b), max(a, b)): self.check_zero(np.sqrt((graph[a][0]-graph[b][0])**2 + (
            graph[a][1]-graph[b][1])**2)) for a in graph.keys() for b in graph.keys()}
        self.__pheromones__ = {(min(a, b), max(a, b)): pheromones_start for a in graph.keys()
                               for b in graph.keys() if a != b}

        return self.vertices, self.__edges__, self.capacity_limit, self.demand, \
            self.__pheromones__, self.optimal_value
