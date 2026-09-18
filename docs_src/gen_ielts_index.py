# -*- coding: utf-8 -*-
"""Build ielts/index.html - the landing page listing every flashcard deck.

Each deck is read for its header title, total card count and category chips,
so adding a lesson is: drop the .html into ielts/, run this script, commit.
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
IELTS = os.path.join(os.path.dirname(HERE), "ielts")
OUT = os.path.join(IELTS, "index.html")


# Display order and card titles on the landing page: file -> (eyebrow, title).
# Decks not listed here are appended afterwards under their own header name.
DECK_INFO = {
    "lesson1.html": ("Vocabulary", "Lesson 1"),
    "lesson2.html": ("Vocabulary", "Lesson 2"),
    "graphs.html": ("Writing Task 1", "Description of the graphs"),
    "fce-education-flashcards.html": ("FCE", "FCE Education"),
}


def ru_plural(n, one, few, many):
    """Russian noun form for n: 1 карточка, 2 карточки, 5 карточек."""
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


def natural_key(name):
    parts = [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", name)]
    order = list(DECK_INFO)
    return (order.index(name) if name in order else len(order), parts)


def describe(path):
    src = open(path, encoding="utf-8").read()
    brand = re.search(r'<div class="brand">(.*?)</div>', src, re.S)
    title = re.sub(r"<[^>]+>", "", brand.group(1)) if brand else os.path.basename(path)
    title = re.sub(r"\s*·\s*EN\s*/\s*RU\s*$", "", html.unescape(title)).strip()

    chips = re.findall(r'<label class="chip" for="cat-[^"]+">([^<]+)</label>', src)
    total, cats = None, []
    for chip in chips:
        m = re.match(r"(.+?)\s+(\d+)$", html.unescape(chip).strip())
        if not m:
            continue
        if m.group(1).lower() == "all":
            total = int(m.group(2))
        else:
            cats.append(m.group(1))
    if total is None:
        total = src.count('<label class="card')
    return title, total, cats


def build():
    decks = sorted((f for f in os.listdir(IELTS)
                    if f.endswith(".html") and f != "index.html"), key=natural_key)
    cards = []
    for f in decks:
        title, total, cats = describe(os.path.join(IELTS, f))
        eyebrow, title = DECK_INFO.get(f, ("Deck", title))
        tags = "".join(f"<span>{html.escape(c)}</span>" for c in cats)
        cards.append(f'''    <a class="deck" href="{html.escape(f)}">
      <div class="eyebrow">{eyebrow}</div>
      <h2>{html.escape(title)}</h2>
      <div class="count">{total} {ru_plural(total, "карточка", "карточки", "карточек")} · cards</div>
      <div class="tags">{tags}</div>
      <div class="go">Открыть →</div>
    </a>''')

    grand = sum(describe(os.path.join(IELTS, f))[1] for f in decks)
    page = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IELTS / FCE · Flashcards</title>
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&amp;display=swap" rel="stylesheet">
<style>
  :root{{--ink:#10262E;--ink2:#0A1A20;--accent:#E3A21C;--muted:#8AA6AD;--line:rgba(255,255,255,.12)}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{min-height:100vh;background:radial-gradient(120% 80% at 50% -10%,#163741 0%,var(--ink) 45%,var(--ink2) 100%);color:#E8F0F1;font-family:"Inter",system-ui,sans-serif;padding:48px 20px 40px}}
  .wrap{{max-width:880px;margin:0 auto}}
  h1{{font-family:"Source Serif 4",serif;font-weight:600;font-size:34px;margin:0 0 6px}}
  h1 i{{color:var(--accent);font-style:normal}}
  .lead{{color:var(--muted);font-size:15px;margin-bottom:32px}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}}
  .deck{{display:flex;flex-direction:column;gap:8px;padding:22px;border:1px solid var(--line);border-radius:16px;background:rgba(255,255,255,.03);color:inherit;text-decoration:none;transition:border-color .15s,transform .15s,background .15s}}
  .deck:hover{{border-color:var(--accent);background:rgba(227,162,28,.06);transform:translateY(-2px)}}
  .eyebrow{{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:600}}
  .deck h2{{font-family:"Source Serif 4",serif;font-size:21px;font-weight:600;line-height:1.25}}
  .count{{color:var(--muted);font-size:13px}}
  .tags{{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}}
  .tags span{{font-size:11.5px;color:var(--muted);border:1px solid var(--line);padding:3px 8px;border-radius:999px}}
  .go{{margin-top:auto;padding-top:10px;color:var(--accent);font-weight:600;font-size:14px}}
  footer{{margin-top:40px;color:var(--muted);font-size:12px}}
</style>
</head>
<body>
  <div class="wrap">
    <h1>IELTS <i>/</i> FCE Flashcards</h1>
    <p class="lead">Карточки для запоминания слов · English ↔ Русский</p>
    <div class="grid">
{chr(10).join(cards)}
    </div>
    <footer>{len(decks)} {ru_plural(len(decks), "набор", "набора", "наборов")} · {grand} {ru_plural(grand, "карточка", "карточки", "карточек")}</footer>
  </div>
</body>
</html>
'''
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"written: {OUT} ({len(decks)} decks)")


if __name__ == "__main__":
    build()
