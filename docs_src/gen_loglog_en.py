# -*- coding: utf-8 -*-
"""English log-log convergence chart for the deck (replaces media image9).

The deck's chart shows six series - Euler, explicit Verlet, and iterated Verlet
with 1..4 velocity-correction iterations - which is a superset of what
experiments/02_integrator_comparison/run.py plots. It reuses that experiment's
helpers so the numbers are computed the same way.
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(os.path.dirname(HERE), "experiments", "02_integrator_comparison")
sys.path.insert(0, EXP)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "experiments"))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "presets", "lagrange"))

import engine
import run as exp02

OUT = os.path.join(HERE, "figures_en")


def fit(log_x, log_y):
    coeffs, cov = np.polyfit(log_x, log_y, 1, cov=True)
    slope = coeffs[0]
    se = np.sqrt(cov[0, 0])
    from scipy.stats import t as t_dist
    ci = t_dist.ppf(0.975, df=len(log_x) - 2) * se
    pred = np.polyval(coeffs, log_x)
    ss_res = np.sum((log_y - pred) ** 2)
    ss_tot = np.sum((log_y - np.mean(log_y)) ** 2)
    return slope, ci, 1 - ss_res / ss_tot


def main():
    os.makedirs(OUT, exist_ok=True)
    state0 = exp02.get_halo_state()
    ref = exp02.compute_reference(state0)
    dt_values = np.logspace(0, np.log10(300), 20)

    series = [
        ("Euler", engine.step_euler, "#d62728", "x"),
        ("Explicit Verlet", engine.step_verlet, "#ff9900", "o"),
    ]
    for n in (1, 2, 3, 4):
        series.append((
            f"Verlet iterated {n}",
            (lambda n_: (lambda s, dt: engine.step_verlet_iterated(s, dt, n_iter=n_)))(n),
            ["#e07b39", "#9467bd", "#2ca02c", "#1f77b4"][n - 1],
            ["v", "D", "s", "^"][n - 1],
        ))

    fig, ax = plt.subplots(figsize=(7.79, 5.48))
    for label, step_fn, colour, marker in series:
        errs = []
        for dt in dt_values:
            errs.append(exp02.max_position_error(state0, dt, step_fn, ref))
            print(f"  {label} dt={dt:.1f}: {errs[-1]:.3e} m", flush=True)
        errs = np.array(errs)
        m = np.isfinite(errs) & (errs > 0)
        slope, ci, r2 = fit(np.log10(dt_values[m]), np.log10(errs[m]))
        ax.loglog(dt_values, errs, marker=marker, color=colour, markersize=4,
                  linewidth=1.2,
                  label=f"{label} (slope={slope:.2f}±{ci:.2f}, R²={r2:.3f})")

    ax.set_xlabel("Step dt (s)")
    ax.set_ylabel("Max. position error (m)")
    ax.set_title("Integrator convergence: Euler, explicit Verlet, iterated Verlet (1-4)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=7, loc="lower right")
    path = os.path.join(OUT, "image9.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"written: {path}")


if __name__ == "__main__":
    main()
