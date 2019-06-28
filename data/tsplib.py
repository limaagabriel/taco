import numpy as np
import matplotlib.pyplot as plt

from pyparsing import *
from data.distance import DistanceFactory


class TSPLIBLoader(object):
    def __init__(self, path):
        self.__data = TSPLIBLoader.__load(path)
        print(self.__data)

    @property
    def name(self):
        return self.__data['NAME']

    @property
    def type(self):
        return self.__data['TYPE']

    @property
    def comment(self):
        return self.__data['COMMENT']

    @property
    def dimension(self):
        return self.__data['DIMENSION']

    @property
    def weight_type(self):
        return self.__data['EDGE_WEIGHT_TYPE']

    def get(self, idx):
        return np.array(self.__data['NODE_COORD_SECTION'][str(idx)])

    @staticmethod
    def __load(path):
        parser = TSPLIBLoader.__get_parser()
        response = parser.parseFile(path, parseAll=True)

        return response.asDict()

    @staticmethod
    def __get_parser():
        equal, space, eof = map(Suppress, [':', ' ', 'EOF'])
        number = pyparsing_common.number()
        field = Word(alphanums + '_')
        spaces = ZeroOrMore(space)
        value = (number + Suppress(lineEnd)) | restOfLine

        attribute = Group(field + spaces + equal + spaces + value)
        attributes = OneOrMore(attribute)

        node = Group(number + Group(number + number) + Suppress(lineEnd))
        nodes = Dict(OneOrMore(node))

        return Dict(attributes + Group('NODE_COORD_SECTION' + nodes + eof))

    @staticmethod
    def __plot_cities(coords):
        plt.scatter(coords[:, 0], coords[:, 1])

    @staticmethod
    def __plot_solution(coords, solutions):
        for solution in solutions:
            plt.plot(coords[solution, 0], coords[solution, 1])

    def plot(self, solutions=None):
        coords = np.zeros((self.dimension, 2))
        for i in range(1, self.dimension + 1):
            coords[i - 1, :] = self.get(i)

        self.__plot_cities(coords)
        if solutions is not None:
            self.__plot_solution(coords, solutions)

        plt.title('{} ({})'.format(self.name, self.comment))
        plt.show()

    def weight(self, i, j):
        a = self.get(i)
        b = self.get(j)

        distance_method = DistanceFactory.get(self.weight_type)
        return distance_method(a, b)
