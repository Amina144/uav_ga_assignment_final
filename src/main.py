import json
from pathlib import Path
from . import config as cfg
from .environment import Environment
from .ga import GeneticAlgorithm
from .experiments import run_sensitivity, run_baseline_comparison
from .plots import (save_plots, save_evolution, save_sensitivity,
                    save_baseline_plot)


def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    env = Environment.demo(cfg.GRID_SIZE, cfg.RANDOM_SEED)

    # 1) Main GA run
    ga = GeneticAlgorithm(env, cfg)
    best, best_history, avg_history = ga.run()
    metrics, route = save_plots(env, best, best_history, avg_history, cfg, out)
    snapshots = save_evolution(env, ga, cfg, out)

    # 2) Hyperparameter sensitivity (several seeds per setting)
    sensitivity = run_sensitivity(env, cfg, cfg.EXPERIMENT_SEEDS)
    save_sensitivity(sensitivity, out)

    # 3) GA vs random-search baseline (same number of evaluations)
    baseline = run_baseline_comparison(env, cfg, cfg.EXPERIMENT_SEEDS)
    save_baseline_plot(env, cfg, ga, best_history, out, cfg.EXPERIMENT_SEEDS)

    result = {
        "grid_size": cfg.GRID_SIZE,
        "start": env.start,
        "goal": env.goal,
        "best_waypoints": best.waypoints,
        "speed_levels": best.speeds,
        "sensor_activation": best.sensors,
        "metrics": metrics,
        "run_info": {
            "max_generations": ga.generations,
            "generations_run": ga.generations_run,
            "stopped_early": ga.stopped_early,
            "evaluations": ga.evaluations,
            "max_range": cfg.MAX_RANGE,
            "snapshot_generations": snapshots,
        },
        "sensitivity_best_fitness": sensitivity,
        "baseline_comparison": baseline,
        "note": "Synthetic teaching simulation; not for real-world flight."
    }
    with open(out / "summary.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print("Simulation complete. Files saved in:", out)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
