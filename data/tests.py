class Tests:
    def __init__(self, instance, n_repetition=1, name="test"):
        self.n_repetition = n_repetition
        self.instance = instance
        self.name = name

    def start(self):
        for i in range(self.n_repetition):
            f = open("results/" + self.name + "_" + str(i), "w")
            results = self.instance.run()
            for result in results:
                print(result)
                f.write(result + '\n')
            f.close
