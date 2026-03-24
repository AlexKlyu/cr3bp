"""Generate clean halo 3D plot: no title, no legend, keep grid+axes. High res."""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../presets/lagrange'))

import engine
from lagrange import compute_halo_ic, correct_halo_ic, bisect

OUT = os.path.dirname(os.path.abspath(__file__))

h = compute_halo_ic(Az_km=15000, point='L1')
hc = correct_halo_ic(
    x0_m=h['x0'] * 1e6, z0_m=h['z0'] * 1e6,
    vy0_ms=h['vy0'] * 1e3, T_guess_s=h['T_hours'] * 3600,
)

state0 = [hc['x0'] * 1e6, 0.0, hc['z0'] * 1e6, 0.0, hc['vy0'] * 1e3, 0.0]
result = engine.run_trajectory(state0, hc['T_hours'] * 3600, dt=30, integrator='verlet')
pos = result['pos'] / 1e6

L1_m = bisect(-engine.d_E + 1e3, engine.d_M - 1e3)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(pos[:, 0], pos[:, 1], pos[:, 2], 'b-', linewidth=0.8)
ax.scatter([pos[0, 0]], [pos[0, 1]], [pos[0, 2]], c='green', s=50)
ax.scatter([L1_m / 1e6], [0], [0], c='red', s=30, marker='^')

ax.set_xlabel('x (тыс. км)')
ax.set_ylabel('y (тыс. км)')
ax.set_zlabel('z (тыс. км)')

png_path = os.path.join(OUT, 'halo_pres.png')
fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close(fig)
print(f"Saved: {png_path}")
