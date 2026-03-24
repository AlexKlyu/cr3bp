"""
Find a direct (Hohmann-like) ballistic transfer to the Moon in the Earth-Moon CR3BP.

Method:
  1. Scan launch angles from LEO at near-escape velocity
  2. Nelder-Mead optimization on (angle, velocity)
  3. Verify with Velocity Verlet integrator (dt=30) to match simulator

Output: simulator-ready ICs (thousand km, km/s).
"""

import sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

G = 6.674e-11
M_E = 5.972e24
M_M = 7.342e22
d_E = 4.67e6
d_M = 3.828e8
w = 2.662e-6
R_E = 6.371e6
R_M = 1.737e6

GM_E = G * M_E
GM_M = G * M_M

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


def evaluate(angle_deg, v_tli_kms, hours=120):
    """
    Launch from LEO at given angle (0=+x from Earth) with TLI velocity.
    Returns trajectory properties or None on crash/failure.
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

    return {
        'min_moon_dist': md,
        't_flyby_h': tf,
        'x0': x0, 'y0': y0,
        'vx0': vx0, 'vy0': vy0,
        'x_range': (np.min(sol.y[0]) / 1e6, np.max(sol.y[0]) / 1e6),
        'y_range': (np.min(sol.y[1]) / 1e6, np.max(sol.y[1]) / 1e6),
        'sol': sol
    }


print("\n" + "=" * 60)
print("PHASE 1: ANGULAR SCAN")
print("=" * 60)

v_tli = 10.80
best_angle = None
best_score = 1e20

for angle_deg in range(180, 270, 5):
    r = evaluate(angle_deg, v_tli, 120)
    if r is None:
        continue
    flag = ' <<<' if r['min_moon_dist'] < 30 else ''
    print(f"  angle={angle_deg:3d}° => "
          f"Moon:{r['min_moon_dist']:.1f} tkm, t={r['t_flyby_h']:.1f}h{flag}")
    sys.stdout.flush()
    if r['min_moon_dist'] < best_score:
        best_score = r['min_moon_dist']
        best_angle = angle_deg

if best_angle is None:
    print("No viable trajectories found in first scan. Trying wider range...")
    for v_try in [10.70, 10.75, 10.85, 10.90]:
        for angle_deg in range(150, 300, 5):
            r = evaluate(angle_deg, v_try, 120)
            if r is None:
                continue
            if r['min_moon_dist'] < best_score:
                best_score = r['min_moon_dist']
                best_angle = angle_deg
                v_tli = v_try
    if best_angle is None:
        print("No viable trajectories found.")
        sys.exit(1)

print(f"\nBest angle: {best_angle}° (min_moon={best_score:.1f} tkm)")

print("\n" + "=" * 60)
print("PHASE 2: NELDER-MEAD OPTIMIZATION")
print("=" * 60)


def objective(params):
    a, v = params
    r = evaluate(a, v, 120)
    if r is None:
        return 1e6
    return r['min_moon_dist']


res = minimize(objective, [best_angle, v_tli], method='Nelder-Mead',
               options={'maxiter': 200, 'xatol': 0.01, 'fatol': 0.01})

a_opt, v_opt = res.x
print(f"  Optimized: angle={a_opt:.2f}°, v={v_opt:.4f} km/s")
sys.stdout.flush()

print("\n" + "=" * 60)
print("VERLET VERIFICATION")
print("=" * 60)

w2 = w * w
two_w = 2 * w
scale = 1e6


def verlet_simulate(x0_tkm, y0_tkm, vx0_kms, vy0_kms, tEnd_h, dt=30):
    """Velocity Verlet integrator matching simulator.html."""
    x, y = x0_tkm * scale, y0_tkm * scale
    vx, vy = vx0_kms * 1000, vy0_kms * 1000
    tEnd_s = tEnd_h * 3600
    nSteps = int(tEnd_s / dt) + 1

    min_moon = 1e20
    min_moon_t = 0
    crash = 0

    for i in range(nSteps):
        t = i * dt
        dx_E = x + d_E
        dx_M = x - d_M
        r_E = np.sqrt(dx_E**2 + y**2)
        r_M = np.sqrt(dx_M**2 + y**2)

        if r_E < R_E:
            crash = 1
            break
        if r_M < R_M:
            crash = 2
            break

        if r_M < min_moon:
            min_moon = r_M
            min_moon_t = t

        K_E = GM_E / (r_E**3)
        K_M = GM_M / (r_M**3)
        K_sum = K_E + K_M

        ax = w2 * x + two_w * vy - K_E * dx_E - K_M * dx_M
        ay = w2 * y - two_w * vx - K_sum * y
        x1 = x + vx * dt + 0.5 * ax * dt * dt
        y1 = y + vy * dt + 0.5 * ay * dt * dt

        vx_h = vx + 0.5 * ax * dt
        vy_h = vy + 0.5 * ay * dt
        dx_E1 = x1 + d_E
        dx_M1 = x1 - d_M
        r_E1 = np.sqrt(dx_E1**2 + y1**2)
        r_M1 = np.sqrt(dx_M1**2 + y1**2)
        K_E1 = GM_E / (r_E1**3)
        K_M1 = GM_M / (r_M1**3)
        ax1 = w2 * x1 + two_w * vy_h - K_E1 * dx_E1 - K_M1 * dx_M1
        ay1 = w2 * y1 - two_w * vx_h - (K_E1 + K_M1) * y1

        vx += 0.5 * (ax + ax1) * dt
        vy += 0.5 * (ay + ay1) * dt
        x = x1
        y = y1

    return {
        'crash': crash,
        'min_moon_km': min_moon / 1000,
        'min_moon_t_h': min_moon_t / 3600,
    }


r = evaluate(a_opt, v_opt, 120)

if r and r['min_moon_dist'] < 50:
    tEnd_h = np.ceil(r['t_flyby_h'])

    x0t = r['x0'] / 1e6
    y0t = r['y0'] / 1e6
    vx0k = r['vx0'] / 1e3
    vy0k = r['vy0'] / 1e3

    rv = verlet_simulate(x0t, y0t, vx0k, vy0k, tEnd_h)
    print(f"  Verlet: min_moon={rv['min_moon_km']:.0f} km at t={rv['min_moon_t_h']:.1f}h, "
          f"crash={rv['crash']}")

    print(f"\n{'=' * 60}")
    print("DIRECT LUNAR TRANSFER FOUND")
    print(f"{'=' * 60}")
    print(f"\n  Launch parameters:")
    print(f"    Angle from Earth +x axis: {a_opt:.2f}°")
    print(f"    TLI velocity: {v_opt:.4f} km/s")
    print(f"\n  Simulator ICs (thousand km, km/s):")
    print(f"    x0  = {x0t:.10f}")
    print(f"    y0  = {y0t:.10f}")
    print(f"    z0  = 0")
    print(f"    vx0 = {vx0k:.10f}")
    print(f"    vy0 = {vy0k:.10f}")
    print(f"    vz0 = 0")
    print(f"    tEnd = {tEnd_h:.0f} hours")
    print(f"\n  Trajectory properties:")
    print(f"    Min Moon distance: {r['min_moon_dist']:.1f} tkm ({r['min_moon_dist']*1e3:.0f} km)")
    print(f"    Time to Moon flyby: {r['t_flyby_h']:.1f} h ({r['t_flyby_h']/24:.1f} days)")
    print(f"    x range: [{r['x_range'][0]:.0f}, {r['x_range'][1]:.0f}] tkm")
    print(f"    y range: [{r['y_range'][0]:.0f}, {r['y_range'][1]:.0f}] tkm")

    print(f"\n  JS preset (copy to simulator.html):")
    print(f"    'hohmann': {{")
    print(f"        name: 'Прямой перелёт к Луне',")
    print(f"        x0: {x0t:.10f}, y0: {y0t:.10f}, z0: 0,")
    print(f"        vx0: {vx0k:.10f}, vy0: {vy0k:.10f}, vz0: 0,")
    print(f"        Fx: 0, Fy: 0, Fz: 0,")
    print(f"        mass: 500, tOn: 0, tDuration: 0,")
    print(f"        a0x: 0, a0y: 0, a0z: 0,")
    print(f"        tEnd: {tEnd_h:.0f}")
    print(f"    }},")
else:
    print(f"\nNo good direct transfer found (min_moon={r['min_moon_dist']:.1f} tkm)")
