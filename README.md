# UAV Disaster-Surveillance Strategy Engine (Genetic Algorithm)

A modular Python simulation of a UAV route-planning problem solved with a Genetic Algorithm (GA).
Course: Artificial Intelligence (BSCS 5), Bahria University Lahore, Assignment 2 (CLO4).
Team: _add three names and roll numbers here_

## What the simulation models

- A 20 x 20 discretized grid (change `GRID_SIZE` in `src/config.py` to 50 if required) with a start cell,
  a goal cell, blocked cells (no-fly zones), hazard cells and high-priority target cells.
- **Chromosome** (`src/chromosome.py`): 8 waypoints `(x, y)`, a speed level (1-3) and a binary sensor flag per waypoint.
- **Fitness** (`src/fitness.py`): `5*coverage + 4*detection - 0.08*energy - 0.06*time - 2.5*risk - 25*blocked - 25*range_excess`.
- **Operators** (`src/operators.py`): tournament selection, segment crossover, spatial/speed/sensor mutation, elitism, repair of blocked or out-of-bounds waypoints.
- **Constraint handling**: blocked cells are avoided by BFS routing, repaired for waypoints and penalised; hazards are penalised through the risk term; a maximum flight range (`MAX_RANGE`) is penalised in proportion to the excess distance.
- **Termination** (`src/ga.py`): stop after `GENERATIONS`, or earlier when the best fitness has not improved for `PATIENCE` generations.
- **Baseline** (`src/baseline.py`): random search with the same number of fitness evaluations as the GA.
- **Experiments** (`src/experiments.py`): hyperparameter sensitivity (population size, mutation rate, tournament size) and GA vs random search, each over several random seeds.

## Project structure

```
src/
  config.py        parameters, weights, constraints
  environment.py   grid, obstacles, hazards, targets, repair
  chromosome.py    chromosome encoding
  operators.py     selection, crossover, mutation
  fitness.py       route expansion (BFS) and fitness evaluation
  ga.py            GeneticAlgorithm class (elitism, early stopping)
  baseline.py      random-search baseline
  experiments.py   sensitivity and baseline experiments
  plots.py         all figures
  main.py          runs everything and writes outputs/
outputs/           generated plots and summary.json
```

## Run locally

Python 3.10+ recommended. Open a terminal in this folder and run:

```
pip install -r requirements.txt
python -m src.main
```

The full run (main GA run, sensitivity study and baseline comparison over 5 seeds each) takes a few minutes.

## Output files (`outputs/`)

- `fitness_convergence.png`: best and average fitness per generation.
- `best_route.png`: grid map with obstacles, hazards, targets and the best route.
- `coverage_heatmap.png`: cells visited by the best route.
- `evolution_paths.png`: best flight path at the first, middle and last generation.
- `evolution_heatmaps.png`: coverage heatmaps at the same three generations.
- `hyperparameter_sensitivity.png`: mean +/- std best fitness over 5 seeds for population size, mutation rate and tournament size.
- `ga_vs_random_search.png`: best-so-far fitness of the GA vs random search with the same evaluation budget.
- `summary.json`: best chromosome, metrics, run information, sensitivity and baseline statistics.

## Important modelling note

This is a teaching simulation, not flight-control software. It does not control real drones. The example uses a single UAV to keep the assignment understandable; the chromosome can be extended to multiple UAVs by adding a segment per vehicle.
