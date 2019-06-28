import sys
import numpy as np
from model.ant import Ant


class AntTeam(object):
    def __init__(self, team_size, initializer, evaluation):
        self.__team_size = team_size

        self.__taboo = []
        self.__solution = []
        self.__evaluation = sys.maxsize
        self.__evaluation_criterion = evaluation
        self.__ants = [Ant(initializer) for _ in range(team_size)]

    @property
    def evaluation(self):
        return self.__evaluation

    @property
    def solution(self):
        return self.__solution.copy()

    @staticmethod
    def __distance_of(solution, loader):
        distance = 0
        current_state = solution[0]
        for state in solution[1:]:
            distance = distance + loader.matrix[current_state, state]
            current_state = state

        return distance

    def __go_back(self, initial_states):
        for idx, state in enumerate(initial_states):
            self.__ants[idx].move_to(state)

    def __update_taboo(self):
        for ant in self.__ants:
            self.__taboo.append(ant.current_state)
        self.__taboo = list(set(self.__taboo))

    def __find_neighborhood(self, loader):
        return list(filter(lambda x: x not in self.__taboo, loader.nodes))

    def build_solution(self, loader, q0, alpha, beta, trails):
        for ant in self.__ants:
            ant.replace()

        self.__taboo = []
        self.__solution = []
        self.__update_taboo()
        initial_states = list(map(lambda x: x.current_state, self.__ants))

        while len(self.__taboo) < len(loader):
            ant = min(self.__ants, key=lambda x: self.__distance_of(x.solution, loader))
            initial = initial_states[self.__ants.index(ant)]
            neighborhood = self.__find_neighborhood(loader)
            next_state = ant.state_transition_rule(loader, neighborhood, q0, alpha, beta, trails)
            distance = self.__distance_of(ant.solution + [next_state, initial], loader)

            for idx, other_ant in enumerate(self.__ants):
                if other_ant == ant:
                    continue

                solution = other_ant.solution + [next_state, initial_states[idx]]
                other_distance = self.__distance_of(solution, loader)
                if other_distance < distance:
                    ant = other_ant
                    distance = other_distance

            next_state = ant.state_transition_rule(loader, neighborhood, q0, alpha, beta, trails)
            ant.move_to(next_state)
            self.__update_taboo()

        self.__go_back(initial_states)
        self.__solution = list(map(lambda x: x.solution, self.__ants))
        self.__evaluation = self.__evaluation_criterion(loader, self.__solution)
