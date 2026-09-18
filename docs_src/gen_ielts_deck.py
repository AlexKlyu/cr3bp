# -*- coding: utf-8 -*-
"""Build flashcard decks for ielts/ from the word lists in ielts_decks.py.

ielts/lesson1.html is used as the template, so every deck shares its look,
flip/shuffle behaviour and EN<->RU toggle. Only the header, category chips
and cards are generated.
"""
import html
import os
import re

from ielts_decks import DECKS

HERE = os.path.dirname(os.path.abspath(__file__))
IELTS = os.path.join(os.path.dirname(HERE), "ielts")
TEMPLATE = os.path.join(IELTS, "lesson1.html")

ACTIVE = "{background:var(--accent); color:#1a1200; border-color:var(--accent); font-weight:600}"


def load_template():
    src = open(TEMPLATE, encoding="utf-8").read()
    style_head = src[:src.index("  #cat-")]                      # base CSS
    style_end = src.index("  @media (prefers-reduced-motion")   # rest of CSS
    style_tail = src[style_end:src.index("<body>")]
    tail = src[src.index('    <div class="foot"'):]             # footer + script
    return style_head, style_tail, tail


def card(cls, kind, en, ru):
    e, r, k = html.escape(en), html.escape(ru), html.escape(kind)
    return f'''      <label class="card {cls}">
        <input type="checkbox" class="flip" aria-label="flip card">
        <div class="inner">
          <div class="face front">
            <div class="kind">{k}</div>
            <div class="term t-en">{e}</div>
            <div class="term t-ru">{r}</div>
            <div class="cue">tap to reveal</div>
          </div>
          <div class="face back">
            <div class="kind">{k}</div>
            <div class="term t-ru">{r}</div>
            <div class="term t-en">{e}</div>
          </div>
        </div>
      </label>'''


def build(deck, style_head, style_tail, tail):
    cats = deck["categories"]
    total = sum(len(words) for _, _, words in cats)
    ids = [cid for cid, _, _ in cats]

    css = "".join(f"  #cat-{c}:checked ~ .app .card:not(.{c}){{display:none}}\n" for c in ids)
    css += ",\n".join(f"  #cat-{c}:checked ~ .app label[for=cat-{c}]"
                      for c in ["all"] + ids) + ACTIVE + "\n"

    radios = ['  <input class="ctrl" type="radio" name="dir" id="dir-en" checked>',
              '  <input class="ctrl" type="radio" name="dir" id="dir-ru">',
              '  <input class="ctrl" type="radio" name="cat" id="cat-all" checked>']
    radios += [f'  <input class="ctrl" type="radio" name="cat" id="cat-{c}">' for c in ids]

    chips = [f'      <label class="chip" for="cat-all">All {total}</label>']
    chips += [f'      <label class="chip" for="cat-{c}">{html.escape(label)} {len(words)}</label>'
              for c, label, words in cats]

    cards = [card(c, label, en, ru) for c, label, words in cats for en, ru in words]
    name = html.escape(deck["name"])

    head = re.sub(r"<title>.*?</title>", f"<title>{name} · English · Russian</title>", style_head)
    page = (head + css + style_tail + "<body>\n" + "\n".join(radios) + "\n"
            f'''  <div class="app">
    <header>
      <div class="brand">{name} <i>·</i> EN / RU</div>
      <div class="dir-toggle">
        <label class="chip" for="dir-en">EN → RU</label>
        <label class="chip" for="dir-ru">RU → EN</label>
      </div>
    </header>
    <div class="cats">
      <button class="chip shuffle-btn" id="shuffleBtn" type="button">🔀 Shuffle</button>
''' + "\n".join(chips) + '''
    </div>
    <div class="deck" id="deck">
''' + "\n".join(cards) + "\n    </div>\n" + tail)

    out = os.path.join(IELTS, deck["file"])
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"written: {out} ({total} cards)")


if __name__ == "__main__":
    parts = load_template()
    for d in DECKS:
        build(d, *parts)
