import argparse
from data.tsplib import TSPLIBLoader
from data.stop import StopCriterion
from data.evaluation import Evaluation
from data.initializer import Initializer
from model import TeamAntColonyOptimization
from model.util import plot_evolution_track
from model.local_search import LocalSearchFactory

parser = argparse.ArgumentParser()
parser.add_argument('problem', help='TSPLIB file (.tsp extension) containing a graph definition')
parser.add_argument('--num-teams', '-n', type=int, default=10,
					help='Number of Ant Teams to instantiate (i.e. swarm size)')
parser.add_argument('--team-size', '-m', type=int, default=2,
					help='Number of ants composing each team (i.e. number of paths in final solution)')
parser.add_argument('--max-iterations', '-i', type=int, default=150,
					help='Number of iterations allowed to run the optimization step')
parser.add_argument('--initial-state', '-s', type=int, default=1,
					help='Defines the initial state (i.e. initial city, where teams are spawned)')
parser.add_argument('--local-search', '-l', choices=LocalSearchFactory.choices(), default=None,
					help='Choose an available local search method to improve output paths')

args = parser.parse_args()

evaluation = Evaluation.minmax()
loader = TSPLIBLoader(args.problem)
initializer = Initializer.fixed_state(args.initial_state)
local_search = LocalSearchFactory.build(args.local_search)
stop_criterion = StopCriterion.iteration_limit(args.max_iterations)
taco = TeamAntColonyOptimization(args.num_teams, args.team_size, initializer, evaluation)

track_base = 'm{}_{}minmax_track.png'
solution_base = '{}2opt_m{}_{}minmax.png'
solutions, score, track = taco.optimize(loader, stop_criterion, local_search)

plot_evolution_track(track_base.format(args.team_size, score), track)
loader.plot(solution_base.format(loader.name, args.team_size, score), solutions=solutions)
