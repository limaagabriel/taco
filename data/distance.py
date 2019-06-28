import numpy as np
from abc import ABC
from abc import abstractmethod


class DistanceDefinition(ABC):
    @abstractmethod
    def __call__(self, a, b):
        pass


class EuclideanDistance(DistanceDefinition):
    def __call__(self, a, b):
        return np.sqrt(np.sum((a - b) ** 2))


class DistanceFactory(object):
    __default_map = {
        'EUC_2D': EuclideanDistance()
    }

    @staticmethod
    def register(key, distance_callable):
        DistanceFactory.__default_map[key] = distance_callable

    @staticmethod
    def get(key):
        if key not in DistanceFactory.__default_map:
            raise ValueError('Distance method not registered.')
        return DistanceFactory.__default_map[key]
