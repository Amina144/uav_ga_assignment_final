# Genetic Algorithm for UAV Disaster Surveillance

**Course:** Artificial Intelligence  
**Assignment:** 2 — CLO4  
**Team members:** [Add three names and roll numbers]

## 1. Problem and objective
The task is to plan a UAV route in a grid containing obstacles, hazard cells, and high-priority target cells. The strategy must increase area coverage and target detection while reducing energy use, flight time, and hazard exposure. Because these objectives conflict, a weighted fitness score is used to compare candidate solutions.

## 2. Chromosome representation
Each chromosome contains three aligned segments:
1. **Waypoints:** a list of `(x, y)` grid coordinates.
2. **Speed profile:** an integer at each waypoint (`1=slow`, `2=medium`, `3=fast`).
3. **Sensor profile:** a binary value at each waypoint (`1=on`, `0=off`).

This hybrid representation is suitable because coordinates describe spatial decisions, speed is a small discrete choice, and sensor activation is binary. The demonstration uses one UAV; a multi-UAV chromosome can store a separate waypoint/speed/sensor segment per drone.

## 3. Fitness function
Let `C` be the fraction of free grid cells visited, `D` the fraction of target cells visited, `E` the energy estimate, `T` the time estimate, `R` the fraction of route cells in hazards, and `I` the fraction of route cells that violate hard constraints.

`Fitness = 5C + 4D - 0.08E - 0.06T - 2.5R - 25I`

Higher fitness is preferred. Coverage and detection are positive rewards. Energy, time, risk, and invalid movement are penalties. The weights express the design preference that target detection and coverage matter strongly, while invalid movement should be heavily discouraged. These are simulation weights, not universal real-world constants.

## 4. Genetic operators and constraint handling
The population is initialized with random chromosomes. Tournament selection chooses parents. Segment crossover swaps corresponding waypoint, speed, and sensor segments after a random cut. Mutation changes coordinates locally, chooses a new speed, or flips sensor activation. Repair clamps coordinates to the grid and moves blocked waypoints to nearby free cells. The fitness function also penalizes blocked route steps and hazard exposure. Elitism keeps a small number of the best candidates in each generation.

## 5. Results and visualization
Run the program and insert the generated figures:
- `outputs/fitness_convergence.png`: best and average fitness across generations.
- `outputs/best_route.png`: evolved route, obstacles, hazards, targets, start, and goal.
- `outputs/coverage_heatmap.png`: route visit frequency.
- `outputs/hyperparameter_sensitivity.png`: comparison of population sizes and mutation rates.

Describe the actual results from `outputs/summary.json`. Do not claim that the GA always finds the global optimum; it is a stochastic search method.

## 6. Hyperparameter sensitivity
The provided experiment compares population sizes of 20, 60, and 100, and mutation rates of 0.05, 0.18, and 0.35 (one seeded run for each setting, with 35 generations). A larger population explores more candidates but takes more computation. A low mutation rate may reduce diversity and cause premature convergence. A high mutation rate explores more widely but may disrupt good solutions. Tournament size controls selection pressure: increasing it favors stronger individuals more strongly, which can speed progress but reduce diversity. For a stronger study, repeat each setting across 3–5 random seeds and compare mean and standard deviation.

## 7. Comparison with random search
The GA repeatedly selects and recombines better candidates, whereas random search generates candidates without learning from previous scores. For a fair comparison, use the same environment and evaluate the same number of candidate chromosomes. Report the best score and, preferably, the average score over multiple seeds. Insert your measured values here after running the experiment.

## 8. Limitations and conclusion
This project is a simplified grid simulation. It uses estimated energy/time costs and a fixed route expansion rule, not real drone physics or flight-control software. The GA demonstrates how a hybrid chromosome, weighted fitness, genetic operators, and repair mechanisms can support multi-objective route planning. Real deployment would require validated dynamics, communications, battery models, geofencing, and safety testing.
