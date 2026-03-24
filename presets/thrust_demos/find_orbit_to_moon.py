"""
Find initial conditions for a realistic orbit-to-Moon transfer preset.

Preset: "Перелёт с орбиты к Луне (TLI)" — Trans-Lunar Injection from orbit.

Unlike the existing "earth_moon_thrust" preset (which starts at ~10.7 km/s,
99.3% of escape velocity, needing only a tiny 108 m/s correction), this
scenario starts from a natural circular orbit with zero excess velocity.
The engine must provide the full TLI delta-v.

Approach:
  - Start on a 50,000 km circular orbit around Earth (same altitude as e_orbit
    preset), positioned below Earth in the rotating frame (270° position).
  - At this position, the prograde velocity points in the +x direction
    (toward the Moon), which is optimal for TLI geometry.
  - Apply ~15.5 kN thrust for 2 minutes to inject onto a trans-lunar path.
  - The spacecraft reaches the Moon after ~19 hours.

Key physics:
  - Circular orbit velocity at 50,000 km: 2.823 km/s
  - Escape velocity at 50,000 km: 3.993 km/s
  - TLI delta-v delivered: ~3,725 m/s (includes radial component for targeting)
  - Fuel consumption (Isp=300s bipropellant): ~359 kg (72% of 500 kg)
  - Without thrust: spacecraft stays in orbit, never closer than 327,000 km to Moon

IMPORTANT: This preset requires adaptive timestepping (dt=5, dtMin=1).
  The 120-second burn at 15.5 kN is too short/intense for dt=30 (only 4 steps).
  Adaptive stepping gives ~24 steps during the burn for accurate trajectory.

Final simulator preset values:
  Fx=15300, Fy=2600, tDuration=120, tEnd=19, dt=5, dtMin=1, adaptiveStep=true

Output: simulator-ready ICs (thousand km, km/s, Newtons, seconds).
"""

import numpy as np
from scipy.optimize import differential_evolution

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
             tOff_s, tEnd_h, dt=5):
    """Velocity Verlet integrator for CR3BP with thrust."""
    x, y = x0_tkm * scale, y0_tkm * scale
    vx, vy = vx0_kms * 1000, vy0_kms * 1000
    tEnd_s = tEnd_h * 3600
    nSteps = int(tEnd_s / dt) + 1

    min_moon = 1e20
    min_moon_t = 0
    crash = 0

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

        K_E = GM_E / (r_E**3)
        K_M = GM_M / (r_M**3)
        K_sum = K_E + K_M

        tX = tY = 0.0
        if t <= tOff_s:
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
        if (t + dt) <= tOff_s:
            tX1 = Fx / mass
            tY1 = Fy / mass
        ax1 = w2 * x1 + two_w * vy_h - K_E1 * dx_E1 - K_M1 * dx_M1 + tX1
        ay1 = w2 * y1 - two_w * vx_h - (K_E1 + K_M1) * y1 + tY1

        vx += 0.5 * (ax + ax1) * dt
        vy += 0.5 * (ay + ay1) * dt
        x = x1
        y = y1

    return {
        'crash': crash,
        'min_moon_km': min_moon / 1000,
        'min_moon_t_h': min_moon_t / 3600,
        'final_x_tkm': x / scale,
        'final_y_tkm': y / scale,
    }


MASS = 500
Isp = 300
g0 = 9.81

v_orb = np.sqrt(GM_E / (50e6)) / 1000
X0 = -4.67
Y0 = -50.0
VX0 = v_orb
VY0 = 0.0

print("=" * 70)
print("ORBIT-TO-MOON TRANSFER (TLI)")
print("=" * 70)

print(f"\nStarting orbit:")
print(f"  Altitude: 50,000 km from Earth center ({50000-6371:.0f} km above surface)")
print(f"  Position in rotating frame: ({X0}, {Y0}) tkm (below Earth, 270° pos)")
print(f"  Circular velocity: {VX0:.10f} km/s (prograde → +x at this position)")
print(f"  Escape velocity: {np.sqrt(2*GM_E/50e6)/1000:.3f} km/s")
print(f"  Delta-v to escape: {(np.sqrt(2*GM_E/50e6)/1000 - v_orb)*1000:.0f} m/s")

print("\n── Step 1: Baseline — orbit without thrust ──")
r0 = simulate(X0, Y0, VX0, VY0, 0, 0, MASS, 0, 200)
print(f"  Without thrust (200h sim): min_moon = {r0['min_moon_km']:.0f} km")
print(f"  Spacecraft stays in Earth orbit, never approaches Moon.")

print("\n── Step 2: Optimize TLI burn parameters ──")


def objective(params):
    Fx, Fy, burn = params
    if burn < 10:
        return 1e8
    r = simulate(X0, Y0, VX0, VY0, Fx, Fy, MASS, burn, 40)
    if r['crash'] != 0:
        return 1e8
    if r['min_moon_km'] < 2000:
        return 1e8
    return r['min_moon_km']


bounds = [(12000, 18000), (0, 5000), (80, 180)]
result = differential_evolution(objective, bounds, seed=42, maxiter=200,
                                tol=0.01, popsize=25)
Fx_opt, Fy_opt, burn_opt = result.x
r_opt = simulate(X0, Y0, VX0, VY0, Fx_opt, Fy_opt, MASS, burn_opt, 40)

print(f"  Optimized: Fx={Fx_opt:.1f} N, Fy={Fy_opt:.1f} N, burn={burn_opt:.1f} s")
print(f"  Min Moon dist: {r_opt['min_moon_km']:.0f} km at t={r_opt['min_moon_t_h']:.1f} h")

print("\n── Step 3: Find clean integer parameters ──")

best = None
best_mm = 1e20
for Fx in range(13500, 15500, 100):
    for Fy in range(2000, 3500, 100):
        for burn in range(110, 140):
            r = simulate(X0, Y0, VX0, VY0, Fx, Fy, MASS, burn, 40)
            if r['crash'] == 0 and 2000 < r['min_moon_km'] < best_mm:
                best_mm = r['min_moon_km']
                best = (Fx, Fy, burn)

if best:
    Fx_f, Fy_f, burn_f = best
else:
    Fx_f = round(Fx_opt / 100) * 100
    Fy_f = round(Fy_opt / 100) * 100
    burn_f = round(burn_opt)

r_f = simulate(X0, Y0, VX0, VY0, Fx_f, Fy_f, MASS, burn_f, 40)
F_mag = np.sqrt(Fx_f**2 + Fy_f**2)
dv = F_mag / MASS * burn_f
fuel = MASS * (1 - np.exp(-dv / (Isp * g0)))
fuel_lh2 = MASS * (1 - np.exp(-dv / (450 * g0)))

print(f"  Selected: Fx={Fx_f} N, Fy={Fy_f} N, burn={burn_f} s")
print(f"  Min Moon dist: {r_f['min_moon_km']:.0f} km at t={r_f['min_moon_t_h']:.1f} h")
print(f"  Crash: {r_f['crash']}")

print("\n── Step 4: Verify — with thrust vs without ──")
print(f"  WITH thrust:    min_moon = {r_f['min_moon_km']:.0f} km (Moon flyby!)")
print(f"  WITHOUT thrust: min_moon = {r0['min_moon_km']:.0f} km (stays in orbit)")

print(f"""
── Physics Summary ──
  Thrust:        |F| = {F_mag:.0f} N ({F_mag/1000:.1f} kN)
  Acceleration:  a = {F_mag/MASS:.1f} m/s² ({F_mag/MASS/g0:.2f} g)
  Burn time:     {burn_f} s ({burn_f/60:.1f} min)
  Delta-v:       {dv:.0f} m/s ({dv/1000:.2f} km/s)
  Transfer time: ~{r_f['min_moon_t_h']:.0f} hours to Moon

  Fuel consumption (Tsiolkovsky rocket equation):
    Bipropellant (Isp=300s): {fuel:.0f} kg ({fuel/MASS*100:.0f}% of {MASS} kg)
    LH₂/LOX     (Isp=450s): {fuel_lh2:.0f} kg ({fuel_lh2/MASS*100:.0f}% of {MASS} kg)

  Comparison with real missions:
    Apollo TLI from LEO:     ~3,100 m/s (S-IVB stage)
    Our TLI from 50,000 km:  {dv:.0f} m/s
    The higher dv accounts for radial thrust component in rotating frame.
""")

tEnd = int(r_f['min_moon_t_h']) + 5
print(f"""
┌─────────────────────────────────────────────────────────────┐
│  SIMULATOR PRESET: orbit_to_moon                             │
├─────────────────────────────────────────────────────────────┤
│  x0  = {X0:.10f}  (tkm)                              │
│  y0  = {Y0:.10f}  (tkm)                             │
│  vx0 = {VX0:.10f}  (km/s)  [circular orbit]         │
│  vy0 = {VY0:.10f}  (km/s)                            │
│  Fx  = {Fx_f}  (N)                                          │
│  Fy  = {Fy_f}  (N)                                           │
│  mass = {MASS}  (kg)                                          │
│  tOn = 0  (h)                                                │
│  tDuration = {burn_f}  (s) = {burn_f/60:.1f} min                          │
│  tEnd = {tEnd}  (h)                                            │
│                                                              │
│  delta-v = {dv:.0f} m/s                                       │
│  fuel (Isp=300s) = {fuel:.0f} kg ({fuel/MASS*100:.0f}%)                          │
└─────────────────────────────────────────────────────────────┘
""")
