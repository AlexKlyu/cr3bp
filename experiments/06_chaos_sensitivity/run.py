"""
Эксперимент 06: Хаотическая чувствительность вблизи L1.

16 траекторий стартуют из L1 со скоростью v=10 м/с в разных направлениях.
Базовой скорости нет — каждый импульс определяет судьбу траектории.
Интеграция 30 суток, Верле dt=30 с.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../presets/lagrange'))

import engine
from lagrange import bisect

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

T_DAYS = 30
T_SEC = T_DAYS * 86400
DT = 30.0
N_PERT = 16
DV = 10.0


def main():
    L1_m = bisect(-engine.d_E + 1e3, engine.d_M - 1e3)
    print(f"L1 = {L1_m / 1e6:.6f} тыс. км")

    angles = np.linspace(0, 2 * np.pi, N_PERT, endpoint=False)
    results = []
    colors = plt.cm.hsv(np.linspace(0, 1, N_PERT, endpoint=False))

    print(f"Интеграция {N_PERT} траекторий (v={DV} м/с, {T_DAYS} суток)...")
    for i, angle in enumerate(angles):
        vx = DV * np.cos(angle)
        vy = DV * np.sin(angle)
        state = [L1_m, 0.0, 0.0, vx, vy, 0.0]
        result = engine.run_trajectory(state, T_SEC, DT, integrator='verlet')
        results.append(result)
        fate = "ОК"
        if result['crush'] == 1:
            fate = "Земля"
        elif result['crush'] == 2:
            fate = "Луна"
        t_end_days = result['t'][-1] / 86400
        pos_final = result['pos'][-1] / 1e6
        print(f"  {i+1:2d}) угол={np.degrees(angle):5.1f}°  "
              f"исход={fate:<6s}  t={t_end_days:5.1f} сут  "
              f"конец=({pos_final[0]:.0f}, {pos_final[1]:.0f}) тыс.км")

    fig, ax = plt.subplots(figsize=(10, 9))

    for i, result in enumerate(results):
        pos = result['pos'] / 1e6
        label = f"{np.degrees(angles[i]):.0f}\u00b0" if i % 4 == 0 else None
        ax.plot(pos[:, 0], pos[:, 1], '-', color=colors[i],
                linewidth=1.0, alpha=0.85, label=label)
        ax.plot(pos[-1, 0], pos[-1, 1], 'o', color=colors[i],
                markersize=4, zorder=15)

    ax.plot(L1_m / 1e6, 0, 'k^', markersize=12, zorder=20, label='L1')
    ax.plot(-engine.d_E / 1e6, 0, 'o', color='#2196F3', markersize=10, zorder=20)
    ax.annotate('Земля', (-engine.d_E / 1e6, 0), fontsize=9,
                ha='center', va='bottom', xytext=(0, 8), textcoords='offset points',
                color='#2196F3')
    ax.plot(engine.d_M / 1e6, 0, 'o', color='gray', markersize=8, zorder=20)
    ax.annotate('Луна', (engine.d_M / 1e6, 0), fontsize=9,
                ha='center', va='bottom', xytext=(0, 8), textcoords='offset points',
                color='gray')

    ax.set_xlabel('x (тыс. км)')
    ax.set_ylabel('y (тыс. км)')
    ax.set_title(f'Хаос вблизи L1: {N_PERT} траекторий, одна скорость ({DV} м/с), '
                 f'разные направления, {T_DAYS} сут')
    ax.legend(fontsize=8, title='Направление', loc='best')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

    png_path = os.path.join(OUT_DIR, 'chaos_fan.png')
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Сохранено: {png_path}")

    divergences = []
    for i in range(N_PERT):
        j = (i + 1) % N_PERT
        n_common = min(len(results[i]['t']), len(results[j]['t']))
        dr = np.sqrt(np.sum((results[i]['pos'][:n_common] - results[j]['pos'][:n_common])**2, axis=1))
        t_days = results[i]['t'][:n_common] / 86400
        divergences.append((t_days, dr / 1e3))

    FIT_T_MIN = 0.5
    FIT_T_MAX = 5.0

    def _compute_r_squared(t_fit, log_dr, coeffs):
        """Вычисляет R² для линейного фита."""
        fitted = np.polyval(coeffs, t_fit)
        ss_res = np.sum((log_dr - fitted) ** 2)
        ss_tot = np.sum((log_dr - np.mean(log_dr)) ** 2)
        return 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    lyapunov_exponents = []
    r_squared_values = []
    for i, (t_days, dr_km) in enumerate(divergences):
        mask = (t_days >= FIT_T_MIN) & (t_days <= FIT_T_MAX) & (dr_km > 0)
        if np.sum(mask) < 10:
            continue
        t_fit = t_days[mask]
        log_dr = np.log(dr_km[mask])
        coeffs = np.polyfit(t_fit, log_dr, 1)
        lam = coeffs[0]
        r2 = _compute_r_squared(t_fit, log_dr, coeffs)
        if lam > 0:
            lyapunov_exponents.append(lam)
            r_squared_values.append(r2)

    LAMBDA_THEORY_LOW = 0.25
    LAMBDA_THEORY_HIGH = 0.35
    LAMBDA_THEORY_MID = 0.5 * (LAMBDA_THEORY_LOW + LAMBDA_THEORY_HIGH)

    if lyapunov_exponents:
        lam_mean = np.mean(lyapunov_exponents)
        lam_std = np.std(lyapunov_exponents)
        r2_mean = np.mean(r_squared_values)
        tau_days = 1.0 / lam_mean
        print(f"\n── Показатель Ляпунова ──")
        print(f"  λ = {lam_mean:.2f} ± {lam_std:.2f} сут⁻¹  ({len(lyapunov_exponents)} пар)")
        print(f"  R² (среднее) = {r2_mean:.4f}")
        print(f"  Время Ляпунова τ = 1/λ = {tau_days:.1f} суток")
        print(f"  Интерпретация: предсказуемость траектории вблизи L1 ~ {tau_days:.0f} суток")
        print(f"\n── Сравнение с теорией ──")
        print(f"  λ_теор (линеаризация L1) ≈ {LAMBDA_THEORY_LOW}–{LAMBDA_THEORY_HIGH} сут⁻¹  "
              f"(τ ≈ 3–4 суток)")
        print(f"  λ_изм  (наш эксперимент) = {lam_mean:.2f} сут⁻¹")
        ratio = lam_mean / LAMBDA_THEORY_MID
        print(f"  Отношение λ_изм / λ_теор ≈ {ratio:.1f}×")
        print(f"  Причина расхождения: конечные возмущения ({DV} м/с) зондируют "
              f"нелинейную область, где расхождение быстрее линеаризации.")

        FIT_WINDOWS = [(0.5, 3.0), (0.5, 5.0), (0.5, 7.0)]
        print(f"\n── Чувствительность λ к окну фита ──")
        for t_lo, t_hi in FIT_WINDOWS:
            lam_window = []
            for (t_d, dr_k) in divergences:
                m = (t_d >= t_lo) & (t_d <= t_hi) & (dr_k > 0)
                if np.sum(m) < 10:
                    continue
                c = np.polyfit(t_d[m], np.log(dr_k[m]), 1)
                if c[0] > 0:
                    lam_window.append(c[0])
            if lam_window:
                print(f"  [{t_lo}–{t_hi}] сут:  λ = {np.mean(lam_window):.2f} ± "
                      f"{np.std(lam_window):.2f} сут⁻¹  ({len(lam_window)} пар)")
            else:
                print(f"  [{t_lo}–{t_hi}] сут:  недостаточно данных")

    fig, ax = plt.subplots(figsize=(10, 5))

    for i, (t_days, dr_km) in enumerate(divergences):
        label = (f"{np.degrees(angles[i]):.0f}\u00b0 и "
                 f"{np.degrees(angles[(i+1) % N_PERT]):.0f}\u00b0") if i % 4 == 0 else None
        ax.semilogy(t_days, dr_km + 0.01, '-', color=colors[i],
                    linewidth=0.8, alpha=0.8, label=label)

    if lyapunov_exponents:
        t_fit_line = np.linspace(0, FIT_T_MAX + 2, 200)
        dr0_values = []
        for t_days, dr_km in divergences:
            idx = np.argmin(np.abs(t_days - FIT_T_MIN))
            if dr_km[idx] > 0:
                dr0_values.append(dr_km[idx])
        dr0_median = np.median(dr0_values) if dr0_values else 1.0
        dr_fit = dr0_median * np.exp(lam_mean * (t_fit_line - FIT_T_MIN))
        ax.semilogy(t_fit_line, dr_fit, 'k--', linewidth=2.0, alpha=0.7,
                    label=f'e$^{{\\lambda t}}$, λ={lam_mean:.1f} сут$^{{-1}}$ '
                          f'(R²={r2_mean:.3f}), τ={tau_days:.1f} сут')
        dr_theory = dr0_median * np.exp(LAMBDA_THEORY_MID * (t_fit_line - FIT_T_MIN))
        ax.semilogy(t_fit_line, dr_theory, 'k:', linewidth=1.5, alpha=0.5,
                    label=f'Линеаризация L1: λ≈{LAMBDA_THEORY_MID:.2f} сут$^{{-1}}$')
        ax.axvspan(FIT_T_MIN, FIT_T_MAX, alpha=0.08, color='yellow')

    ax.set_xlabel('Время (сутки)')
    ax.set_ylabel('Расхождение между соседями (км)')
    ax.set_title(f'Расхождение соседних траекторий (\u0394угол={360/N_PERT:.1f}°, v={DV} м/с)')
    ax.legend(fontsize=7, loc='upper left')
    ax.grid(True, alpha=0.3)

    png_path = os.path.join(OUT_DIR, 'divergence.png')
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Сохранено: {png_path}")

    import csv
    csv_path = os.path.join(OUT_DIR, 'lyapunov.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['pair', 'angle_i_deg', 'angle_j_deg', 'lyapunov_exp_per_day', 'r_squared'])
        pair_idx = 0
        for i, (t_days, dr_km) in enumerate(divergences):
            j = (i + 1) % N_PERT
            mask = (t_days >= FIT_T_MIN) & (t_days <= FIT_T_MAX) & (dr_km > 0)
            if np.sum(mask) < 10:
                continue
            t_fit = t_days[mask]
            log_dr = np.log(dr_km[mask])
            coeffs = np.polyfit(t_fit, log_dr, 1)
            lam = coeffs[0]
            r2 = _compute_r_squared(t_fit, log_dr, coeffs)
            if lam > 0:
                w.writerow([pair_idx, f'{np.degrees(angles[i]):.1f}',
                            f'{np.degrees(angles[j]):.1f}', f'{lam:.4f}',
                            f'{r2:.4f}'])
                pair_idx += 1
        w.writerow([])
        w.writerow(['mean', '', '', f'{lam_mean:.4f}', f'{r2_mean:.4f}'])
        w.writerow(['std', '', '', f'{lam_std:.4f}', ''])
        w.writerow(['lyapunov_time_days', '', '', f'{tau_days:.2f}', ''])
        w.writerow(['lambda_theory_range', '', '', f'{LAMBDA_THEORY_LOW}-{LAMBDA_THEORY_HIGH}', ''])
    print(f"Сохранено: {csv_path}")


if __name__ == '__main__':
    main()
