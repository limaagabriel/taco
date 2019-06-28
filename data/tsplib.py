import numpy as np
import matplotlib.pyplot as plt

from pyparsing import *
from data.distance import DistanceFactory


class TSPLIBLoader(object):
    def __init__(self, path):
        self.__data = TSPLIBLoader.__load(path)
        self.__distance = DistanceFactory.get(self.weight_type)
        self.__matrix = self.__build_adjacency_matrix()

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

    @property
    def matrix(self):
        return self.__matrix.copy()

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
            for i in range(len(solution)):
                solution[i] = solution[i] - 1
            plt.plot(coords[solution, 0], coords[solution, 1])

    def __build_adjacency_matrix(self):
        n = self.dimension
        matrix = np.zeros((n + 1, n + 1))

        for i in range(1, n + 1):
            for j in range(1, n + 1):
                matrix[i, j] = self.weight(i, j)
        return matrix

    def __getitem__(self, idx):
        return np.array(self.__data['NODE_COORD_SECTION'][str(idx)])

    def __len__(self):
        return self.dimension

    @property
    def nodes(self):
        return list(range(1, self.dimension + 1))

    def plot(self, solutions=None):
        coords = np.zeros((self.dimension, 2))
        for i in range(1, self.dimension + 1):
            coords[i - 1, :] = self[i]

        if solutions is not None:
            self.__plot_solution(coords, solutions)
        self.__plot_cities(coords)

        plt.title('{} - {}'.format(self.name, self.comment))
        plt.show()

    def weight(self, i, j):
        a = self[i]
        b = self[j]
        return self.__distance(a, b)
