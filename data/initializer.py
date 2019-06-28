import numpy as np
from abc import ABC
from abc import abstractmethod


class InitializerDefinition(ABC):
    @abstractmethod
    def __call__(self):
        pass


class Initializer(object):
    @staticmethod
    def uniform(bounds):
        class UniformInitializer(InitializerDefinition):
            def __call__(self):
                return np.random.uniform(bounds[0], bounds[1])

        return UniformInitializer()

    @staticmethod
    def fixed_state(state):
        class FixedStateInitializer(InitializerDefinition):
            def __call__(self):
                return state

        return FixedStateInitializer()
