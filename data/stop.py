import sys
from abc import ABC
from abc import abstractmethod


class StopCriterionDefinition(ABC):
    def __init__(self):
        self.__iterations = 0

    def initialize(self):
        self.__iterations = 0

    @property
    def iterations(self):
        return self.__iterations

    def __call__(self, criterion):
        self.__iterations += 1
        return self.check(self.__iterations, criterion)

    @abstractmethod
    def check(self, iterations, criterion):
        pass


class StopCriterion(object):
    @staticmethod
    def iteration_limit(max_iterations):
        class IterativeStopCriterion(StopCriterionDefinition):
            def check(self, iterations, length):
                return iterations > max_iterations

        return IterativeStopCriterion()

    @staticmethod
    def best_length(criterion_limit, max_iterations=sys.maxsize):
        class BestCriterionStopCriterion(StopCriterionDefinition):
            def check(self, iterations, criterion):
                return criterion < criterion_limit or iterations > max_iterations

        return BestCriterionStopCriterion()
