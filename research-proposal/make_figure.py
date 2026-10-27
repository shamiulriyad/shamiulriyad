"""Generate figure.svg: the conceptual multi-die reconstruction example (Fig. 1).

Every panel is drawn from ONE layout definition (LINES, CONNECTORS, VIAS below), so the
die pattern is identical in all inputs, maps and outputs. Defects and regions are also
defined once (DEFECTS, REGIONS) and reused everywhere, which keeps the inputs, the
evidence matrix, the reference and the uncertainty map logically consistent.

Usage:  python3 research-proposal/make_figure.py
"""
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent / "figure.svg"

# ---------------------------------------------------------------- palette
INK, MUTED, NAVY = "#1c2430", "#5b6573", "#1f3a5f"
SUBSTRATE, METAL, VIA = "#dde3ea", "#7d8da3", "#34465e"
RELIABLE, RELIABLE_LINE = "#e3ecf6", "#9fb0c6"
DEFECT = "#c0392b"
UNCERTAIN = "#b7791f"
REDUCED = "#c3cad4"
FONT = "'Liberation Sans', Arial, sans-serif"

# ---------------------------------------------------------------- die layout (die units 0..100)
# Lines extend past the die so rotated inputs show no empty corners.
LINES = [(12, 20), (34, 42), (58, 66), (80, 88)]                 # horizontal metal (y0, y1)
CONNECTORS = [(22, 30, 20, 34), (64, 72, 42, 58), (40, 48, 66, 80)]  # vertical (x0, x1, y0, y1)
VIAS = [(48, 38), (56, 62), (90, 84)]                             # centres, 5x5

# Defects: id -> (owning dies, drawing)
DEFECTS = {
    "a": ([1], "particle"),
    "b": ([2], "bridge"),
    "c": ([3], "open"),
    "d": ([4], "scratch"),
    "e": ([5], "residue"),
    "f": ([1, 2, 3, 4, 5], "notch"),   # repeats in every die (systematic / mask-level)
}
# Region that the estimated map marks around each defect (die units).
REGIONS = {
    "a": ("circle", 30, 16, 10),
    "b": ("rect", 5, 39, 17, 22),
    "c": ("rect", 64, 75, 18, 18),
    "d": ("rect", 56, 18, 40, 18),
    "e": ("circle", 88, 50, 9),
    "f": ("rect", 24, 53, 20, 15),
}
TAG_AT = {"a": (47, 9), "b": (13, 29), "c": (73, 70), "d": (49, 28), "e": (88, 68), "f": (34, 75)}
# Per-die estimated state of each region: the scratch on die 4 is ambiguous -> uncertain.
STATE = {}
for r, (dies, _) in DEFECTS.items():
    for k in range(1, 6):
        STATE[(k, r)] = ("uncertain" if (r == "d" and k == 4) else "defective") if k in dies else "reliable"
# Pose of each raw input: (rotation deg, dx, dy) in die units.
POSE = {1: (-5, 0, 0), 2: (3, 4, -3), 3: (0, -5, 4), 4: (5, 0, 0), 5: (-2, 3, 3)}

# ---------------------------------------------------------------- geometry of the figure
W, H = 1860, 873
TH = 134                     # thumbnail size
S = TH / 100                 # die units -> svg units in thumbnails
ROW0, PITCH = 90, 144        # first row top, row pitch
COL_A, COL_B, COL_C = 90, 310, 530
MX0, MPITCH = 745, 48        # evidence-matrix first column centre and pitch
REF_X, UNC_X, OUT_Y, OS = 1118, 1500, 92, 330   # outputs
COLS = ["a", "b", "c", "d", "e", "f", "rest"]


def row_cy(k):
    return ROW0 + PITCH * (k - 1) + TH / 2


def layout(defects=(), extend=True):
    """SVG for the die pattern in die units, with the given defects drawn in."""
    x0, x1 = (-30, 130) if extend else (0, 100)
    s = [f'<rect x="{x0}" y="{x0}" width="{x1 - x0}" height="{x1 - x0}" fill="{SUBSTRATE}"/>']
    for y0, y1 in LINES:
        s.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{METAL}"/>')
    for a, b, c, d in CONNECTORS:
        s.append(f'<rect x="{a}" y="{c}" width="{b - a}" height="{d - c}" fill="{METAL}"/>')
    for cx, cy in VIAS:
        s.append(f'<rect x="{cx - 2.5}" y="{cy - 2.5}" width="5" height="5" fill="{VIA}"/>')
    for d in defects:
        s.append(DEFECT_SVG[DEFECTS[d][1]])
    return "".join(s)


DEFECT_SVG = {
    "particle": '<path d="M24,12 C25,7 33,7 36,11 C39,15 37,22 31,23 C26,24 22,18 24,12 Z" fill="#26292e"/>',
    "bridge": f'<path d="M10,42 L17,42 L16,48 L18,53 L16,58 L9,58 L11,52 L9,47 Z" fill="{METAL}" stroke="#56667c" stroke-width="0.6"/>',
    "open": f'<rect x="70" y="79.5" width="6" height="9" fill="{SUBSTRATE}"/>',
    "scratch": '<path d="M59,32 L93,21" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round"/>'
               '<path d="M62,34 L90,25" stroke="#ffffff" stroke-width="0.9" stroke-linecap="round"/>',
    "residue": '<path d="M83,48 C84,44 91,44 93,48 C95,52 91,56 87,55 C83,54 82,51 83,48 Z" fill="#ffffff" stroke="#4a4f57" stroke-width="1.1"/>',
    "notch": f'<path d="M28,58 L40,58 L38,63 L30,63 Z" fill="{SUBSTRATE}"/>',
}


def region_shape(r, **attrs):
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    g = REGIONS[r]
    if g[0] == "circle":
        return f'<circle cx="{g[1]}" cy="{g[2]}" r="{g[3]}" {a}/>'
    return f'<rect x="{g[1]}" y="{g[2]}" width="{g[3]}" height="{g[4]}" rx="1.5" {a}/>'


def tag(x, y, letter, colour, r=13, size=21):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#ffffff" stroke="{colour}" stroke-width="2"/>'
            f'<text x="{x:.1f}" y="{y + size * 0.36:.1f}" font-size="{size}" font-weight="700" fill="{colour}" '
            f'text-anchor="middle">{letter}</text>')


def transform_point(px, py, pose):
    """Die point -> thumbnail point for a raw (posed) input."""
    ang, dx, dy = pose
    t = math.radians(ang)
    x, y = px - 50, py - 50
    xr = x * math.cos(t) - y * math.sin(t) + 50 + dx
    yr = x * math.sin(t) + y * math.cos(t) + 50 + dy
    return xr, yr


def thumb(x, y, inner, scale=S, size=TH, frame=MUTED):
    return (f'<g transform="translate({x},{y}) scale({scale})"><g clip-path="url(#clip)">{inner}</g></g>'
            f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="none" stroke="{frame}" stroke-width="1.2"/>')


def corner_marks():
    p = f'stroke="{NAVY}" stroke-width="2.2" fill="none" vector-effect="non-scaling-stroke"'
    return (f'<path d="M9,17 L9,9 L17,9" {p}/><path d="M83,9 L91,9 L91,17" {p}/>'
            f'<path d="M9,83 L9,91 L17,91" {p}/><path d="M83,91 L91,91 L91,83" {p}/>')


def arrow(x1, y1, x2, y2, w=2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{MUTED}" stroke-width="{w}" marker-end="url(#ah)"/>'


def check(cx, cy, colour):
    return f'<path d="M{cx - 8},{cy} L{cx - 2},{cy + 7} L{cx + 9},{cy - 7}" stroke="{colour}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def cross(cx, cy, colour):
    return (f'<path d="M{cx - 7},{cy - 7} L{cx + 7},{cy + 7} M{cx + 7},{cy - 7} L{cx - 7},{cy + 7}" '
            f'stroke="{colour}" stroke-width="3" stroke-linecap="round"/>')


def build():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT}">',
         '<defs>',
         '<clipPath id="clip"><rect x="0" y="0" width="100" height="100"/></clipPath>',
         f'<pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         f'<rect width="7" height="7" fill="#fbf3e4"/><rect width="3" height="7" fill="{UNCERTAIN}"/></pattern>',
         f'<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>',
         '</defs>']

    # ---- column headers
    def header(x, letter, title, sub, anchor="start"):
        return (f'<text x="{x}" y="30" font-size="26" font-weight="700" fill="{NAVY}" text-anchor="{anchor}">{letter}'
                f'<tspan font-weight="600" fill="{INK}"> {title}</tspan></text>'
                f'<text x="{x}" y="60" font-size="23" fill="{MUTED}" text-anchor="{anchor}">{sub}</text>')
    o.append(header(COL_A, "A", "Inputs", "misaligned"))
    o.append(header(COL_B, "B", "Registration", "common frame"))
    o.append(header(COL_C, "C", "Defect maps", "estimates only"))
    o.append(header(MX0 - 12, "D", "Evidence per region", "which die is used where"))
    o.append(header(REF_X, "E", "Output", ""))
    o.append(f'<text x="{REF_X + 130}" y="30" font-size="20" font-weight="600" letter-spacing="1" fill="{DEFECT}">'
             f'CONCEPTUAL EXAMPLE — NOT EXPERIMENTAL DATA</text>')

    # ---- per-die rows: A raw, B registered, C estimated map
    for k in range(1, 6):
        y = ROW0 + PITCH * (k - 1)
        cy = row_cy(k)
        own = [r for r, (dies, _) in DEFECTS.items() if k in dies]
        o.append(f'<text x="0" y="{cy + 9}" font-size="26" font-weight="600" fill="{INK}">Die {k}</text>')
        ang, dx, dy = POSE[k]
        posed = (f'<g transform="translate({dx},{dy}) rotate({ang} 50 50)">{layout(own)}{corner_marks()}</g>')
        o.append(thumb(COL_A, y, posed))
        for r in own:  # tags at transformed defect positions, drawn upright
            tx, ty = transform_point(*TAG_AT[r], POSE[k])
            tx = min(max(tx, 8), 92)
            ty = min(max(ty, 8), 92)
            o.append(tag(COL_A + tx * S, y + ty * S, r, DEFECT, r=13, size=21))
        o.append(arrow(COL_A + TH + 10, cy, COL_B - 12, cy, 1.6))
        aligned = layout(own) + corner_marks()
        grid = (f'<path d="M50,0 L50,100 M0,50 L100,50" stroke="{NAVY}" stroke-width="1" stroke-dasharray="4 4" '
                f'vector-effect="non-scaling-stroke" opacity="0.6"/>')
        o.append(thumb(COL_B, y, aligned + grid))
        o.append(arrow(COL_B + TH + 10, cy, COL_C - 12, cy, 1.6))
        # estimated map: faint pattern, reliable tint, then regions
        m = [f'<rect x="0" y="0" width="100" height="100" fill="{RELIABLE}"/>']
        for y0, y1 in LINES:
            m.append(f'<rect x="0" y="{y0}" width="100" height="{y1 - y0}" fill="{RELIABLE_LINE}" opacity="0.45"/>')
        for a, b, c, d in CONNECTORS:
            m.append(f'<rect x="{a}" y="{c}" width="{b - a}" height="{d - c}" fill="{RELIABLE_LINE}" opacity="0.45"/>')
        for r in own:
            if STATE[(k, r)] == "defective":
                m.append(region_shape(r, fill=DEFECT, fill_opacity="0.88"))
            else:
                m.append(region_shape(r, fill="url(#hatch)", stroke=UNCERTAIN, stroke_width="0.8"))
        o.append(thumb(COL_C, y, "".join(m)))

    # ---- D: evidence matrix (rows = dies, columns = regions)
    mx = lambda i: MX0 + MPITCH * i
    for i, c in enumerate(COLS):
        if c == "rest":
            o.append(f'<text x="{mx(i)}" y="{ROW0 - 4}" font-size="22" fill="{MUTED}" text-anchor="middle">rest</text>')
        else:
            o.append(tag(mx(i), ROW0 - 12, c, NAVY if c != "f" else UNCERTAIN, r=13, size=21))
    # highlight column f
    fx = mx(COLS.index("f"))
    o.append(f'<rect x="{fx - 24}" y="{ROW0 + 8}" width="48" height="{PITCH * 4 + TH + 70}" rx="6" fill="#fbf3e4" stroke="{UNCERTAIN}" stroke-width="1.2"/>')
    for k in range(1, 6):
        cy = row_cy(k)
        o.append(f'<line x1="{mx(0) - 26}" y1="{cy}" x2="{mx(len(COLS) - 1) + 26}" y2="{cy}" stroke="#e3e8ee" stroke-width="1"/>')
        for i, c in enumerate(COLS):
            st = "reliable" if c == "rest" else STATE[(k, c)]
            x0, y0 = mx(i) - 19, cy - 19
            if st == "reliable":
                o.append(f'<rect x="{x0}" y="{y0}" width="38" height="38" rx="5" fill="{RELIABLE}" stroke="{RELIABLE_LINE}"/>' + check(mx(i), cy, NAVY))
            elif st == "defective":
                o.append(f'<rect x="{x0}" y="{y0}" width="38" height="38" rx="5" fill="{DEFECT}"/>' + cross(mx(i), cy, "#ffffff"))
            else:
                o.append(f'<rect x="{x0}" y="{y0}" width="38" height="38" rx="5" fill="url(#hatch)" stroke="{UNCERTAIN}"/>'
                         f'<text x="{mx(i)}" y="{cy + 9}" font-size="25" font-weight="700" fill="{INK}" text-anchor="middle">?</text>')
    # support counts
    yc = ROW0 + PITCH * 4 + TH + 44
    o.append(f'<text x="{mx(0) - 34}" y="{yc + 8}" font-size="23" font-weight="600" fill="{INK}" text-anchor="end">reliable dies used</text>')
    for i, c in enumerate(COLS):
        n = 5 if c == "rest" else sum(STATE[(k, c)] == "reliable" for k in range(1, 6))
        colour = UNCERTAIN if n == 0 else NAVY
        o.append(f'<text x="{mx(i)}" y="{yc + 9}" font-size="25" font-weight="700" fill="{colour}" text-anchor="middle">{n}</text>')

    # ---- E: outputs
    ox = OS / 100
    o.append(arrow(mx(len(COLS) - 1) + 34, OUT_Y + OS / 2, REF_X - 12, OUT_Y + OS / 2, 2.4))
    o.append(f'<text x="{(mx(len(COLS) - 1) + 34 + REF_X - 12) / 2}" y="{OUT_Y + OS / 2 - 14}" font-size="23" fill="{MUTED}" text-anchor="middle">fuse</text>')
    ref = [layout((), extend=False)]
    for r in "abcde":
        ref.append(region_shape(r, fill="none", stroke=NAVY, stroke_width="1.4", stroke_dasharray="3 2.5", vector_effect="non-scaling-stroke"))
    ref.append(region_shape("f", fill="url(#hatch)", stroke=UNCERTAIN, stroke_width="1.6", vector_effect="non-scaling-stroke"))
    o.append(thumb(REF_X, OUT_Y, "".join(ref), scale=ox, size=OS, frame=NAVY))
    unc = [f'<rect x="0" y="0" width="100" height="100" fill="#fbfcfd"/>']
    for y0, y1 in LINES:
        unc.append(f'<rect x="0" y="{y0}" width="100" height="{y1 - y0}" fill="none" stroke="#d5dbe3" stroke-width="0.5"/>')
    for r in "abcde":
        unc.append(region_shape(r, fill=REDUCED))
    unc.append(region_shape("f", fill="url(#hatch)", stroke=UNCERTAIN, stroke_width="1.6", vector_effect="non-scaling-stroke"))
    o.append(thumb(UNC_X, OUT_Y, "".join(unc), scale=ox, size=OS, frame=NAVY))
    for r in "abcdef":
        tx, ty = TAG_AT[r]
        col = UNCERTAIN if r == "f" else NAVY
        o.append(tag(REF_X + tx * ox, OUT_Y + ty * ox, r, col, r=14, size=22))
        o.append(tag(UNC_X + tx * ox, OUT_Y + ty * ox, r, col, r=14, size=22))
    lab_y = OUT_Y + OS + 36
    for x, title, sub in ((REF_X, "Candidate reference", "digital estimate, not a die"),
                          (UNC_X, "Uncertainty map", "dies supporting each pixel")):
        o.append(f'<text x="{x + OS / 2}" y="{lab_y}" font-size="25" font-weight="600" fill="{INK}" text-anchor="middle">{title}</text>')
        o.append(f'<text x="{x + OS / 2}" y="{lab_y + 30}" font-size="23" fill="{MUTED}" text-anchor="middle">{sub}</text>')

    # ---- legend (two stacked columns), provenance hint, all-defective callout
    ly = lab_y + 88
    def key(x, y, fill, stroke, text):
        o.append(f'<rect x="{x}" y="{y - 19}" width="25" height="25" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
        o.append(f'<text x="{x + 35}" y="{y + 1}" font-size="23" fill="{INK}">{text}</text>')
    o.append(f'<text x="{REF_X}" y="{ly}" font-size="23" font-weight="700" fill="{INK}">C, D: per die and region</text>')
    for i, (fill, stroke, text) in enumerate([(RELIABLE, RELIABLE_LINE, "reliable: used"),
                                               (DEFECT, DEFECT, "defective: excluded"),
                                               ("url(#hatch)", UNCERTAIN, "uncertain: excluded")]):
        key(REF_X, ly + 40 + 36 * i, fill, stroke, text)
    o.append(f'<text x="{UNC_X}" y="{ly}" font-size="23" font-weight="700" fill="{INK}">E: reliable dies</text>')
    for i, (fill, stroke, text) in enumerate([("#fbfcfd", RELIABLE_LINE, "5 of 5"),
                                               (REDUCED, REDUCED, "4 of 5: reconstructed"),
                                               ("url(#hatch)", UNCERTAIN, "0 of 5: not reconstructed")]):
        key(UNC_X, ly + 40 + 36 * i, fill, stroke, text)
    hy = ly + 40 + 36 * 2 + 50
    o.append(f'<text x="{REF_X}" y="{hy}" font-size="23" fill="{INK}"><tspan font-weight="700">Read D by column:</tspan> region a is rebuilt from</text>')
    o.append(f'<text x="{REF_X}" y="{hy + 31}" font-size="23" fill="{INK}">dies 2–5 only; d skips die 4 (uncertain); “rest” uses all 5.</text>')
    bh = 106
    ny = H - 4 - bh
    o.append(f'<rect x="{REF_X}" y="{ny}" width="{UNC_X + OS - REF_X}" height="{bh}" rx="6" fill="#fbf3e4" stroke="{UNCERTAIN}" stroke-width="1.4"/>')
    o.append(f'<text x="{REF_X + 18}" y="{ny + 32}" font-size="23" font-weight="700" fill="{UNCERTAIN}">f is defective in all five dies → no evidence</text>')
    o.append(f'<text x="{REF_X + 18}" y="{ny + 63}" font-size="23" fill="{INK}">The region is flagged, not filled with invented</text>')
    o.append(f'<text x="{REF_X + 18}" y="{ny + 92}" font-size="23" fill="{INK}">structure. If f went undetected, it would leak through.</text>')

    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    OUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUT}")
