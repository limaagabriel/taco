# Team Ant Colony Optimization (TACO) :ant:
This algorithm was proposed in 2008 by Illari Vallivaara. It is a swarm-based approach to optimize combinatorial problems (e.g., finding the shortest path in a graph that covers all of its nodes).

## How it works?
For a better understanding of this algorithm, let me describe first how the ACS algorithm works. Then, I'll introduce TACO as a generalization of it.

### Ant Colony System (ACS)
The Ant Colony System algorithm, proposed by Dorigo and Gambardella in 1997 is a well-known swarm intelligence algorithm for combinatorial optimization. It works by producing a complex behavior derived from the interaction of simple reactive agents. The interaction mechanism used here is called pheromone, which is inspired by how ants work together to achieve objectives as a colony.

The pheromone mechanism provides a way of describing to other ants which path is a promising solution given an objective. It means that, if a graph edge leads to a possible output, the agents should deposit some pheromone there. For example, when searching for the shortest path from point *A* to point *B*, the edges which compose the best solution should have more pheromone deposited in it. The figure below describes how this mechanism work.

![ACS example](https://www.funpecrp.com.br/gmr/year2005/vol3-4/images/wob09fig2.jpg)

Then, when an agent *T* is trying to move from a node M to another node, it considers how distant M is to its neighbors and how much pheromone is on the path to them. The rule which defines how to use these measurements is often called state transition rule. The ACS algorithm defines this rule in a way the agents are biased towards the shortest path, which contains successful edges.

Thereby, all ants contained in the initial population iteratively constructs a candidate solution. During the iterative search procedure, the pheromone mechanism increases the chances of ants choosing better edges when constructing paths. Therefore, it enables the algorithm to find better solutions.

### Team ant colony optimization (TACO)
TACO is pretty similar to ACS in every aspect. The main difference between these two algorithms is the agent definition. Every agent in TACO is a team of *m* ACS ants. Each team constructs a candidate solution iteratively. Also, it deposits pheromone as a single ant would do. However, each agent inside a team is instructed to build disjoint paths to solve *mTSP*-like problems (find multiple tracks that, combined, cover every node in a graph). TACO is essentially ACS when *m = 1*, and it should encounter only one route that includes all graph nodes. Therefore, TACO is said to be an ACS generalization.

The state transition rule is slightly modified to enable collective work among ants. While there are unvisited nodes, the algorithm designs an ant *T* to move based on its path length (the ant with the shortest path). It chooses the next state *j* based on the ACS state transition rule. Then, to avoid sub-optimal movements, the algorithm checks if there is another ant *P* which can move to *j* and finish its displacement with a shorter path than *T*. If it meets this condition, it selects *P* as the current moving ant, and it should move to another state based on the ACS state transition rule. If not, *T* moves to *j*.
## Usage

```python main.py problems/eil51.tsp```

It supports TSPLIB files. If you have any graph definition in this format, you can change `problems/eil51.tsp` to point to your file.

To get help about other available parameters, invoke the help page by running `python main.py --help`
