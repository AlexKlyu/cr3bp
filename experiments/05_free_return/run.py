"""
Experiment 05: Free Return Trajectory (Apollo-13 style).

Uses known optimal initial conditions found by
presets/free_return/find_free_return.py (Nelder-Mead: angle~226.5°, v~10.78 km/s).
Integration via engine.run_trajectory() for plotting.

Optimality criterion:
  A trajectory is considered 'optimal' if it minimizes the Earth return
  distance (closest approach after lunar flyby) subject to the condition
  that a lunar flyby occurred (distance < ~70,000 km).
  This ensures safe ballistic Earth return without additional corrections —
  the key requirement of a free return trajectory.

Sensitivity analysis:
  After the main trajectory, a parametric sweep of v_TLI ± 50 m/s
  (5 values) is performed. For each run the following are recorded:
  minimum Moon distance, Earth return distance, Jacobi integral (energy check).
  Results are saved to sensitivity.csv and visualized in sensitivity.png.
"""

import os
import sys
import csv
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import engine

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')

ANGLE_DEG = 226.50
V_TLI_KMS = 10.7793

R_E = engine.R_E
LEO_ALT = 400e3
r_LEO = R_E + LEO_ALT

angle_rad = math.radians(ANGLE_DEG)
X0_M = -engine.d_E + r_LEO * math.cos(angle_rad)
Y0_M = r_LEO * math.sin(angle_rad)
VX0_MS = -V_TLI_KMS * 1e3 * math.sin(angle_rad)
VY0_MS = V_TLI_KMS * 1e3 * math.cos(angle_rad)

T_HOURS = 180.0

SENSITIVITY_DV = [-50, -25, 0, +25, +50]


def _compute_ic(v_tli_kms):
    """Initial conditions for a given v_TLI (km/s) at a fixed angle."""
    v_ms = v_tli_kms * 1e3
    x0 = -engine.d_E + r_LEO * math.cos(angle_rad)
    y0 = r_LEO * math.sin(angle_rad)
    vx0 = -v_ms * math.sin(angle_rad)
    vy0 = v_ms * math.cos(angle_rad)
    return [x0, y0, 0.0, vx0, vy0, 0.0]


def _analyze_trajectory(result):
    """
    Extract lunar flyby and Earth return from integration result.
    Returns (moon_flyby_km, earth_return_km, jacobi_mean).
    """
    pos = result['pos']
    r_moon = np.sqrt((pos[:, 0] - engine.d_M)**2 + pos[:, 1]**2 + pos[:, 2]**2)
    r_earth = np.sqrt((pos[:, 0] + engine.d_E)**2 + pos[:, 1]**2 + pos[:, 2]**2)

    i_flyby = np.argmin(r_moon)
    moon_flyby_km = r_moon[i_flyby] / 1e3

    if i_flyby + 10 < len(r_earth):
        r_earth_post = r_earth[i_flyby:]
        i_return_rel = np.argmin(r_earth_post)
        earth_return_km = r_earth_post[i_return_rel] / 1e3
    else:
        earth_return_km = float('nan')

    jacobi_mean = float(np.mean(result['jacobi']))

    return moon_flyby_km, earth_return_km, jacobi_mean


def run_sensitivity():
    """
    Parametric sweep: v_TLI ± 50 m/s.
    Returns a list of result dicts.
    """
    rows = []
    for dv in SENSITIVITY_DV:
        v_tli = V_TLI_KMS + dv / 1e3
        state0 = _compute_ic(v_tli)
        result = engine.run_trajectory(state0, T_HOURS * 3600, dt=30, integrator='verlet')
        moon_km, earth_km, jacobi = _analyze_trajectory(result)
        rows.append({
            'dv_ms': dv,
            'v_tli_ms': v_tli * 1e3,
            'moon_flyby_km': moon_km,
            'earth_return_km': earth_km,
            'jacobi': jacobi,
        })
        print(f"  Δv={dv:+.0f} m/s → v_TLI={v_tli:.4f} km/s: "
              f"r_Moon={moon_km:.0f} km, r_Earth={earth_km:.0f} km, "
              f"C_J={jacobi:.6e}")
    return rows


def save_sensitivity_csv(rows):
    """Save sensitivity results to CSV."""
    csv_path = os.path.join(OUT_DIR, 'sensitivity.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['dv_ms', 'v_tli_ms', 'moon_flyby_km', 'earth_return_km', 'jacobi'])
        for r in rows:
            w.writerow([
                f"{r['dv_ms']:.0f}",
                f"{r['v_tli_ms']:.3f}",
                f"{r['moon_flyby_km']:.1f}",
                f"{r['earth_return_km']:.1f}",
                f"{r['jacobi']:.6e}",
            ])
    print(f"Saved: {csv_path}")
    return csv_path


def plot_sensitivity(rows):
    """
    Sensitivity plot: two subplots —
    lunar flyby distance and Earth return distance vs Δv.
    """
    dvs = [r['dv_ms'] for r in rows]
    moon_kms = [r['moon_flyby_km'] for r in rows]
    earth_kms = [r['earth_return_km'] for r in rows]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)

    ax1.plot(dvs, moon_kms, 'o-', color='#FF6F00', linewidth=1.5, markersize=6)
    ax1.set_ylabel('Min distance to Moon (km)')
    ax1.set_title('Free return sensitivity to v_TLI')
    ax1.grid(True, alpha=0.3)
    ax1.axvline(0, color='gray', linestyle='--', alpha=0.5, label='Optimum')
    ax1.legend()

    ax2.plot(dvs, earth_kms, 's-', color='#1976D2', linewidth=1.5, markersize=6)
    ax2.set_xlabel('Δv_TLI (m/s)')
    ax2.set_ylabel('Earth return distance (km)')
    ax2.grid(True, alpha=0.3)
    ax2.axvline(0, color='gray', linestyle='--', alpha=0.5)

    fig.tight_layout()
    png_path = os.path.join(OUT_DIR, 'sensitivity.png')
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {png_path}")
    return png_path


def print_sensitivity_gradient(rows):
    """
    Estimate sensitivity gradient via finite differences
    around the optimal value (Δv=0).
    """
    by_dv = {r['dv_ms']: r for r in rows}
    if -25 in by_dv and +25 in by_dv:
        dr_moon = by_dv[+25]['moon_flyby_km'] - by_dv[-25]['moon_flyby_km']
        dr_earth = by_dv[+25]['earth_return_km'] - by_dv[-25]['earth_return_km']
        grad_moon = dr_moon / 50.0
        grad_earth = dr_earth / 50.0
        print(f"\n  Sensitivity: +1 m/s → Δr_Moon ≈ {grad_moon:.1f} km")
        print(f"  Sensitivity: +1 m/s → Δr_Earth ≈ {grad_earth:.1f} km")
    else:
        print("  Could not compute gradient (no ±25 m/s points)")


def main():
    print(f"Free return IC: angle={ANGLE_DEG}°, v={V_TLI_KMS} km/s")
    print(f"  x0  = {X0_M/1e6:.10f} Tkm")
    print(f"  y0  = {Y0_M/1e6:.10f} Tkm")
    print(f"  vx0 = {VX0_MS/1e3:.10f} km/s")
    print(f"  vy0 = {VY0_MS/1e3:.10f} km/s")

    state0 = [X0_M, Y0_M, 0.0, VX0_MS, VY0_MS, 0.0]
    result = engine.run_trajectory(state0, T_HOURS * 3600, dt=30, integrator='verlet')

    pos = result['pos']
    pos_tkm = pos / 1e6

    r_moon = np.sqrt((pos[:, 0] - engine.d_M)**2 + pos[:, 1]**2 + pos[:, 2]**2)
    r_earth = np.sqrt((pos[:, 0] + engine.d_E)**2 + pos[:, 1]**2 + pos[:, 2]**2)

    i_flyby = np.argmin(r_moon)
    min_moon_km = r_moon[i_flyby] / 1e3
    t_flyby_h = result['t'][i_flyby] / 3600
    print(f"\n  Lunar flyby: {min_moon_km:.0f} km at t={t_flyby_h:.1f} h")

    if i_flyby + 10 < len(r_earth):
        r_earth_post = r_earth[i_flyby:]
        i_return_rel = np.argmin(r_earth_post)
        i_return = i_flyby + i_return_rel
        min_earth_km = r_earth[i_return] / 1e3
        t_return_h = result['t'][i_return] / 3600
        print(f"  Earth return: {min_earth_km:.0f} km at t={t_return_h:.1f} h")
    else:
        min_earth_km = float('nan')
        t_return_h = float('nan')
        print("  Earth return: not detected")

    csv_path = os.path.join(OUT_DIR, 'free_return_ic.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['parameter', 'value', 'unit'])
        w.writerow(['angle', f'{ANGLE_DEG:.2f}', 'deg'])
        w.writerow(['v_TLI', f'{V_TLI_KMS:.4f}', 'km/s'])
        w.writerow(['x0', f'{X0_M / 1e6:.10f}', 'Tkm'])
        w.writerow(['y0', f'{Y0_M / 1e6:.10f}', 'Tkm'])
        w.writerow(['vx0', f'{VX0_MS / 1e3:.10f}', 'km/s'])
        w.writerow(['vy0', f'{VY0_MS / 1e3:.10f}', 'km/s'])
        w.writerow(['min_dist_moon_km', f'{min_moon_km:.0f}', 'km'])
        w.writerow(['t_flyby', f'{t_flyby_h:.1f}', 'hours'])
        w.writerow(['min_dist_earth_km', f'{min_earth_km:.0f}', 'km'])
        w.writerow(['t_return', f'{t_return_h:.1f}', 'hours'])
    print(f"Saved: {csv_path}")

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.plot(pos_tkm[:, 0], pos_tkm[:, 1], 'b-', linewidth=0.8, label='Trajectory')

    ax.plot(pos_tkm[0, 0], pos_tkm[0, 1], 'go', markersize=8, label='Start', zorder=10)
    ax.plot(pos_tkm[i_flyby, 0], pos_tkm[i_flyby, 1], 'r*', markersize=12,
            label=f'Lunar flyby ({min_moon_km:.0f} km)', zorder=10)
    if not math.isnan(t_return_h):
        ax.plot(pos_tkm[i_return, 0], pos_tkm[i_return, 1], 'ms', markersize=8,
                label=f'Earth return ({min_earth_km:.0f} km)', zorder=10)

    earth_x = -engine.d_E / 1e6
    ax.plot(earth_x, 0, 'o', color='#2196F3', markersize=10, zorder=5)
    ax.annotate('Earth', (earth_x, 4), fontsize=9, ha='center', color='#2196F3')

    moon_x = engine.d_M / 1e6
    ax.plot(moon_x, 0, 'o', color='gray', markersize=6, zorder=5)
    ax.annotate('Moon', (moon_x, 4), fontsize=9, ha='center', color='gray')

    ax.set_xlabel('x (Tkm)')
    ax.set_ylabel('y (Tkm)')
    ax.set_title(f'Free return (v={V_TLI_KMS:.2f} km/s, '
                 f'angle={ANGLE_DEG:.1f}°, T={t_return_h:.0f} h)')
    ax.legend(loc='lower left')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    png_path = os.path.join(OUT_DIR, 'free_return_trajectory.png')
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {png_path}")

    print(f"\n{'='*60}")
    print("Sensitivity analysis: v_TLI ± 50 m/s")
    print(f"{'='*60}")
    sens_rows = run_sensitivity()
    save_sensitivity_csv(sens_rows)
    plot_sensitivity(sens_rows)
    print_sensitivity_gradient(sens_rows)


if __name__ == '__main__':
    main()
