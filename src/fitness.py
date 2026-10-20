from collections import deque

def shortest_free_segment(env, start, goal):
    """BFS path between two points using 4-neighbour moves and avoiding blocked cells."""
    if env.is_blocked(start) or env.is_blocked(goal):
        return [start, goal]
    queue = deque([start])
    parent = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        x, y = current
        for nxt in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if (0 <= nxt[0] < env.size and 0 <= nxt[1] < env.size
                    and not env.is_blocked(nxt) and nxt not in parent):
                parent[nxt] = current
                queue.append(nxt)
    if goal not in parent:
        # In a disconnected map, return a direct segment so the violation is penalized.
        return [start, goal]
    path, node = [], goal
    while node is not None:
        path.append(node)
        node = parent[node]
    return list(reversed(path))

def expand_route(env, chromosome):
    """Connect start, chromosome waypoints and goal with obstacle-avoiding BFS segments."""
    stops = [env.start] + chromosome.waypoints + [env.goal]
    route = [stops[0]]
    for a, b in zip(stops, stops[1:]):
        segment = shortest_free_segment(env, a, b)
        route.extend(segment[1:])
    return route

def evaluate(env, chromosome, cfg):
    route = expand_route(env, chromosome)
    unique_cells = set(route)
    free_route_cells = {p for p in unique_cells if not env.is_blocked(p)}
    covered_targets = len(env.targets.intersection(free_route_cells))
    coverage = len(free_route_cells) / max(1, env.size * env.size - len(env.obstacles))
    detection = covered_targets / max(1, len(env.targets))

    blocked_steps = sum(1 for p in route if env.is_blocked(p))
    risk_cells = sum(1 for p in route if p in env.hazards)
    distance = max(0, len(route) - 1)
    avg_speed = sum(chromosome.speeds) / max(1, len(chromosome.speeds))
    time_cost = distance / max(0.5, avg_speed)
    sensor_cost = sum(chromosome.sensors) * 0.7
    energy_cost = distance * (0.7 + 0.15 * avg_speed) + sensor_cost
    risk_ratio = risk_cells / max(1, len(route))

    # Hard constraint: maximum flight range (penalty grows with the excess distance).
    range_exceeded = max(0, distance - cfg.MAX_RANGE)
    range_excess = range_exceeded / cfg.MAX_RANGE

    fitness = (
        cfg.W_COVERAGE * coverage
        + cfg.W_DETECTION * detection
        - cfg.W_ENERGY * energy_cost
        - cfg.W_TIME * time_cost
        - cfg.W_RISK * risk_ratio
        - cfg.INVALID_PENALTY * (blocked_steps / max(1, len(route)))
        - cfg.RANGE_PENALTY * range_excess
    )
    metrics = {
        "fitness": fitness,
        "coverage": coverage,
        "target_detection": detection,
        "energy_cost": energy_cost,
        "time_cost": time_cost,
        "risk_ratio": risk_ratio,
        "blocked_steps": blocked_steps,
        "distance_steps": distance,
        "range_exceeded": range_exceeded,
    }
    return fitness, metrics, route
