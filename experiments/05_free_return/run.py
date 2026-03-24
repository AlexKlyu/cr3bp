"""
Эксперимент 05: Траектория свободного возврата (стиль Apollo-13).

Используются известные оптимальные НУ, найденные скриптом
presets/free_return/find_free_return.py (Нелдер-Мид: угол~226.5°, v~10.78 км/с).
Интеграция через engine.run_trajectory() для построения графика.

Критерий оптимальности:
  «Оптимальной» считается траектория, минимизирующая расстояние
  возврата к Земле (ближайший подход после лунного пролёта) при условии,
  что пролёт Луны состоялся (расстояние < ~70 000 км).
  Это обеспечивает безопасное баллистическое возвращение к Земле
  без дополнительных коррекций — ключевое требование свободного возврата.

Анализ чувствительности:
  После основной траектории проводится параметрический прогон v_TLI ± 50 м/с
  (5 значений). Для каждого запуска фиксируются: минимальное расстояние
  до Луны, расстояние возврата к Земле, интеграл Якоби (контроль энергии).
  Результаты сохраняются в sensitivity.csv и визуализируются в sensitivity.png.
"""

import os
import sys
import csv
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import engine

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')

ANGLE_DEG = 226.50
V_TLI_KMS = 10.7793

R_E = engine.R_E
LEO_ALT = 400e3
r_LEO = R_E + LEO_ALT

angle_rad = math.radians(ANGLE_DEG)
X0_M = -engine.d_E + r_LEO * math.cos(angle_rad)
Y0_M = r_LEO * math.sin(angle_rad)
VX0_MS = -V_TLI_KMS * 1e3 * math.sin(angle_rad)
VY0_MS = V_TLI_KMS * 1e3 * math.cos(angle_rad)

T_HOURS = 180.0

SENSITIVITY_DV = [-50, -25, 0, +25, +50]


def _compute_ic(v_tli_kms):
    """Начальные условия для заданной v_TLI (км/с) при фиксированном угле."""
    v_ms = v_tli_kms * 1e3
    x0 = -engine.d_E + r_LEO * math.cos(angle_rad)
    y0 = r_LEO * math.sin(angle_rad)
    vx0 = -v_ms * math.sin(angle_rad)
    vy0 = v_ms * math.cos(angle_rad)
    return [x0, y0, 0.0, vx0, vy0, 0.0]


def _analyze_trajectory(result):
    """
    Из результата интеграции извлечь пролёт Луны и возврат к Земле.
    Возвращает (moon_flyby_km, earth_return_km, jacobi_mean).
    """
    pos = result['pos']
    r_moon = np.sqrt((pos[:, 0] - engine.d_M)**2 + pos[:, 1]**2 + pos[:, 2]**2)
    r_earth = np.sqrt((pos[:, 0] + engine.d_E)**2 + pos[:, 1]**2 + pos[:, 2]**2)

    i_flyby = np.argmin(r_moon)
    moon_flyby_km = r_moon[i_flyby] / 1e3

    if i_flyby + 10 < len(r_earth):
        r_earth_post = r_earth[i_flyby:]
        i_return_rel = np.argmin(r_earth_post)
        earth_return_km = r_earth_post[i_return_rel] / 1e3
    else:
        earth_return_km = float('nan')

    jacobi_mean = float(np.mean(result['jacobi']))

    return moon_flyby_km, earth_return_km, jacobi_mean


def run_sensitivity():
    """
    Параметрический прогон: v_TLI ± 50 м/с.
    Возвращает список словарей с результатами.
    """
    rows = []
    for dv in SENSITIVITY_DV:
        v_tli = V_TLI_KMS + dv / 1e3
        state0 = _compute_ic(v_tli)
        result = engine.run_trajectory(state0, T_HOURS * 3600, dt=30, integrator='verlet')
        moon_km, earth_km, jacobi = _analyze_trajectory(result)
        rows.append({
            'dv_ms': dv,
            'v_tli_ms': v_tli * 1e3,
            'moon_flyby_km': moon_km,
            'earth_return_km': earth_km,
            'jacobi': jacobi,
        })
        print(f"  Δv={dv:+.0f} м/с → v_TLI={v_tli:.4f} км/с: "
              f"r_Луна={moon_km:.0f} км, r_Земля={earth_km:.0f} км, "
              f"C_J={jacobi:.6e}")
    return rows


def save_sensitivity_csv(rows):
    """Сохранение результатов чувствительности в CSV."""
    csv_path = os.path.join(OUT_DIR, 'sensitivity.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['dv_ms', 'v_tli_ms', 'moon_flyby_km', 'earth_return_km', 'jacobi'])
        for r in rows:
            w.writerow([
                f"{r['dv_ms']:.0f}",
                f"{r['v_tli_ms']:.3f}",
                f"{r['moon_flyby_km']:.1f}",
                f"{r['earth_return_km']:.1f}",
                f"{r['jacobi']:.6e}",
            ])
    print(f"Сохранено: {csv_path}")
    return csv_path


def plot_sensitivity(rows):
    """
    График чувствительности: два подграфика —
    расстояние пролёта Луны и расстояние возврата к Земле vs Δv.
    """
    dvs = [r['dv_ms'] for r in rows]
    moon_kms = [r['moon_flyby_km'] for r in rows]
    earth_kms = [r['earth_return_km'] for r in rows]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)

    ax1.plot(dvs, moon_kms, 'o-', color='#FF6F00', linewidth=1.5, markersize=6)
    ax1.set_ylabel('Мин. расстояние до Луны (км)')
    ax1.set_title('Чувствительность свободного возврата к v_TLI')
    ax1.grid(True, alpha=0.3)
    ax1.axvline(0, color='gray', linestyle='--', alpha=0.5, label='Оптимум')
    ax1.legend()

    ax2.plot(dvs, earth_kms, 's-', color='#1976D2', linewidth=1.5, markersize=6)
    ax2.set_xlabel('Δv_TLI (м/с)')
    ax2.set_ylabel('Расстояние возврата к Земле (км)')
    ax2.grid(True, alpha=0.3)
    ax2.axvline(0, color='gray', linestyle='--', alpha=0.5)

    fig.tight_layout()
    png_path = os.path.join(OUT_DIR, 'sensitivity.png')
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Сохранено: {png_path}")
    return png_path


def print_sensitivity_gradient(rows):
    """
    Оценка градиента чувствительности по конечным разностям
    вокруг оптимального значения (Δv=0).
    """
    by_dv = {r['dv_ms']: r for r in rows}
    if -25 in by_dv and +25 in by_dv:
        dr_moon = by_dv[+25]['moon_flyby_km'] - by_dv[-25]['moon_flyby_km']
        dr_earth = by_dv[+25]['earth_return_km'] - by_dv[-25]['earth_return_km']
        grad_moon = dr_moon / 50.0
        grad_earth = dr_earth / 50.0
        print(f"\n  Чувствительность: +1 м/с → Δr_Луна ≈ {grad_moon:.1f} км")
        print(f"  Чувствительность: +1 м/с → Δr_Земля ≈ {grad_earth:.1f} км")
    else:
        print("  Не удалось вычислить градиент (нет точек ±25 м/с)")


def main():
    print(f"НУ свободного возврата: угол={ANGLE_DEG}°, v={V_TLI_KMS} км/с")
    print(f"  x0  = {X0_M/1e6:.10f} тыс.км")
    print(f"  y0  = {Y0_M/1e6:.10f} тыс.км")
    print(f"  vx0 = {VX0_MS/1e3:.10f} км/с")
    print(f"  vy0 = {VY0_MS/1e3:.10f} км/с")

    state0 = [X0_M, Y0_M, 0.0, VX0_MS, VY0_MS, 0.0]
    result = engine.run_trajectory(state0, T_HOURS * 3600, dt=30, integrator='verlet')

    pos = result['pos']
    pos_tkm = pos / 1e6

    r_moon = np.sqrt((pos[:, 0] - engine.d_M)**2 + pos[:, 1]**2 + pos[:, 2]**2)
    r_earth = np.sqrt((pos[:, 0] + engine.d_E)**2 + pos[:, 1]**2 + pos[:, 2]**2)

    i_flyby = np.argmin(r_moon)
    min_moon_km = r_moon[i_flyby] / 1e3
    t_flyby_h = result['t'][i_flyby] / 3600
    print(f"\n  Пролёт Луны: {min_moon_km:.0f} км при t={t_flyby_h:.1f} ч")

    if i_flyby + 10 < len(r_earth):
        r_earth_post = r_earth[i_flyby:]
        i_return_rel = np.argmin(r_earth_post)
        i_return = i_flyby + i_return_rel
        min_earth_km = r_earth[i_return] / 1e3
        t_return_h = result['t'][i_return] / 3600
        print(f"  Возврат к Земле: {min_earth_km:.0f} км при t={t_return_h:.1f} ч")
    else:
        min_earth_km = float('nan')
        t_return_h = float('nan')
        print("  Возврат к Земле: не обнаружен")

    csv_path = os.path.join(OUT_DIR, 'free_return_ic.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['параметр', 'значение', 'единица'])
        w.writerow(['угол', f'{ANGLE_DEG:.2f}', 'град'])
        w.writerow(['v_TLI', f'{V_TLI_KMS:.4f}', 'км/с'])
        w.writerow(['x0', f'{X0_M / 1e6:.10f}', 'тыс.км'])
        w.writerow(['y0', f'{Y0_M / 1e6:.10f}', 'тыс.км'])
        w.writerow(['vx0', f'{VX0_MS / 1e3:.10f}', 'км/с'])
        w.writerow(['vy0', f'{VY0_MS / 1e3:.10f}', 'км/с'])
        w.writerow(['мин_расст_Луна_км', f'{min_moon_km:.0f}', 'км'])
        w.writerow(['t_пролёт', f'{t_flyby_h:.1f}', 'часы'])
        w.writerow(['мин_расст_Земля_км', f'{min_earth_km:.0f}', 'км'])
        w.writerow(['t_возврат', f'{t_return_h:.1f}', 'часы'])
    print(f"Сохранено: {csv_path}")

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.plot(pos_tkm[:, 0], pos_tkm[:, 1], 'b-', linewidth=0.8, label='Траектория')

    ax.plot(pos_tkm[0, 0], pos_tkm[0, 1], 'go', markersize=8, label='Старт', zorder=10)
    ax.plot(pos_tkm[i_flyby, 0], pos_tkm[i_flyby, 1], 'r*', markersize=12,
            label=f'Пролёт Луны ({min_moon_km:.0f} км)', zorder=10)
    if not math.isnan(t_return_h):
        ax.plot(pos_tkm[i_return, 0], pos_tkm[i_return, 1], 'ms', markersize=8,
                label=f'Возврат к Земле ({min_earth_km:.0f} км)', zorder=10)

    earth_x = -engine.d_E / 1e6
    ax.plot(earth_x, 0, 'o', color='#2196F3', markersize=10, zorder=5)
    ax.annotate('Земля', (earth_x, 4), fontsize=9, ha='center', color='#2196F3')

    moon_x = engine.d_M / 1e6
    ax.plot(moon_x, 0, 'o', color='gray', markersize=6, zorder=5)
    ax.annotate('Луна', (moon_x, 4), fontsize=9, ha='center', color='gray')

    ax.set_xlabel('x (тыс. км)')
    ax.set_ylabel('y (тыс. км)')
    ax.set_title(f'Свободный возврат (v={V_TLI_KMS:.2f} км/с, '
                 f'угол={ANGLE_DEG:.1f}°, T={t_return_h:.0f} ч)')
    ax.legend(loc='lower left')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    png_path = os.path.join(OUT_DIR, 'free_return_trajectory.png')
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Сохранено: {png_path}")

    print(f"\n{'='*60}")
    print("Анализ чувствительности: v_TLI ± 50 м/с")
    print(f"{'='*60}")
    sens_rows = run_sensitivity()
    save_sensitivity_csv(sens_rows)
    plot_sensitivity(sens_rows)
    print_sensitivity_gradient(sens_rows)


if __name__ == '__main__':
    main()
