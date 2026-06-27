"""
Experiment 04: Halo Orbit near L1.

Uses compute_halo_ic() + correct_halo_ic() from lagrange.py,
then integrates one period via engine.run_trajectory() for a 3D plot.
"""

import os
import sys
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../presets/lagrange'))

import engine
from lagrange import compute_halo_ic, correct_halo_ic

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    h = compute_halo_ic(Az_km=15000, point='L1')
    print(f"Richardson IC: x0={h['x0']:.6f} Tkm, z0={h['z0']:.6f} Tkm, "
          f"vy0={h['vy0']:.6f} km/s, T={h['T_hours']:.2f} h")

    hc = correct_halo_ic(
        x0_m=h['x0'] * 1e6,
        z0_m=h['z0'] * 1e6,
        vy0_ms=h['vy0'] * 1e3,
        T_guess_s=h['T_hours'] * 3600,
    )
    print(f"Corrected IC: x0={hc['x0']:.6f} Tkm, z0={hc['z0']:.6f} Tkm, "
          f"vy0={hc['vy0']:.6f} km/s, T={hc['T_hours']:.2f} h")
    print(f"  Converged in {hc['_iterations']} iterations (err={hc['_err']:.3e})")

    csv_path = os.path.join(OUT_DIR, 'halo_ic.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['parameter', 'value', 'unit'])
        w.writerow(['x0', f"{hc['x0']:.10f}", 'Tkm'])
        w.writerow(['z0', f"{hc['z0']:.10f}", 'Tkm'])
        w.writerow(['vy0', f"{hc['vy0']:.10f}", 'km/s'])
        w.writerow(['T', f"{hc['T_hours']:.4f}", 'hours'])
        w.writerow(['T', f"{hc['T_days']:.4f}", 'days'])
        w.writerow(['Az', '15000', 'km'])
        w.writerow(['Ax', f"{h['Ax_km']:.1f}", 'km'])
    print(f"Saved: {csv_path}")

    state0 = [hc['x0'] * 1e6, 0.0, hc['z0'] * 1e6, 0.0, hc['vy0'] * 1e3, 0.0]
    T_sec = hc['T_hours'] * 3600
    result = engine.run_trajectory(state0, T_sec, dt=30, integrator='verlet')

    pos = result['pos'] / 1e6
    J = result['jacobi']
    J_drift = np.max(np.abs(J - J[0]) / abs(J[0]))
    print(f"  Integration: {len(result['t'])} steps, max Jacobi drift={J_drift:.2e}")

    closure_km = np.sqrt(np.sum((result['pos'][-1] - result['pos'][0])**2)) / 1e3
    print(f"  Closure error: {closure_km:.1f} km")

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(pos[:, 0], pos[:, 1], pos[:, 2], 'b-', linewidth=0.8)
    ax.scatter([pos[0, 0]], [pos[0, 1]], [pos[0, 2]], c='green', s=50, label='Start')

    from lagrange import bisect
    L1_m = bisect(-engine.d_E + 1e3, engine.d_M - 1e3)
    ax.scatter([L1_m / 1e6], [0], [0], c='red', s=30, marker='^', label='L1')

    ax.set_xlabel('x (Tkm)')
    ax.set_ylabel('y (Tkm)')
    ax.set_zlabel('z (Tkm)')
    ax.set_title(f'Halo orbit near L1 (Az=15000 km, T={hc["T_hours"]:.1f} h)')
    ax.legend()

    png_path = os.path.join(OUT_DIR, 'halo_3d.png')
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {png_path}")


if __name__ == '__main__':
    main()
