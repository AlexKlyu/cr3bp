# -*- coding: utf-8 -*-
"""Word lists for the flashcard decks built by gen_ielts_deck.py.

Each deck: output file, <title>/header name, and categories. A category is
(css id, chip label, [(english, russian), ...]).
"""

DECKS = [
    {
        "file": "lesson2.html",
        "name": "Lesson 2",
        "categories": [
            ("phrases", "Useful phrases", [
                ("devote to", "посвящать время"),
                ("enlarge my scope of", "расширить свой кругозор в области"),
                ("enable", "позволять"),
                ("essential", "важный"),
                ("experienced", "пережить изменения"),
            ]),
            ("linking", "Linking words", [
                ("as far as I'm concerned", "насколько я знаю"),
                ("respectively", "соответственно"),
                ("overall", "в общем"),
                ("although", "хотя"),
                ("as for the other", "что насчёт остального"),
                ("whereas", "в то время как"),
            ]),
        ],
    },
    {
        "file": "lesson3.html",
        "name": "Lesson 3",
        "categories": [
            ("words", "Words & phrases", [
                ("to intend to", "намереваться"),
                ("to set an assignment", "задать задание"),
                ("terrific", "потрясающий, замечательный"),
                ("acquainted", "знакомый (be acquainted with — быть знакомым с)"),
                ("to be fond of", "любить, увлекаться"),
            ]),
        ],
    },
    {
        "file": "graphs.html",
        "name": "Description of the graphs",
        "categories": [
            ("rise", "Rise", [
                ("increased, rose, climbed, grew, went up, escalated", "рос"),
            ]),
            ("fall", "Fall", [
                ("decreased, fell, dropped, declined, came down", "падал"),
            ]),
            ("stable", "No change", [
                ("remained stable, leveled off, stabilized, remained the same",
                 "не изменялся"),
            ]),
            ("fluct", "Fluctuation", [
                ("fluctuated", "колебался"),
            ]),
            ("peak", "Peak & low", [
                ("peaked, reached a high of", "достиг наивысшей отметки"),
                ("dropped, reached a low of", "достиг наинизшей отметки"),
            ]),
            ("degree", "Degree of change", [
                ("slightly, slowly, minimally, minor", "не сильно (менялся)"),
                ("sharply, rapidly, dramatically, significantly, considerably, "
                 "substantially, major", "сильно (менялся)"),
                ("moderately, modestly", "средне (менялся)"),
                ("steadily", "стабильно, равномерно"),
                ("gradually", "постепенно"),
            ]),
            ("compare", "Comparison", [
                ("gender distribution", "распределение по полу"),
                ("gap", "разрыв, разница"),
                ("predominate", "преобладать"),
            ]),
            ("phrase", "Useful phrases", [
                ("as can be seen from the graph", "как видно из графика"),
            ]),
            ("approx", "Approximation", [
                ("nearly, approximately", "примерно"),
                ("roughly", "грубо"),
                ("just above", "чуть выше"),
                ("just under", "чуть ниже"),
            ]),
        ],
    },
]
