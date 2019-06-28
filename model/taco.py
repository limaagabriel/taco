import sys
from model.team import AntTeam


class TeamAntColonyOptimization(object):
    def __init__(self, n_teams, team_size):
        self.__best_solution = []
        self.__best_evaluation = sys.maxsize
        self.__teams = [AntTeam(team_size) for _ in range(n_teams)]

    def optimize(self, loader, stop_criterion):
        while not stop_criterion(self.__best_evaluation):
            for team in self.__teams:
                team.build_solution(loader)
                if team.evaluation < self.__best_evaluation:
                    self.__best_solution = team.solution
                    self.__best_evaluation = team.evaluation

        return self.__best_solution, self.__best_evaluation
