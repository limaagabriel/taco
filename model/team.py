import sys
from model.ant import Ant


class AntTeam(object):
    def __init__(self, team_size, initializer, evaluation):
        self.__team_size = team_size

        self.__taboo = []
        self.__solution = []
        self.__loader = None
        self.__initial_states = []
        self.__evaluation = sys.maxsize
        self.__evaluation_criterion = evaluation
        self.__ants = [Ant(initializer) for _ in range(team_size)]

    @property
    def evaluation(self):
        return self.__evaluation

    @property
    def solution(self):
        return self.__solution.copy()

    def __distance_of(self, solution):
        distance = 0
        current_state = solution[0]
        for state in solution[1:]:
            distance = distance + self.__loader.matrix[current_state, state]
            current_state = state

        return distance

    def __find_init(self, ant):
        return self.__initial_states[self.__ants.index(ant)]

    def __go_back(self, initial_states):
        for idx, state in enumerate(initial_states):
            self.__ants[idx].move_to(state)

    def __update_taboo(self):
        for ant in self.__ants:
            self.__taboo.append(ant.current_state)
        self.__taboo = list(set(self.__taboo))

    def __find_neighborhood(self):
        return list(filter(lambda x: x not in self.__taboo, self.__loader.nodes))

    def __find_moving_ant(self, ant, transition_params):
        another_ant_found = None
        next_state = ant.state_transition_rule(*transition_params)

        i1 = self.__find_init(ant)
        d1 = self.__distance_of(ant.solution + [next_state, i1])

        for other_ant in filter(lambda x: x != ant, self.__ants):
            i2 = self.__find_init(other_ant)
            d2 = self.__distance_of(other_ant.solution + [next_state, i2])
            if d2 < d1 and (another_ant_found is None or d2 < another_ant_found[1]):
                another_ant_found = (other_ant, d2)

        if another_ant_found is None:
            return ant, next_state
        return self.__find_moving_ant(another_ant_found[0], transition_params)

    def build_solution(self, loader, q0, alpha, beta, trails, local_search):
        for ant in self.__ants:
            ant.replace()

        self.__taboo = []
        self.__solution = []
        self.__update_taboo()
        self.__loader = loader
        self.__initial_states = list(map(lambda x: x.current_state, self.__ants))

        while len(self.__taboo) < len(loader):
            neighborhood = self.__find_neighborhood()
            transition_params = [loader, neighborhood, q0, alpha, beta, trails]
            first_ant = min(self.__ants, key=lambda x: self.__distance_of(x.solution))
            ant, next_state = self.__find_moving_ant(first_ant, transition_params)
            ant.move_to(next_state)
            self.__update_taboo()

        self.__go_back(self.__initial_states)
        self.__solution = list(map(lambda x: x.solution, self.__ants))
        if local_search is not None:
            def evaluation(x):
                return self.__evaluation_criterion(loader, x)
            self.__solution = local_search(self.__solution, evaluation)
        self.__evaluation = self.__evaluation_criterion(loader, self.__solution)
