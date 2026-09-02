# -*- coding: utf-8 -*-
"""Swap the Russian images inside the English deck for English ones.

translate_deck.py only reaches text runs. A number of the deck's images are
rendered pictures - maths captions, charts, a screenshot of the simulator - with
their wording baked into pixels. This rewrites those entries in the .pptx
archive, leaving every other part byte-identical.

Replacements live in docs_src/figures_en/ and are named after the media part
they replace (image9.jpg replaces ppt/media/image9.jpg, and so on).
"""
import os
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIGS = os.path.join(HERE, "figures_en")
DECK = os.path.join(ROOT, "public", "presentation_2503_en.pptx")

# Images whose text is baked in and which have no English source we can rebuild.
KNOWN_UNTRANSLATED = {
    "image13.png": "Desmos screenshot (labels Земля/Луна) - no source file exists",
}


def main():
    if not os.path.isdir(FIGS):
        sys.exit(f"missing {FIGS}; run gen_deck_figures.py first")

    replacements = {f"ppt/media/{n}": os.path.join(FIGS, n)
                    for n in sorted(os.listdir(FIGS))
                    if not n.startswith(".")}

    tmp = DECK + ".tmp"
    swapped = []
    with zipfile.ZipFile(DECK) as src, \
         zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        names = set(src.namelist())
        for missing in set(replacements) - names:
            sys.exit(f"{missing} is not in the deck - check the media name")
        for item in src.infolist():
            if item.filename in replacements:
                with open(replacements[item.filename], "rb") as fh:
                    dst.writestr(item, fh.read())
                swapped.append(item.filename)
            else:
                dst.writestr(item, src.read(item.filename))

    shutil.move(tmp, DECK)
    for name in swapped:
        print(f"  replaced {name}")
    print(f"{len(swapped)} images swapped in {DECK}")

    for name, why in KNOWN_UNTRANSLATED.items():
        print(f"  STILL RUSSIAN: {name} - {why}")

    # re-render the PDF so it matches the deck
    exe = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    if os.path.exists(exe) or shutil.which("soffice"):
        subprocess.run([exe if os.path.exists(exe) else "soffice",
                        "--headless", "--norestore", "--convert-to", "pdf",
                        "--outdir", os.path.dirname(DECK), DECK],
                       check=True, capture_output=True)
        print(f"re-rendered: {os.path.splitext(DECK)[0]}.pdf")


if __name__ == "__main__":
    main()
