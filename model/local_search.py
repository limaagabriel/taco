import random
from abc import ABC
from abc import abstractmethod
from simanneal import Annealer


class LocalSearchMethod(ABC):
    @abstractmethod
    def __call__(self, solutions, evaluation):
        pass


class SimulatedAnnealing(LocalSearchMethod):
    class __Annealer(Annealer):
        def __init__(self, state, evaluation):
            self.evaluation = evaluation
            super().__init__(state.copy())

        def move(self):
            num_solutions = len(self.state)
            idx = random.randint(0, num_solutions - 1)

            a = random.randint(1, len(self.state[idx]) - 2)
            b = random.randint(1, len(self.state[idx]) - 2)
            self.state[idx][a], self.state[idx][b] = self.state[idx][b], self.state[idx][a]

        def energy(self):
            return self.evaluation(self.state)

    def __call__(self, solutions, evaluation):
        return SimulatedAnnealing.__Annealer(solutions, evaluation).anneal()[0]


class K2Opt(LocalSearchMethod):
    @staticmethod
    def __swap(solution, i, j):
        new_solution = solution[:]
        new_solution[i:j] = solution[j - 1:i - 1:-1]

        return new_solution

    def __call__(self, solutions, evaluation):
        solutions = solutions.copy()
        for idx, solution in enumerate(solutions):
            best = solution.copy()
            improved = True

            while improved:
                improved = False
                for i in range(1, len(solution) - 2):
                    for j in range(i + 1, len(solution)):
                        if j - i == 1:
                            continue

                        new_solution = self.__swap(solution, i, j)
                        cost_a = evaluation([solution])
                        cost_b = evaluation([new_solution])
                        if cost_b < cost_a:
                            best = new_solution
                            improved = True
                solution = best
            solutions[idx] = best
        return solutions


class LocalSearchFactory(object):
    @staticmethod
    def __list_methods():
        return LocalSearchMethod.__subclasses__()

    @staticmethod
    def choices():
        return list(map(lambda x: x.__name__, LocalSearchFactory.__list_methods()))
        
    @staticmethod
    def build(name=None):
        if name is None:
            return None

        methods = LocalSearchFactory.__list_methods()
        method = list(filter(lambda x: name == x.__name__,  methods))
        if len(method) == 0:
            raise ValueError('A local search strategy named \'{}\' is not available yet.')
        return method[0]()
