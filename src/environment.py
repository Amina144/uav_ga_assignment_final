from dataclasses import dataclass
import random

@dataclass
class Environment:
    size: int
    start: tuple
    goal: tuple
    obstacles: set
    hazards: set
    targets: set

    @classmethod
    def demo(cls, size=20, seed=17):
        rng = random.Random(seed)
        start, goal = (1, 1), (size - 2, size - 2)
        obstacles, hazards, targets = set(), set(), set()

        # Create reproducible blocked cells, avoiding start/goal.
        while len(obstacles) < int(size * size * 0.10):
            p = (rng.randrange(size), rng.randrange(size))
            if p not in (start, goal):
                obstacles.add(p)

        while len(hazards) < int(size * size * 0.08):
            p = (rng.randrange(size), rng.randrange(size))
            if p not in obstacles and p not in (start, goal):
                hazards.add(p)

        while len(targets) < max(8, int(size * size * 0.04)):
            p = (rng.randrange(size), rng.randrange(size))
            if p not in obstacles and p not in hazards and p not in (start, goal):
                targets.add(p)

        return cls(size, start, goal, obstacles, hazards, targets)

    def is_blocked(self, point):
        x, y = point
        return not (0 <= x < self.size and 0 <= y < self.size) or point in self.obstacles

    def repair_point(self, point):
        """Clamp a point to the grid and move it to the nearest free cell if blocked."""
        x, y = point
        x = max(0, min(self.size - 1, int(round(x))))
        y = max(0, min(self.size - 1, int(round(y))))
        candidate = (x, y)
        if not self.is_blocked(candidate):
            return candidate
        for radius in range(1, self.size):
            options = []
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if max(abs(dx), abs(dy)) == radius:
                        q = (x + dx, y + dy)
                        if not self.is_blocked(q):
                            options.append(q)
            if options:
                return min(options, key=lambda q: abs(q[0]-x) + abs(q[1]-y))
        return self.start
