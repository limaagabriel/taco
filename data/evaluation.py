import numpy as np
from abc import ABC
from abc import abstractmethod


class EvaluationDefinition(ABC):
    def __init__(self):
        self.__loader = None

    def total_distance(self, solution):
        distance = 0
        current_state = solution[0]
        for state in solution[1:]:
            distance = distance + self.__loader.matrix[current_state, state]
            current_state = state
        return distance

    def __call__(self, loader, solutions):
        self.__loader = loader
        size = len(solutions)
        distances = np.zeros(size)

        for i in range(size):
            distances[i] = self.total_distance(solutions[i])

        return self.evaluate(distances)

    @abstractmethod
    def evaluate(self, distances):
        pass


class Evaluation(object):
    @staticmethod
    def squared_sum():
        class SquaredSumEvaluation(EvaluationDefinition):
            def evaluate(self, distances):
                return (distances ** 2).sum()

        return SquaredSumEvaluation()

    @staticmethod
    def minmax():
        class MinMaxEvaluation(EvaluationDefinition):
            def evaluate(self, distances):
                return distances.max()

        return MinMaxEvaluation()
