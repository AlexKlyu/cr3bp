"""free_return_pres.png: same as free_return_trajectory.png but no title, no top/right spines."""
import os, sys, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import engine

OUT = os.path.dirname(os.path.abspath(__file__))

ANGLE_DEG = 226.50
V_TLI_KMS = 10.7793
r_LEO = engine.R_E + 400e3
angle_rad = math.radians(ANGLE_DEG)

X0_M = -engine.d_E + r_LEO * math.cos(angle_rad)
Y0_M = r_LEO * math.sin(angle_rad)
VX0_MS = -V_TLI_KMS * 1e3 * math.sin(angle_rad)
VY0_MS = V_TLI_KMS * 1e3 * math.cos(angle_rad)

state0 = [X0_M, Y0_M, 0.0, VX0_MS, VY0_MS, 0.0]
result = engine.run_trajectory(state0, 180.0 * 3600, dt=30, integrator='verlet')
pos = result['pos']

r_moon = np.sqrt((pos[:, 0] - engine.d_M)**2 + pos[:, 1]**2 + pos[:, 2]**2)
r_earth = np.sqrt((pos[:, 0] + engine.d_E)**2 + pos[:, 1]**2 + pos[:, 2]**2)
i_flyby = np.argmin(r_moon)
i_return = i_flyby + np.argmin(r_earth[i_flyby:])
min_moon_km = r_moon[i_flyby] / 1e3
min_earth_km = r_earth[i_return] / 1e3

pos_tkm = pos[:i_return + 1] / 1e6

fig, ax = plt.subplots(figsize=(10, 8))

ax.plot(pos_tkm[:, 0], pos_tkm[:, 1], 'b-', linewidth=0.8, label='Траектория')

ax.plot(pos_tkm[0, 0], pos_tkm[0, 1], 'go', markersize=8, label='Старт', zorder=10)
ax.plot(pos_tkm[i_flyby, 0], pos_tkm[i_flyby, 1], 'r*', markersize=12,
        label=f'Пролёт Луны ({min_moon_km:.0f} км)', zorder=10)
ax.plot(pos_tkm[-1, 0], pos_tkm[-1, 1], 'ms', markersize=8,
        label=f'Возврат к Земле ({min_earth_km:.0f} км)', zorder=10)

earth_x = -engine.d_E / 1e6
ax.plot(earth_x, 0, 'o', color='#2196F3', markersize=10, zorder=5)
ax.annotate('Земля', (earth_x, 0), fontsize=9, ha='left', va='bottom',
            xytext=(12, 6), textcoords='offset points', color='#2196F3')

moon_x = engine.d_M / 1e6
ax.plot(moon_x, 0, 'o', color='gray', markersize=6, zorder=5)
ax.annotate('Луна', (moon_x, 0), fontsize=9, ha='right', va='bottom',
            xytext=(-12, 6), textcoords='offset points', color='gray')

ax.set_xlabel('x (тыс. км)')
ax.set_ylabel('y (тыс. км)')
ax.legend(loc='lower left')
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig.savefig(os.path.join(OUT, 'free_return_pres.png'), dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close(fig)
print(f"Saved: {OUT}/free_return_pres.png")
