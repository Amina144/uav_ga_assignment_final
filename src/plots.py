from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from .fitness import evaluate
from .baseline import random_search


def _grid(env):
    grid = np.zeros((env.size, env.size))
    for x, y in env.obstacles: grid[y, x] = 1
    for x, y in env.hazards: grid[y, x] = 2
    for x, y in env.targets: grid[y, x] = 3
    return grid


def _draw_route(ax, env, route, title):
    ax.imshow(_grid(env), origin="lower", interpolation="nearest")
    rx, ry = zip(*route)
    ax.plot(rx, ry, marker=".", linewidth=1.3, color="white")
    ax.scatter([env.start[0]], [env.start[1]], marker="s", s=60, color="red", zorder=3)
    ax.scatter([env.goal[0]], [env.goal[1]], marker="*", s=120, color="gold", zorder=3)
    ax.set_xlim(-0.5, env.size - 0.5); ax.set_ylim(-0.5, env.size - 0.5)
    ax.set_title(title, fontsize=9)


def _visits(env, route):
    visits = np.zeros((env.size, env.size))
    for x, y in route:
        if 0 <= x < env.size and 0 <= y < env.size:
            visits[y, x] += 1
    return visits


def save_plots(env, best, best_history, avg_history, cfg, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    _, metrics, route = evaluate(env, best, cfg)

    plt.figure(figsize=(8, 4.5))
    plt.plot(best_history, label="Best fitness")
    plt.plot(avg_history, label="Average fitness")
    plt.xlabel("Generation")
    plt.ylabel("Fitness (higher is better)")
    plt.title("GA Fitness Convergence")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "fitness_convergence.png", dpi=160)
    plt.close()

    plt.figure(figsize=(7, 7))
    ax = plt.gca()
    ax.imshow(_grid(env), origin="lower", interpolation="nearest")
    rx, ry = zip(*route)
    ax.plot(rx, ry, marker=".", linewidth=1.5, label="Best UAV route")
    ax.scatter([env.start[0]], [env.start[1]], marker="s", s=70, label="Start")
    ax.scatter([env.goal[0]], [env.goal[1]], marker="*", s=120, label="Goal")
    ax.set_xlim(-0.5, env.size - 0.5); ax.set_ylim(-0.5, env.size - 0.5)
    ax.set_xlabel("X coordinate"); ax.set_ylabel("Y coordinate")
    ax.set_title("Evolved UAV Route (1=obstacle, 2=hazard, 3=target)")
    ax.legend(loc="upper left", fontsize=8)
    plt.tight_layout()
    plt.savefig(out / "best_route.png", dpi=160)
    plt.close()

    plt.figure(figsize=(7, 6))
    plt.imshow(_visits(env, route), origin="lower", interpolation="nearest")
    plt.colorbar(label="Number of route visits")
    plt.xlabel("X coordinate"); plt.ylabel("Y coordinate")
    plt.title("Route Coverage Heatmap")
    plt.tight_layout()
    plt.savefig(out / "coverage_heatmap.png", dpi=160)
    plt.close()
    return metrics, route


def save_evolution(env, ga, cfg, out_dir):
    """Flight paths and coverage heatmaps of the best individual at 3 stages of evolution."""
    out = Path(out_dir)
    n = len(ga.best_per_gen)
    picks = sorted({0, n // 2, n - 1})
    fig_r, axes_r = plt.subplots(1, len(picks), figsize=(4.6 * len(picks), 4.8))
    fig_h, axes_h = plt.subplots(1, len(picks), figsize=(4.6 * len(picks), 4.4))
    axes_r = np.atleast_1d(axes_r); axes_h = np.atleast_1d(axes_h)
    for k, g in enumerate(picks):
        fit, m, route = evaluate(env, ga.best_per_gen[g], cfg)
        _draw_route(axes_r[k], env, route, f"Generation {g + 1}  (fitness {fit:.2f})")
        im = axes_h[k].imshow(_visits(env, route), origin="lower", interpolation="nearest")
        axes_h[k].set_title(f"Generation {g + 1}  (coverage {m['coverage'] * 100:.1f}%)", fontsize=9)
    fig_h.colorbar(im, ax=list(axes_h), label="Route visits", shrink=0.85)
    fig_r.tight_layout(); fig_r.savefig(out / "evolution_paths.png", dpi=150); plt.close(fig_r)
    fig_h.savefig(out / "evolution_heatmaps.png", dpi=150, bbox_inches="tight"); plt.close(fig_h)
    return [g + 1 for g in picks]


def save_sensitivity(sens, out_dir):
    """Grouped bar chart (mean +/- std over seeds) for the three hyperparameters."""
    out = Path(out_dir)
    groups = []
    for label, e in sens.items():
        if e["group"] not in groups:
            groups.append(e["group"])
    fig, axes = plt.subplots(1, len(groups), figsize=(4.4 * len(groups), 4.2), sharey=True)
    for ax, g in zip(np.atleast_1d(axes), groups):
        items = [(l, e) for l, e in sens.items() if e["group"] == g]
        ax.bar([l.replace(" (default)", "*") for l, _ in items],
               [e["mean"] for _, e in items],
               yerr=[e["std"] for _, e in items], capsize=4)
        ax.set_title(g, fontsize=10)
        ax.tick_params(axis="x", rotation=15, labelsize=8)
    np.atleast_1d(axes)[0].set_ylabel("Best fitness (mean ± std)")
    fig.suptitle("Hyperparameter sensitivity (* = default, 5 seeds each)", fontsize=10)
    fig.tight_layout()
    fig.savefig(out / "hyperparameter_sensitivity.png", dpi=150)
    plt.close(fig)


def save_baseline_plot(env, cfg, ga, best_history, out_dir, seeds):
    """Best-so-far fitness vs number of evaluations: GA against random search."""
    out = Path(out_dir)
    budget = ga.evaluations
    ga_curve = np.repeat(best_history, ga.population_size)[:budget]
    rs = np.array([random_search(env, cfg, budget, seed=1000 + s)[2] for s in seeds])
    x = np.arange(1, budget + 1)
    plt.figure(figsize=(8, 4.5))
    plt.plot(x[:len(ga_curve)], ga_curve, label="Genetic Algorithm", linewidth=2)
    plt.plot(x, rs.mean(axis=0), label=f"Random search (mean of {len(seeds)} seeds)", linewidth=2)
    plt.fill_between(x, rs.min(axis=0), rs.max(axis=0), alpha=0.25, label="Random search (min-max)")
    plt.xlabel("Fitness evaluations")
    plt.ylabel("Best fitness so far")
    plt.title("GA vs Random Search (same evaluation budget)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "ga_vs_random_search.png", dpi=160)
    plt.close()
