# -*- coding: utf-8 -*-
"""Clean English chaos-fan figure for the deck (replaces media image18).

The deck uses a presentation variant of experiment 06 with no title and no
legend; only the slide's own heading carries the wording. No generator for it
survived, so this reproduces it from the experiment's own parameters.
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "experiments"))
sys.path.insert(0, os.path.join(ROOT, "presets", "lagrange"))

import engine
from lagrange import bisect

OUT = os.path.join(HERE, "figures_en")

T_DAYS, DT, N_PERT, DV = 30, 30.0, 16, 10.0


def main():
    os.makedirs(OUT, exist_ok=True)
    t_sec = T_DAYS * 86400
    l1 = bisect(-engine.d_E + 1e3, engine.d_M - 1e3)
    angles = np.linspace(0, 2 * np.pi, N_PERT, endpoint=False)
    colours = plt.cm.hsv(np.linspace(0, 1, N_PERT, endpoint=False))

    fig, ax = plt.subplots(figsize=(9.5, 6.36))
    for i, angle in enumerate(angles):
        state = [l1, 0.0, 0.0, DV * np.cos(angle), DV * np.sin(angle), 0.0]
        res = engine.run_trajectory(state, t_sec, DT, integrator="verlet")
        pos = res["pos"] / 1e6
        ax.plot(pos[:, 0], pos[:, 1], "-", color=colours[i], linewidth=0.8, alpha=0.85)
        ax.plot(pos[-1, 0], pos[-1, 1], "o", color=colours[i], markersize=4)
        print(f"  trajectory {i+1}/{N_PERT}", flush=True)

    ax.plot(l1 / 1e6, 0, "k^", markersize=11, zorder=20)
    ax.annotate("L1", (l1 / 1e6, 0), fontsize=9, ha="right", va="top",
                xytext=(-10, -8), textcoords="offset points", color="#444444")
    ax.plot(-engine.d_E / 1e6, 0, "o", color="#2196F3", markersize=10, zorder=20)
    ax.annotate("Earth", (-engine.d_E / 1e6, 0), fontsize=9, ha="center",
                va="bottom", xytext=(0, 9), textcoords="offset points",
                color="#2196F3")
    ax.plot(engine.d_M / 1e6, 0, "o", color="gray", markersize=8, zorder=20)
    ax.annotate("Moon", (engine.d_M / 1e6, 0), fontsize=9, ha="center",
                va="bottom", xytext=(0, 16), textcoords="offset points",
                color="gray")

    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")
    path = os.path.join(OUT, "image18.png")
    fig.savefig(path, dpi=300, bbox_inches="tight", transparent=True)
    print(f"written: {path}")


if __name__ == "__main__":
    main()
