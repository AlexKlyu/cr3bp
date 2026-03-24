# Каталог экспериментов

Автономные Python-скрипты, воспроизводящие физику симулятора (`simulator_light.html`)
и генерирующие количественные результаты (CSV, PNG) для защиты.

## Физическая модель

Все скрипты используют **идентичные** уравнения и константы из симулятора:

```python
# Константы CR3BP (Земля-Луна)
G   = 6.674e-11       # м³/(кг·с²)
M_E = 5.972e24         # кг
M_M = 7.342e22         # кг
R_E = 6.371e6          # м (радиус Земли)
R_M = 1.737e6          # м (радиус Луны)
d_E = 4.67e6           # м (Земля от барицентра)
d_M = 3.828e8          # м (Луна от барицентра)
w   = 2.662e-6         # рад/с
```

### Ускорение (вращающаяся система координат)

```
ax = w²x + 2w·vy - GM_E·(x+d_E)/r_E³ - GM_M·(x-d_M)/r_M³
ay = w²y - 2w·vx - (GM_E/r_E³ + GM_M/r_M³)·y
az =              - (GM_E/r_E³ + GM_M/r_M³)·z
```

### Интеграторы

| Метод | Порядок | Описание |
|-------|---------|----------|
| Эйлер | O(h) | v += a·dt, r += v·dt |
| Верле полушаговый | O(h)* | r += v·dt + 0.5·a·dt², v_half, a_new, v_new. *Деградация из-за Кориолиса |
| Верле итерированный | O(h²) | То же + 3 итерации для неявного уравнения скорости |

\*Полушаговый Верле деградирует до O(h) в CR3BP из-за силы Кориолиса (2w×v).
Подробности — в `verlet_variants.pdf`.

### Адаптивный шаг

```
dt = dt_max / (1 + (v/v_ref) · (dt_max/dt_min - 1))
```
где v_ref = 1000 м/с.

### Интеграл Якоби

```
C_J = 2Ω - v²,  где Ω = 0.5·w²·(x²+y²) + GM_E/r_E + GM_M/r_M
```

Дрейф: `e = (C_J(t) - C_J(0)) / C_J(0)` — мера накопленной ошибки.

---

## Структура файлов

```
experiments/
├── GUIDE.md                        ← этот файл
├── FEEDBACK.md                     ← аудит результатов
├── engine.py                       ← общий модуль: константы, ускорение, интеграторы, Якоби
├── gen_notes.py                    ← генератор experiment_notes.pdf для всех экспериментов
├── verlet_variants.pdf             ← описание двух вариантов Верле (полушаг. vs итерир.)
│
├── 01_jacobi_drift/
│   ├── run.py                      ← дрейф Якоби: 6 конфигураций × 3 сценария
│   ├── experiment_notes.pdf
│   ├── drift_table.csv             ← 3 сценария × 6 конфигураций = 18 строк
│   ├── drift_halo.png              ← e(t), 2 панели (фикс | адапт)
│   ├── drift_freereturn.png
│   └── drift_chaos.png
│
├── 02_integrator_comparison/
│   ├── run.py                      ← log-log сходимость 3 интеграторов
│   ├── experiment_notes.pdf
│   ├── NOTES.md                    ← заметки о Верле и Кориолисе
│   ├── loglog.png                  ← три прямые с аппроксимацией наклонов
│   └── convergence_table.csv
│
├── 03_lagrange_points/
│   ├── run.py                      ← обёртка → presets/lagrange/lagrange.py
│   ├── experiment_notes.pdf
│   └── lagrange_points.csv         ← L1–L5 координаты + ошибки vs аналитика
│
├── 04_halo_orbit/
│   ├── run.py                      ← обёртка → compute_halo_ic() + correct_halo_ic()
│   ├── experiment_notes.pdf
│   ├── halo_ic.csv
│   └── halo_3d.png
│
├── 05_free_return/
│   ├── run.py                      ← жёстко заданные оптимальные НУ
│   ├── experiment_notes.pdf
│   ├── free_return_ic.csv
│   └── free_return_trajectory.png
│
├── 06_chaos_sensitivity/
│   ├── run.py                      ← 16 траекторий из L1, v=10 м/с
│   ├── experiment_notes.pdf
│   ├── chaos_fan.png
│   └── divergence.png
│
└── 07_thrust_maneuver/
    ├── run.py                      ← обёртка → find_thrust_params.py:simulate()
    ├── experiment_notes.pdf
    ├── thrust_comparison.png
    └── thrust_table.csv
```

---

## Описания экспериментов

### 01 — Дрейф интеграла Якоби

**Цель:** количественно измерить накопление ошибки для 6 конфигураций интегратора.

| Интегратор | Фикс. шаг | Адапт. шаг |
|---|---|---|
| Эйлер | ✓ | ✓ |
| Верле полушаговый | ✓ | ✓ |
| Верле итерированный | ✓ | ✓ |

**Сценарии:** гало-орбита L1, свободный возврат, хаос вблизи L1.

**Результаты (гало, dt=30 с):** Эйлер фикс: e=2.2×10⁻⁶, Верле итерир. адапт: e=1.9×10⁻¹².

**Выход:** drift_table.csv (18 строк), 3 PNG (по 2 панели: фикс | адапт).

### 02 — Сходимость интеграторов (log-log)

**Цель:** построить graph ошибки позиции vs шага dt в log-log масштабе.

- dt от 1 до 300 с (логарифмическая сетка, 20 точек)
- Для каждого dt: интеграция гало-орбиты 100 ч
- Три интегратора: Эйлер, Верле полушаговый, Верле итерированный
- Эталон: scipy RK45, rtol=10⁻¹²

**Результаты:** Эйлер: наклон 1.00, Верле полушаг.: наклон 1.00, Верле итерир.: наклон 1.97.

**Выход:** loglog.png (три прямые), convergence_table.csv.

### 03 — Точки Лагранжа

**Источник:** `presets/lagrange/lagrange.py` — `compute_lagrange_points()`, `bisect()`, `newton_2d()`.

**Результаты:** L1 = 323.696, L2 = 446.531, L3 = −386.651, L4 = (188.08, 332.92), L5 = (188.08, −332.92) тыс. км. Ошибка аналитики: 1977–2812 км.

**Выход:** lagrange_points.csv.

### 04 — Гало-орбита L1

**Источник:** `lagrange.py` → `compute_halo_ic()` + `correct_halo_ic()`.

**Результаты:** Az=15 000 км, T=293.4 ч, замыкание 3.6 км, дрейф Якоби 3.8×10⁻¹¹.

**Выход:** halo_ic.csv, halo_3d.png.

### 05 — Свободный возврат

**Начальные условия:** жёстко заданные оптимальные значения из find_free_return.py (угол 226.5°, v=10.779 км/с).

**Результаты:** пролёт Луны 3 399 км (t=63.6 ч), возврат к Земле 8 081 км (t=168.1 ч).

**Выход:** free_return_ic.csv, free_return_trajectory.png.

### 06 — Хаотическая чувствительность вблизи L1

**Цель:** показать хаотическую чувствительность — одна скорость, разные направления → разные судьбы.

- 16 траекторий из L1, v=10 м/с в 16 направлениях (шаг 22.5°)
- Время интеграции: 30 суток, Верле dt=30 с

**Результаты:** часть уходит к Луне (~380 tkm), часть петляет к Земле (~80–120 tkm).

**Выход:** chaos_fan.png, divergence.png.

### 07 — Манёвр с тягой

**Источник:** `presets/thrust_demos/find_thrust_params.py` — `simulate()`.

**Сценарии:**
1. Земля→Луна: 5 Н × 3 ч, Δv=108 м/с → без тяги не долетает, с тягой — пролёт Луны 2 494 км
2. Побег от L1: 0.05 Н × 2 ч, Δv=0.72 м/с → уход на 101 000 км

Кросс-валидация engine.py vs find_thrust_params.py:simulate(). Примечание: engine.py использует
итерированный Верле, find_thrust_params.py — полушаговый. Небольшие расхождения ожидаемы.

**Выход:** thrust_comparison.png, thrust_table.csv.

---

## Общий модуль `engine.py`

```python
# API:
# — Константы —
G, M_E, M_M, R_E, R_M, d_E, d_M, w, GM_E, GM_M

# — Физика —
compute_acceleration(x, y, z, vx, vy, vz, thrust=None) → (ax, ay, az)
compute_jacobi(x, y, z, vx, vy, vz) → float
cr3bp_eom(t, state) → dstate/dt          # для scipy.integrate.solve_ivp

# — Интеграторы (пошаговые) —
step_euler(state, dt, thrust=None) → state
step_verlet(state, dt, thrust=None) → state             # полушаговый (как в симуляторе)
step_verlet_iterated(state, dt, thrust=None) → state     # итерированный, O(h²)
adaptive_dt(v, dt_min, dt_max, v_ref=1000) → float

# — Высокий уровень —
run_trajectory(state0, T, dt, integrator='verlet',       # 'euler', 'verlet', 'verlet_half'
               adaptive=False, thrust=None) → dict
#   integrator='verlet' → итерированный (по умолчанию)
#   integrator='verlet_half' → полушаговый (как в симуляторе)
#   Возвращает: {t, pos, vel, jacobi, crush}
```

Все функции работают в **СИ** (метры, м/с, секунды). Перевод в тыс. км — только на выходе.

---

## Запуск

```bash
# Один эксперимент
python experiments/01_jacobi_drift/run.py

# Все эксперименты
for d in experiments/[0-9]*/; do python "$d/run.py"; done

# Генерация PDF-заметок
python experiments/gen_notes.py
```
