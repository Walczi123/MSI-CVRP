import numpy as np


class Test:
    def __init__(self,  instance, graph=None, name="test", seed=None):
        self.instance = instance
        self.base_graph = graph
        self.name = name
        self.seed = seed

    def start(self):
        if self.seed is not None:
            np.random.seed(self.seed)
        self.instance.reset(self.base_graph)
        results = self.instance.run()
        self.save_to_file(results, "results/" +
                          self.name + "_" + str(self.instance.iterations) + "_" + str(self.seed) + ".txt")

    def save_to_file(self, results, file_path):
        f = open(file_path, "w")
        optimal = results.pop()
        best_result = results.pop()
        f.write('Optimal solution '+str(optimal)+'\n')
        f.write('Seed '+str(self.seed)+'\n')
        f.write('Number of iterations '+str(self.instance.iterations)+'\n')
        f.write('Number of cars '+str(self.instance.cars_limit)+'\n')
        f.write("Best Solution:"+"\t"+str(best_result[0]) +
                "\t"+str(best_result[1]) +
                "\t"+str(best_result[2]) +
                "\t"+str(best_result[3])+'\n\n')
        f.write("iteration"+"\t"+"paths" +
                "\t"+"result" +
                "\t"+"hipotesis 1" +
                "\t" + "hipotesis 2"+'\n')
        results = [str(i)+"\t"+str(result[0]) +
                   "\t"+str(result[1]) +
                   "\t"+str(result[2]) +
                   "\t"+str(result[3])+'\n'
                   for (i, result) in results]
        f.writelines(results)
        f.close
