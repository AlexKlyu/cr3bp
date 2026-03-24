"""
Вычисление точек Лагранжа L1-L5 для CR3BP (Земля-Луна).

L1, L2, L3 — метод бисекции на оси x (f(x) = 0, где f — ускорение стационарной точки).
L4, L5 — метод Ньютона в 2D (ax=0, ay=0), начальное приближение — равносторонний треугольник.
"""

import math

G = 6.674e-11
M_E = 5.972e24
M_M = 7.342e22
d_E = 4.67e6
d_M = 3.828e8
w = 2.662e-6

GM_E = G * M_E
GM_M = G * M_M


def accel_x(x):
    """Ускорение по x для стационарной точки на оси x (y=z=0)."""
    r_E = abs(x + d_E)
    r_M = abs(x - d_M)
    return w**2 * x - GM_E * (x + d_E) / r_E**3 - GM_M * (x - d_M) / r_M**3


def accel_xy(x, y):
    """Ускорение (ax, ay) для стационарной точки в плоскости xy."""
    r_E = math.sqrt((x + d_E)**2 + y**2)
    r_M = math.sqrt((x - d_M)**2 + y**2)
    ax = w**2 * x - GM_E * (x + d_E) / r_E**3 - GM_M * (x - d_M) / r_M**3
    ay = w**2 * y - GM_E * y / r_E**3 - GM_M * y / r_M**3
    return ax, ay


def bisect_trace(a, b, n_iter=200):
    """Бисекция с записью промежуточных шагов."""
    trace = []
    for _ in range(n_iter):
        m = (a + b) / 2
        f_m = accel_x(m)
        trace.append((a, b, m, f_m))
        if accel_x(a) * f_m < 0:
            b = m
        else:
            a = m
    return trace


def newton_2d_trace(x0, y0, n_iter=20, h=1.0, tol=1e-15):
    """Метод Ньютона с записью промежуточных шагов."""
    x, y = x0, y0
    trace = []
    for _ in range(n_iter):
        ax, ay = accel_xy(x, y)
        trace.append((x, y, ax, ay))
        if math.sqrt(ax**2 + ay**2) < tol:
            break
        ax1, ay1 = accel_xy(x + h, y)
        ax2, ay2 = accel_xy(x, y + h)
        j00, j01 = (ax1 - ax) / h, (ax2 - ax) / h
        j10, j11 = (ay1 - ay) / h, (ay2 - ay) / h
        det = j00 * j11 - j01 * j10
        x -= (j11 * ax - j01 * ay) / det
        y -= (-j10 * ax + j00 * ay) / det
    return trace


def bisect(a, b, n_iter=200):
    """Бисекция для нахождения корня accel_x на интервале [a, b]."""
    for _ in range(n_iter):
        m = (a + b) / 2
        if accel_x(a) * accel_x(m) < 0:
            b = m
        else:
            a = m
    return (a + b) / 2


def newton_2d(x0, y0, n_iter=20, h=1.0, tol=1e-15):
    """Метод Ньютона для 2D (ax=0, ay=0). Якобиан через конечные разности."""
    x, y = x0, y0
    for _ in range(n_iter):
        ax, ay = accel_xy(x, y)
        if math.sqrt(ax**2 + ay**2) < tol:
            break
        ax1, ay1 = accel_xy(x + h, y)
        ax2, ay2 = accel_xy(x, y + h)
        j00, j01 = (ax1 - ax) / h, (ax2 - ax) / h
        j10, j11 = (ay1 - ay) / h, (ay2 - ay) / h
        det = j00 * j11 - j01 * j10
        x -= (j11 * ax - j01 * ay) / det
        y -= (-j10 * ax + j00 * ay) / det
    return x, y


def compute_halo_ic(Az_km=15000, northern=True, point='L1'):
    """
    Начальные условия для гало-орбиты у L1 или L2 (метод Ричардсона, 3-й порядок).

    Az_km: амплитуда по z (км)
    northern: True — северная ветвь, False — южная
    point: 'L1' или 'L2'
    Возвращает dict с x0, z0 (тыс. км), vy0 (км/с), T_hours, T_days.
    """
    if point not in ('L1', 'L2'):
        raise ValueError(f"point должен быть 'L1' или 'L2', получено: {point!r}")

    mu = M_M / (M_E + M_M)
    L = d_E + d_M

    if point == 'L1':
        Lp_m = bisect(-d_E + 1e3, d_M - 1e3)
        gamma = (d_M - Lp_m) / L

        def cn(n):
            return (1 / gamma**3) * (
                mu + (-1)**n * (1 - mu) * gamma**(n + 1) / (1 - gamma)**(n + 1)
            )
    else:
        Lp_m = bisect(d_M + 1e3, d_M * 1.5)
        gamma = (Lp_m - d_M) / L

        def cn(n):
            return (1 / gamma**3) * (
                (-1)**n * mu + (1 - mu) * gamma**(n + 1) / (1 + gamma)**(n + 1)
            )

    c2, c3, c4 = cn(2), cn(3), cn(4)

    poly_b = 2 - c2
    poly_c = (1 - c2) * (1 + 2 * c2)
    disc = poly_b**2 - 4 * poly_c
    lam = math.sqrt((poly_b + math.sqrt(disc)) / 2)

    k = (lam**2 + 1 + 2 * c2) / (2 * lam)

    Delta = lam**2 - c2

    d1 = 3 * lam**2 / k * (k * (6 * lam**2 - 1) - 2 * lam)
    d2 = 8 * lam**2 / k * (k * (11 * lam**2 - 1) - 2 * lam)

    a21 = 3 * c3 * (k**2 - 2) / (4 * (1 + 2 * c2))
    a22 = 3 * c3 / (4 * (1 + 2 * c2))
    a23 = -3 * c3 * lam / (4 * k * d1) * (3 * k**3 * lam - 6 * k * (k - lam) + 4)
    a24 = -3 * c3 * lam / (4 * k * d1) * (2 + 3 * k * lam)

    b21 = -3 * c3 * lam / (2 * d1) * (3 * k * lam - 4)
    b22 = 3 * c3 * lam / d1

    d21 = -c3 / (2 * lam**2)

    a31 = (
        -9 * lam / (4 * d2) * (4 * c3 * (k * a23 - b21) + k * c4 * (4 + k**2))
        + (9 * lam**2 + 1 - c2) / (2 * d2)
        * (3 * c3 * (2 * a21 + a23 + 5 * d21) / 8 + 3 * c4 * (12 - k**2) / 8)
    )

    a32 = (
        -9 * lam / (4 * d2) * (4 * c3 * (k * a24 - b22) + k * c4)
        - 3 * (9 * lam**2 + 1 - c2) / (8 * d2)
        * (c3 * (a21 + a24) + c4 * (12 - k**2) / 3)
    )

    b31 = 3 / (8 * d2) * (
        8 * lam * (3 * c3 * (k * b21 - 2 * a21) - c4 * (2 + 3 * k**2))
        + (9 * lam**2 + 1 + 2 * c2)
        * (4 * c3 * (k * a23 - b21) + k * c4 * (4 + k**2))
    )

    b32 = 3 / (8 * d2) * (
        8 * lam * (3 * c3 * (k * b22 + 2 * a24) + c4 * (2 + 3 * k**2))
        - (9 * lam**2 + 1 + 2 * c2)
        * (4 * c3 * (k * a24 - b22) + k * c4)
    )

    d31 = 3 / (64 * lam**2) * (4 * c3 * a21 + c4)
    d32 = 3 / (64 * lam**2) * (4 * c3 * (a23 - d21) + c4 * (4 + k**2))

    s1 = (
        (3 / 2) * c3 * (2 * a21 * (k**2 - 2) - a23 * (k**2 + 2) - 2 * k * b21)
        - (3 / 8) * c4 * (3 * k**4 - 8 * k**2 + 8)
    )
    s2 = (
        (3 / 2) * c3 * (2 * a22 * (k**2 - 2) + a24 * (k**2 + 2) + 2 * k * b22 + 5 * d21)
        + (3 / 8) * c4 * (12 - k**2)
    )

    a1 = -(3 / 2) * c3 * (2 * a21 + a23 + 5 * d21) - (3 / 8) * c4 * (12 - k**2)
    a2 = (3 / 2) * c3 * (d21 - 2 * a22) + (3 / 8) * c4 * (12 - k**2)
    l1 = a1 + 2 * lam**2 * s1
    l2 = a2 + 2 * lam**2 * s2

    scale_pos = gamma * L
    Az_n = Az_km * 1e3 / scale_pos

    Ax_sq = -(l2 * Az_n**2 + Delta) / l1
    if Ax_sq < 0:
        raise ValueError(
            f"Нет гало-орбиты для Az={Az_km} км (Ax²={Ax_sq:.6e} < 0). "
            "Попробуйте другую амплитуду."
        )
    Ax = math.sqrt(Ax_sq)

    omega = 1 + s1 * Ax**2 + s2 * Az_n**2

    dm = 1 if northern else -1

    x_n = (
        a21 * Ax**2 + a22 * Az_n**2 - Ax
        + (a23 * Ax**2 - a24 * Az_n**2)
        + (a31 * Ax**3 - a32 * Ax * Az_n**2)
    )
    z_n = dm * (
        Az_n
        - 2 * d21 * Ax * Az_n
        + (d32 * Az_n * Ax**2 - d31 * Az_n**3)
    )
    vy_n = (
        k * Ax
        + 2 * (b21 * Ax**2 - b22 * Az_n**2)
        + 3 * (b31 * Ax**3 - b32 * Ax * Az_n**2)
    ) * lam * omega

    scale_vel = gamma * L * w

    x0_m = Lp_m + x_n * scale_pos
    z0_m = z_n * scale_pos
    vy0_ms = vy_n * scale_vel

    x0_tkm = x0_m / 1e6
    z0_tkm = z0_m / 1e6
    vy0_kms = vy0_ms / 1e3

    T_norm = 2 * math.pi / (lam * omega)
    T_sec = T_norm / w
    T_hours = T_sec / 3600

    return {
        'x0': x0_tkm,
        'z0': z0_tkm,
        'vy0': vy0_kms,
        'T_hours': T_hours,
        'T_days': T_hours / 24,
        'Ax_km': Ax * scale_pos / 1e3,
        'Az_km': Az_km,
        '_point': point,
        '_mu': mu,
        '_gamma': gamma,
        '_c2': c2, '_c3': c3, '_c4': c4,
        '_lam': lam, '_k': k, '_Delta': Delta,
        '_l1': l1, '_l2': l2,
        '_Ax_n': Ax, '_Az_n': Az_n,
        '_omega': omega,
    }


def _cr3bp_eom(t, state):
    """
    Уравнения движения CR3BP в размерных единицах (СИ).
    state = [x, y, z, vx, vy, vz] в метрах и м/с.
    """
    x, y, z, vx, vy, vz = state

    dx_E = x + d_E
    dx_M = x - d_M
    r_E = math.sqrt(dx_E**2 + y**2 + z**2)
    r_M = math.sqrt(dx_M**2 + y**2 + z**2)
    r_E3 = r_E**3
    r_M3 = r_M**3

    ax = (w**2 * x + 2 * w * vy
          - GM_E * dx_E / r_E3
          - GM_M * dx_M / r_M3)
    ay = (w**2 * y - 2 * w * vx
          - GM_E * y / r_E3
          - GM_M * y / r_M3)
    az = (-GM_E * z / r_E3
          - GM_M * z / r_M3)

    return [vx, vy, vz, ax, ay, az]


def correct_halo_ic(x0_m, z0_m, vy0_ms, T_guess_s, tol=1e-10, max_iter=30):
    """
    Дифференциальная коррекция начальных условий гало-орбиты.

    Стартовое состояние: (x0, 0, z0, 0, vy0, 0) — пересечение плоскости xz.
    Ищем x0, vy0 такие, что при следующем пересечении y=0 выполняется vx=0, vz=0.

    Возвращает dict с x0 (тыс. км), z0 (тыс. км), vy0 (км/с), T_hours.
    """
    from scipy.integrate import solve_ivp

    x0 = x0_m
    z0 = z0_m
    vy0 = vy0_ms

    for iteration in range(max_iter):
        def y_cross(t, state):
            return state[1]
        y_cross.terminal = True
        y_cross.direction = -1

        state0 = [x0, 0.0, z0, 0.0, vy0, 0.0]
        half_T_guess = T_guess_s / 2

        sol = solve_ivp(
            _cr3bp_eom, [0, half_T_guess * 2],
            state0, events=y_cross,
            rtol=1e-12, atol=1e-14, max_step=60.0,
        )

        if len(sol.t_events[0]) == 0:
            raise RuntimeError(
                f"Итерация {iteration}: не найдено пересечение y=0. "
                "Попробуйте другую амплитуду."
            )

        t_half = sol.t_events[0][0]
        sf = sol.y_events[0][0]
        xf, yf, zf, vxf, vyf, vzf = sf

        err = math.sqrt(vxf**2 + vzf**2)
        if err < tol:
            T_sec = 2 * t_half
            return {
                'x0': x0 / 1e6,
                'z0': z0 / 1e6,
                'vy0': vy0 / 1e3,
                'T_hours': T_sec / 3600,
                'T_days': T_sec / 86400,
                '_converged': True,
                '_iterations': iteration + 1,
                '_err': err,
            }

        eps_x = 1.0
        eps_vy = 1e-4

        state_px = [x0 + eps_x, 0.0, z0, 0.0, vy0, 0.0]
        sol_px = solve_ivp(
            _cr3bp_eom, [0, half_T_guess * 2],
            state_px, events=y_cross,
            rtol=1e-12, atol=1e-14, max_step=60.0,
        )
        sf_px = sol_px.y_events[0][0]
        dvx_dx = (sf_px[3] - vxf) / eps_x
        dvz_dx = (sf_px[5] - vzf) / eps_x

        state_pv = [x0, 0.0, z0, 0.0, vy0 + eps_vy, 0.0]
        sol_pv = solve_ivp(
            _cr3bp_eom, [0, half_T_guess * 2],
            state_pv, events=y_cross,
            rtol=1e-12, atol=1e-14, max_step=60.0,
        )
        sf_pv = sol_pv.y_events[0][0]
        dvx_dvy = (sf_pv[3] - vxf) / eps_vy
        dvz_dvy = (sf_pv[5] - vzf) / eps_vy

        det = dvx_dx * dvz_dvy - dvx_dvy * dvz_dx
        if abs(det) < 1e-30:
            raise RuntimeError(f"Итерация {iteration}: вырожденный якобиан")

        dx0 = -(dvz_dvy * vxf - dvx_dvy * vzf) / det
        dvy0 = -(-dvz_dx * vxf + dvx_dx * vzf) / det

        x0 += dx0
        vy0 += dvy0

        T_guess_s = 2 * t_half

    raise RuntimeError(f"Не сошлось за {max_iter} итераций (err={err:.3e})")


def compute_lagrange_points():
    """Вычисление всех 5 точек Лагранжа. Возвращает dict {name: (x, y)} в метрах."""
    eps = 1e3
    L1 = bisect(-d_E + eps, d_M - eps)
    L2 = bisect(d_M + eps, d_M * 1.5)
    L3 = bisect(-d_M * 1.5, -d_E - eps)

    D = d_E + d_M
    L4x, L4y = newton_2d(D / 2 - d_E, D * math.sin(math.pi / 3))
    L5x, L5y = newton_2d(D / 2 - d_E, -D * math.sin(math.pi / 3))

    return {
        'L1': (L1, 0.0),
        'L2': (L2, 0.0),
        'L3': (L3, 0.0),
        'L4': (L4x, L4y),
        'L5': (L5x, L5y),
    }


if __name__ == '__main__':
    points = compute_lagrange_points()
    print("Точки Лагранжа (тыс. км):")
    print("-" * 55)
    for name, (x, y) in points.items():
        x_tkm, y_tkm = x / 1e6, y / 1e6
        if y == 0:
            print(f"  {name}: x = {x_tkm:.13f}")
        else:
            print(f"  {name}: x = {x_tkm:.11f}, y = {y_tkm:.9f}")

    print("\nПроверка (ускорение в точке, м/с²):")
    print("-" * 55)
    for name, (x, y) in points.items():
        ax, ay = accel_xy(x, y)
        print(f"  {name}: ax = {ax:.3e}, ay = {ay:.3e}")

    for lp, az_km in [('L1', 15000), ('L2', 20000)]:
        print(f"\n{'=' * 55}")
        print(f"Гало-орбита у {lp} (Ричардсон, 3-й порядок)")
        print("=" * 55)
        try:
            h = compute_halo_ic(Az_km=az_km, point=lp)
            print(f"  Az = {h['Az_km']:.0f} км, Ax = {h['Ax_km']:.0f} км")
            print(f"  γ = {h['_gamma']:.6f}")
            print(f"  c2 = {h['_c2']:.4f}, c3 = {h['_c3']:.4f}, c4 = {h['_c4']:.4f}")
            print(f"  λ = {h['_lam']:.4f}, k = {h['_k']:.4f}")
            print(f"  x0  = {h['x0']:.10f} тыс. км")
            print(f"  z0  = {h['z0']:.10f} тыс. км")
            print(f"  vy0 = {h['vy0']:.10f} км/с")
            print(f"  T   = {h['T_hours']:.2f} ч = {h['T_days']:.2f} дн")

            print(f"\n{'=' * 55}")
            print(f"Дифференциальная коррекция ({lp})")
            print("=" * 55)
            hc = correct_halo_ic(
                x0_m=h['x0'] * 1e6,
                z0_m=h['z0'] * 1e6,
                vy0_ms=h['vy0'] * 1e3,
                T_guess_s=h['T_hours'] * 3600,
            )
            print(f"  Сошлось за {hc['_iterations']} итераций (err={hc['_err']:.3e})")
            print(f"  x0  = {hc['x0']:.10f} тыс. км")
            print(f"  z0  = {hc['z0']:.10f} тыс. км")
            print(f"  vy0 = {hc['vy0']:.10f} км/с")
            print(f"  T   = {hc['T_hours']:.2f} ч = {hc['T_days']:.2f} дн")
            print(f"\nПресет для simulator.html:")
            print(f"  x0: {hc['x0']:.10f}, z0: {hc['z0']:.10f},")
            print(f"  vy0: {hc['vy0']:.10f},")
            print(f"  tEnd: {hc['T_hours']:.0f}")
        except (ValueError, RuntimeError) as e:
            print(f"  ОШИБКА: {e}")
