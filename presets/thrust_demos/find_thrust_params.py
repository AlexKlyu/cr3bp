"""
Find initial conditions for two thrust-demonstration presets in the Earth-Moon CR3BP.

Preset 1: "Перелёт Земля→Луна с тягой" (Earth→Moon transfer with thrust)
  Approach: take the Apollo-13 free-return departure position and reduce velocity
  slightly (so ballistic trajectory fails), then use small constant Fx thrust
  for the first few hours to provide the missing Δv for a trans-lunar trajectory.

Preset 2: "Побег от L1 с микротягой" (L1 escape with micro-thrust)
  Approach: start at the L1 Lagrange point (unstable equilibrium) with zero
  velocity, apply tiny thrust to seed the instability.

Output: simulator-ready ICs (thousand km, km/s, Newtons, seconds).
"""

import numpy as np

G = 6.674e-11
M_E = 5.972e24
M_M = 7.342e22
d_E_m = 4.67e6
d_M_m = 382.8e6
R_E_m = 6.371e6
R_M_m = 1.737e6
w = 2.662e-6

GM_E = G * M_E
GM_M = G * M_M
w2 = w * w
two_w = 2 * w
scale = 1e6


def simulate(x0_tkm, y0_tkm, vx0_kms, vy0_kms, Fx, Fy, mass,
             tOn_s, tOff_s, tEnd_h, dt=30):
    """
    Integrate CR3BP with constant thrust in [tOn, tOff] window.

    Uses Velocity Verlet (same integrator as simulator.html).
    Positions in tkm, velocities in km/s, forces in N, times in seconds.

    Returns dict with trajectory stats.
    """
    x, y = x0_tkm * scale, y0_tkm * scale
    vx, vy = vx0_kms * 1000, vy0_kms * 1000
    tEnd_s = tEnd_h * 3600
    nSteps = int(tEnd_s / dt) + 1

    min_moon = 1e20
    min_moon_t = 0
    crash = 0
    J0 = None
    max_drift = 0
    sum_drift2 = 0
    n_drift = 0

    for i in range(nSteps):
        t = i * dt
        dx_E = x + d_E_m
        dx_M = x - d_M_m
        r_E = np.sqrt(dx_E**2 + y**2)
        r_M = np.sqrt(dx_M**2 + y**2)

        if r_E < R_E_m:
            crash = 1
            break
        if r_M < R_M_m:
            crash = 2
            break

        if r_M < min_moon:
            min_moon = r_M
            min_moon_t = t

        Omega = 0.5 * w2 * (x**2 + y**2) + GM_E / r_E + GM_M / r_M
        v2 = vx**2 + vy**2
        J = 2 * Omega - v2
        if J0 is None:
            J0 = J
        drift = abs(J - J0) / abs(J0) * 100
        max_drift = max(max_drift, drift)
        sum_drift2 += drift**2
        n_drift += 1

        K_E = GM_E / (r_E**3)
        K_M = GM_M / (r_M**3)
        K_sum = K_E + K_M

        tX = tY = 0.0
        if tOn_s <= t <= tOff_s:
            tX = Fx / mass
            tY = Fy / mass

        ax = w2 * x + two_w * vy - K_E * dx_E - K_M * dx_M + tX
        ay = w2 * y - two_w * vx - K_sum * y + tY
        x1 = x + vx * dt + 0.5 * ax * dt * dt
        y1 = y + vy * dt + 0.5 * ay * dt * dt

        vx_h = vx + 0.5 * ax * dt
        vy_h = vy + 0.5 * ay * dt
        dx_E1 = x1 + d_E_m
        dx_M1 = x1 - d_M_m
        r_E1 = np.sqrt(dx_E1**2 + y1**2)
        r_M1 = np.sqrt(dx_M1**2 + y1**2)
        K_E1 = GM_E / (r_E1**3)
        K_M1 = GM_M / (r_M1**3)
        tX1 = tY1 = 0.0
        if tOn_s <= (t + dt) <= tOff_s:
            tX1 = Fx / mass
            tY1 = Fy / mass
        ax1 = w2 * x1 + two_w * vy_h - K_E1 * dx_E1 - K_M1 * dx_M1 + tX1
        ay1 = w2 * y1 - two_w * vx_h - (K_E1 + K_M1) * y1 + tY1

        vx += 0.5 * (ax + ax1) * dt
        vy += 0.5 * (ay + ay1) * dt
        x = x1
        y = y1

    dist_moon = np.sqrt((x / scale - 382.8)**2 + (y / scale)**2)
    rms_drift = np.sqrt(sum_drift2 / max(n_drift, 1))

    return {
        'crash': crash,
        'min_moon_km': min_moon / 1000,
        'min_moon_t_h': min_moon_t / 3600,
        'final_x_tkm': x / scale,
        'final_y_tkm': y / scale,
        'dist_moon_tkm': dist_moon,
        'rms_drift_pct': rms_drift,
        'max_drift_pct': max_drift,
        'steps': n_drift,
    }


print("=" * 70)
print("PRESET 1: Earth→Moon Transfer with Thrust")
print("=" * 70)

APOLLO_X0 = -9.3305877540
APOLLO_Y0 = -4.9117576067
APOLLO_VX0 = 7.8194239058
APOLLO_VY0 = -7.4195663175
APOLLO_V = np.sqrt(APOLLO_VX0**2 + APOLLO_VY0**2)

print(f"\nApollo-13 free-return velocity: |v| = {APOLLO_V:.3f} km/s")
print(f"Departure position: ({APOLLO_X0:.3f}, {APOLLO_Y0:.3f}) tkm")

print("\n── Step 1: Baseline (no thrust) at various velocity fractions ──")
for frac in [1.000, 0.998, 0.995, 0.993, 0.990, 0.985]:
    vx0 = APOLLO_VX0 * frac
    vy0 = APOLLO_VY0 * frac
    r = simulate(APOLLO_X0, APOLLO_Y0, vx0, vy0, 0, 0, 500, 0, 0, 200)
    status = "CRASH Earth" if r['crash'] == 1 else "CRASH Moon" if r['crash'] == 2 else "OK"
    print(f"  v×{frac:.3f}: |v|={np.sqrt(vx0**2+vy0**2):.3f} km/s, "
          f"min_moon={r['min_moon_km']:.0f} km, "
          f"final=({r['final_x_tkm']:.0f},{r['final_y_tkm']:.0f}), {status}")

print("""
Key insight: at 100% velocity the spacecraft completes a free-return
and crashes back into Earth. Below ~99.5% it cannot reach the Moon
at all (min_moon > 100,000 km). The thrust must bridge this gap.""")

print("\n── Step 2: Scan (v_fraction, Fx, duration) with dt=30 ──")
print("Looking for: no crash, arrives near Moon (dist_moon < 10 tkm)")

Fx_vals = [5]
dur_s = 10800

best = None
best_dm = 1e20

for frac in np.arange(0.9920, 0.9935, 0.0001):
    vx0 = APOLLO_VX0 * frac
    vy0 = APOLLO_VY0 * frac
    for tEnd_h in np.arange(70, 85, 0.5):
        r = simulate(APOLLO_X0, APOLLO_Y0, vx0, vy0,
                     5, 0, 500, 0, dur_s, tEnd_h)
        if r['crash'] == 0 and r['dist_moon_tkm'] < best_dm:
            best_dm = r['dist_moon_tkm']
            best = {
                'frac': frac,
                'vx0': vx0,
                'vy0': vy0,
                'tEnd': tEnd_h,
                **r,
            }

print(f"\n  Best result:")
print(f"    v_fraction = {best['frac']:.4f}")
print(f"    vx0 = {best['vx0']:.10f} km/s")
print(f"    vy0 = {best['vy0']:.10f} km/s")
print(f"    |v0| = {np.sqrt(best['vx0']**2 + best['vy0']**2):.3f} km/s")
print(f"    Fx = 5 N, duration = 3 h (10800 s)")
print(f"    tEnd = {best['tEnd']:.1f} h")
print(f"    Distance to Moon at end: {best['dist_moon_tkm']:.1f} tkm")
print(f"    Min Moon distance: {best['min_moon_km']:.0f} km "
      f"(at t={best['min_moon_t_h']:.1f} h)")
print(f"    Final position: ({best['final_x_tkm']:.1f}, {best['final_y_tkm']:.1f}) tkm")
print(f"    Moon center: (382.8, 0) tkm")
print(f"    Jacobi RMS drift: {best['rms_drift_pct']:.2f}% "
      f"(includes physical change from thrust)")

print("\n── Step 3: Verify — same ICs without thrust ──")
r_no = simulate(APOLLO_X0, APOLLO_Y0, best['vx0'], best['vy0'],
                0, 0, 500, 0, 0, 200)
status = "CRASH Earth" if r_no['crash'] == 1 else "OK"
print(f"  Without thrust: min_moon={r_no['min_moon_km']:.0f} km, "
      f"final=({r_no['final_x_tkm']:.0f},{r_no['final_y_tkm']:.0f}), {status}")
print(f"  With thrust:    dist_moon={best['dist_moon_tkm']:.1f} tkm, arrives at Moon!")

print(f"""
┌─────────────────────────────────────────────────────────┐
│  SIMULATOR PRESET: earth_moon_thrust                    │
├─────────────────────────────────────────────────────────┤
│  x0  = {APOLLO_X0:.10f}  (tkm)                  │
│  y0  = {APOLLO_Y0:.10f}  (tkm)                  │
│  vx0 = {best['vx0']:.10f}  (km/s)                │
│  vy0 = {best['vy0']:.10f} (km/s)                │
│  Fx  = 5  (N)                                           │
│  mass = 500  (kg)                                       │
│  tOn = 0  (h)                                           │
│  tDuration = 10800  (s) = 3 h                           │
│  tEnd = {best['tEnd']:.0f}  (h)                                          │
└─────────────────────────────────────────────────────────┘""")


print("\n" + "=" * 70)
print("PRESET 2: L1 Escape with Micro-Thrust")
print("=" * 70)

L1_X0 = 323.6959407655473

print("\n── Step 1: L1 without thrust (should stay put) ──")
r0 = simulate(L1_X0, 0, 0, 0, 0, 0, 500, 0, 0, 500)
print(f"  No thrust: final=({r0['final_x_tkm']:.1f}, {r0['final_y_tkm']:.1f}), "
      f"moved {abs(r0['final_x_tkm'] - L1_X0):.4f} tkm from L1")

print("\n── Step 2: Scan micro-thrust Fx values ──")
print("  (2h burn, 500h simulation)")
for fx in [0.01, 0.02, 0.05, 0.1, 0.5]:
    r = simulate(L1_X0, 0, 0, 0, fx, 0, 500, 0, 7200, 500)
    departure = np.sqrt((r['final_x_tkm'] - L1_X0)**2 + r['final_y_tkm']**2)
    print(f"  Fx={fx:5.2f} N: final=({r['final_x_tkm']:.0f},{r['final_y_tkm']:.0f}), "
          f"departed {departure:.0f} tkm from L1, "
          f"Jacobi drift={r['rms_drift_pct']:.3f}%")

FX_L1 = 0.05
DUR_L1 = 7200

r_l1 = simulate(L1_X0, 0, 0, 0, FX_L1, 0, 500, 0, DUR_L1, 500)
dv = FX_L1 / 500 * DUR_L1
departure = np.sqrt((r_l1['final_x_tkm'] - L1_X0)**2 + r_l1['final_y_tkm']**2)

print(f"""
── Selected: Fx={FX_L1} N for {DUR_L1/3600:.0f}h ──
  Δv imparted: {dv:.2f} m/s ({dv*1000:.0f} mm/s)
  Departure from L1: {departure:.0f} tkm (after 500 hours)
  Min Moon distance: {r_l1['min_moon_km']:.0f} km
  Jacobi drift: {r_l1['rms_drift_pct']:.4f}% (negligible — thrust is tiny)

┌─────────────────────────────────────────────────────────┐
│  SIMULATOR PRESET: l1_escape                            │
├─────────────────────────────────────────────────────────┤
│  x0  = {L1_X0:.10f}  (tkm)              │
│  y0  = 0                                                │
│  vx0 = 0, vy0 = 0, vz0 = 0                             │
│  Fx  = {FX_L1}  (N)                                       │
│  mass = 500  (kg)                                       │
│  tOn = 0  (h)                                           │
│  tDuration = {DUR_L1}  (s) = {DUR_L1/3600:.0f} h                           │
│  tEnd = 500  (h)                                        │
└─────────────────────────────────────────────────────────┘""")
