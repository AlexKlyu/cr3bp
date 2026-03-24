"""thrust_pres.png: top panel of thrust_comparison.png, no title, no top/right spines."""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import engine

OUT = os.path.dirname(os.path.abspath(__file__))

x0_tkm = -9.3305877540
y0_tkm = -4.9117576067
vx0_kms = 7.7654698808
vy0_kms = -7.3683713099
Fx = 5.0
mass = 500.0
tOn_s = 0
tDur_s = 10800
tOff_s = tOn_s + tDur_s
tEnd_h = 72

x0_m = x0_tkm * 1e6
y0_m = y0_tkm * 1e6
vx0_ms = vx0_kms * 1e3
vy0_ms = vy0_kms * 1e3
T_sec = tEnd_h * 3600

def thrust_fn(t):
    if tOn_s <= t < tOff_s:
        return (Fx / mass, 0.0, 0.0)
    return (0.0, 0.0, 0.0)

state0 = [x0_m, y0_m, 0.0, vx0_ms, vy0_ms, 0.0]
r_thrust = engine.run_trajectory(list(state0), T_sec, dt=30, integrator='verlet', thrust=thrust_fn)
r_no = engine.run_trajectory(list(state0), T_sec, dt=30, integrator='verlet')

pos_t = r_thrust['pos'] / 1e6
pos_n = r_no['pos'] / 1e6

fig, ax = plt.subplots(figsize=(10, 8))

ax.plot(pos_n[:, 0], pos_n[:, 1], 'b--', linewidth=0.6, alpha=0.7, label='Без тяги')
ax.plot(pos_t[:, 0], pos_t[:, 1], 'r-', linewidth=0.8, label='С тягой')
ax.plot(pos_t[0, 0], pos_t[0, 1], 'go', markersize=6)

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
ax.legend()
ax.set_aspect(3.4)
ax.grid(True, alpha=0.3)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

png_path = os.path.join(OUT, 'thrust_pres.png')
fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close(fig)
print(f"Saved: {png_path}")
