import statistics
from .ga import GeneticAlgorithm
from .fitness import evaluate
from .baseline import random_search

# (group, label, GA keyword arguments)
SENSITIVITY_CASES = [
    ("Population size", "Pop 20", {"population_size": 20}),
    ("Population size", "Pop 60 (default)", {"population_size": 60}),
    ("Population size", "Pop 100", {"population_size": 100}),
    ("Mutation rate", "Mut 0.05", {"mutation_rate": 0.05}),
    ("Mutation rate", "Mut 0.18 (default)", {"mutation_rate": 0.18}),
    ("Mutation rate", "Mut 0.35", {"mutation_rate": 0.35}),
    ("Selection pressure", "Tournament 2", {"tournament_size": 2}),
    ("Selection pressure", "Tournament 4 (default)", {"tournament_size": 4}),
    ("Selection pressure", "Tournament 8", {"tournament_size": 8}),
]


def _stats(values):
    return {"mean": statistics.mean(values),
            "std": statistics.pstdev(values),
            "runs": values}


def run_sensitivity(env, cfg, seeds):
    """Run every setting on several seeds; return mean/std of the best fitness."""
    results = {}
    cache = {}
    for group, label, kwargs in SENSITIVITY_CASES:
        key = tuple(sorted(kwargs.items()))
        fits, gens = [], []
        for s in seeds:
            ga = GeneticAlgorithm(env, cfg, seed=s, **kwargs)
            best, _, _ = ga.run()
            fits.append(evaluate(env, best, cfg)[0])
            gens.append(ga.generations_run)
        entry = _stats(fits)
        entry["group"] = group
        entry["mean_generations"] = statistics.mean(gens)
        results[label] = entry
    return results


def run_baseline_comparison(env, cfg, seeds):
    """GA vs random search with the same number of fitness evaluations per seed."""
    ga_fits, rs_fits, budgets = [], [], []
    for s in seeds:
        ga = GeneticAlgorithm(env, cfg, seed=s)
        best, _, _ = ga.run()
        ga_fits.append(evaluate(env, best, cfg)[0])
        budgets.append(ga.evaluations)
        _, rs_best, _ = random_search(env, cfg, ga.evaluations, seed=1000 + s)
        rs_fits.append(rs_best)
    return {
        "seeds": list(seeds),
        "evaluations_per_run": budgets,
        "ga": _stats(ga_fits),
        "random_search": _stats(rs_fits),
        "ga_wins": sum(g > r for g, r in zip(ga_fits, rs_fits)),
    }
