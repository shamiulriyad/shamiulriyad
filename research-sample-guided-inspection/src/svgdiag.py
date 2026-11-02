"""Tiny SVG diagram helper so every block diagram shares one visual language.

All diagrams are plain SVG text: editable in Inkscape / Illustrator / a text
editor, and rendered as vectors in the PDF.
"""
from html import escape

NAVY = "#1F3A5F"
TEAL = "#0F7C80"
TEAL_L = "#E2F1F1"
NAVY_L = "#E7EDF5"
AMBER = "#B7791F"
AMBER_L = "#FBF1DF"
RED = "#B03A2E"
RED_L = "#F8E5E2"
GRAY = "#5B6573"
GRAY_L = "#F2F4F7"
INK = "#1C2430"

STYLES = {
    "navy": (NAVY_L, NAVY),
    "teal": (TEAL_L, TEAL),
    "amber": (AMBER_L, AMBER),
    "red": (RED_L, RED),
    "gray": (GRAY_L, GRAY),
    "white": ("#FFFFFF", GRAY),
}


class Diagram:
    def __init__(self, w, h, title=None):
        self.w, self.h = w, h
        self.parts = []
        if title:
            self.text(w / 2, 18, title, size=13, weight="700", color=NAVY)

    # -- primitives -------------------------------------------------------
    def text(self, x, y, s, size=10, weight="400", color=INK, anchor="middle", italic=False):
        style = "font-style:italic;" if italic else ""
        lines = s.split("\n")
        for i, line in enumerate(lines):
            self.parts.append(
                f'<text x="{x:.1f}" y="{y + i * size * 1.22:.1f}" font-size="{size}" font-weight="{weight}" '
                f'fill="{color}" text-anchor="{anchor}" style="{style}">{escape(line)}</text>')

    def rect(self, x, y, w, h, fill, stroke, rx=6, sw=1.3, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
                          f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def box(self, x, y, w, h, title, sub=None, style="navy", size=10.5, subsize=8.6, dash=None, num=None):
        fill, stroke = STYLES[style]
        self.rect(x, y, w, h, fill, stroke, dash=dash)
        n_sub = len(sub.split("\n")) if sub else 0
        n_title = len(title.split("\n"))
        total = n_title * size * 1.22 + n_sub * subsize * 1.22
        y0 = y + h / 2 - total / 2 + size * 0.9
        self.text(x + w / 2, y0, title, size=size, weight="700", color=stroke if style != "white" else INK)
        if sub:
            self.text(x + w / 2, y0 + n_title * size * 1.22, sub, size=subsize, color=INK)
        if num is not None:
            self.parts.append(f'<circle cx="{x + 2:.1f}" cy="{y + 2:.1f}" r="8.5" fill="{stroke}"/>')
            self.text(x + 2, y + 5.5, str(num), size=9, weight="700", color="#FFFFFF")
        return (x, y, w, h)

    def arrow(self, x1, y1, x2, y2, color=GRAY, label=None, dash=None, sw=1.5, lx=None, ly=None,
              lsize=8.4, lcolor=None, anchor="middle"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        mid = {GRAY: "ag", TEAL: "at", AMBER: "aa", NAVY: "an", RED: "ar"}.get(color, "ag")
        self.parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
                          f'stroke-width="{sw}"{d} marker-end="url(#{mid})"/>')
        if label:
            self.text(lx if lx is not None else (x1 + x2) / 2, ly if ly is not None else (y1 + y2) / 2 - 4,
                      label, size=lsize, color=lcolor or color, anchor=anchor, italic=True)

    def path(self, d, color=GRAY, dash=None, sw=1.5, arrow=True, fill="none"):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        mid = {GRAY: "ag", TEAL: "at", AMBER: "aa", NAVY: "an", RED: "ar"}.get(color, "ag")
        m = f' marker-end="url(#{mid})"' if arrow else ""
        self.parts.append(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{sw}"{da}{m}/>')

    def raw(self, s):
        self.parts.append(s)

    def badge(self, x, y, s, style="amber", size=8.4, w=None):
        fill, stroke = STYLES[style]
        w = w or (len(s) * size * 0.56 + 14)
        self.rect(x - w / 2, y - size - 3, w, size + 9, fill, stroke, rx=9, sw=1)
        self.text(x, y, s, size=size, weight="700", color=stroke)

    # -- output -------------------------------------------------------------
    def svg(self):
        defs = "".join(
            f'<marker id="{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
            for k, c in (("ag", GRAY), ("at", TEAL), ("aa", AMBER), ("an", NAVY), ("ar", RED)))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
                f'font-family="Liberation Sans, Arial, Helvetica, sans-serif">'
                f'<defs>{defs}</defs><rect width="100%" height="100%" fill="#FFFFFF"/>' + "".join(self.parts) + "</svg>")

    def save(self, path):
        with open(path, "w") as f:
            f.write(self.svg())
