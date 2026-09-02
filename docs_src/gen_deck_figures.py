# -*- coding: utf-8 -*-
"""English replacements for the Russian images embedded in the deck.

The deck carries a number of rendered images - maths captions and charts - whose
text is baked into pixels, so translate_deck.py (which only touches text runs)
cannot reach them. This script regenerates the caption images in English; the
charts come from the experiment scripts run with FIG_LANG=en.

Output: docs_src/figures_en/<media name>.png, consumed by swap_deck_media.py.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures_en")

# Maths captions, keyed by the media file they replace. Sizes are matched to the
# originals so the slide layout is unaffected.
CAPTIONS = {
    "image10": (r"slope $1.00 \rightarrow \mathcal{O}(h)$", 705, 96),
    "image11": (r"slope $1.97 \rightarrow \mathcal{O}(h^2)$", 741, 103),
    "image8": (r"$e = \frac{C_J(t) - C_J(0)}{C_J(0)}$  —  measure of accumulated error",
               1882, 185),
}


def render_caption(expr, width_px, height_px, path):
    """Render text/maths to a transparent PNG of the given pixel size."""
    dpi = 200
    fig = plt.figure(figsize=(width_px / dpi, height_px / dpi), dpi=dpi)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, expr, ha="center", va="center",
             fontsize=26, color="#000000")
    fig.savefig(path, dpi=dpi, transparent=True,
                bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (expr, w, h) in CAPTIONS.items():
        path = os.path.join(OUT, f"{name}.png")
        render_caption(expr, w, h, path)
        print(f"written: {path}")


if __name__ == "__main__":
    main()
