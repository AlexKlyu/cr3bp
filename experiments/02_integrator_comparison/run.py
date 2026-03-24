"""
Эксперимент 02: Сравнение интеграторов — log-log график сходимости.

Шаг dt от 1 до 300 с, гало-орбита 100 ч,
ошибка позиции относительно эталона (scipy RK45).
Три интегратора:
  Эйлер              — ожидаемый наклон ~1 (O(h))
  Верле полушаговый   — ожидаемый наклон ~1 (O(h), деградация из-за Кориолиса)
  Верле итерированный — ожидаемый наклон ~2 (O(h²))
"""

import os
import sys
import csv
import math
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../presets/lagrange'))

import engine
from lagrange import compute_halo_ic, correct_halo_ic

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
T_HOURS = 100.0
T_SEC = T_HOURS * 3600


def get_halo_state():
    h = compute_halo_ic(Az_km=15000, point='L1')
    hc = correct_halo_ic(
        x0_m=h['x0'] * 1e6,
        z0_m=h['z0'] * 1e6,
        vy0_ms=h['vy0'] * 1e3,
        T_guess_s=h['T_hours'] * 3600,
    )
    return [hc['x0'] * 1e6, 0.0, hc['z0'] * 1e6, 0.0, hc['vy0'] * 1e3, 0.0]


def compute_reference(state0):
    """Эталонная траектория: scipy RK45, rtol=1e-12."""
    print("  Вычисление эталонной траектории (scipy RK45, rtol=1e-12)...")
    sol = solve_ivp(engine.cr3bp_eom, [0, T_SEC], state0,
                    rtol=1e-12, atol=1e-14, max_step=60.0, dense_output=True)
    if not sol.success:
        raise RuntimeError(f"Эталонная интеграция не удалась: {sol.message}")
    print(f"  Эталон: {len(sol.t)} шагов, t_конец={sol.t[-1]/3600:.1f} ч")
    return sol.sol


def max_position_error(state0, dt, step_fn, ref_sol):
    """Интегрируем с данным dt, сравниваем позиции с эталоном."""
    state = list(state0)
    t = 0.0
    max_err = 0.0

    while t < T_SEC:
        ref_state = ref_sol(t)
        dx = state[0] - ref_state[0]
        dy = state[1] - ref_state[1]
        dz = state[2] - ref_state[2]
        err = math.sqrt(dx**2 + dy**2 + dz**2)
        if err > max_err:
            max_err = err

        dt_cur = min(dt, T_SEC - t)
        if dt_cur <= 0:
            break
        state = step_fn(state, dt_cur)
        t += dt_cur

    return max_err


def main():
    state0 = get_halo_state()
    ref_sol = compute_reference(state0)

    dt_values = np.logspace(0, np.log10(300), 20)

    euler_errors = []
    verlet_half_errors = []
    verlet_iter_errors = []

    print(f"Интеграция гало-орбиты {T_HOURS} ч, {len(dt_values)} значений dt...")
    for dt in dt_values:
        print(f"  dt={dt:.1f} с ...", end=' ', flush=True)
        e_euler = max_position_error(state0, dt, engine.step_euler, ref_sol)
        e_vhalf = max_position_error(state0, dt, engine.step_verlet, ref_sol)
        e_viter = max_position_error(state0, dt, engine.step_verlet_iterated, ref_sol)
        euler_errors.append(e_euler)
        verlet_half_errors.append(e_vhalf)
        verlet_iter_errors.append(e_viter)
        print(f"Эйлер={e_euler:.2e} м, Верле полушаг.={e_vhalf:.2e} м, "
              f"Верле итерир.={e_viter:.2e} м")

    euler_errors = np.array(euler_errors)
    verlet_half_errors = np.array(verlet_half_errors)
    verlet_iter_errors = np.array(verlet_iter_errors)

    log_dt = np.log10(dt_values)
    mask_e = np.isfinite(euler_errors) & (euler_errors > 0)
    mask_vh = np.isfinite(verlet_half_errors) & (verlet_half_errors > 0)
    mask_vi = np.isfinite(verlet_iter_errors) & (verlet_iter_errors > 0)

    def fit_slope_with_stats(log_x, log_y):
        """Аппроксимация наклона с R² и 95% доверительным интервалом."""
        coeffs, cov = np.polyfit(log_x, log_y, 1, cov=True)
        slope, intercept = coeffs
        slope_se = np.sqrt(cov[0, 0])
        from scipy.stats import t as t_dist
        n = len(log_x)
        t_val = t_dist.ppf(0.975, df=n - 2)
        ci_95 = t_val * slope_se
        y_pred = slope * log_x + intercept
        ss_res = np.sum((log_y - y_pred) ** 2)
        ss_tot = np.sum((log_y - np.mean(log_y)) ** 2)
        r_squared = 1 - ss_res / ss_tot
        return slope, intercept, r_squared, ci_95

    slope_e, intercept_e, r2_e, ci_e = fit_slope_with_stats(
        log_dt[mask_e], np.log10(euler_errors[mask_e]))
    slope_vh, intercept_vh, r2_vh, ci_vh = fit_slope_with_stats(
        log_dt[mask_vh], np.log10(verlet_half_errors[mask_vh]))
    slope_vi, intercept_vi, r2_vi, ci_vi = fit_slope_with_stats(
        log_dt[mask_vi], np.log10(verlet_iter_errors[mask_vi]))

    print(f"\nНаклон Эйлера: {slope_e:.2f} ± {ci_e:.2f} (95% ДИ), R²={r2_e:.4f} (ожидается ~1)")
    print(f"Наклон Верле полушаг.: {slope_vh:.2f} ± {ci_vh:.2f} (95% ДИ), R²={r2_vh:.4f} (ожидается ~1, деградация из-за Кориолиса)")
    print(f"Наклон Верле итерир.: {slope_vi:.2f} ± {ci_vi:.2f} (95% ДИ), R²={r2_vi:.4f} (ожидается ~2)")

    csv_path = os.path.join(OUT_DIR, 'convergence_table.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['dt_s', 'error_euler_m', 'error_verlet_half_m', 'error_verlet_iter_m'])
        for i in range(len(dt_values)):
            w.writerow([f'{dt_values[i]:.2f}',
                        f'{euler_errors[i]:.6e}',
                        f'{verlet_half_errors[i]:.6e}',
                        f'{verlet_iter_errors[i]:.6e}'])
    print(f"Сохранено: {csv_path}")

    fit_csv_path = os.path.join(OUT_DIR, 'fit_results.csv')
    with open(fit_csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['integrator', 'slope', 'slope_95ci', 'r_squared'])
        w.writerow(['Эйлер', f'{slope_e:.4f}', f'{ci_e:.4f}', f'{r2_e:.6f}'])
        w.writerow(['Верле полушаг.', f'{slope_vh:.4f}', f'{ci_vh:.4f}', f'{r2_vh:.6f}'])
        w.writerow(['Верле итерир.', f'{slope_vi:.4f}', f'{ci_vi:.4f}', f'{r2_vi:.6f}'])
    print(f"Сохранено: {fit_csv_path}")

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.loglog(dt_values[mask_e], euler_errors[mask_e], 'o-',
              label=f'Эйлер (наклон={slope_e:.2f}±{ci_e:.2f}, R²={r2_e:.3f})',
              color='#e74c3c', markersize=5)
    ax.loglog(dt_values[mask_vh], verlet_half_errors[mask_vh], 'D-',
              label=f'Верле полушаг. (наклон={slope_vh:.2f}±{ci_vh:.2f}, R²={r2_vh:.3f})',
              color='#f39c12', markersize=5)
    ax.loglog(dt_values[mask_vi], verlet_iter_errors[mask_vi], 's-',
              label=f'Верле итерир. (наклон={slope_vi:.2f}±{ci_vi:.2f}, R²={r2_vi:.3f})',
              color='#2ecc71', markersize=5)

    dt_fit = np.logspace(0, np.log10(300), 100)
    ax.loglog(dt_fit, 10**(intercept_e + slope_e * np.log10(dt_fit)),
              '--', color='#e74c3c', alpha=0.4)
    ax.loglog(dt_fit, 10**(intercept_vh + slope_vh * np.log10(dt_fit)),
              '--', color='#f39c12', alpha=0.4)
    ax.loglog(dt_fit, 10**(intercept_vi + slope_vi * np.log10(dt_fit)),
              '--', color='#2ecc71', alpha=0.4)

    ax.set_xlabel('Шаг dt (с)')
    ax.set_ylabel('Макс. ошибка позиции (м)')
    ax.set_title('Сходимость интеграторов: Эйлер, Верле полушаг., Верле итерир.')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')

    png_path = os.path.join(OUT_DIR, 'loglog.png')
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Сохранено: {png_path}")


if __name__ == '__main__':
    main()
