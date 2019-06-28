import uuid
import numpy as np


class Ant(object):
    def __init__(self, initializer):
        self.__solution = []
        self.__initializer = initializer
        self.__current_state = initializer()
        self.__id = str(uuid.uuid4())

    def move_to(self, state):
        self.__current_state = state
        self.__solution.append(state)

    @property
    def id(self):
        return self.__id

    @property
    def solution(self):
        return self.__solution.copy()

    @property
    def current_state(self):
        return self.__current_state

    def replace(self):
        self.__current_state = self.__initializer()
        self.__solution = [self.__current_state]

    def state_transition_rule(self, loader, neighborhood, q0, alpha, beta, trails):
        if len(neighborhood) == 1:
            return neighborhood[0]

        if np.random.uniform(0, 1) <= q0:
            return self.__exploit(loader, neighborhood, alpha, beta, trails)
        return self.__explore(loader, neighborhood, alpha, beta, trails)

    def __get_targets(self, loader, neighborhood, alpha, beta, trails):
        possible_trails = trails[self.current_state, neighborhood]
        attractiveness = loader.matrix[self.current_state, neighborhood] ** -1

        return (possible_trails ** alpha) * (attractiveness ** beta)

    def __exploit(self, loader, neighborhood, alpha, beta, trails):
        targets = self.__get_targets(loader, neighborhood, alpha, beta, trails)
        return neighborhood[targets.argmax()]

    def __explore(self, loader, neighborhood, alpha, beta, trails):
        targets = self.__get_targets(loader, neighborhood, alpha, beta, trails)

        probabilities = targets / targets.sum()
        return np.random.choice(neighborhood, p=probabilities)

    def __eq__(self, other):
        return self.id == other.id
