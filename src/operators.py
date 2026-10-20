import random
from .chromosome import Chromosome

def tournament_selection(population, scores, tournament_size, rng=random):
    candidates = [rng.randrange(len(population)) for _ in range(tournament_size)]
    winner = max(candidates, key=lambda i: scores[i])
    return population[winner].copy()

def crossover(parent_a, parent_b, rng=random):
    """Segment crossover: waypoint, speed and sensor values swap at the same cut point."""
    n = len(parent_a.waypoints)
    if n < 2:
        return parent_a.copy(), parent_b.copy()
    cut = rng.randint(1, n - 1)
    child1 = Chromosome(
        parent_a.waypoints[:cut] + parent_b.waypoints[cut:],
        parent_a.speeds[:cut] + parent_b.speeds[cut:],
        parent_a.sensors[:cut] + parent_b.sensors[cut:])
    child2 = Chromosome(
        parent_b.waypoints[:cut] + parent_a.waypoints[cut:],
        parent_b.speeds[:cut] + parent_a.speeds[cut:],
        parent_b.sensors[:cut] + parent_a.sensors[cut:])
    return child1, child2

def mutate(chromosome, env, mutation_rate, rng=random):
    """Spatial mutation changes waypoint coordinates; other mutations change speed/sensor."""
    child = chromosome.copy()
    for i in range(len(child.waypoints)):
        if rng.random() < mutation_rate:
            x, y = child.waypoints[i]
            child.waypoints[i] = (x + rng.randint(-3, 3), y + rng.randint(-3, 3))
        if rng.random() < mutation_rate:
            child.speeds[i] = rng.randint(1, 3)
        if rng.random() < mutation_rate:
            child.sensors[i] = 1 - child.sensors[i]
    child.waypoints = [env.repair_point(p) for p in child.waypoints]
    return child
