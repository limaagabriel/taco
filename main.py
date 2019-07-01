from data.tsplib import TSPLIBLoader
from data.stop import StopCriterion
from data.evaluation import Evaluation
from data.initializer import Initializer
from model import TeamAntColonyOptimization
from model.util import plot_evolution_track
from model.local_search import K2OptLocalSearch

n_teams = 10
team_size = 4

evaluation = Evaluation.minmax()
initializer = Initializer.fixed_state(1)
loader = TSPLIBLoader('problems/eil51.tsp')
local_search = K2OptLocalSearch()
stop_criterion = StopCriterion.iteration_limit(150)
taco = TeamAntColonyOptimization(n_teams, team_size, initializer, evaluation)

track_base = 'm{}_{}minmax_track.png'
solution_base = '{}2opt_m{}_{}minmax.png'
solutions, score, track = taco.optimize(loader, stop_criterion, local_search)
loader.plot(solution_base.format(loader.name, team_size, score), solutions=solutions)
plot_evolution_track(track_base.format(team_size, score), track)
