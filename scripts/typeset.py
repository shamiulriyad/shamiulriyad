"""Tiny SVG typesetter: draws text as glyph outlines.

GitHub renders README SVGs as images, so they cannot load web fonts and fall
back to whatever the viewer has installed. Outlining the text keeps the
typography identical everywhere. Glyphs are defined once per document and
placed with <use>.
"""

import html
import os

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")


class Font:
    def __init__(self, filename, key):
        self.key = key
        self.tt = TTFont(os.path.join(FONT_DIR, filename))
        self.glyphs = self.tt.getGlyphSet()
        self.cmap = self.tt.getBestCmap()
        self.upm = self.tt["head"].unitsPerEm
        self.hmtx = self.tt["hmtx"]
        self.kern = self._pair_kerning()

    def _pair_kerning(self):
        """Format-1 and format-2 PairPos kerning from GPOS, flattened to a dict."""
        pairs = {}
        if "GPOS" not in self.tt:
            return pairs
        for lookup in self.tt["GPOS"].table.LookupList.Lookup:
            for sub in lookup.SubTable:
                if sub.LookupType == 9:
                    sub = sub.ExtSubTable
                if getattr(sub, "LookupType", None) != 2:
                    continue
                firsts = sub.Coverage.glyphs
                if sub.Format == 1:
                    for first, pset in zip(firsts, sub.PairSet):
                        for rec in pset.PairValueRecord:
                            v = getattr(rec.Value1, "XAdvance", 0) if rec.Value1 else 0
                            if v:
                                pairs.setdefault((first, rec.SecondGlyph), v)
                elif sub.Format == 2:
                    c1 = sub.ClassDef1.classDefs if sub.ClassDef1 else {}
                    c2 = sub.ClassDef2.classDefs
                    seconds = {}
                    for g, c in c2.items():
                        seconds.setdefault(c, []).append(g)
                    for first in firsts:
                        row = sub.Class1Record[c1.get(first, 0)]
                        for cls, rec in enumerate(row.Class2Record):
                            v = getattr(rec.Value1, "XAdvance", 0) if rec.Value1 else 0
                            if v:
                                for second in seconds.get(cls, []):
                                    pairs.setdefault((first, second), v)
        return pairs

    def name(self, ch):
        return self.cmap.get(ord(ch), ".notdef")

    def path(self, glyph):
        pen = SVGPathPen(self.glyphs)
        self.glyphs[glyph].draw(pen)
        return pen.getCommands()

    def layout(self, s, tracking_units=0):
        """Yield (glyph, x) in font units; return total advance."""
        x, out, prev = 0, [], None
        for ch in s:
            g = self.name(ch)
            if prev is not None:
                x += self.kern.get((prev, g), 0) + tracking_units
            out.append((g, x))
            x += self.hmtx[g][0]
            prev = g
        return out, x

    def width(self, s, size, tracking=0):
        scale = size / self.upm
        return self.layout(s, tracking / scale)[1] * scale


class Doc:
    def __init__(self, width, height, label):
        self.w, self.h, self.label = width, height, label
        self.defs, self.extra_defs, self.body = {}, [], []

    def add(self, svg):
        self.body.append(svg)

    def define(self, svg):
        self.extra_defs.append(svg)

    def text(self, font, s, x, y, size, fill, anchor="start", tracking=0, opacity=1.0):
        """Place a single line. y is the baseline. tracking is in px."""
        scale = size / font.upm
        glyphs, adv = font.layout(s, tracking / scale)
        width = adv * scale
        if anchor == "middle":
            x -= width / 2
        elif anchor == "end":
            x -= width
        uses = []
        for g, gx in glyphs:
            if g in ("space", "uni00A0", ".notdef") or not font.path(g):
                continue
            gid = f"{font.key}-{g}".replace(".", "_")
            if gid not in self.defs:
                self.defs[gid] = font.path(g)
            uses.append(f'<use xlink:href="#{gid}" x="{gx:.0f}"/>')
        op = f' opacity="{opacity}"' if opacity != 1 else ""
        self.add(f'<g fill="{fill}"{op} transform="translate({x:.2f} {y:.2f}) scale({scale:.5f} {-scale:.5f})">{"".join(uses)}</g>')
        return width

    def wrap(self, font, s, size, max_width, tracking=0):
        lines, line = [], ""
        for word in s.split():
            trial = f"{line} {word}".strip()
            if line and font.width(trial, size, tracking) > max_width:
                lines.append(line)
                line = word
            else:
                line = trial
        if line:
            lines.append(line)
        return lines

    def paragraph(self, font, s, x, y, size, fill, max_width, leading=1.5, tracking=0, opacity=1.0):
        lines = self.wrap(font, s, size, max_width, tracking)
        for i, line in enumerate(lines):
            self.text(font, line, x, y + i * size * leading, size, fill, tracking=tracking, opacity=opacity)
        return y + (len(lines) - 1) * size * leading

    def render(self):
        glyphs = "".join(f'<path id="{k}" d="{d}"/>' for k, d in self.defs.items())
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" '
            f'aria-label="{html.escape(self.label)}"><title>{html.escape(self.label)}</title>'
            f'<defs>{glyphs}{"".join(self.extra_defs)}</defs>{"".join(self.body)}</svg>\n'
        )
