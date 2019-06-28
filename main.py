from data.tsplib import TSPLIBLoader
from data.stop import StopCriterion
from model import TeamAntColonyOptimization

taco = TeamAntColonyOptimization()
loader = TSPLIBLoader('problems/eil51.tsp')
stop_criterion = StopCriterion.iteration_limit(2500)

solutions, lengths = taco.optimize(loader, stop_criterion)
loader.plot(solutions=solutions)
