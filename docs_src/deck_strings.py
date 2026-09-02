# -*- coding: utf-8 -*-
"""Russian -> English strings for public/presentation_2503.pptx.

Keyed by the exact paragraph text as it appears in the deck (whitespace
normalised). Anything missing is reported by translate_deck.py rather than
silently left in Russian.
"""

T = {
# slide 1 — title
"Численное интегрирование": "Numerical integration",
"в ограниченной задаче трёх тел": "in the restricted three-body problem",
"Создание инструмента для изучения движения тела в системе Земля-Луна":
    "Building a tool for studying motion in the Earth–Moon system",
"Ключников Александр": "Alexander Klyuchnikov",
"Научный руководитель": "Supervisor",
"Бабинцев В.А., доцент каф. общей физики МФТИ":
    "V. A. Babintsev, Associate Professor, Dept. of General Physics, MIPT",
"Олимпиада Старт в науку": "“Start in Science” Olympiad",
"МФТИ, 2026": "MIPT, 2026",

# slide 2 — introduction
"Введение в тему": "Introduction",
"Задача трёх тел": "The three-body problem",
"Классическая задача": "A classical problem",
"небесной механики.": "of celestial mechanics.",
"Аналитического решения": "No analytical solution",
"не существует": "exists",
"КОЗТТ": "CR3BP",
"Два массивных тела": "Two massive bodies",
"движутся по окружности.": "move on circular orbits.",
"Третье тело — малой массы": "The third body has negligible mass",
"Вращающаяся система": "Rotating frame",
"Земля и Луна неподвижны.": "The Earth and Moon are stationary.",
"Появляются ускорение Кориолиса": "Coriolis and centrifugal",
"и центробежное": "accelerations appear",
"Круговая ограниченная задача трёх тел — базовая модель для изучения динамики в системе Земля–Луна":
    "The circular restricted three-body problem is the basic model for studying dynamics in the Earth–Moon system",

# slide 3 — relevance
"Актуальность и аналоги": "Relevance and existing tools",
"КОЗТТ — базовая модель динамики Земля–Луна. Аналитического решения не существует":
    "The CR3BP is the basic model of Earth–Moon dynamics. No analytical solution exists",
"Инструмент": "Tool",
"Тяга": "Thrust",
"Якоби": "Jacobi",
"Веб": "Web",
"«Орбита. Челлендж»": "“Orbit. Challenge”",
"Я искал готовый симулятор — и не нашёл":
    "I looked for an existing simulator and found none",

# slide 4 — features
"●  3D визуализация системы Земля–Луна": "●  3D visualisation of the Earth–Moon system",
"●  Три интегратора с контролем Якоби": "●  Three integrators with Jacobi-based accuracy control",
"●  Двигатель с настройкой окна тяги": "●  Engine with a configurable thrust window",
"●  Точки Лагранжа L1–L5": "●  Lagrange points L1–L5",

# slide 5 — aims
"Цели и задачи": "Aim and objectives",
"Создание обучающего веб-симулятора траекторий в системе Земля–Луна":
    "Building an educational web simulator for trajectories in the Earth–Moon system",
"Изучить теоретические основы КОЗТТ": "Study the theoretical foundations of the CR3BP",
"Вывести уравнения движения во вращающейся системе координат":
    "Derive the equations of motion in a rotating frame",
"Реализовать расчёт траектории методом Эйлера":
    "Implement trajectory computation using the Euler method",
"Реализовать метод Верле, сравнить точность с Эйлером":
    "Implement the Verlet method and compare its accuracy with Euler",
"Численно найти точки Лагранжа L1–L5": "Find the Lagrange points L1–L5 numerically",
"Создать интерактивный 3D веб-симулятор": "Create an interactive 3D web simulator",

# slide 6 — model
"Математическая модель": "Mathematical model",
"Уравнения движения во вращающейся системе координат:":
    "Equations of motion in the rotating frame:",
"грав. постоянная": "grav. constant",
"массы тел": "body masses",
"от барицентра": "from the barycentre",
"до центров масс": "to the centres of mass",
"угл. скорость": "angular velocity",
"2ωẏ  и  −2ωẋ  — ускорение от силы Кориолиса. Зависит от скорости":
    "2ωẏ and −2ωẋ — the Coriolis acceleration. It depends on velocity",
"+ модель тяги: F = const в окне [tₒₙ, toff]":
    "+ thrust model: F = const within the window [t_on, t_off]",
"масса топлива": "fuel mass",

# slide 7 — applicability
"Область применимости": "Scope of applicability",
"Круговая орбита": "Circular orbit",
"Орбита Луны считается круговой": "The Moon's orbit is treated as circular",
"(реальный эксцентриситет = 0.055)": "(actual eccentricity = 0.055)",
"Малая масса КА": "Negligible spacecraft mass",
"Масса аппарата пренебрежимо мала": "The spacecraft's mass is negligible",
"по сравнению с Землёй и Луной": "compared with the Earth and the Moon",
"Без Солнца": "No Sun",
"Не учитывается притяжение": "The attraction of the Sun and other",
"Солнца и других тел": "bodies is not taken into account",
"Модель корректна для качественного": "The model is valid for qualitative study",
"изучения динамики и учебных целей": "of the dynamics and for educational use",
"Для реальных миссий используются": "Real missions are designed with",
"полные эфемеридные модели": "full ephemeris models",

# slide 8 — integrators
"Три интегратора": "Three integrators",
"Метод Эйлера": "The Euler method",
"Простой, порядок O(h)": "Simple, order O(h)",
"Не сохраняет энергию": "Does not conserve energy",
"Верле с явной обработкой Кор. члена": "Verlet with explicit Coriolis handling",
"Симплектический, O(h²) теор": "Symplectic, O(h²) in theory",
"Но Кориолис все портит": "But Coriolis spoils it",
"Деградация до O(h) в КОЗТТ": "Degrades to O(h) in the CR3BP",
"O(h) в КОЗТТ": "O(h) in the CR3BP",
"Верле с  итеративной коррекцией скорости": "Verlet with iterative velocity correction",
"3 итерации за шаг уточняют v": "3 iterations per step refine v",
"Восстанавливает порядок O(h²)": "Restores order O(h²)",
"Кориолисово ускорение 2ω × v зависит от скорости → Верле с явной обработкой Кориолисова члена теряет порядок → итерации восстанавливают O(h²)":
    "The Coriolis acceleration 2ω × v depends on velocity → Verlet with explicit Coriolis handling loses its order → iteration restores O(h²)",

# slide 9 — Jacobi
"Интеграл Якоби": "The Jacobi integral",
"Единственная сохраняющаяся величина в КОЗТТ":
    "The only conserved quantity in the CR3BP",
"Отлично": "Excellent",
"Хорошо": "Good",
"Допустимо": "Acceptable",
"Плохо": "Poor",

# slide 10 — log-log
"Log-log сходимость": "Log-log convergence",
"Эйлер": "Euler",
"Верле явный": "Explicit Verlet",
"Верле итеративный": "Iterative Verlet",
"dt = 30 с  |  R² = 0.999": "dt = 30 s  |  R² = 0.999",
"Эйлер: 8 400 м": "Euler: 8,400 m",
"Верле явн.: 1 900 м": "Explicit Verlet: 1,900 m",
"Верле итрат.: 0.13 м": "Iterative Verlet: 0.13 m",
"64 600× точнее по позиции": "64,600× more accurate in position",

# slide 11 — adaptive step
"Адаптивный шаг": "Adaptive step",
"Вблизи тел 1/r растёт → нужен мелкий шаг":
    "Near a body 1/r grows → a smaller step is needed",
"Далеко от тел": "Far from the bodies",
"Силы малы, шаг максимален": "Forces are small, the step is at its maximum",
"Переходная зона": "Transition zone",
"dt уменьшается": "dt decreases",
"пропорционально v": "in proportion to v",
"Вблизи тела": "Near a body",
"Силы велики, шаг минимален": "Forces are large, the step is at its minimum",

# slide 12 — Desmos
"Поиск точек Лагранжа: Desmos": "Locating the Lagrange points: Desmos",
"Графический анализ суммарного ускорения в Desmos":
    "Graphical analysis of the total acceleration in Desmos",
"От графика к алгоритму": "From graph to algorithm",
"Графическое исследование привело к формализации метода бисекции для автоматического поиска точек Лагранжа":
    "The graphical investigation led to formalising the bisection method for locating the Lagrange points automatically",

# slide 13 — Lagrange points
"Точки Лагранжа L1–L5": "Lagrange points L1–L5",
"5 точек равновесия системы Земля–Луна": "5 equilibrium points of the Earth–Moon system",
"Точка": "Point",
"x,  км": "x,  km",
"y,  км": "y,  km",
"Метод": "Method",
"Ост. ускор., м/с²": "Resid. accel., m/s²",
"Бисекция": "Bisection",
"Ньютон": "Newton",
"График в Desmos → смена знака → бисекция → точность < 10⁻¹⁸ м/с²":
    "Desmos graph → sign change → bisection → accuracy < 10⁻¹⁸ m/s²",
"Аналитические приближения (сфера Хилла) дают отн. ошибку 0.4–0.8% — численное решение точнее":
    "Analytical approximations (Hill sphere) give a relative error of 0.4–0.8% — the numerical solution is more accurate",

# slide 14 — contribution
"Личный вклад": "Personal contribution",
"Физика": "Physics",
"Вывод уравнений движения КОЗТТ во вращающейся системе координат":
    "Derivation of the CR3BP equations of motion in a rotating frame",
"Валидация": "Validation",
"Реализация интеграла Якоби как инструмента проверки точности":
    "Implementation of the Jacobi integral as an accuracy-checking tool",
"Числ. методы": "Num. methods",
"3 интегратора; обнаружение деградации Верле и реализация варианта с итеративной коррекцией скорости":
    "3 integrators; discovering the degradation of Verlet and implementing the variant with iterative velocity correction",
"Эксперименты": "Experiments",
"Серия из 7 вычислительных экспериментов для количественной верификации":
    "A series of 7 computational experiments for quantitative verification",
"Алгоритмы": "Algorithms",
"Нахождение точек Лагранжа L1–L5: бисекция + метод Ньютона":
    "Locating the Lagrange points L1–L5: bisection + Newton's method",
"Разработка": "Development",
"3D веб-симулятор + скрипты поиска начальных условий":
    "3D web simulator + scripts for finding initial conditions",

# slide 15 — future work
"Пути развития": "Directions for development",
"Удержание орбиты": "Station keeping",
"Поддержание аппарата вблизи гало-орбиты":
    "Holding the spacecraft near a halo orbit",
"Лабораторные работы": "Laboratory exercises",
"Набор заданий на базе симулятора": "A set of assignments built on the simulator",

# slide 16 — conclusions
"Выводы": "Conclusions",
"Изучены теоретические основы КОЗТТ, выведены уравнения движения":
    "The theoretical foundations of the CR3BP were studied and the equations of motion derived",
"Реализованы 3 интегратора. Верле с итеративной коррекцией скорости точнее Эйлера в 64 600×":
    "3 integrators were implemented. Verlet with iterative velocity correction is 64,600× more accurate than Euler",
"Точки Лагранжа L1–L5 найдены численно (ост. уск. < 10⁻¹⁸)":
    "The Lagrange points L1–L5 were found numerically (resid. accel. < 10⁻¹⁸)",
"Модель верифицирована серией из 7 численных экспериментов":
    "The model was verified by a series of 7 numerical experiments",
"Создан обучающий 3D веб-симулятор, опубликован онлайн":
    "An educational 3D web simulator was built and published online",

# slide 17 — thanks
"Спасибо за внимание": "Thank you for your attention",
"МФТИ  ·  Старт в науку  ·  2026  ·  Ключников Александр":
    "MIPT  ·  Start in Science  ·  2026  ·  Alexander Klyuchnikov",

# slide 18 — appendix
"Приложение": "Appendix",
"Дополнительные материалы для ответов на вопросы":
    "Supplementary material for answering questions",

# slide 19 — chaos
"Хаос у L1": "Chaos at L1",
"10 м/с": "10 m/s",
"Показатель Ляпунова λ": "Lyapunov exponent λ",
"0.64 сут⁻¹": "0.64 day⁻¹",
"Горизонт предсказуемости": "Predictability horizon",
"~2 суток": "~2 days",
"Направлений / время": "Directions / time",
"16 / 30 сут": "16 / 30 days",

# slide 20 — halo
"Гало-орбита L1": "Halo orbit at L1",
"Амплитуда Az": "Amplitude Az",
"15 000 км": "15,000 km",
"Период": "Period",
"293 ч (12.2 дня)": "293 h (12.2 days)",
"Замыкание": "Closure error",
"3.6 км": "3.6 km",
"Дрейф Якоби": "Jacobi drift",

# slide 21 — free return
"Свободный возврат": "Free return",
"Пролёт Луны": "Lunar flyby",
"3 399 км": "3,399 km",
"Возврат к Земле": "Return to Earth",
"8 081 км": "8,081 km",
"Время полёта": "Flight time",
"168 ч": "168 h",
"+1 м/с → Δr Луна": "+1 m/s → Δr Moon",
"+89 км": "+89 km",

# slide 22 — thrust transfer
"Перелёт с тягой": "Powered transfer",
"Тяга / время": "Thrust / duration",
"5 Н / 3 ч": "5 N / 3 h",
"108 м/с": "108 m/s",
"2 494 км": "2,494 km",
"Топливо": "Fuel",
"18 кг (3.6%)": "18 kg (3.6%)",

# slide 23 — integrator comparison
"Сравнение интеграторов": "Integrator comparison",
"Дрейф интеграла Якоби, гало-орбита L1, dt = 30 с, T = 720 ч":
    "Jacobi integral drift, halo orbit at L1, dt = 30 s, T = 720 h",
"Интегратор": "Integrator",
"Режим": "Mode",
"Макс. дрейф": "Max. drift",
"фикс.": "fixed",
"Верле полушаг.": "Verlet half-step",
"Верле итерир.": "Verlet iterated",
"по дрейфу Якоби": "by Jacobi drift",
"по ошибке позиции": "by position error",

# slide 24 — ready for labs
"Готовый инструмент для лабораторных": "A ready-made tool for laboratory work",
"Симулятор готов к использованию в учебном процессе — без установки, в браузере":
    "The simulator is ready for classroom use — no installation, runs in the browser",
"Гало-орбиты": "Halo orbits",
"Параметрическое исследование:": "Parametric study:",
"период, замыкание, дрейф Якоби": "period, closure error, Jacobi drift",
"Чувствительность к начальным": "Sensitivity to initial",
"условиям, облёт Луны": "conditions, lunar flyby",
"Хаос и Ляпунов": "Chaos and Lyapunov",
"Горизонт предсказуемости,": "Predictability horizon,",
"расхождение траекторий": "divergence of trajectories",
"Оптимизация тяги": "Thrust optimisation",
"Подбор окна включения": "Choosing the engine",
"двигателя для манёвра": "firing window for a manoeuvre",
"Браузерный доступ  ·  Не требует установки  ·  7 готовых экспериментов  ·  Открытый код":
    "Browser access  ·  No installation  ·  7 ready-made experiments  ·  Open source",

# slide 25 — stack
"Технический стек": "Technical stack",
"3D-симулятор": "3D simulator",
"~1 500 строк": "~1,500 lines",
"SciPy (RK45 для валидации)": "SciPy (RK45 for validation)",
"Matplotlib · 7 скриптов": "Matplotlib · 7 scripts",
"Деплой": "Deployment",
"NVMe SSD · 210 ₽/мес": "NVMe SSD · 210 ₽/month",
"Инструменты": "Tools",
"Desmos (исследование L1–L5)": "Desmos (exploring L1–L5)",
"Python ~2 500 строк": "Python ~2,500 lines",
"Весь код написан с нуля  ·  Three.js + Python + NumPy  ·  VPS за 210 ₽/мес":
    "All code written from scratch  ·  Three.js + Python + NumPy  ·  VPS at 210 ₽/month",

# slide 26 — references
"Список литературы": "References",
"Белецкий В.В. - «Очерки о движении космических тел»":
    "V. V. Beletsky — Essays on the Motion of Celestial Bodies",
"Дубошин Г.Н. - «Небесная механика. Основные задачи и методы»":
    "G. N. Duboshin — Celestial Mechanics: Principal Problems and Methods",
"Охоцимский Д.Е., Сихарулидзе Ю.Г. - «Основы механики космического полёта»":
    "D. E. Okhotsimsky, Yu. G. Sikharulidze — Fundamentals of Space Flight Mechanics",
"Целоусова А.А - «Численно-аналитические методы построения траекторий в задачах трёх и четырёх тел»":
    "A. A. Tselousova — Numerical-Analytical Methods for Constructing Trajectories in the Three- and Four-Body Problems",

# slide 27 — timeline
"Эволюция проекта": "Project timeline",
"Сен 2025": "Sep 2025",
"Мар 2026": "Mar 2026",
"Теория КОЗТТ": "CR3BP theory",
"Лагранж": "Lagrange",
"Адапт. шаг": "Adaptive step",
"Траектории": "Trajectories",
"Числ. эксп.": "Num. experiments",
"Публикация": "Publication",
"7 месяцев: от теории до публикации на сайте":
    "7 months: from theory to publication on the web",

# slide 28 — derivation
"Вывод уравнений движения": "Derivation of the equations of motion",
"Система уравнений движения через эффективный потенциал:":
    "The equations of motion expressed via the effective potential:",
"эфф. потенциал": "eff. potential",
"2ωẏ  и  −2ωẋ  — члены Кориолиса, не входят в Ω":
    "2ωẏ and −2ωẋ — the Coriolis terms; they are not part of Ω",

# slide 15 — future work (inside grouped shapes)
"Эллиптическая орбита": "Elliptical orbit",
"Учёт эксцентриситета Луны": "Accounting for the Moon's eccentricity",
"Гравитация Солнца": "Solar gravity",
"Расширение до задачи четырёх тел": "Extension to the four-body problem",
"Давление света": "Radiation pressure",
"Учет давления света от Солнца": "Accounting for solar radiation pressure",
}
