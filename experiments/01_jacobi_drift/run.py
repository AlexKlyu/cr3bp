"""
Experiment 01: Jacobi Integral Drift.

6 integrator configurations (Euler / Verlet half-step / Verlet iterated)
x (fixed / adaptive) x 3 scenarios (halo orbit, free return, chaos near L1).

For each scenario — two side-by-side plots (fixed step and adaptive step)
with a shared Y axis for easy comparison.
"""

import os
import sys
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../presets/lagrange'))

import engine
from lagrange import compute_halo_ic, correct_halo_ic, bisect

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_halo_ic():
    h = compute_halo_ic(Az_km=15000, point='L1')
    hc = correct_halo_ic(
        x0_m=h['x0'] * 1e6,
        z0_m=h['z0'] * 1e6,
        vy0_ms=h['vy0'] * 1e3,
        T_guess_s=h['T_hours'] * 3600,
    )
    x0 = hc['x0'] * 1e6
    z0 = hc['z0'] * 1e6
    vy0 = hc['vy0'] * 1e3
    T_h = hc['T_hours']
    return [x0, 0.0, z0, 0.0, vy0, 0.0], T_h * 3600

def get_free_return_ic():
    x0 = -9.3305877540e6
    y0 = -4.9117576067e6
    vx0 = 7.8194239058e3
    vy0 = -7.4195663175e3
    T_h = 200.0
    return [x0, y0, 0.0, vx0, vy0, 0.0], T_h * 3600

def get_chaos_ic():
    L1_m = bisect(-engine.d_E + 1e3, engine.d_M - 1e3)
    vy0 = 100.0
    T_h = 336.0
    return [L1_m, 0.0, 0.0, 0.0, vy0, 0.0], T_h * 3600

SCENARIOS = {
    'halo': ('Halo Orbit L1', get_halo_ic),
    'freereturn': ('Free Return', get_free_return_ic),
    'chaos': ('Chaos near L1', get_chaos_ic),
}

CONFIGS = [
    ('Euler fixed',          'euler',       False),
    ('Euler adaptive',       'euler',       True),
    ('Verlet half-step fixed',  'verlet_half', False),
    ('Verlet half-step adaptive', 'verlet_half', True),
    ('Verlet iterated fixed',   'verlet',      False),
    ('Verlet iterated adaptive', 'verlet',      True),
]

DT = 30.0


def jacobi_drift_series(state0, T, integrator, adaptive):
    """Integrate trajectory, return (times, relative drift array)."""
    result = engine.run_trajectory(state0, T, DT, integrator=integrator,
                                   adaptive=adaptive, dt_min=1.0)
    J = result['jacobi']
    if len(J) == 0:
        return np.array([]), np.array([])
    J0 = J[0]
    drift = np.abs(J - J0) / abs(J0)
    return result['t'], drift


def main():
    rows = []
    fig_data = {}

    for sc_key, (sc_name, ic_fn) in SCENARIOS.items():
        print(f"Scenario: {sc_name}")
        state0, T = ic_fn()
        fig_data[sc_key] = []

        for cfg_name, integ, adap in CONFIGS:
            print(f"  Config: {cfg_name} ...", end=' ', flush=True)
            times, drift = jacobi_drift_series(list(state0), T, integ, adap)
            if len(drift) == 0:
                max_drift = float('nan')
                rms_drift = float('nan')
            else:
                max_drift = float(np.max(drift))
                rms_drift = float(np.sqrt(np.mean(drift**2)))
            print(f"max={max_drift:.2e}, rms={rms_drift:.2e}")
            rows.append({
                'scenario': sc_name,
                'config': cfg_name,
                'max_drift': max_drift,
                'rms_drift': rms_drift,
                'steps': len(times),
            })
            fig_data[sc_key].append((cfg_name, integ, adap, times, drift))

    csv_path = os.path.join(OUT_DIR, 'drift_table.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['scenario', 'config', 'max_drift', 'rms_drift', 'steps'])
        w.writeheader()
        w.writerows(rows)
    print(f"\nSaved: {csv_path}")

    colors = {
        'euler': '#e74c3c',
        'verlet_half': '#f39c12',
        'verlet': '#2ecc71',
    }
    labels = {
        'euler': 'Euler',
        'verlet_half': 'Verlet half-step',
        'verlet': 'Verlet iterated',
    }

    for sc_key, (sc_name, _) in SCENARIOS.items():
        fig, (ax_fix, ax_adp) = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

        for cfg_name, integ, adap, times, drift in fig_data[sc_key]:
            if len(times) == 0:
                continue
            ax = ax_adp if adap else ax_fix
            ax.semilogy(times / 3600, drift + 1e-20,
                        label=labels[integ], color=colors[integ], linewidth=0.9)

        ax_fix.set_xlabel('Time (hours)')
        ax_fix.set_ylabel('Relative Jacobi drift |e(t)|')
        ax_fix.set_title(f'{sc_name}: fixed step (dt={DT:.0f} s)')
        ax_fix.legend(fontsize=9)
        ax_fix.grid(True, alpha=0.3)

        ax_adp.set_xlabel('Time (hours)')
        ax_adp.set_title(f'{sc_name}: adaptive step (dt=1..{DT:.0f} s)')
        ax_adp.legend(fontsize=9)
        ax_adp.grid(True, alpha=0.3)

        fig.tight_layout()
        png_path = os.path.join(OUT_DIR, f'drift_{sc_key}.png')
        fig.savefig(png_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"Saved: {png_path}")


if __name__ == '__main__':
    main()
