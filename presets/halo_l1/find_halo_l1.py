"""
Find initial conditions for the L1 halo orbit preset in the Earth-Moon CR3BP.

Two-stage approach:
  Stage 1: Richardson's 3rd-order analytical approximation → initial guess.
  Stage 2: Numerical differential correction (shooting method) → exact ICs.

The Richardson guess alone fails because halo orbits are dynamically unstable:
any error in ICs grows exponentially (e-folding time ~4 days at L1), so the
3rd-order truncation error causes the trajectory to escape within one period.

Output: simulator-ready ICs (thousand km, km/s, hours).
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lagrange'))
from lagrange import compute_halo_ic, correct_halo_ic

AZ_KM = 15000
POINT = 'L1'

print("=" * 65)
print(f"Finding L1 Halo Orbit ICs  (Az = {AZ_KM:,} km)")
print("=" * 65)

print("\n── Stage 1: Richardson's 3rd-order analytical guess ──")

h = compute_halo_ic(Az_km=AZ_KM, northern=True, point=POINT)

print(f"  Mass parameter μ = {h['_mu']:.6f}")
print(f"  γ₁ (L1-Moon distance / L) = {h['_gamma']:.6f}")
print(f"  Legendre coefficients: c₂={h['_c2']:.4f}, c₃={h['_c3']:.4f}, c₄={h['_c4']:.4f}")
print(f"  In-plane frequency λ = {h['_lam']:.4f}")
print(f"  Out-of-plane frequency ν = √c₂ = {h['_c2']**0.5:.4f}")
print(f"  Amplitude ratio k = {h['_k']:.4f}")
print(f"  Frequency detuning Δ = λ²−c₂ = {h['_Delta']:.4f}")
print(f"  Halo constraint coeffs: l₁={h['_l1']:.4f}, l₂={h['_l2']:.4f}")
print(f"  Ax = {h['Ax_km']:.0f} km, Az = {h['Az_km']:.0f} km")
print(f"  Frequency correction ω = {h['_omega']:.6f}")
print(f"\n  Richardson ICs (simulator units):")
print(f"    x0  = {h['x0']:.10f}  (tkm)")
print(f"    z0  = {h['z0']:.10f}  (tkm)")
print(f"    vy0 = {h['vy0']:.10f}  (km/s)")
print(f"    T   = {h['T_hours']:.2f} h  ({h['T_days']:.2f} days)")

print("""
  WARNING: These are APPROXIMATE. The 3rd-order expansion error is
  non-negligible for Az/(γL) ≈ 0.25. When propagated numerically,
  this guess will NOT form a closed orbit — the trajectory escapes
  from L1 due to exponential instability (e-folding time ~4 days).""")

print("\n── Stage 2: Differential correction (shooting method) ──")
print("  Free variables: x₀, vy₀")
print("  Fixed: z₀ (from Az)")
print("  Target: vx_f = 0, vz_f = 0 at next y=0 crossing (half-period)")
print("  Method: Newton's method with finite-difference Jacobian")
print("  Integrator: scipy RK45 (rtol=1e-12)")

hc = correct_halo_ic(
    x0_m=h['x0'] * 1e6,
    z0_m=h['z0'] * 1e6,
    vy0_ms=h['vy0'] * 1e3,
    T_guess_s=h['T_hours'] * 3600,
)

print(f"\n  Converged in {hc['_iterations']} iterations (residual = {hc['_err']:.3e} m/s)")

print("\n── Comparison: Richardson vs Corrected ──")
print(f"  {'Parameter':<12} {'Richardson':>14} {'Corrected':>14} {'Δ':>12}")
print(f"  {'─'*12} {'─'*14} {'─'*14} {'─'*12}")
print(f"  {'x₀ (tkm)':<12} {h['x0']:>14.3f} {hc['x0']:>14.3f} {hc['x0']-h['x0']:>+12.3f}")
print(f"  {'vy₀ (km/s)':<12} {h['vy0']:>14.5f} {hc['vy0']:>14.5f} {hc['vy0']-h['vy0']:>+12.5f}")
print(f"  {'T (hours)':<12} {h['T_hours']:>14.1f} {hc['T_hours']:>14.1f} {hc['T_hours']-h['T_hours']:>+12.1f}")
print(f"\n  vy₀ correction: {(hc['vy0']-h['vy0'])/h['vy0']*100:+.0f}%")
print(f"  x₀ correction:  {(hc['x0']-h['x0'])/h['x0']*100:+.1f}%")

print(f"""
┌─────────────────────────────────────────────────────────┐
│  SIMULATOR PRESET: halo_l1                               │
├─────────────────────────────────────────────────────────┤
│  x0  = {hc['x0']:.10f}  (tkm)                  │
│  y0  = 0                                                │
│  z0  = {hc['z0']:.10f}  (tkm)                  │
│  vx0 = 0, vy0 = {hc['vy0']:.10f}, vz0 = 0       │
│  tEnd = {hc['T_hours']:.0f}  (h)                                        │
│  No thrust (Fx = Fy = Fz = 0)                           │
└─────────────────────────────────────────────────────────┘

  JS preset (copy to simulator.html):
    'halo_l1': {{
        name: 'Гало-орбита L1',
        x0: {hc['x0']:.10f}, y0: 0, z0: {hc['z0']:.10f},
        vx0: 0, vy0: {hc['vy0']:.10f}, vz0: 0,
        Fx: 0, Fy: 0, Fz: 0,
        mass: 500, tOn: 0, tDuration: 0,
        a0x: 0, a0y: 0, a0z: 0,
        tEnd: {hc['T_hours']:.0f}
    }},
""")
