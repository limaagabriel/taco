import sys


class AntTeam(object):
    def __init__(self, team_size):
        self.__team_size = team_size

        self.__solution = []
        self.__evaluation = sys.maxsize

    @property
    def evaluation(self):
        return self.__evaluation

    @property
    def solution(self):
        return self.__solution

    def build_solution(self, loader):
        self.__solution = []
