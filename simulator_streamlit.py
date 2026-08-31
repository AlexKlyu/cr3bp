import json
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


import st_i18n

STRINGS = {
    "page_title":     {"ru": "CR3BP Симулятор", "en": "CR3BP Simulator"},
    "params":         {"ru": "Параметры", "en": "Parameters"},
    "pos_header":     {"ru": "Начальное положение (тыс. км)", "en": "Initial position (10³ km)"},
    "vel_header":     {"ru": "Начальная скорость (км/с)", "en": "Initial velocity (km/s)"},
    "method_header":  {"ru": "Метод интегрирования", "en": "Integration method"},
    "method":         {"ru": "Метод", "en": "Method"},
    "simtime_header": {"ru": "Время симуляции", "en": "Simulation time"},
    "time_s":         {"ru": "Время (с)", "en": "Time (s)"},
    "engine_header":  {"ru": "Двигатель", "en": "Engine"},
    "engine_enable":  {"ru": "Включить двигатель", "en": "Enable engine"},
    "fx":             {"ru": "Fx (Н)", "en": "Fx (N)"},
    "fy":             {"ru": "Fy (Н)", "en": "Fy (N)"},
    "fz":             {"ru": "Fz (Н)", "en": "Fz (N)"},
    "mass":           {"ru": "Масса (кг)", "en": "Mass (kg)"},
    "engine_on":      {"ru": "Вкл (с)", "en": "On (s)"},
    "engine_off":     {"ru": "Выкл (с)", "en": "Off (s)"},
    "spinner":        {"ru": "Вычисление траектории...", "en": "Computing trajectory..."},
    "results_title":  {"ru": "Результаты симуляции", "en": "Simulation results"},
    "flight_time":    {"ru": "Время полёта", "en": "Flight time"},
    "unit_s":         {"ru": "с", "en": "s"},
    "points":         {"ru": "Точек траектории", "en": "Trajectory points"},
    "crush_earth":    {"ru": "Столкновение с Землёй", "en": "Collision with Earth"},
    "crush_moon":     {"ru": "Столкновение с Луной", "en": "Collision with the Moon"},
    "status":         {"ru": "Статус", "en": "Status"},
    "motion_params":  {"ru": "Параметры движения", "en": "Motion parameters"},
    "plot_coords":    {"ru": "Координаты (км)", "en": "Coordinates (km)"},
    "plot_vel":       {"ru": "Скорости (м/с)", "en": "Velocities (m/s)"},
    "plot_mod":       {"ru": "Модули: расстояние (км), скорость (м/с), ускорение (м/с²)",
                       "en": "Magnitudes: distance (km), velocity (m/s), acceleration (m/s²)"},
    "axis_t":         {"ru": "t (с)", "en": "t (s)"},
}

LANG = st_i18n.resolve_lang()
t = st_i18n.translator(STRINGS, LANG)


with open("config.json", "r") as f:
    config = json.load(f)

DEFAULT_X0_TKM = config["initial_position_tkm"]["x0"]
DEFAULT_Y0_TKM = config["initial_position_tkm"]["y0"]
DEFAULT_Z0_TKM = config["initial_position_tkm"]["z0"]
DEFAULT_VX0_KMS = config["initial_velocity_kms"]["vx0"]
DEFAULT_VY0_KMS = config["initial_velocity_kms"]["vy0"]
DEFAULT_VZ0_KMS = config["initial_velocity_kms"]["vz0"]
DEFAULT_A0_X = config["initial_acceleration"]["a0_x"]
DEFAULT_A0_Y = config["initial_acceleration"]["a0_y"]
DEFAULT_A0_Z = config["initial_acceleration"]["a0_z"]


G = 6.674e-11
M_E = 5.972e24
M_M = 7.342e22
R_E = 6371e3
R_M = 1737e3
d_E = 4.67e6
d_M = 3.828e8
w = 2.662e-6


def compute_trajectory(x0, y0, z0, vx0, vy0, vz0, t_end, dt=1.0,
                       F_x=0.0, F_y=0.0, F_z=0.0, M_0=1.0, t_on=0.0, t_off=0.0,
                       a0_x=0.0, a0_y=0.0, a0_z=0.0, method='Verlet'):
    """
    Numerical integration of the CR3BP (velocity Verlet).
    Optimised by pre-computing constants.
    """
    n_steps = int(t_end / dt) + 1

    GM_E = G * M_E
    GM_M = G * M_M
    w2 = w * w
    two_w = 2 * w
    dt2_half = 0.5 * dt * dt

    state = np.array([x0, y0, z0, vx0, vy0, vz0], dtype=np.float64)

    results = {
        'time': [], 'cx': [], 'cy': [], 'cz': [],
        'velx': [], 'vely': [], 'velz': [],
        'radius': [], 'fullvelocity': [], 'fullacceleration': []
    }

    crush = 0

    for i in range(n_steps):
        t = i * dt
        x, y, z, vx, vy, vz = state

        dx_E = x + d_E
        dx_M = x - d_M
        r_E = np.sqrt(dx_E*dx_E + y*y + z*z)
        r_M = np.sqrt(dx_M*dx_M + y*y + z*z)

        r_E3 = r_E * r_E * r_E
        r_M3 = r_M * r_M * r_M
        K_E = GM_E / r_E3
        K_M = GM_M / r_M3
        K_sum = K_E + K_M

        if t_on <= t <= t_off:
            Fx, Fy, Fz = F_x / M_0, F_y / M_0, F_z / M_0
        else:
            Fx, Fy, Fz = 0.0, 0.0, 0.0

        ax = w2*x + two_w*vy - K_E*dx_E - K_M*dx_M + Fx + a0_x
        ay = w2*y - two_w*vx - K_sum*y + Fy + a0_y
        az = -K_sum*z + Fz + a0_z

        results['time'].append(t)
        results['cx'].append(x)
        results['cy'].append(y)
        results['cz'].append(z)
        results['velx'].append(vx)
        results['vely'].append(vy)
        results['velz'].append(vz)
        results['radius'].append(np.sqrt(x*x + y*y + z*z))
        results['fullvelocity'].append(np.sqrt(vx*vx + vy*vy + vz*vz))
        results['fullacceleration'].append(np.sqrt(ax*ax + ay*ay + az*az))

        if r_E <= R_E:
            crush = 1
            break
        if r_M <= R_M:
            crush = 2
            break

        if method == 'Euler':
            state[0] = x + vx*dt
            state[1] = y + vy*dt
            state[2] = z + vz*dt
            state[3] = vx + ax*dt
            state[4] = vy + ay*dt
            state[5] = vz + az*dt
        else:
            x_new = x + vx*dt + ax*dt2_half
            y_new = y + vy*dt + ay*dt2_half
            z_new = z + vz*dt + az*dt2_half

            dx_E_new = x_new + d_E
            dx_M_new = x_new - d_M
            r_E_new = np.sqrt(dx_E_new*dx_E_new + y_new*y_new + z_new*z_new)
            r_M_new = np.sqrt(dx_M_new*dx_M_new + y_new*y_new + z_new*z_new)
            K_E_new = GM_E / (r_E_new * r_E_new * r_E_new)
            K_M_new = GM_M / (r_M_new * r_M_new * r_M_new)
            K_sum_new = K_E_new + K_M_new

            vx_half = vx + ax * 0.5 * dt
            vy_half = vy + ay * 0.5 * dt

            t_new = (i + 1) * dt
            if t_on <= t_new <= t_off:
                Fx_new, Fy_new, Fz_new = F_x / M_0, F_y / M_0, F_z / M_0
            else:
                Fx_new, Fy_new, Fz_new = 0.0, 0.0, 0.0

            ax_new = w2*x_new + two_w*vy_half - K_E_new*dx_E_new - K_M_new*dx_M_new + Fx_new + a0_x
            ay_new = w2*y_new - two_w*vx_half - K_sum_new*y_new + Fy_new + a0_y
            az_new = -K_sum_new*z_new + Fz_new + a0_z

            state[0] = x_new
            state[1] = y_new
            state[2] = z_new
            state[3] = vx + 0.5*(ax + ax_new)*dt
            state[4] = vy + 0.5*(ay + ay_new)*dt
            state[5] = vz + 0.5*(az + az_new)*dt

    for key in results:
        results[key] = np.array(results[key])

    results['crush'] = crush
    results['n_points'] = len(results['time'])

    return results


def create_2d_plots(data):
    """2D parameter plots."""

    time = data['time']

    fig_pos = make_subplots(rows=1, cols=3, subplot_titles=('X(t)', 'Y(t)', 'Z(t)'))
    fig_pos.add_trace(go.Scatter(x=time, y=data['cx']/1000, name='X', line=dict(color='red')), row=1, col=1)
    fig_pos.add_trace(go.Scatter(x=time, y=data['cy']/1000, name='Y', line=dict(color='green')), row=1, col=2)
    fig_pos.add_trace(go.Scatter(x=time, y=data['cz']/1000, name='Z', line=dict(color='blue')), row=1, col=3)
    fig_pos.update_layout(height=300, title_text=t("plot_coords"), showlegend=False)
    fig_pos.update_xaxes(title_text=t("axis_t"))

    fig_vel = make_subplots(rows=1, cols=3, subplot_titles=('Vx(t)', 'Vy(t)', 'Vz(t)'))
    fig_vel.add_trace(go.Scatter(x=time, y=data['velx'], name='Vx', line=dict(color='red')), row=1, col=1)
    fig_vel.add_trace(go.Scatter(x=time, y=data['vely'], name='Vy', line=dict(color='green')), row=1, col=2)
    fig_vel.add_trace(go.Scatter(x=time, y=data['velz'], name='Vz', line=dict(color='blue')), row=1, col=3)
    fig_vel.update_layout(height=300, title_text=t("plot_vel"), showlegend=False)
    fig_vel.update_xaxes(title_text=t("axis_t"))

    fig_mod = make_subplots(rows=1, cols=3, subplot_titles=('|R|(t)', '|V|(t)', '|A|(t)'))
    fig_mod.add_trace(go.Scatter(x=time, y=data['radius']/1000, name='R', line=dict(color='cyan')), row=1, col=1)
    fig_mod.add_trace(go.Scatter(x=time, y=data['fullvelocity'], name='V', line=dict(color='orange')), row=1, col=2)
    fig_mod.add_trace(go.Scatter(x=time, y=data['fullacceleration'], name='A', line=dict(color='magenta')), row=1, col=3)
    fig_mod.update_layout(height=300, title_text=t("plot_mod"), showlegend=False)
    fig_mod.update_xaxes(title_text=t("axis_t"))

    return fig_pos, fig_vel, fig_mod


st.set_page_config(page_title=t("page_title"), layout="wide")

LANG = st_i18n.language_picker(LANG)
t = st_i18n.translator(STRINGS, LANG)

st.sidebar.title(t("params"))

st.sidebar.subheader(t("pos_header"))
x0_tkm = st.sidebar.number_input("x₀", value=DEFAULT_X0_TKM, step=0.1, format="%.3f")
y0_tkm = st.sidebar.number_input("y₀", value=DEFAULT_Y0_TKM, step=0.1, format="%.3f")
z0_tkm = st.sidebar.number_input("z₀", value=DEFAULT_Z0_TKM, step=0.1, format="%.3f")

st.sidebar.subheader(t("vel_header"))
vx0_kms = st.sidebar.number_input("Vx₀", value=DEFAULT_VX0_KMS, step=0.1, format="%.3f")
vy0_kms = st.sidebar.number_input("Vy₀", value=DEFAULT_VY0_KMS, step=0.1, format="%.3f")
vz0_kms = st.sidebar.number_input("Vz₀", value=DEFAULT_VZ0_KMS, step=0.1, format="%.3f")

st.sidebar.subheader(t("method_header"))
integrator = st.sidebar.radio(t("method"), ["Verlet", "Euler"], horizontal=True)

st.sidebar.subheader(t("simtime_header"))
t_end = st.sidebar.slider(t("time_s"), 100, 10000, 3600, 100)

st.sidebar.subheader(t("engine_header"))
use_engine = st.sidebar.checkbox(t("engine_enable"))
if use_engine:
    F_x = st.sidebar.number_input(t("fx"), value=0, step=100)
    F_y = st.sidebar.number_input(t("fy"), value=1000, step=100)
    F_z = st.sidebar.number_input(t("fz"), value=0, step=100)
    M_0 = st.sidebar.number_input(t("mass"), value=1000, min_value=1, step=100)
    t_on = st.sidebar.number_input(t("engine_on"), value=0, step=100)
    t_off = st.sidebar.number_input(t("engine_off"), value=1000, step=100)
else:
    F_x, F_y, F_z, M_0, t_on, t_off = 0, 0, 0, 1, 0, 0

x0 = x0_tkm * 1e6
y0 = y0_tkm * 1e6
z0 = z0_tkm * 1e6
vx0 = vx0_kms * 1000
vy0 = vy0_kms * 1000
vz0 = vz0_kms * 1000

with st.spinner(t("spinner")):
    result = compute_trajectory(
        x0, y0, z0, vx0, vy0, vz0, t_end,
        F_x=F_x, F_y=F_y, F_z=F_z, M_0=M_0, t_on=t_on, t_off=t_off,
        a0_x=DEFAULT_A0_X, a0_y=DEFAULT_A0_Y, a0_z=DEFAULT_A0_Z,
        method=integrator
    )

if result:

    st.title(t("results_title"))

    col1, col2, col3 = st.columns(3)
    col1.metric(t("flight_time"), f"{result['time'][-1]:.0f} {t('unit_s')}")
    col2.metric(t("points"), f"{result['n_points']}")

    status = "OK"
    if result['crush'] == 1:
        status = t("crush_earth")
    elif result['crush'] == 2:
        status = t("crush_moon")
    col3.metric(t("status"), status)

    st.subheader(t("motion_params"))
    fig_pos, fig_vel, fig_mod = create_2d_plots(result)
    st.plotly_chart(fig_pos, use_container_width=True)
    st.plotly_chart(fig_vel, use_container_width=True)
    st.plotly_chart(fig_mod, use_container_width=True)
