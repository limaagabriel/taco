# Team Ant Colony Optimization (TACO)

This algorithm is a swarm-based approach to optimize combinatorial problems (e.g., finding the shortest path in a graph which covers all of its nodes). It was proposed by Illari Vallivaara (2008) as an extension to the well-known Ant Colony System algorithm (ACS, proposed by Dorigo and Gambardella, 1997).

## How ACS works

It works in a swarm fashion, where it spawns a population of simple reactive agents and a complex behavior emerges from these agents interacting with each other. The interaction mechanism used here is called _pheromone_, which is inspired by how ants work together to achieve objectives as a colony.

The pheromone mechanism is used to tell other ants which path is a promising solution given an objective. It means that, if a graph edge leads to the right solution, the agents should deposit some pheromone there. For example, when searching for the shortest path from point A to point B, the edges which composes the best solution should have more pheromone deposited in it. 

Then, when an agent T is trying to move from a node M to another node, it considers how distant M is to its neighbors and how much pheromone is on the path to them. The rule which defines how to use these measurements is often called _state transition rule_. The ACS algorithm defines this rule in a way the agents are biased towards the shortest path, which contains successful edges.

Thereby, all ants contained in the initial population iteratively constructs a candidate solution. During the iterative search procedure, the pheromone mechanism increases the chances of ants choosing better edges when constructing paths. Therefore,  it enables the algorithm to find better solutions.

## How TACO works

TACO is pretty similar to ACS in every aspect. The main difference here is the agent definition. Every agent in TACO is a team of _m_ ACS ants. Each team iteratively constructs a candidate solution and deposit pheromone as a single Ant would do. However, each agent inside a team is instructed to construct disjoint paths to solve _mTSP_-like problems (find multiple paths that, combined, covers every node in a graph). Therefore, TACO is said to be an ACS generalization (TACO is essentially ACS when _m = 1_, and it should find only one path that covers all graph nodes).

The state transition rule is slightly modified to enable collective work among ants. While there are unvisited nodes, an ant _T_ is chosen to move based on its path length (the ant with the shortest path). It chooses the next state _j_ based on ACS state transition rule. Then, to avoid sub-optimal movements, the algorithm checks if there is another ant _P_ which can move to _j_ and finish its movement with a shorter path than _T_. If this condition is met, the moving ant is now _P_, and it should move to another state based on ACS state transition rule. If not, _T_ moves to _j_.

## Usage

```python main.py problems/eil51.tsp```

It supports TSPLIB files. If you have any graph definition in this format, you can change `problems/eil51.tsp` to point to your file.

To get help about other available parameters, invoke the help page by running `python main.py --help`
