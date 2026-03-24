"""
Визуализация сходимости алгоритмов вычисления точек Лагранжа (CR3BP Земля-Луна).
Интерактивный слайдер для пошагового просмотра итераций.
"""

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

st.set_page_config(page_title="Точки Лагранжа — сходимость", layout="wide")
st.title("Визуализация сходимости: точки Лагранжа (CR3BP)")


def to_tkm(v):
    """Метры → тыс. км."""
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

selected = st.sidebar.selectbox("Точка Лагранжа", ["L1", "L2", "L3", "L4", "L5"])

if selected in bisect_params:
    a0, b0 = bisect_params[selected]
    trace = bisect_trace(a0, b0)
else:
    x0, y0 = newton_params[selected]
    trace = newton_2d_trace(x0, y0)

max_iter = len(trace) - 1
step = st.sidebar.number_input("Итерация", 0, max_iter, 0, step=1)

st.subheader("Карта системы Земля—Луна")

map_fig = go.Figure()

map_fig.add_trace(go.Scatter(
    x=[to_tkm(-d_E)], y=[0], mode='markers+text',
    marker=dict(size=16, color='deepskyblue'), text=['Земля'], textposition='bottom center',
    name='Земля',
))
map_fig.add_trace(go.Scatter(
    x=[to_tkm(d_M)], y=[0], mode='markers+text',
    marker=dict(size=12, color='gray'), text=['Луна'], textposition='bottom center',
    name='Луна',
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
        name='Интервал [a, b]',
    ))
else:
    cur_x, cur_y = trace[step][0], trace[step][1]
    xs = [to_tkm(trace[i][0]) for i in range(step + 1)]
    ys = [to_tkm(trace[i][1]) for i in range(step + 1)]
    map_fig.add_trace(go.Scatter(
        x=xs, y=ys, mode='lines+markers',
        marker=dict(size=4, color='green'), line=dict(dash='dot', color='green'),
        name='Путь итераций',
    ))

map_fig.add_trace(go.Scatter(
    x=[to_tkm(cur_x)], y=[to_tkm(cur_y)],
    mode='markers', marker=dict(size=16, color='red', symbol='star'),
    name=f'Итерация {step}',
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
    xaxis_title='x (тыс. км)', yaxis_title='y (тыс. км)',
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
        name=f'mid (итерация {step})',
    ))
    fx_fig.update_layout(
        title=f'f(x) = ускорение на оси x — итерация {step}',
        xaxis_title='x (тыс. км)', yaxis_title='f(x) (м/с²)', height=450,
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
        name='текущая', showlegend=False,
    ))
    conv_fig.update_layout(
        title='Сходимость середины интервала',
        xaxis_title='Итерация', yaxis_title='x (тыс. км)',
        xaxis=dict(range=[0, max_iter]), height=450,
    )
    with col2:
        st.plotly_chart(conv_fig, use_container_width=True)

    st.subheader(f"Таблица итераций (0..{step})")
    rows = trace[:step + 1]
    df = pd.DataFrame(rows, columns=['a (м)', 'b (м)', 'mid (м)', 'f(mid) (м/с²)'])
    df.index.name = 'Итерация'
    df['a (тыс. км)'] = df['a (м)'] / 1e6
    df['b (тыс. км)'] = df['b (м)'] / 1e6
    df['mid (тыс. км)'] = df['mid (м)'] / 1e6
    st.dataframe(df[['a (тыс. км)', 'b (тыс. км)', 'mid (тыс. км)', 'f(mid) (м/с²)']],
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
        name='|ускорение|', marker=dict(size=5), line=dict(color='royalblue'),
    ))
    cur_mag = math.sqrt(ax_cur**2 + ay_cur**2)
    conv_fig.add_trace(go.Scatter(
        x=[step], y=[cur_mag],
        mode='markers', marker=dict(size=12, color='red'),
        name='текущая', showlegend=False,
    ))
    conv_fig.update_layout(
        title='Сходимость |ускорения|',
        xaxis_title='Итерация', yaxis_title='|a| (м/с²)',
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
        marker=dict(size=6, color='green'), name='Итерации',
    ))
    px, py = points[selected]
    path_fig.add_trace(go.Scatter(
        x=[to_tkm(px)], y=[to_tkm(py)], mode='markers',
        marker=dict(size=12, color='red', symbol='star'), name=selected,
    ))
    path_fig.update_layout(
        title=f'Крупный план: путь → {selected}',
        xaxis_title='x (тыс. км)', yaxis_title='y (тыс. км)',
        yaxis=dict(scaleanchor='x'), height=450,
    )
    with col2:
        st.plotly_chart(path_fig, use_container_width=True)

    st.subheader(f"Таблица итераций (0..{step})")
    rows = trace[:step + 1]
    df = pd.DataFrame(rows, columns=['x (м)', 'y (м)', 'ax (м/с²)', 'ay (м/с²)'])
    df.index.name = 'Итерация'
    df['x (тыс. км)'] = df['x (м)'] / 1e6
    df['y (тыс. км)'] = df['y (м)'] / 1e6
    df['|a| (м/с²)'] = np.sqrt(df['ax (м/с²)']**2 + df['ay (м/с²)']**2)
    st.dataframe(df[['x (тыс. км)', 'y (тыс. км)', 'ax (м/с²)', 'ay (м/с²)', '|a| (м/с²)']],
                 use_container_width=True, height=300)
