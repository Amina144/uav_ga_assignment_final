GRID_SIZE = 20
NUM_WAYPOINTS = 8
POPULATION_SIZE = 60
GENERATIONS = 100
MUTATION_RATE = 0.18
TOURNAMENT_SIZE = 4
ELITE_COUNT = 2
CROSSOVER_RATE = 0.85
RANDOM_SEED = 17

# Termination: stop after GENERATIONS, or earlier if the best fitness has not
# improved for PATIENCE consecutive generations (stagnation / early stopping).
PATIENCE = 20

# Hard constraint: maximum flight range (route length in grid steps).
# Routes longer than MAX_RANGE are penalised in proportion to the excess.
MAX_RANGE = 90
RANGE_PENALTY = 25.0

# Number of independent seeds used in the sensitivity and baseline experiments.
EXPERIMENT_SEEDS = [1, 2, 3, 4, 5]

# Fitness weights. Coverage/detection are rewards; cost terms are penalties.
W_COVERAGE = 5.0
W_DETECTION = 4.0
W_ENERGY = 0.08
W_TIME = 0.06
W_RISK = 2.5
INVALID_PENALTY = 25.0
