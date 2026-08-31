"""
Convergence visualisation for the Lagrange-point algorithms (CR3BP Earth-Moon).
Interactive slider for stepping through the iterations.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import st_i18n

STRINGS = {
    "page_title":    {"ru": "Точки Лагранжа — сходимость", "en": "Lagrange points — convergence"},
    "title":         {"ru": "Визуализация сходимости: точки Лагранжа (CR3BP)",
                      "en": "Convergence visualisation: Lagrange points (CR3BP)"},
    "point":         {"ru": "Точка Лагранжа", "en": "Lagrange point"},
    "iteration":     {"ru": "Итерация", "en": "Iteration"},
    "map_header":    {"ru": "Карта системы Земля—Луна", "en": "Map of the Earth—Moon system"},
    "earth":         {"ru": "Земля", "en": "Earth"},
    "moon":          {"ru": "Луна", "en": "Moon"},
    "interval":      {"ru": "Интервал [a, b]", "en": "Interval [a, b]"},
    "iter_path":     {"ru": "Путь итераций", "en": "Iteration path"},
    "axis_x_tkm":    {"ru": "x (тыс. км)", "en": "x (10³ km)"},
    "axis_y_tkm":    {"ru": "y (тыс. км)", "en": "y (10³ km)"},
    "fx_title":      {"ru": "f(x) = ускорение на оси x — итерация",
                      "en": "f(x) = acceleration along x — iteration"},
    "axis_fx":       {"ru": "f(x) (м/с²)", "en": "f(x) (m/s²)"},
    "current":       {"ru": "текущая", "en": "current"},
    "conv_mid":      {"ru": "Сходимость середины интервала", "en": "Convergence of the interval midpoint"},
    "iter_table":    {"ru": "Таблица итераций", "en": "Iteration table"},
    "col_a_m":       {"ru": "a (м)", "en": "a (m)"},
    "col_b_m":       {"ru": "b (м)", "en": "b (m)"},
    "col_mid_m":     {"ru": "mid (м)", "en": "mid (m)"},
    "col_fmid":      {"ru": "f(mid) (м/с²)", "en": "f(mid) (m/s²)"},
    "col_a_tkm":     {"ru": "a (тыс. км)", "en": "a (10³ km)"},
    "col_b_tkm":     {"ru": "b (тыс. км)", "en": "b (10³ km)"},
    "col_mid_tkm":   {"ru": "mid (тыс. км)", "en": "mid (10³ km)"},
    "accel_abs":     {"ru": "|ускорение|", "en": "|acceleration|"},
    "conv_accel":    {"ru": "Сходимость |ускорения|", "en": "Convergence of |acceleration|"},
    "axis_accel":    {"ru": "|a| (м/с²)", "en": "|a| (m/s²)"},
    "iterations":    {"ru": "Итерации", "en": "Iterations"},
    "closeup":       {"ru": "Крупный план: путь →", "en": "Close-up: path →"},
    "col_x_m":       {"ru": "x (м)", "en": "x (m)"},
    "col_y_m":       {"ru": "y (м)", "en": "y (m)"},
    "col_ax":        {"ru": "ax (м/с²)", "en": "ax (m/s²)"},
    "col_ay":        {"ru": "ay (м/с²)", "en": "ay (m/s²)"},
    "col_x_tkm":     {"ru": "x (тыс. км)", "en": "x (10³ km)"},
    "col_y_tkm":     {"ru": "y (тыс. км)", "en": "y (10³ km)"},
    "col_a_abs":     {"ru": "|a| (м/с²)", "en": "|a| (m/s²)"},
}

LANG = st_i18n.resolve_lang()
t = st_i18n.translator(STRINGS, LANG)

import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lagrange import (
    d_E, d_M,
    accel_x, accel_xy,
    bisect_trace, newton_2d_trace,
    compute_lagrange_points,
)

st.set_page_config(page_title=t("page_title"), layout="wide")

LANG = st_i18n.language_picker(LANG)
t = st_i18n.translator(STRINGS, LANG)

st.title(t("title"))


def to_tkm(v):
    """Metres -> 10^3 km."""
    return v / 1e6


points = compute_lagrange_points()

eps = 1e3
bisect_params = {
    'L1': (-d_E + eps, d_M - eps),
    'L2': (d_M + eps, d_M * 1.5),
    'L3': (-d_M * 1.5, -d_E - eps),
}
D = d_E + d_M
newton_params = {
    'L4': (D / 2 - d_E, D * math.sin(math.pi / 3)),
    'L5': (D / 2 - d_E, -D * math.sin(math.pi / 3)),
}

selected = st.sidebar.selectbox(t("point"), ["L1", "L2", "L3", "L4", "L5"])

if selected in bisect_params:
    a0, b0 = bisect_params[selected]
    trace = bisect_trace(a0, b0)
else:
    x0, y0 = newton_params[selected]
    trace = newton_2d_trace(x0, y0)

max_iter = len(trace) - 1
step = st.sidebar.number_input(t("iteration"), 0, max_iter, 0, step=1)

st.subheader(t("map_header"))

map_fig = go.Figure()

map_fig.add_trace(go.Scatter(
    x=[to_tkm(-d_E)], y=[0], mode='markers+text',
    marker=dict(size=16, color='deepskyblue'), text=[t("earth")], textposition='bottom center',
    name=t("earth"),
))
map_fig.add_trace(go.Scatter(
    x=[to_tkm(d_M)], y=[0], mode='markers+text',
    marker=dict(size=12, color='gray'), text=[t("moon")], textposition='bottom center',
    name=t("moon"),
))

for name, (px, py) in points.items():
    map_fig.add_trace(go.Scatter(
        x=[to_tkm(px)], y=[to_tkm(py)], mode='markers+text',
        marker=dict(size=8, color='orange', symbol='diamond'),
        text=[name], textposition='top center', name=name,
    ))

if selected in bisect_params:
    cur_x, cur_y = trace[step][2], 0.0
    a_cur, b_cur = trace[step][0], trace[step][1]
    map_fig.add_trace(go.Scatter(
        x=[to_tkm(a_cur), to_tkm(b_cur)], y=[0, 0],
        mode='lines', line=dict(color='orange', width=6),
        name=t("interval"),
    ))
else:
    cur_x, cur_y = trace[step][0], trace[step][1]
    xs = [to_tkm(trace[i][0]) for i in range(step + 1)]
    ys = [to_tkm(trace[i][1]) for i in range(step + 1)]
    map_fig.add_trace(go.Scatter(
        x=xs, y=ys, mode='lines+markers',
        marker=dict(size=4, color='green'), line=dict(dash='dot', color='green'),
        name=t("iter_path"),
    ))

map_fig.add_trace(go.Scatter(
    x=[to_tkm(cur_x)], y=[to_tkm(cur_y)],
    mode='markers', marker=dict(size=16, color='red', symbol='star'),
    name=f'{t("iteration")} {step}',
))

lx, ly = points[selected]
full_xs = [to_tkm(-d_E), to_tkm(d_M), to_tkm(cur_x), to_tkm(lx)]
full_ys = [0, 0, to_tkm(cur_y), to_tkm(ly)]

if selected not in bisect_params:
    full_xs += [to_tkm(trace[i][0]) for i in range(step + 1)]
    full_ys += [to_tkm(trace[i][1]) for i in range(step + 1)]
    key_xs, key_ys = full_xs, full_ys
else:
    a_tkm, b_tkm = to_tkm(trace[step][0]), to_tkm(trace[step][1])
    full_span = to_tkm(d_M) - to_tkm(-d_E)
    ab_span = b_tkm - a_tkm
    if ab_span < full_span * 0.2:
        key_xs = [a_tkm, b_tkm, to_tkm(lx)]
        key_ys = [0, to_tkm(ly)]
    else:
        key_xs = full_xs + [a_tkm, b_tkm]
        key_ys = full_ys

x_min, x_max = min(key_xs), max(key_xs)
y_min, y_max = min(key_ys), max(key_ys)
pad_x = max((x_max - x_min) * 0.15, 10)
pad_y = max((y_max - y_min) * 0.15, 10)

map_fig.update_layout(
    xaxis_title=t("axis_x_tkm"), yaxis_title=t("axis_y_tkm"),
    height=500, showlegend=True,
    xaxis=dict(range=[x_min - pad_x, x_max + pad_x]),
    yaxis=dict(range=[y_min - pad_y, y_max + pad_y], scaleanchor='x'),
)
st.plotly_chart(map_fig, use_container_width=True)

if selected in bisect_params:
    cur = trace[step]
    a_cur, b_cur, m_cur, f_cur = cur

    col1, col2 = st.columns(2)

    x_range = np.linspace(a0, b0, 500)
    f_vals = [accel_x(xi) for xi in x_range]

    fx_fig = go.Figure()
    fx_fig.add_trace(go.Scatter(
        x=[to_tkm(xi) for xi in x_range], y=f_vals,
        mode='lines', name='f(x)', line=dict(color='royalblue'),
    ))
    fx_fig.add_hline(y=0, line_dash='dash', line_color='gray')
    fx_fig.add_vrect(x0=to_tkm(a_cur), x1=to_tkm(b_cur),
                     fillcolor='orange', opacity=0.15, line_width=0)
    fx_fig.add_vline(x=to_tkm(a_cur), line_dash='dot', line_color='orange')
    fx_fig.add_vline(x=to_tkm(b_cur), line_dash='dot', line_color='orange')
    fx_fig.add_trace(go.Scatter(
        x=[to_tkm(m_cur)], y=[f_cur],
        mode='markers', marker=dict(size=12, color='red', symbol='x'),
        name=f'mid ({t("iteration").lower()} {step})',
    ))
    fx_fig.update_layout(
        title=f'{t("fx_title")} {step}',
        xaxis_title=t("axis_x_tkm"), yaxis_title=t("axis_fx"), height=450,
    )
    with col1:
        st.plotly_chart(fx_fig, use_container_width=True)

    iters_so_far = list(range(step + 1))
    m_vals = [to_tkm(trace[i][2]) for i in iters_so_far]
    a_vals = [to_tkm(trace[i][0]) for i in iters_so_far]
    b_vals = [to_tkm(trace[i][1]) for i in iters_so_far]

    conv_fig = go.Figure()
    conv_fig.add_trace(go.Scatter(x=iters_so_far, y=a_vals, mode='lines',
                                  name='a', line=dict(dash='dash', color='orange')))
    conv_fig.add_trace(go.Scatter(x=iters_so_far, y=b_vals, mode='lines',
                                  name='b', line=dict(dash='dash', color='orange')))
    conv_fig.add_trace(go.Scatter(x=iters_so_far, y=m_vals, mode='lines+markers',
                                  name='midpoint', marker=dict(size=3), line=dict(color='royalblue')))
    conv_fig.add_trace(go.Scatter(
        x=[step], y=[to_tkm(m_cur)],
        mode='markers', marker=dict(size=12, color='red', symbol='circle'),
        name=t("current"), showlegend=False,
    ))
    conv_fig.update_layout(
        title=t("conv_mid"),
        xaxis_title=t("iteration"), yaxis_title=t("axis_x_tkm"),
        xaxis=dict(range=[0, max_iter]), height=450,
    )
    with col2:
        st.plotly_chart(conv_fig, use_container_width=True)

    st.subheader(f'{t("iter_table")} (0..{step})')
    rows = trace[:step + 1]
    df = pd.DataFrame(rows, columns=[t("col_a_m"), t("col_b_m"), t("col_mid_m"), t("col_fmid")])
    df.index.name = t("iteration")
    df[t("col_a_tkm")] = df[t("col_a_m")] / 1e6
    df[t("col_b_tkm")] = df[t("col_b_m")] / 1e6
    df[t("col_mid_tkm")] = df[t("col_mid_m")] / 1e6
    st.dataframe(df[[t("col_a_tkm"), t("col_b_tkm"), t("col_mid_tkm"), t("col_fmid")]],
                 use_container_width=True, height=300)

else:
    cur = trace[step]
    x_cur, y_cur, ax_cur, ay_cur = cur

    col1, col2 = st.columns(2)

    iters_so_far = list(range(step + 1))
    accel_mag = [math.sqrt(trace[i][2]**2 + trace[i][3]**2) for i in iters_so_far]

    conv_fig = go.Figure()
    conv_fig.add_trace(go.Scatter(
        x=iters_so_far, y=accel_mag, mode='lines+markers',
        name=t("accel_abs"), marker=dict(size=5), line=dict(color='royalblue'),
    ))
    cur_mag = math.sqrt(ax_cur**2 + ay_cur**2)
    conv_fig.add_trace(go.Scatter(
        x=[step], y=[cur_mag],
        mode='markers', marker=dict(size=12, color='red'),
        name=t("current"), showlegend=False,
    ))
    conv_fig.update_layout(
        title=t("conv_accel"),
        xaxis_title=t("iteration"), yaxis_title=t("axis_accel"),
        yaxis_type='log', xaxis=dict(range=[0, max_iter]), height=450,
    )
    with col1:
        st.plotly_chart(conv_fig, use_container_width=True)

    path_xs = [to_tkm(trace[i][0]) for i in range(step + 1)]
    path_ys = [to_tkm(trace[i][1]) for i in range(step + 1)]
    path_fig = go.Figure()
    path_fig.add_trace(go.Scatter(
        x=path_xs, y=path_ys, mode='lines+markers+text',
        text=[str(i) for i in range(step + 1)], textposition='top right',
        marker=dict(size=6, color='green'), name=t("iterations"),
    ))
    px, py = points[selected]
    path_fig.add_trace(go.Scatter(
        x=[to_tkm(px)], y=[to_tkm(py)], mode='markers',
        marker=dict(size=12, color='red', symbol='star'), name=selected,
    ))
    path_fig.update_layout(
        title=f'{t("closeup")} {selected}',
        xaxis_title=t("axis_x_tkm"), yaxis_title=t("axis_y_tkm"),
        yaxis=dict(scaleanchor='x'), height=450,
    )
    with col2:
        st.plotly_chart(path_fig, use_container_width=True)

    st.subheader(f'{t("iter_table")} (0..{step})')
    rows = trace[:step + 1]
    df = pd.DataFrame(rows, columns=[t("col_x_m"), t("col_y_m"), t("col_ax"), t("col_ay")])
    df.index.name = t("iteration")
    df[t("col_x_tkm")] = df[t("col_x_m")] / 1e6
    df[t("col_y_tkm")] = df[t("col_y_m")] / 1e6
    df[t("col_a_abs")] = np.sqrt(df[t("col_ax")]**2 + df[t("col_ay")]**2)
    st.dataframe(df[[t("col_x_tkm"), t("col_y_tkm"), t("col_ax"), t("col_ay"), t("col_a_abs")]],
                 use_container_width=True, height=300)
