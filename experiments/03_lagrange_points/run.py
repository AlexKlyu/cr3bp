"""
Эксперимент 03: Точки Лагранжа — обёртка над presets/lagrange/lagrange.py.

Вычисляет L1-L5 численно и сравнивает с аналитическими приближениями.
"""

import os
import sys
import csv
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../presets/lagrange'))

import engine
from lagrange import compute_lagrange_points, accel_xy

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def analytical_approximations():
    """Аналитические приближения для L1-L5 (ведущий порядок).

    Источники:
      L1, L2 — разложение по (μ/3)^(1/3) (радиус сферы Хилла):
        Murray C.D., Dermott S.F. "Solar System Dynamics", Cambridge, 1999, §3.4
      L3 — разложение по μ:
        Szebehely V. "Theory of Orbits", Academic Press, 1967, гл. 5
      L4, L5 — точное решение (вершины равносторонних треугольников):
        Lagrange J.-L. "Essai sur le Problème des Trois Corps", 1772
    """
    mu = engine.M_M / (engine.M_E + engine.M_M)
    D = engine.d_E + engine.d_M

    r_H = D * (mu / 3) ** (1 / 3)

    L1_x = engine.d_M - r_H
    L2_x = engine.d_M + r_H
    L3_x = -(D + 5 * mu * D / 12)

    L4_x = D / 2 - engine.d_E
    L4_y = D * math.sqrt(3) / 2
    L5_x = L4_x
    L5_y = -L4_y

    return {
        'L1': (L1_x, 0.0),
        'L2': (L2_x, 0.0),
        'L3': (L3_x, 0.0),
        'L4': (L4_x, L4_y),
        'L5': (L5_x, L5_y),
    }


def main():
    numerical = compute_lagrange_points()
    analytical = analytical_approximations()

    rows = []
    print("Точки Лагранжа (тыс. км):")
    print(f"{'Имя':<5} {'x_числ (тыс.км)':>16} {'y_числ (тыс.км)':>16} "
          f"{'x_аналит (тыс.км)':>18} {'y_аналит (тыс.км)':>18} {'ошибка (км)':>12}")
    print("-" * 90)

    for name in ['L1', 'L2', 'L3', 'L4', 'L5']:
        xn, yn = numerical[name]
        xa, ya = analytical[name]
        err_m = math.sqrt((xn - xa) ** 2 + (yn - ya) ** 2)

        ax_res, ay_res = accel_xy(xn, yn)

        print(f"{name:<5} {xn/1e6:>16.6f} {yn/1e6:>16.6f} "
              f"{xa/1e6:>18.6f} {ya/1e6:>18.6f} {err_m/1e3:>12.1f}")

        rows.append({
            'name': name,
            'x_num_m': xn,
            'y_num_m': yn,
            'x_num_tkm': xn / 1e6,
            'y_num_tkm': yn / 1e6,
            'x_analytical_m': xa,
            'y_analytical_m': ya,
            'error_km': err_m / 1e3,
            'residual_ax': ax_res,
            'residual_ay': ay_res,
        })

    csv_path = os.path.join(OUT_DIR, 'lagrange_points.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"\nСохранено: {csv_path}")


if __name__ == '__main__':
    main()
