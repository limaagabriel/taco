from data.tsplib import TSPLIBLoader
from data.stop import StopCriterion
from data.initializer import Initializer
from model import TeamAntColonyOptimization

initializer = Initializer.fixed_state(1)
loader = TSPLIBLoader('problems/eil51.tsp')
taco = TeamAntColonyOptimization(10, 2, initializer)
stop_criterion = StopCriterion.iteration_limit(150)

solutions, lengths = taco.optimize(loader, stop_criterion)
loader.plot(solutions=solutions)
