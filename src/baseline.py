import random
from .chromosome import Chromosome
from .fitness import evaluate


def random_search(env, cfg, n_evals, seed):
    """Baseline: sample random chromosomes and keep the best one seen so far.

    Returns (best_chromosome, best_fitness, best_so_far_history) where the history
    has one entry per evaluated chromosome.
    """
    rng = random.Random(seed)
    best, best_score = None, float("-inf")
    history = []
    for _ in range(n_evals):
        candidate = Chromosome.random(env, cfg.NUM_WAYPOINTS, rng)
        score = evaluate(env, candidate, cfg)[0]
        if score > best_score:
            best, best_score = candidate, score
        history.append(best_score)
    return best, best_score, history
