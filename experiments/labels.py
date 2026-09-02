# -*- coding: utf-8 -*-
"""Bilingual labels for generated figures.

Figures are Russian by default, exactly as before. Set FIG_LANG=en to emit
English variants alongside them (filenames gain an "_en" suffix), which is how
the English presentation deck gets its charts.
"""
import os

LANG = os.environ.get("FIG_LANG", "ru").lower()

_EN = {
    # axes
    "x (тыс. км)": "x (10³ km)",
    "y (тыс. км)": "y (10³ km)",
    "z (тыс. км)": "z (10³ km)",
    "Шаг dt (с)": "Step dt (s)",
    "Макс. ошибка позиции (м)": "Max. position error (m)",
    # bodies / points
    "Земля": "Earth",
    "Луна": "Moon",
    # free return
    "Траектория": "Trajectory",
    "Старт": "Start",
    "Пролёт Луны": "Lunar flyby",
    "Возврат к Земле": "Return to Earth",
    "км": "km",
    # thrust
    "Без тяги": "No thrust",
    "С тягой": "With thrust",
    # chaos
    "Направление": "Direction",
    # integrators
    "Эйлер": "Euler",
    "Верле явный": "Explicit Verlet",
    "Верле полушаг.": "Verlet half-step",
    "Верле итерир.": "Verlet iterated",
    "наклон": "slope",
}


def L(text):
    """Translate a figure label when FIG_LANG=en; otherwise pass it through."""
    if LANG != "en":
        return text
    return _EN.get(text, text)


def suffix():
    """Filename suffix for the current language."""
    return "_en" if LANG == "en" else ""
