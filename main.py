from data.tsplib import TSPLIBLoader
from data.stop import StopCriterion
from data.evaluation import Evaluation
from data.initializer import Initializer
from model import TeamAntColonyOptimization

n_teams = 10
team_size = 2

evaluation = Evaluation.minmax()
initializer = Initializer.fixed_state(1)
loader = TSPLIBLoader('problems/eil51.tsp')
stop_criterion = StopCriterion.iteration_limit(150)
taco = TeamAntColonyOptimization(n_teams, team_size, initializer, evaluation)

solutions, score = taco.optimize(loader, stop_criterion)
loader.plot(solutions=solutions)
print(score)
