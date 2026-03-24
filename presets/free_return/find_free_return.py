"""
Find a free-return trajectory (Apollo-13 style) in the Earth-Moon CR3BP.

Method:
  1. Scan launch angles from LEO at near-escape velocity
  2. Nelder-Mead optimization on (angle, velocity)

Output: simulator-ready ICs (thousand km, km/s).
"""

import sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from scipy.signal import argrelmin

G = 6.674e-11
M_E = 5.972e24
M_M = 7.342e22
d_E = 4.67e6
d_M = 3.828e8
w = 2.662e-6
R_E = 6.371e6
R_M = 1.737e6

LEO_ALT = 400e3
r_LEO = R_E + LEO_ALT

print(f"Earth center: x = {-d_E/1e6:.2f} tkm")
print(f"Moon center:  x = {d_M/1e6:.2f} tkm")
print(f"LEO radius:   {r_LEO/1e6:.3f} tkm from Earth center")
print(f"Escape v at LEO: {np.sqrt(2*G*M_E/r_LEO)/1e3:.3f} km/s")


def cr3bp(t, state):
    x, y, z, vx, vy, vz = state
    dx_E = x + d_E
    dx_M = x - d_M
    r_E = np.sqrt(dx_E**2 + y**2 + z**2)
    r_M = np.sqrt(dx_M**2 + y**2 + z**2)
    K_E = G * M_E / r_E**3
    K_M = G * M_M / r_M**3
    ax = w**2 * x + 2*w*vy - K_E*dx_E - K_M*dx_M
    ay = w**2 * y - 2*w*vx - (K_E + K_M)*y
    az = -(K_E + K_M)*z
    return [vx, vy, vz, ax, ay, az]


def evaluate(angle_deg, v_tli_kms, hours=600):
    """
    Launch from LEO at given angle (0=+x from Earth) with TLI velocity.
    Returns trajectory properties or None on failure.
    """
    angle = np.radians(angle_deg)
    x0 = -d_E + r_LEO * np.cos(angle)
    y0 = r_LEO * np.sin(angle)
    vx0 = -v_tli_kms * 1e3 * np.sin(angle)
    vy0 = v_tli_kms * 1e3 * np.cos(angle)

    state0 = [x0, y0, 0, vx0, vy0, 0]
    try:
        sol = solve_ivp(cr3bp, [0, hours * 3600], state0,
                        rtol=1e-9, atol=1e-11, max_step=1200)
        if not sol.success:
            return None
    except Exception:
        return None

    r_E_arr = np.sqrt((sol.y[0] + d_E)**2 + sol.y[1]**2)
    r_M_arr = np.sqrt((sol.y[0] - d_M)**2 + sol.y[1]**2)

    if np.min(r_E_arr) < R_E or np.min(r_M_arr) < R_M:
        return None

    mi = np.argmin(r_M_arr)
    md = r_M_arr[mi] / 1e6
    tf = sol.t[mi] / 3600

    er = 9999
    ei = None
    if mi < len(r_E_arr) - 5 and tf > 10:
        r_E_post = r_E_arr[mi:]
        order = max(3, len(r_E_post) // 30)
        local_mins = argrelmin(r_E_post, order=order)[0]
        if len(local_mins) > 0:
            bi = local_mins[np.argmin(r_E_post[local_mins])]
            er = r_E_post[bi] / 1e6
            ei = mi + bi

    tr = sol.t[ei] / 3600 if ei else hours

    return {
        'min_moon_dist': md,
        'min_earth_return': er,
        't_flyby_h': tf,
        't_return_h': tr,
        'x0': x0, 'y0': y0,
        'vx0': vx0, 'vy0': vy0,
        'x_range': (np.min(sol.y[0]) / 1e6, np.max(sol.y[0]) / 1e6),
        'y_range': (np.min(sol.y[1]) / 1e6, np.max(sol.y[1]) / 1e6),
        'sol': sol
    }


print("\n" + "=" * 60)
print("PHASE 1: ANGULAR SCAN")
print("=" * 60)

v_tli = 10.85
best_angle = None
best_score = 1e20

for angle_deg in range(180, 270, 5):
    r = evaluate(angle_deg, v_tli, 400)
    if r is None:
        continue
    score = r['min_moon_dist'] + r['min_earth_return']
    flag = ' <<<' if r['min_moon_dist'] < 30 else ''
    print(f"  angle={angle_deg:3d}° => "
          f"Moon:{r['min_moon_dist']:.1f} Return:{r['min_earth_return']:.0f}{flag}")
    sys.stdout.flush()
    if score < best_score:
        best_score = score
        best_angle = angle_deg

if best_angle is None:
    print("No viable trajectories found.")
    sys.exit(1)

print(f"\nBest angle: {best_angle}° (score={best_score:.0f})")

print("\n" + "=" * 60)
print("PHASE 2: NELDER-MEAD OPTIMIZATION")
print("=" * 60)


def objective(params):
    a, v = params
    r = evaluate(a, v, 600)
    if r is None:
        return 1e6
    if r['min_moon_dist'] < 2:
        return 1e6
    return r['min_earth_return'] + 0.5 * r['min_moon_dist']


res = minimize(objective, [best_angle, v_tli], method='Nelder-Mead',
               options={'maxiter': 80, 'xatol': 0.1, 'fatol': 0.5})

a_opt, v_opt = res.x
print(f"  Optimized: angle={a_opt:.2f}°, v={v_opt:.4f} km/s")
sys.stdout.flush()

r = evaluate(a_opt, v_opt, 600)

if r and r['min_earth_return'] < 9000:
    tEnd_h = r['t_return_h'] * 1.10

    print(f"\n{'=' * 60}")
    print("FREE-RETURN TRAJECTORY FOUND")
    print(f"{'=' * 60}")
    print(f"\n  Launch parameters:")
    print(f"    Angle from Earth +x axis: {a_opt:.2f}°")
    print(f"    TLI velocity: {v_opt:.4f} km/s")
    print(f"\n  Simulator ICs (thousand km, km/s):")
    print(f"    x0  = {r['x0']/1e6:.10f}")
    print(f"    y0  = {r['y0']/1e6:.10f}")
    print(f"    z0  = 0")
    print(f"    vx0 = {r['vx0']/1e3:.10f}")
    print(f"    vy0 = {r['vy0']/1e3:.10f}")
    print(f"    vz0 = 0")
    print(f"    tEnd = {tEnd_h:.0f} hours")
    print(f"\n  Trajectory properties:")
    print(f"    Min Moon distance:    {r['min_moon_dist']:.1f} tkm ({r['min_moon_dist']*1e3:.0f} km)")
    print(f"    Earth return dist:    {r['min_earth_return']:.1f} tkm ({r['min_earth_return']*1e3:.0f} km)")
    print(f"    Time to Moon flyby:   {r['t_flyby_h']:.1f} h ({r['t_flyby_h']/24:.1f} days)")
    print(f"    Time to Earth return: {r['t_return_h']:.1f} h ({r['t_return_h']/24:.1f} days)")
    print(f"    x range: [{r['x_range'][0]:.0f}, {r['x_range'][1]:.0f}] tkm")
    print(f"    y range: [{r['y_range'][0]:.0f}, {r['y_range'][1]:.0f}] tkm")

    x0t = r['x0'] / 1e6
    y0t = r['y0'] / 1e6
    vx0k = r['vx0'] / 1e3
    vy0k = r['vy0'] / 1e3

    print(f"\n  JS preset (copy to simulator.html):")
    print(f"    'apollo13': {{")
    print(f"        name: 'Apollo-13 Свободный возврат',")
    print(f"        x0: {x0t:.10f}, y0: {y0t:.10f}, z0: 0,")
    print(f"        vx0: {vx0k:.10f}, vy0: {vy0k:.10f}, vz0: 0,")
    print(f"        Fx: 0, Fy: 0, Fz: 0,")
    print(f"        mass: 500, tOn: 0, tDuration: 0,")
    print(f"        a0x: 0, a0y: 0, a0z: 0,")
    print(f"        tEnd: {tEnd_h:.0f}")
    print(f"    }},")
else:
    print(f"\nNo good free-return trajectory found.")
