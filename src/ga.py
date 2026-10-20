import random
from .chromosome import Chromosome
from .fitness import evaluate
from .operators import tournament_selection, crossover, mutate


class GeneticAlgorithm:
    """Genetic Algorithm with elitism, tournament selection and early stopping."""

    def __init__(self, env, cfg, population_size=None, generations=None,
                 mutation_rate=None, tournament_size=None, patience=None, seed=None):
        self.env, self.cfg = env, cfg
        self.population_size = population_size or cfg.POPULATION_SIZE
        self.generations = generations or cfg.GENERATIONS
        self.mutation_rate = cfg.MUTATION_RATE if mutation_rate is None else mutation_rate
        self.tournament_size = tournament_size or cfg.TOURNAMENT_SIZE
        self.patience = cfg.PATIENCE if patience is None else patience
        self.rng = random.Random(cfg.RANDOM_SEED if seed is None else seed)
        # Filled in by run()
        self.best_per_gen = []      # best chromosome of every generation
        self.generations_run = 0
        self.evaluations = 0
        self.stopped_early = False

    def run(self):
        pop = [Chromosome.random(self.env, self.cfg.NUM_WAYPOINTS, self.rng)
               for _ in range(self.population_size)]
        best_history, avg_history = [], []
        best_overall, best_score = None, float("-inf")
        stagnant = 0
        self.best_per_gen = []
        self.stopped_early = False

        for gen in range(self.generations):
            scored = [evaluate(self.env, c, self.cfg)[0] for c in pop]
            gen_best_idx = max(range(len(pop)), key=lambda i: scored[i])
            if scored[gen_best_idx] > best_score + 1e-9:
                best_score = scored[gen_best_idx]
                best_overall = pop[gen_best_idx].copy()
                stagnant = 0
            else:
                stagnant += 1
            self.best_per_gen.append(pop[gen_best_idx].copy())
            best_history.append(max(scored))
            avg_history.append(sum(scored) / len(scored))
            self.generations_run = gen + 1

            # Termination criterion 2: no improvement for `patience` generations.
            if self.patience and stagnant >= self.patience:
                self.stopped_early = True
                break

            ranked = sorted(zip(scored, pop), key=lambda x: x[0], reverse=True)
            new_pop = [c.copy() for _, c in ranked[:self.cfg.ELITE_COUNT]]
            while len(new_pop) < self.population_size:
                p1 = tournament_selection(pop, scored, self.tournament_size, self.rng)
                p2 = tournament_selection(pop, scored, self.tournament_size, self.rng)
                if self.rng.random() < self.cfg.CROSSOVER_RATE:
                    c1, c2 = crossover(p1, p2, self.rng)
                else:
                    c1, c2 = p1.copy(), p2.copy()
                new_pop.append(mutate(c1, self.env, self.mutation_rate, self.rng))
                if len(new_pop) < self.population_size:
                    new_pop.append(mutate(c2, self.env, self.mutation_rate, self.rng))
            pop = new_pop

        self.evaluations = self.population_size * self.generations_run
        return best_overall, best_history, avg_history
