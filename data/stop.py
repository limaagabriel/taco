import sys
from tqdm import tqdm
from abc import ABC
from abc import abstractmethod


class StopCriterionDefinition(ABC):
    def __init__(self):
        self.__iterations = 0
        self.__pbar = tqdm(total=self.estimated_iterations())

    def __del__(self):
        self.__pbar.close()

    def initialize(self):
        self.__iterations = 0

    @property
    def iterations(self):
        return self.__iterations

    def __call__(self, criterion):
        self.__iterations += 1
        self.__pbar.update(1)
        return self.check(self.__iterations, criterion)

    @abstractmethod
    def check(self, iterations, criterion):
        pass

    @abstractmethod
    def estimated_iterations(self):
        pass


class StopCriterion(object):
    @staticmethod
    def iteration_limit(max_iterations):
        class IterativeStopCriterion(StopCriterionDefinition):
            def estimated_iterations(self):
                return max_iterations

            def check(self, iterations, length):
                return iterations > max_iterations

        return IterativeStopCriterion()

    @staticmethod
    def best_length(criterion_limit, max_iterations=sys.maxsize):
        class BestCriterionStopCriterion(StopCriterionDefinition):
            def estimated_iterations(self):
                return None

            def check(self, iterations, criterion):
                return criterion < criterion_limit or iterations > max_iterations

        return BestCriterionStopCriterion()
