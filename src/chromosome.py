from dataclasses import dataclass
import random

@dataclass
class Chromosome:
    # Each waypoint is an (x, y) grid coordinate.
    waypoints: list
    # Integer speed levels: 1=slow, 2=medium, 3=fast.
    speeds: list
    # Binary sensor profile: 1=on, 0=off at that waypoint.
    sensors: list

    def copy(self):
        return Chromosome(self.waypoints[:], self.speeds[:], self.sensors[:])

    @classmethod
    def random(cls, env, n_waypoints, rng=random):
        points = [(rng.randrange(env.size), rng.randrange(env.size)) for _ in range(n_waypoints)]
        points = [env.repair_point(p) for p in points]
        speeds = [rng.randint(1, 3) for _ in range(n_waypoints)]
        sensors = [rng.randint(0, 1) for _ in range(n_waypoints)]
        return cls(points, speeds, sensors)
