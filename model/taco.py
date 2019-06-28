import sys
import numpy as np
from model.team import AntTeam


class TeamAntColonyOptimization(object):
    def __init__(self, n_teams, team_size, initializer, rho=0.1, q0=0.9, alpha=1, beta=2):
        self.__q0 = q0
        self.__rho = rho
        self.__beta = beta
        self.__alpha = alpha
        self.__n_teams = n_teams
        self.__best_solution = []
        self.__best_evaluation = sys.maxsize
        self.__teams = [AntTeam(team_size, initializer) for _ in range(n_teams)]

    def optimize(self, loader, stop_criterion):
        min_p = 1e-4
        n = loader.dimension + 1
        pheromone_trails = np.ones((n, n))

        while not stop_criterion(self.__best_evaluation):
            self.__build_solutions(loader, pheromone_trails)
            self.__update_best_solution()

            self.__local_pheromone_update(pheromone_trails)
            self.__global_pheromone_update(pheromone_trails)
            pheromone_trails[pheromone_trails < min_p] = min_p

        return self.__best_solution, self.__best_evaluation

    def __build_solutions(self, loader, trails):
        for team in self.__teams:
            team.build_solution(loader, self.__q0, self.__alpha, self.__beta, trails)

    def __update_best_solution(self):
        for team in self.__teams:
            if team.evaluation < self.__best_evaluation:
                self.__best_evaluation = team.evaluation
                self.__best_solution = team.solution

    def __local_pheromone_update(self, trails):
        step = 1
        delta_matrix = np.zeros_like(trails)

        for team in self.__teams:
            for solution in team.solution:
                src = solution[:-1]
                dest = solution[1:]
                delta_matrix[src, dest] += step

        trails *= 1 - self.__rho
        trails += self.__rho * delta_matrix

    def __global_pheromone_update(self, trails):
        step = 1.0 / self.__best_evaluation
        delta_matrix = np.zeros_like(trails)
        for solution in self.__best_solution:
            src = solution[:-1]
            dest = solution[1:]
            delta_matrix[src, dest] += step

        trails *= 1 - self.__rho
        trails += self.__rho * delta_matrix
