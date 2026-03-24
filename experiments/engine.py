"""
Общий физический движок CR3BP для экспериментов.

Источники:
  presets/lagrange/lagrange.py    -> константы, _cr3bp_eom()
  presets/hohmann/find_hohmann.py -> схема Верле
  sandbox/simulator_light.html   -> ускорение, Якоби, адаптивный шаг
"""

import math
import numpy as np

G = 6.674e-11
M_E = 5.972e24
M_M = 7.342e22
R_E = 6.371e6
R_M = 1.737e6
d_E = 4.67e6
d_M = 3.828e8
w = 2.662e-6

GM_E = G * M_E
GM_M = G * M_M
w2 = w * w
two_w = 2 * w


def compute_acceleration(x, y, z, vx, vy, vz, thrust=None):
    """
    Ускорение CR3BP во вращающейся системе координат (СИ).
    thrust: None или (ax_t, ay_t, az_t) в м/с².
    Возвращает (ax, ay, az).
    """
    dx_E = x + d_E
    dx_M = x - d_M
    r_E = math.sqrt(dx_E**2 + y**2 + z**2)
    r_M = math.sqrt(dx_M**2 + y**2 + z**2)

    K_E = GM_E / (r_E**3)
    K_M = GM_M / (r_M**3)
    K_sum = K_E + K_M

    ax = w2 * x + two_w * vy - K_E * dx_E - K_M * dx_M
    ay = w2 * y - two_w * vx - K_sum * y
    az = -K_sum * z

    if thrust is not None:
        ax += thrust[0]
        ay += thrust[1]
        az += thrust[2]

    return ax, ay, az


def compute_jacobi(x, y, z, vx, vy, vz):
    """Интеграл Якоби C_J = 2*Omega - v² (СИ)."""
    dx_E = x + d_E
    dx_M = x - d_M
    r_E = math.sqrt(dx_E**2 + y**2 + z**2)
    r_M = math.sqrt(dx_M**2 + y**2 + z**2)

    Omega = 0.5 * w2 * (x**2 + y**2) + GM_E / r_E + GM_M / r_M
    v2 = vx**2 + vy**2 + vz**2
    return 2 * Omega - v2


def cr3bp_eom(t, state):
    """Уравнения движения для scipy.integrate.solve_ivp. state = [x,y,z,vx,vy,vz] (СИ)."""
    x, y, z, vx, vy, vz = state
    ax, ay, az = compute_acceleration(x, y, z, vx, vy, vz)
    return [vx, vy, vz, ax, ay, az]


def step_euler(state, dt, thrust=None):
    """Шаг интегратора Эйлера. state = [x,y,z,vx,vy,vz] (СИ)."""
    x, y, z, vx, vy, vz = state
    ax, ay, az = compute_acceleration(x, y, z, vx, vy, vz, thrust)
    vx += ax * dt; vy += ay * dt; vz += az * dt
    x += vx * dt;  y += vy * dt;  z += vz * dt
    return [x, y, z, vx, vy, vz]


def step_verlet(state, dt, thrust=None):
    """
    Шаг Velocity Verlet (СИ).
    Полушаговые скорости для кориолисовых членов в новой позиции,
    как в simulator_light.html и find_hohmann.py.
    """
    x, y, z, vx, vy, vz = state
    ax, ay, az = compute_acceleration(x, y, z, vx, vy, vz, thrust)

    x1 = x + vx * dt + 0.5 * ax * dt * dt
    y1 = y + vy * dt + 0.5 * ay * dt * dt
    z1 = z + vz * dt + 0.5 * az * dt * dt

    vx_h = vx + 0.5 * ax * dt
    vy_h = vy + 0.5 * ay * dt
    vz_h = vz + 0.5 * az * dt

    ax1, ay1, az1 = compute_acceleration(x1, y1, z1, vx_h, vy_h, vz_h, thrust)

    vx += 0.5 * (ax + ax1) * dt
    vy += 0.5 * (ay + ay1) * dt
    vz += 0.5 * (az + az1) * dt

    return [x1, y1, z1, vx, vy, vz]


def step_verlet_iterated(state, dt, thrust=None, n_iter=3):
    """
    Итерированный Velocity Verlet (СИ).
    Решает неявное уравнение скорости итерациями (n_iter раз),
    корректно обрабатывая кориолисову силу 2ω×v.
    Сходимость O(h²) вместо O(h) у стандартного полушагового Верле.
    Цена: n_iter+1 вычислений силы на шаг вместо 2.
    """
    x, y, z, vx, vy, vz = state
    ax, ay, az = compute_acceleration(x, y, z, vx, vy, vz, thrust)

    x1 = x + vx * dt + 0.5 * ax * dt * dt
    y1 = y + vy * dt + 0.5 * ay * dt * dt
    z1 = z + vz * dt + 0.5 * az * dt * dt

    vx_new = vx + ax * dt
    vy_new = vy + ay * dt
    vz_new = vz + az * dt

    for _ in range(n_iter):
        ax1, ay1, az1 = compute_acceleration(x1, y1, z1, vx_new, vy_new, vz_new, thrust)
        vx_new = vx + 0.5 * (ax + ax1) * dt
        vy_new = vy + 0.5 * (ay + ay1) * dt
        vz_new = vz + 0.5 * (az + az1) * dt

    return [x1, y1, z1, vx_new, vy_new, vz_new]


def adaptive_dt(v, dt_min, dt_max, v_ref=1000.0):
    """Адаптивный шаг: меньше dt при больших скоростях."""
    ratio = v / v_ref
    dt_ratio = dt_max / dt_min - 1
    dt = dt_max / (1 + ratio * dt_ratio)
    return max(dt_min, min(dt_max, dt))


def run_trajectory(state0, T, dt, integrator='verlet', adaptive=False,
                   thrust=None, dt_min=1.0):
    """
    Интеграция траектории CR3BP.

    state0: [x,y,z,vx,vy,vz] в СИ (м, м/с)
    T: полное время (с)
    dt: шаг по времени (с), или dt_max при адаптивном шаге
    integrator: 'euler' или 'verlet'
    adaptive: адаптивный шаг по времени
    thrust: None или callable thrust(t) -> (ax,ay,az) в м/с²

    Возвращает dict:
      t: массив времён
      pos: Nx3 позиции (м)
      vel: Nx3 скорости (м/с)
      jacobi: массив интеграла Якоби
      crush: 0=ОК, 1=столкновение с Землёй, 2=столкновение с Луной
    """
    if integrator == 'verlet':
        step_fn = step_verlet_iterated
    elif integrator == 'verlet_half':
        step_fn = step_verlet
    else:
        step_fn = step_euler

    times = []
    positions = []
    velocities = []
    jacobi_vals = []
    crush = 0

    state = list(state0)
    t = 0.0

    while t < T:
        x, y, z, vx, vy, vz = state

        times.append(t)
        positions.append([x, y, z])
        velocities.append([vx, vy, vz])
        jacobi_vals.append(compute_jacobi(x, y, z, vx, vy, vz))

        dx_E = x + d_E
        dx_M = x - d_M
        r_E = math.sqrt(dx_E**2 + y**2 + z**2)
        r_M = math.sqrt(dx_M**2 + y**2 + z**2)
        if r_E <= R_E:
            crush = 1
            break
        if r_M <= R_M:
            crush = 2
            break

        if adaptive:
            v = math.sqrt(vx**2 + vy**2 + vz**2)
            dt_cur = adaptive_dt(v, dt_min, dt)
            dt_cur = min(dt_cur, T - t)
        else:
            dt_cur = min(dt, T - t)

        if dt_cur <= 0:
            break

        thr = None
        if thrust is not None:
            thr = thrust(t)

        state = step_fn(state, dt_cur, thr)
        t += dt_cur

    return {
        't': np.array(times),
        'pos': np.array(positions),
        'vel': np.array(velocities),
        'jacobi': np.array(jacobi_vals),
        'crush': crush,
    }
