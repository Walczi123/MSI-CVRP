def create_ants():
    pass


def find_solution():
    pass


def choose_solution():
    pass


def evaporate_feromone():
    pass


def update_feromone():
    pass


def main():
    n = 1000  # amount of iterations
    best_solution = 0
    for i in range(0, n):
        ants = create_ants()
        for ant in ants:
            solution = find_solution()
            best_solution = choose_solution(best_solution, solution)
        evaporate_feromone()
        for ant in ants:
            update_feromone(best_solution, ant)
    return best_solution


if __name__ == "__main__":
    solution = main()
    solution.print()
