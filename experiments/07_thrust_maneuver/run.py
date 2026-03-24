"""
Эксперимент 07: Сравнение манёвров с тягой.

Гипотеза: малая тяга (~Н) в течение нескольких часов создаёт Δv,
достаточный для качественного изменения траектории вблизи неустойчивых
точек, при минимальном расходе топлива.

Два пресета:
  1. Перелёт Земля-Луна (5 Н, 3 ч)
  2. Побег от L1 с микротягой (0.05 Н, 2 ч)

Для каждого сценария дополнительно вычисляется:
  - Массовая доля топлива по формуле Циолковского:
        m_fuel / m_0 = 1 - exp(-Δv / (g0 * Isp))
    для химического (Isp=300 с) и электрического (Isp=3000 с) двигателей.
  - Сравнение с Δv идеального перелёта Гомана (Земля → Луна).

Используется engine.run_trajectory() для траекторий,
presets/thrust_demos/find_thrust_params.py:simulate() для кросс-валидации.
"""

import os
import sys
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../presets/thrust_demos'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../presets/lagrange'))

import engine
from find_thrust_params import simulate
from lagrange import bisect

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

g0 = 9.80665
ISP_CHEM = 300
ISP_ELEC = 3000
M0_KG = 500.0


def tsiolkovsky_fuel_mass(dv_ms, m0, isp):
    """Масса топлива по уравнению Циолковского: m_fuel = m0 * (1 - exp(-Δv / (g0·Isp)))."""
    return m0 * (1.0 - np.exp(-dv_ms / (g0 * isp)))


def hohmann_dv():
    """
    Δv идеального перелёта Гомана (Земля → Луна).

    v_LEO = sqrt(GM_E / r_LEO),  r_LEO = R_E + 200 км
    v_transfer = sqrt(GM_E * (2/r_LEO - 2/(r_LEO + d_moon)))
    Δv = v_transfer - v_LEO
    """
    r_LEO = engine.R_E + 200e3
    d_moon = engine.d_E + engine.d_M
    v_LEO = np.sqrt(engine.GM_E / r_LEO)
    v_transfer = np.sqrt(engine.GM_E * (2.0 / r_LEO - 2.0 / (r_LEO + d_moon)))
    return v_transfer - v_LEO, v_LEO, v_transfer

PRESET1 = {
    'name': 'Перелёт Земля\u2192Луна (5 Н, 3 ч)',
    'x0_tkm': -9.3305877540,
    'y0_tkm': -4.9117576067,
    'vx0_kms': 7.7654698808,
    'vy0_kms': -7.3683713099,
    'Fx': 5.0,
    'Fy': 0.0,
    'mass': 500.0,
    'tOn_s': 0,
    'tDuration_s': 10800,
    'tEnd_h': 72,
}

PRESET2 = {
    'name': 'Побег от L1 (0.05 Н, 2 ч)',
    'Fx': 0.05,
    'Fy': 0.0,
    'mass': 500.0,
    'tOn_s': 0,
    'tDuration_s': 7200,
    'tEnd_h': 500,
}


def run_preset(preset, ax_plot):
    """Запуск одного пресета: с тягой и без, график, статистика."""
    name = preset['name']
    x0_tkm = preset['x0_tkm']
    y0_tkm = preset['y0_tkm']
    vx0_kms = preset['vx0_kms']
    vy0_kms = preset['vy0_kms']
    Fx = preset['Fx']
    Fy = preset['Fy']
    mass = preset['mass']
    tOn_s = preset['tOn_s']
    tDur_s = preset['tDuration_s']
    tOff_s = tOn_s + tDur_s
    tEnd_h = preset['tEnd_h']

    x0_m = x0_tkm * 1e6
    y0_m = y0_tkm * 1e6
    vx0_ms = vx0_kms * 1e3
    vy0_ms = vy0_kms * 1e3
    T_sec = tEnd_h * 3600

    r_cross = simulate(x0_tkm, y0_tkm, vx0_kms, vy0_kms,
                       Fx, Fy, mass, tOn_s, tOff_s, tEnd_h)
    print(f"  Кросс-валидация: мин_Луна={r_cross['min_moon_km']:.0f} км, "
          f"столкн={r_cross['crash']}, дрейф={r_cross['rms_drift_pct']:.4f}%")

    def thrust_fn(t):
        if tOn_s <= t < tOff_s:
            return (Fx / mass, Fy / mass, 0.0)
        return (0.0, 0.0, 0.0)

    state0 = [x0_m, y0_m, 0.0, vx0_ms, vy0_ms, 0.0]
    r_thrust = engine.run_trajectory(list(state0), T_sec, dt=30,
                                     integrator='verlet', thrust=thrust_fn)

    r_no = engine.run_trajectory(list(state0), T_sec, dt=30, integrator='verlet')

    pos_t = r_thrust['pos'] / 1e6
    pos_n = r_no['pos'] / 1e6

    ax_plot.plot(pos_n[:, 0], pos_n[:, 1], 'b--', linewidth=0.6, alpha=0.7, label='Без тяги')
    ax_plot.plot(pos_t[:, 0], pos_t[:, 1], 'r-', linewidth=0.8, label='С тягой')
    ax_plot.plot(pos_t[0, 0], pos_t[0, 1], 'go', markersize=6)

    earth_x = -engine.d_E / 1e6
    moon_x = engine.d_M / 1e6
    ax_plot.plot(earth_x, 0, 'o', color='#2196F3', markersize=8, zorder=5)
    ax_plot.annotate('Земля', (earth_x, 0), fontsize=9, ha='left', va='bottom',
                     xytext=(10, 5), textcoords='offset points', color='#2196F3')
    ax_plot.plot(moon_x, 0, 'o', color='gray', markersize=5, zorder=5)
    ax_plot.annotate('Луна', (moon_x, 0), fontsize=9, ha='right', va='bottom',
                     xytext=(-10, 5), textcoords='offset points', color='gray')

    ax_plot.set_xlabel('x (тыс. км)')
    ax_plot.set_ylabel('y (тыс. км)')
    ax_plot.set_title(name)
    ax_plot.legend(fontsize=8)
    ax_plot.grid(True, alpha=0.3)

    dv = (Fx / mass) * tDur_s

    n_min = min(len(r_thrust['pos']), len(r_no['pos']))
    sep_km = np.sqrt(np.sum((r_thrust['pos'][n_min-1] - r_no['pos'][n_min-1])**2)) / 1e3

    fuel_chem = tsiolkovsky_fuel_mass(dv, M0_KG, ISP_CHEM)
    fuel_elec = tsiolkovsky_fuel_mass(dv, M0_KG, ISP_ELEC)
    print(f"  Циолковский (Isp={ISP_CHEM} с, хим.):  m_топл = {fuel_chem:.3f} кг "
          f"({fuel_chem / M0_KG * 100:.2f}% от m₀)")
    print(f"  Циолковский (Isp={ISP_ELEC} с, эл.):  m_топл = {fuel_elec:.4f} кг "
          f"({fuel_elec / M0_KG * 100:.4f}% от m₀)")

    dv_hohmann, _, _ = hohmann_dv()
    print(f"  Δv Гомана ≈ {dv_hohmann / 1e3:.2f} км/с vs малая тяга Δv = {dv:.0f} м/с "
          f"(но за {tDur_s / 3600:.0f} ч работы двигателя)")

    return {
        'preset': name,
        'F_N': Fx,
        'burn_s': tDur_s,
        'dv_ms': dv,
        'separation_km': sep_km,
        'cross_min_moon_km': r_cross['min_moon_km'],
        'cross_crash': r_cross['crash'],
        'fuel_mass_chemical_kg': round(fuel_chem, 4),
        'fuel_mass_electric_kg': round(fuel_elec, 4),
        'hohmann_dv_ms': round(dv_hohmann, 2),
    }


def main():
    L1_m = bisect(-engine.d_E + 1e3, engine.d_M - 1e3)
    PRESET2['x0_tkm'] = L1_m / 1e6
    PRESET2['y0_tkm'] = 0.0
    PRESET2['vx0_kms'] = 0.0
    PRESET2['vy0_kms'] = 0.0

    fig, axes = plt.subplots(2, 1, figsize=(10, 12))
    rows = []

    for preset, ax in zip([PRESET1, PRESET2], axes):
        print(f"\n{preset['name']}:")
        row = run_preset(preset, ax)
        rows.append(row)
        print(f"  \u0394v={row['dv_ms']:.2f} м/с, расхождение={row['separation_km']:.0f} км")

    dv_h, v_leo, v_tr = hohmann_dv()
    print(f"\n{'=' * 60}")
    print(f"Справка: идеальный перелёт Гомана (LEO → Луна)")
    print(f"  v_LEO       = {v_leo:.1f} м/с")
    print(f"  v_перигей   = {v_tr:.1f} м/с")
    print(f"  Δv Гомана   = {dv_h:.1f} м/с ≈ {dv_h / 1e3:.2f} км/с")
    print(f"  Топливо (хим., Isp={ISP_CHEM} с): "
          f"{tsiolkovsky_fuel_mass(dv_h, M0_KG, ISP_CHEM):.1f} кг из {M0_KG:.0f} кг")
    print(f"  Топливо (эл., Isp={ISP_ELEC} с):  "
          f"{tsiolkovsky_fuel_mass(dv_h, M0_KG, ISP_ELEC):.1f} кг из {M0_KG:.0f} кг")
    print(f"\nВывод: непрерывная малая тяга — это манёвр коррекции/управления,")
    print(f"а не замена импульсного перелёта Гомана для выхода на переходную орбиту.")
    print(f"{'=' * 60}")

    fig.tight_layout()
    png_path = os.path.join(OUT_DIR, 'thrust_comparison.png')
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"\nСохранено: {png_path}")

    csv_path = os.path.join(OUT_DIR, 'thrust_table.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"Сохранено: {csv_path}")


if __name__ == '__main__':
    main()
