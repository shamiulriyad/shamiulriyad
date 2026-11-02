"""Generate every figure and diagram of the dossier into ../figures/.

    python3 src/figures.py

All die images are SYNTHETIC renderings from prototype/toy_reference_memory.py.
They are conceptual illustrations, not SEM / optical measurements and not
experimental results; every caption in the dossier says so.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "prototype"))
sys.path.insert(0, HERE)
import toy_reference_memory as toy  # noqa: E402
from svgdiag import Diagram, NAVY, TEAL, AMBER, RED, GRAY  # noqa: E402
from tables import ROADMAP  # noqa: E402

OUT = os.path.join(ROOT, "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 8.5, "svg.fonttype": "none",
    "axes.edgecolor": "#5B6573", "axes.linewidth": 0.6, "figure.dpi": 150,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.04,
})
HEAT = LinearSegmentedColormap.from_list("heat", ["#0b1f33", "#1F3A5F", "#0F7C80", "#F2C14E", "#C0392B"])
STAMP = "Synthetic conceptual illustration — not real SEM / optical data"


def stamp(fig, y=-0.01):
    fig.text(0.5, y, STAMP, ha="center", va="top", fontsize=7, color="#8a5a12", style="italic")


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), format="svg")
    plt.close(fig)


def show(ax, img, title=None, cmap="gray", vmin=0, vmax=1, color="#1C2430", fs=8.5):
    ax.imshow(img, cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([])
    if title:
        ax.set_title(title, fontsize=fs, color=color, pad=3)


RNG = np.random.default_rng(3)
DEMO = toy.demo()


# ===========================================================================
# Illustrations
# ===========================================================================
def wafer_grid(radius=1.0, pitch=0.14):
    cells = []
    n = int(radius / pitch) + 2
    for i in range(-n, n):
        for j in range(-n, n):
            x, y = i * pitch, j * pitch
            corners = [(x, y), (x + pitch, y), (x, y + pitch), (x + pitch, y + pitch)]
            inside = all(np.hypot(cx, cy) < radius * 0.97 for cx, cy in corners)
            if inside:
                cells.append((i, j, x, y))
    return cells


def fig_wafer_die():
    fig = plt.figure(figsize=(7.2, 3.1))
    ax = fig.add_axes([0.0, 0.0, 0.42, 1.0])
    ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(patches.Circle((0, 0), 1.0, fc="#c9d3df", ec="#1F3A5F", lw=1.2))
    ax.add_patch(patches.Wedge((0, -1.0), 0.05, 0, 180, fc="white", ec="#1F3A5F", lw=1))
    pitch = 0.14
    cells = wafer_grid(1.0, pitch)
    pick = (2, 1)
    for i, j, x, y in cells:
        fc = "#8fa6bf"
        ax.add_patch(patches.Rectangle((x + 0.008, y + 0.008), pitch - 0.016, pitch - 0.016, fc=fc, ec="#1F3A5F", lw=0.4))
    px, py = pick[0] * pitch, pick[1] * pitch
    ax.add_patch(patches.Rectangle((px, py), pitch, pitch, fc="#F2C14E", ec="#B7791F", lw=1.4))
    ax.text(0, -1.17, "Wafer (e.g. 300 mm silicon disc)\nwith a grid of identical dies", ha="center", va="top", fontsize=8.5, color="#1F3A5F")
    ax.annotate("notch (orientation\nreference)", xy=(0, -0.98), xytext=(0.55, -1.12), fontsize=7.5, color="#5B6573",
                arrowprops=dict(arrowstyle="-", color="#5B6573", lw=0.7))
    ax.annotate("scribe lines\n(saw streets)", xy=(-0.42, 0.28), xytext=(-1.18, 0.75), fontsize=7.5, color="#5B6573",
                arrowprops=dict(arrowstyle="-", color="#5B6573", lw=0.7))
    ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.38, 1.1)
    ax2 = fig.add_axes([0.55, 0.08, 0.40, 0.86])
    die = toy.render_die(RNG)
    show(ax2, die)
    ax2.set_title("One die, magnified (stylised layout)", fontsize=8.5, color="#1F3A5F")
    for txt, xy, xyt in [("orientation mark", (24, 16), (205, 8)), ("memory array\n(repeated vias)", (92, 60), (205, 55)),
                         ("bond pads", (180, 112), (205, 112)), ("metal lines", (100, 140), (205, 160))]:
        ax2.annotate(txt, xy=xy, xytext=xyt, fontsize=7.5, color="#1C2430", annotation_clip=False,
                     arrowprops=dict(arrowstyle="-", color="#0F7C80", lw=0.8))
    con = patches.ConnectionPatch(xyA=(px + pitch, py + pitch), coordsA=ax.transData, xyB=(0, 0), coordsB=ax2.transData, color="#B7791F", lw=0.8, ls="--")
    fig.add_artist(con)
    con = patches.ConnectionPatch(xyA=(px + pitch, py), coordsA=ax.transData, xyB=(0, 191), coordsB=ax2.transData, color="#B7791F", lw=0.8, ls="--")
    fig.add_artist(con)
    stamp(fig, 0.0)
    save(fig, "ill_01_wafer_and_die.svg")


def fig_normal_vs_defect():
    rng = np.random.default_rng(11)
    normal = toy.render_die(rng)
    defective, mask = toy.add_defects(toy.render_die(rng), kinds=("particle", "scratch", "bridge", "missing_via"))
    fig = plt.figure(figsize=(7.2, 3.6))
    gs = fig.add_gridspec(2, 4, width_ratios=[1.6, 1.6, 1, 1], hspace=0.28, wspace=0.08)
    a = fig.add_subplot(gs[:, 0]); show(a, normal, "(a) Normal die", color="#0F7C80")
    b = fig.add_subplot(gs[:, 1]); show(b, defective, "(b) Defective die", color="#B03A2E")
    lab, n = ndimage.label(ndimage.binary_dilation(mask, iterations=3))
    for sl in ndimage.find_objects(lab):
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        b.add_patch(patches.Rectangle((x0 - 2, y0 - 2), x1 - x0 + 4, y1 - y0 + 4, fill=False, ec="#C0392B", lw=1.1))
    crops = [("particle", (70, 140)), ("scratch", (133, 65)), ("bridge", (118, 128)), ("missing via", (65, 61))]
    for k, (name, (cy, cx)) in enumerate(crops):
        ax = fig.add_subplot(gs[k // 2, 2 + k % 2])
        r = 14
        show(ax, defective[cy - r:cy + r, cx - r:cx + r])
        ax.set_title(f"(c{k + 1}) {name}", fontsize=8, color="#B03A2E", pad=2)
        ax_n = ax.inset_axes([0.0, -0.02, 0.36, 0.36])
        show(ax_n, normal[cy - r:cy + r, cx - r:cx + r])
        for s in ax_n.spines.values():
            s.set_edgecolor("#0F7C80"); s.set_linewidth(1.2)
    fig.text(0.79, 0.015, "large panel: defective crop · small inset: same place on the normal die", ha="center", fontsize=6.8, color="#5B6573")
    stamp(fig, -0.02)
    save(fig, "ill_02_normal_vs_defective.svg")


def fig_rotations():
    rng = np.random.default_rng(5)
    base, _ = toy.add_defects(toy.render_die(rng), kinds=("particle",))
    views = [("0°", base), ("90°", np.rot90(base, 1)), ("180°", np.rot90(base, 2)), ("270°", np.rot90(base, 3)),
             ("37° (arbitrary)", np.clip(ndimage.rotate(base, 37, reshape=False, mode="constant", cval=0.08), 0, 1)),
             ("shift + 8% scale", np.clip(ndimage.shift(ndimage.zoom(base, 1.08)[8:200, 8:200], (6, -9), mode="constant", cval=0.08), 0, 1)),
             ("illumination\ngradient", np.clip(base * (0.65 + 0.6 * np.linspace(0, 1, 192)[None, :]), 0, 1))]
    fig, axs = plt.subplots(1, 7, figsize=(7.4, 1.65))
    for ax, (t, im) in zip(axs, views):
        show(ax, im, t)
    stamp(fig, 0.02)
    save(fig, "ill_03_rotations.svg")


def fig_refs_targets():
    rng = np.random.default_rng(21)
    refs = [toy.render_die(rng, jitter=0.7) for _ in range(5)]
    tg = [toy.render_die(rng, jitter=0.7),
          toy.add_defects(toy.render_die(rng), kinds=("particle",), seed=1)[0],
          toy.render_die(rng, jitter=0.7),
          toy.add_defects(toy.render_die(rng), kinds=("scratch",), seed=2)[0],
          toy.add_defects(toy.render_die(rng), kinds=("bridge",), seed=3)[0],
          np.rot90(toy.render_die(rng, jitter=0.7), 1)]
    labels = [("Normal", "#0F7C80"), ("Suspicious\n(known: particle?)", "#B7791F"), ("Normal", "#0F7C80"),
              ("Unknown anomaly", "#B03A2E"), ("Suspicious", "#B7791F"), ("Normal\n(after alignment)", "#0F7C80")]
    fig = plt.figure(figsize=(7.4, 3.4))
    fig.text(0.02, 0.95, "(a) K = 5 reference dies given to the system (normal)", fontsize=9, color="#0F7C80", weight="bold")
    for k, r in enumerate(refs):
        ax = fig.add_axes([0.02 + k * 0.105, 0.55, 0.095, 0.36]); show(ax, r)
        for s in ax.spines.values():
            s.set_edgecolor("#0F7C80"); s.set_linewidth(2)
    fig.patches.append(patches.FancyArrowPatch((0.555, 0.73), (0.64, 0.73), transform=fig.transFigure, arrowstyle="-|>", mutation_scale=12, color="#0F7C80"))
    fig.patches.append(patches.FancyBboxPatch((0.65, 0.6), 0.32, 0.27, transform=fig.transFigure, boxstyle="round,pad=0.01", fc="#E2F1F1", ec="#0F7C80"))
    fig.text(0.81, 0.79, "Reference memory M", ha="center", fontsize=9, weight="bold", color="#0F7C80")
    fig.text(0.81, 0.66, "patch features of normal dies\n(no network re-training)", ha="center", fontsize=8, color="#1C2430")
    fig.text(0.02, 0.45, "(b) Previously unseen dies inspected against M (status labels are illustrative)", fontsize=9, color="#1F3A5F", weight="bold")
    for k, (im, (lab, col)) in enumerate(zip(tg, labels)):
        ax = fig.add_axes([0.02 + k * 0.163, 0.08, 0.13, 0.32]); show(ax, im)
        for s in ax.spines.values():
            s.set_edgecolor(col); s.set_linewidth(2)
        fig.text(0.02 + k * 0.163 + 0.065, 0.065, lab, ha="center", va="top", fontsize=7.5, color=col, weight="bold")
    stamp(fig, -0.05)
    save(fig, "ill_04_references_and_targets.svg")


def fig_localisation():
    """Diagram 6 — localisation chain, computed by the toy pipeline."""
    d = DEMO
    raw = np.clip(d["target"] * (0.45 + 0.9 * np.linspace(0, 1, 192)[None, :]) + 0.04 * np.sin(np.linspace(0, 3, 192))[:, None], 0, 1)
    fig, axs = plt.subplots(1, 5, figsize=(7.4, 1.95))
    show(axs[0], raw, "1. Original die\n(as acquired)")
    show(axs[1], d["refs"][0], "2. Normal reference\n(1 of K = 5)", color="#0F7C80")
    show(axs[2], d["target"], "3. Target die\n(preprocessed)")
    im = axs[3].imshow(d["amap"], cmap=HEAT, vmin=0, vmax=np.percentile(d["amap"], 99.8))
    axs[3].set_xticks([]); axs[3].set_yticks([]); axs[3].set_title("4. Anomaly map S\n(patch NN distance)", fontsize=8.5, pad=3)
    show(axs[4], d["target"], "5. Highlighted defect\nregions (S > τ)", color="#B03A2E")
    axs[4].contour(d["decision"], levels=[0.5], colors="#C0392B", linewidths=1.0)
    lab, n = ndimage.label(d["decision"])
    for k, sl in enumerate(ndimage.find_objects(lab)):
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        if (y1 - y0) * (x1 - x0) < 20:
            continue
        axs[4].add_patch(patches.Rectangle((x0 - 2, y0 - 2), x1 - x0 + 4, y1 - y0 + 4, fill=False, ec="#F2C14E", lw=1))
        sc = d["amap"][sl].max()
        axs[4].text(x0, y0 - 3, f"{sc:.2f}", color="#F2C14E", fontsize=6, va="bottom")
    cb = fig.colorbar(im, ax=axs[3], fraction=0.046, pad=0.02); cb.ax.tick_params(labelsize=6)
    stamp(fig, 0.0)
    save(fig, "dia_06_localisation.svg")


def fig_rotation_diagram():
    """Diagram 5 — rotation-robust inspection, computed by the toy pipeline."""
    d = DEMO
    fig = plt.figure(figsize=(7.4, 3.9))
    gs = fig.add_gridspec(2, 5, hspace=0.42, wspace=0.12)
    rots = [0, 90, 180, 270, 37]
    for k, a in enumerate(rots):
        ax = fig.add_subplot(gs[0, k])
        im = np.rot90(d["target"], a // 90) if a % 90 == 0 else np.clip(ndimage.rotate(d["target"], a, reshape=False, mode="constant", cval=0.08), 0, 1)
        show(ax, im, f"same die at {a}°")
    vmax = np.percentile(DEMO["amap"], 99.8)
    ax = fig.add_subplot(gs[1, 0]); show(ax, d["rot_target"], "(a) target at 37°", fs=8)
    ax = fig.add_subplot(gs[1, 1]); ax.imshow(d["naive_map"], cmap=HEAT, vmin=0, vmax=vmax); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("(b) no alignment:\nfalse alarms", fontsize=8, color="#B03A2E", pad=3)
    w, v = toy.warp_reference(d["refs"][0], d["angle_est"])
    ax = fig.add_subplot(gs[1, 2]); show(ax, np.where(v, w, 0.08), fs=8, title=f"(c) reference warped\n(estimated θ = {d['angle_est']:.0f}°)", color="#0F7C80")
    ax = fig.add_subplot(gs[1, 3]); ax.imshow(d["aligned_map"], cmap=HEAT, vmin=0, vmax=vmax); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("(d) aligned:\ndefects stand out", fontsize=8, color="#0F7C80", pad=3)
    ax = fig.add_subplot(gs[1, 4]); show(ax, d["rot_target"], fs=8, title="(e) regions on untouched\ntarget pixels")
    ax.contour(d["aligned_map"] > d["tau"], levels=[0.5], colors="#C0392B", linewidths=1)
    stamp(fig, 0.02)
    save(fig, "dia_05_rotation.svg")


def fig_wafermap():
    rng = np.random.default_rng(8)
    pitch = 0.1
    cells = wafer_grid(1.0, pitch)
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.3))
    for ax in axs:
        ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(patches.Circle((0, 0), 1.0, fc="#eef2f6", ec="#1F3A5F", lw=1))
        ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.12)
    scores = {}
    for i, j, x, y in cells:
        cx, cy = x + pitch / 2, y + pitch / 2
        s = rng.gamma(2.0, 0.08)
        if np.hypot(cx, cy) > 0.78 and cx > 0.1 and cy < 0.3:
            s += rng.uniform(0.35, 0.8)          # edge cluster
        if abs(cy - (0.9 * cx - 0.05)) < 0.06 and -0.6 < cx < 0.1:
            s += 0.55                              # scratch-like line
        scores[(i, j)] = s
    for (i, j, x, y) in cells:
        s = scores[(i, j)]
        col = HEAT(min(s / 0.9, 1.0))
        axs[0].add_patch(patches.Rectangle((x + 0.005, y + 0.005), pitch - 0.01, pitch - 0.01, fc=col, ec="white", lw=0.3))
        flag = s > 0.45
        axs[1].add_patch(patches.Rectangle((x + 0.005, y + 0.005), pitch - 0.01, pitch - 0.01,
                                           fc="#C0392B" if flag else "#9fb8a9", ec="white", lw=0.3))
    axs[0].set_title("(a) Per-die anomaly score\n(max of each die's anomaly map)", fontsize=8.5)
    axs[1].set_title("(b) Suspicious dies (score > τ) and\nspatial clusters", fontsize=8.5)
    axs[1].add_patch(patches.Ellipse((0.62, -0.25), 0.62, 0.95, angle=20, fill=False, ec="#B7791F", lw=1.4, ls="--"))
    axs[1].text(0.72, -0.85, "edge cluster", color="#B7791F", fontsize=7.5, bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
    axs[1].add_patch(patches.Ellipse((-0.25, -0.3), 0.95, 0.22, angle=42, fill=False, ec="#B7791F", lw=1.4, ls="--"))
    axs[1].text(-0.62, -0.78, "line (scratch-like)\npattern", color="#B7791F", fontsize=7.5, ha="center", bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
    stamp(fig, 0.03)
    save(fig, "ill_06_wafer_map.svg")


def fig_data_types():
    rng = np.random.default_rng(4)
    die, _ = toy.add_defects(toy.render_die(rng), kinds=("particle", "scratch"))
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.9), gridspec_kw=dict(width_ratios=[1, 1.1]))
    show(axs[0], die, "(a) Die-surface IMAGE\n(one die · pixels · µm–nm detail)", color="#1F3A5F")
    axs[0].text(96, 205, "question: WHERE on this die is a defect?", ha="center", fontsize=7.5, color="#5B6573")
    ax = axs[1]; ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(patches.Circle((0, 0), 1.0, fc="#eef2f6", ec="#1F3A5F"))
    pitch = 0.125
    for i, j, x, y in wafer_grid(1.0, pitch):
        bad = (np.hypot(x, y) > 0.7 and rng.random() < 0.6) or rng.random() < 0.05
        ax.add_patch(patches.Rectangle((x + 0.006, y + 0.006), pitch - 0.012, pitch - 0.012, fc="#C0392B" if bad else "#9fb8a9", ec="white", lw=0.3))
    ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.25, 1.12)
    ax.set_title("(b) WAFER MAP (one cell = one die · pass/fail)\ne.g. WM-811K", fontsize=8.5, color="#1F3A5F")
    ax.text(0, -1.18, "question: WHICH dies fail, in what spatial pattern?", ha="center", fontsize=7.5, color="#5B6573")
    stamp(fig, 0.02)
    save(fig, "ill_00_data_types.svg")


def fig_feedback_ui():
    d = DEMO
    fig = plt.figure(figsize=(7.2, 3.0))
    fig.patches.append(patches.FancyBboxPatch((0.01, 0.04), 0.98, 0.9, transform=fig.transFigure, boxstyle="round,pad=0.005", fc="#F7F9FB", ec="#5B6573", zorder=-5))
    fig.text(0.03, 0.89, "Review card · Wafer W07 · die (12, 5) · recipe LAYER-M1 · status: SUSPICIOUS · score 0.93 (τ = 0.45)", fontsize=8.2, weight="bold", color="#1F3A5F")
    ax = fig.add_axes([0.03, 0.1, 0.26, 0.72]); show(ax, d["target"], "target die", color="#1C2430")
    ax2 = fig.add_axes([0.31, 0.1, 0.26, 0.72]); ax2.imshow(d["target"], cmap="gray"); ax2.imshow(np.ma.masked_less(d["amap"], d["tau"]), cmap=HEAT, alpha=0.75, vmin=0, vmax=1.2)
    ax2.set_xticks([]); ax2.set_yticks([]); ax2.set_title("anomaly overlay (3 regions)", fontsize=8.5, pad=3)
    btns = [("Confirm defect", "#0F7C80"), ("Reject (false alarm)", "#5B6573"), ("Correct location", "#1F3A5F"),
            ("Assign label: particle / scratch / bridge …", "#1F3A5F"), ("Mark UNKNOWN → investigate", "#B03A2E")]
    for k, (t, c) in enumerate(btns):
        y = 0.72 - k * 0.13
        fig.patches.append(patches.FancyBboxPatch((0.61, y), 0.36, 0.09, transform=fig.transFigure, boxstyle="round,pad=0.006", fc="white", ec=c, lw=1.4))
        fig.text(0.79, y + 0.045, t, ha="center", va="center", fontsize=8, color=c, weight="bold")
    fig.text(0.79, 0.075, "Each action is logged with reviewer ID, time and memory version.\nNothing enters memory before the verification gate (Section 18.10).", ha="center", fontsize=6.8, color="#5B6573")
    stamp(fig, 0.03)
    save(fig, "ill_07_feedback_card.svg")


# ===========================================================================
# Block diagrams (pure SVG)
# ===========================================================================
def dia_concept():
    D = Diagram(780, 290, "Diagram 1 · Complete research concept")
    W, H, G, X0 = 128, 74, 26, 18
    row1 = [("1 Reference\nsamples", "K = 1–10 dies\n(normal; optional\nknown defects)", "teal"),
            ("2 Sample\nenrolment", "preprocess, crop,\nalign to template", "teal"),
            ("3 Feature\nextraction", "frozen pretrained\nencoder, multi-scale", "navy"),
            ("4 Reference\nmemory M", "patch features +\nprototypes, versioned", "teal"),
            ("5 New die\ninspection", "unseen die, any\norientation", "navy")]
    row2 = [("6 Anomaly\ndetection", "distance to memory\n→ anomaly score", "navy"),
            ("7 Defect\nlocalisation", "anomaly map,\nregions, boxes", "navy"),
            ("8 Engineer\nverification", "confirm / reject /\ncorrect / label", "amber"),
            ("9 Reference\nadaptation", "gated, reversible\nmemory update", "amber")]
    xs = [X0 + k * (W + G) for k in range(5)]
    for k, (t, s, st) in enumerate(row1):
        D.box(xs[k], 40, W, H, t, s, st, size=10, subsize=8)
        if k < 4:
            D.arrow(xs[k] + W, 77, xs[k + 1] - 2, 77)
    xs2 = [xs[4], xs[3], xs[2], xs[1]]
    for k, (t, s, st) in enumerate(row2):
        D.box(xs2[k], 160, W, H, t, s, st, size=10, subsize=8)
        if k < 3:
            D.arrow(xs2[k], 197, xs2[k + 1] + W + 2, 197)
    D.arrow(xs[4] + W / 2, 114, xs[4] + W / 2, 158)
    D.path(f"M{xs[1] + W / 2},{160} L{xs[1] + W / 2},{137} L{xs[3] + W / 2 - 20},{137} L{xs[3] + W / 2 - 20},{116}", color=AMBER, dash="5,3")
    D.text((xs[1] + xs[3]) / 2 + W / 2 - 10, 132, "verified knowledge flows back into memory", size=8.3, color=AMBER, italic=True)
    D.box(X0, 160, W, H, "Output", "status · heat map ·\nscore · confidence", "white", size=10, subsize=8)
    D.path(f"M{xs2[1] + W / 2},{234} L{xs2[1] + W / 2},{252} L{X0 + W / 2},{252} L{X0 + W / 2},{236}", color=GRAY, dash="3,3")
    D.text((xs2[1] + X0 + W) / 2, 266, "inspection report", size=8, color=GRAY, italic=True)
    D.text(390, 283, "Teal = reference knowledge · navy = automatic inspection · amber = human-verified feedback", size=8.5, color=GRAY)
    D.save(os.path.join(OUT, "dia_01_concept.svg"))


def dia_architecture():
    D = Diagram(800, 740, "Diagram 2 · Detailed system architecture")
    D.text(110, 44, "A · Reference enrolment", size=10, weight="700", color=TEAL)
    D.text(110, 56, "(once per die type / recipe)", size=8, color=GRAY)
    D.text(507, 44, "B · Inspection of a new die", size=10, weight="700", color=NAVY)
    D.text(507, 56, "(every die)", size=8, color=GRAY)
    D.text(712, 44, "C · Feedback", size=10, weight="700", color=AMBER)
    D.text(712, 56, "(verified cases)", size=8, color=GRAY)
    # Enrolment column
    ex, ew = 18, 186
    E = [("Reference dies", "K normal images; optional\nfew known-defect images", "teal"),
         ("Preprocess + QC", "focus / noise / saturation\ncheck; reject bad images", "teal"),
         ("Canonical pose", "register each reference to\none template die", "teal"),
         ("Shared encoder f", "same frozen weights as\ninspection (layers 2+3)", "teal"),
         ("Memory QC", "remove outliers, de-duplicate,\ncoreset subsample", "teal")]
    for k, (t, s, st) in enumerate(E):
        y = 70 + k * 76
        D.box(ex, y, ew, 56, t, s, st, size=10, subsize=7.9)
        if k < len(E) - 1:
            D.arrow(ex + ew / 2, y + 56, ex + ew / 2, y + 74, color=TEAL)
    # Memory bank
    mx, my, mw, mh = 222, 300, 166, 200
    D.box(mx, my, mw, mh, "Reference memory M", "normal patch features M_N\n\nknown-defect prototypes\nM_D (optional)\n\nversion log, provenance,\nquarantine buffer", "teal", size=11, subsize=8.4)
    D.arrow(ex + ew, 98 + 4 * 76, mx - 2, 420, color=TEAL)
    D.text(196, 452, "enrol", size=8, color=TEAL, italic=True)
    # Inspection column
    ix, iw = 404, 206
    steps = [("Input", "die / wafer images + metadata\n(wafer ID, die index, recipe)"),
             ("1 Preprocessing", "illumination & contrast norm.;\nquality check (no smoothing)"),
             ("2 Die extraction", "find die grid, crop, index (i, j)"),
             ("3 Geometric registration", "estimate T (rotation, shift, scale);\nwarp the REFERENCE, not target"),
             ("4 Visual feature encoder f", "frozen CNN / ViT;\nmulti-scale patch features"),
             ("5 Feature matching", "k-NN search in M (within\naligned search window)"),
             ("6 Anomaly scoring", "patch distance → map S,\nimage score A(x)"),
             ("7 Localisation", "upsample, threshold τ →\nregions, boxes, masks"),
             ("8 Known / unknown triage", "match region features to M_D:\nknown class or UNKNOWN"),
             ("9 Confidence estimation", "calibrated score; margin to τ;\nreview flag if uncertain")]
    for k, (t, s) in enumerate(steps):
        y = 64 + k * 58
        D.box(ix, y, iw, 44, t, s, "navy" if k else "gray", size=9.6, subsize=7.6)
        D.arrow(ix + iw / 2, y + 44, ix + iw / 2, y + 56, color=NAVY)
    D.box(ix, 644, iw, 50, "Output", "Normal / Suspicious / Unknown · heat map\nmask or box · A(x) · confidence", "white", size=10, subsize=7.8)
    D.arrow(mx + mw, 372, ix - 2, 372, color=TEAL)
    D.arrow(ix - 2, 386, mx + mw + 2, 386, color=NAVY)
    D.text(396, 364, "query", size=7.6, color=NAVY, anchor="end", italic=True)
    D.path(f"M{mx + mw - 30},{my} L{mx + mw - 30},{258} L{ix - 2},{258}", color=TEAL, dash="4,3")
    D.text(mx + mw - 26, 252, "reference pose", size=7.6, color=TEAL, anchor="start", italic=True)
    D.path(f"M{mx + mw - 10},{my + mh} L{mx + mw - 10},{548} L{ix - 2},{548}", color=TEAL, dash="4,3")
    D.text(mx + mw - 6, 562, "defect prototypes", size=7.6, color=TEAL, anchor="start", italic=True)
    # Feedback column
    fx, fw = 630, 160
    F = [("Engineer verification", "via review queue: confirm ·\nreject · correct · label · unknown"),
         ("Verification gate", "quarantine; novelty gate;\n2nd review for 'normal' adds"),
         ("Regression check", "held-out dies: accept the\nnew version or roll back"),
         ("Versioned memory update", "add / remove / relabel items;\nlog provenance")]
    for k, (t, s) in enumerate(F):
        y = 330 + k * 92
        D.box(fx, y, fw, 62, t, s, "amber", size=9.6, subsize=7.8)
        if k < len(F) - 1:
            D.arrow(fx + fw / 2, y + 62, fx + fw / 2, y + 90, color=AMBER)
    D.path(f"M{ix + iw},{669} L{620},{669} L{620},{361} L{fx - 2},{361}", color=AMBER)
    D.path(f"M{fx + fw / 2},{330 + 3 * 92 + 62} L{fx + fw / 2},{722} L{mx + 40},{722} L{mx + 40},{my + mh + 2}", color=AMBER)
    D.text(470, 716, "verified, gated update of M (no weight training)", size=8.2, color=AMBER, italic=True)
    D.text(110, 492, "Optional (periodic):\nfine-tune encoder with replay;\nsee Diagram 8", size=7.8, color=GRAY)
    D.save(os.path.join(OUT, "dia_02_architecture.svg"))


def wafer_svg(D, cx, cy, r, pitch, colors, label=None):
    D.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#EEF2F6" stroke="{NAVY}" stroke-width="1.2"/>')
    n = int(r / pitch) + 1
    cells = []
    for i in range(-n, n):
        for j in range(-n, n):
            x, y = cx + i * pitch, cy + j * pitch
            if all(np.hypot(px - cx, py - cy) < r * 0.96 for px, py in [(x, y), (x + pitch, y), (x, y + pitch), (x + pitch, y + pitch)]):
                cells.append((i, j, x, y))
    for (i, j, x, y) in cells:
        c = colors.get((i, j), "#B9C6D6")
        D.raw(f'<rect x="{x + 1:.1f}" y="{y + 1:.1f}" width="{pitch - 2:.1f}" height="{pitch - 2:.1f}" fill="{c}" stroke="#FFFFFF" stroke-width="0.6"/>')
    if label:
        D.text(cx, cy + r + 18, label, size=9.5, weight="700", color=NAVY)
    return cells


def dia_same_wafer():
    D = Diagram(780, 300, "Diagram 3 · Same-wafer inspection (Scenario 1)")
    ref = {(-2, -1): TEAL, (1, -3): TEAL, (2, 1): TEAL, (-3, 2): TEAL, (0, 2): TEAL}
    col = dict(ref)
    col[(3, -1)] = RED
    col[(-1, 0)] = AMBER
    wafer_svg(D, 150, 150, 110, 24, col, "Wafer W07 (one lot, one layer)")
    D.box(320, 70, 150, 70, "Enrol references", "5 normal dies (teal),\nchosen spread across\nthe wafer", "teal", size=10, subsize=8)
    D.box(320, 170, 150, 66, "Reference memory M", "built only from\nwafer W07 references", "teal", size=10, subsize=8)
    D.arrow(262, 105, 318, 105, color=TEAL)
    D.arrow(395, 140, 395, 168, color=TEAL)
    D.box(540, 60, 220, 190, "Inspect every other die", None, "white", size=10)
    D.raw(f'<rect x="556" y="100" width="16" height="16" fill="#B9C6D6"/>')
    D.text(580, 112, "normal (most dies)", size=8.5, anchor="start")
    D.raw(f'<rect x="556" y="128" width="16" height="16" fill="{AMBER}"/>')
    D.text(580, 140, "suspicious → review", size=8.5, anchor="start")
    D.raw(f'<rect x="556" y="156" width="16" height="16" fill="{RED}"/>')
    D.text(580, 168, "defect localised", size=8.5, anchor="start")
    D.raw(f'<rect x="556" y="184" width="16" height="16" fill="{TEAL}"/>')
    D.text(580, 196, "reference die (not scored)", size=8.5, anchor="start")
    D.text(650, 226, "same tool, recipe and lot:\nsmallest domain shift", size=8.2, color=GRAY)
    D.arrow(470, 203, 538, 170, color=NAVY, label="compare", lx=505, ly=178)
    D.text(390, 290, "Evaluation must keep reference dies out of the test set and report results per wafer (Section 20).", size=8.4, color=GRAY)
    D.save(os.path.join(OUT, "dia_03_same_wafer.svg"))


def dia_cross_wafer():
    D = Diagram(800, 350, "Diagram 4 · Cross-wafer and cross-type generalisation (Scenario 2)")
    ref = {(-2, -1): TEAL, (1, -2): TEAL, (2, 1): TEAL, (-2, 2): TEAL, (0, 1): TEAL}
    wafer_svg(D, 110, 170, 90, 22, ref, "Wafer A · lot 1 · design X")
    D.box(225, 125, 130, 80, "Memory M(A)", "references from\nwafer A only", "teal", size=10, subsize=8)
    D.arrow(200, 165, 223, 165, color=TEAL)
    wafer_svg(D, 470, 100, 62, 22, {(1, 0): AMBER}, None)
    D.text(470, 182, "Wafer B · lot 7 · same design X", size=9.2, weight="700", color=NAVY)
    wafer_svg(D, 470, 262, 62, 15, {(2, -1): AMBER, (-1, 1): AMBER}, None)
    D.text(470, 342, "Wafer C · different design Y", size=9.2, weight="700", color=NAVY)
    D.arrow(355, 150, 400, 110, color=NAVY, dash="5,3")
    D.arrow(355, 185, 400, 250, color=NAVY, dash="5,3")
    D.badge(378, 120, "?", "amber", w=22)
    D.badge(378, 230, "?", "amber", w=22)
    D.box(560, 52, 225, 104, "2a · Cross-wafer, same design", "Shift: process drift, focus,\nillumination, tool, lot.\nHypothesis H3: works with a small\nloss; re-enrol 1–2 dies if not.", "navy", size=9.6, subsize=8)
    D.box(560, 210, 225, 104, "2b · Cross-type (new design)", "Layout itself is different: memory\nof design X has no normal\nexample of design Y. Expected to\nfail without new references.", "red", size=9.6, subsize=8)
    D.badge(200, 52, "Research objective — requires validation, not assumed", "amber", size=8.6)
    D.save(os.path.join(OUT, "dia_04_cross_wafer.svg"))


def dia_feedback():
    D = Diagram(780, 400, "Diagram 7 · Feedback-driven adaptation cycle")
    nodes = [(60, 60, "1 AI inspection", "memory version v_t;\nscores, maps, status"),
             (310, 60, "2 Review queue", "prioritise uncertain,\nunknown, high-impact"),
             (560, 60, "3 Engineer verification", "confirm · reject · correct\n· label · mark unknown"),
             (560, 250, "4 Verification gate", "quarantine; novelty gate;\n2nd reviewer for 'normal'"),
             (310, 250, "5 Versioned memory update", "M_(t+1) = U(M_t, verified\nfeedback); log provenance"),
             (60, 250, "6 Regression check", "held-out dies: no loss in\nAUROC / recall → accept")]
    st = ["navy", "navy", "amber", "amber", "teal", "gray"]
    for (x, y, t, s), sty in zip(nodes, st):
        D.box(x, y, 170, 74, t, s, sty, size=10, subsize=8.2)
    D.arrow(230, 97, 308, 97, color=NAVY)
    D.arrow(480, 97, 558, 97, color=NAVY)
    D.arrow(645, 134, 645, 248, color=AMBER, label="verified decisions", lx=650, ly=195, anchor="start")
    D.arrow(558, 287, 482, 287, color=AMBER, label="accepted items", ly=280)
    D.arrow(308, 287, 232, 287, color=TEAL, label="candidate v_(t+1)", ly=280)
    D.arrow(145, 248, 145, 136, color=TEAL, label="deploy v_(t+1)", lx=150, ly=195, anchor="start")
    D.path("M100,324 C100,370 400,370 395,326", color=RED, dash="5,3")
    D.text(250, 375, "fail → roll back to v_t and inspect the offending feedback", size=8.4, color=RED, italic=True)
    D.text(645, 360, "rejected / doubtful feedback\nstays in quarantine", size=8.2, color=AMBER, italic=True)
    D.text(390, 175, "The model weights stay frozen in this loop;\nonly the reference memory changes, and every change can be undone.", size=8.8, color=GRAY)
    D.save(os.path.join(OUT, "dia_07_feedback.svg"))


def dia_train_infer():
    D = Diagram(800, 420, "Diagram 8 · Training vs enrolment vs inference vs update")
    cols = [(18, 170, "Stage"), (194, 250, "What happens"), (450, 110, "How often"), (566, 120, "What changes"), (692, 100, "Compute")]
    for x, w, t in cols:
        D.text(x + w / 2, 46, t, size=9.6, weight="700", color=NAVY)
    rows = [("Offline pre-training", "Encoder (e.g. WRN-50, DINOv2) trained\non large public data by its authors;\nwe download the weights", "once (not by us)", "nothing in our\nproject", "none", "gray", "WEIGHTS FROZEN"),
            ("Reference enrolment", "K reference dies → preprocess → align\n→ features → memory M (with QC)", "per die type /\nrecipe", "memory M", "seconds–\nminutes, GPU/CPU", "teal", ""),
            ("Inference (inspection)", "new die → align → features → compare\nwith M → map S, score A, status", "every die", "nothing\n(read-only)", "ms–s per die", "navy", ""),
            ("Feedback update", "verified feedback → gate → versioned\nedit of M → regression check", "per verified\nbatch", "memory M\n(versioned)", "seconds", "amber", ""),
            ("Optional fine-tuning", "periodic adaptation of encoder with\nreplay of old data; only after validation", "rare (e.g.\nper quarter)", "encoder\nweights", "hours, GPU", "red", "ADVANCED / OPTIONAL")]
    for k, (a, b, c, d_, e, sty, tag) in enumerate(rows):
        y = 60 + k * 70
        D.box(18, y, 170, 58, a, tag or None, sty, size=10, subsize=7.6)
        D.rect(194, y, 250, 58, "#FFFFFF", "#C9D1DB", rx=4, sw=1)
        D.text(319, y + 32 - (b.count("\n")) * 5.1, b, size=8.3)
        for (x, w, _), val in zip(cols[2:], (c, d_, e)):
            D.rect(x, y, w - 6, 58, "#FFFFFF", "#C9D1DB", rx=4, sw=1)
            D.text(x + (w - 6) / 2, y + 32 - (val.count("\n")) * 5.1, val, size=8.4)
    D.text(400, 416, "Core project = rows 2–4 (no gradient training). Row 5 is an optional extension that must pass the same regression checks.", size=8.5, color=GRAY)
    D.save(os.path.join(OUT, "dia_08_train_vs_inference.svg"))


def dia_workflow():
    D = Diagram(800, 250, "End-to-end research workflow (Artifact 6)")
    steps = [("Literature\n& gap", "teal"), ("Data audit\n& splits", "teal"), ("Baseline\nreproduction", "navy"), ("Few-shot\nenrolment", "navy"),
             ("Rotation &\nalignment", "navy"), ("Localisation", "navy"), ("Unknown\ntriage", "navy"), ("Feedback\nadaptation", "amber"),
             ("Comparison\n& ablation", "gray"), ("Paper &\nrelease", "gray")]
    w, g = 70, 9
    for k, (t, s) in enumerate(steps):
        x = 14 + k * (w + g)
        D.box(x, 70, w, 62, t, None, s, size=8.8)
        if k < len(steps) - 1:
            D.arrow(x + w, 101, x + w + g - 1, 101, sw=1.2)
    gates = [(2, "Gate 1: published numbers\nreproduced on MVTec AD"), (4, "Gate 2: few-shot curves\nwith confidence intervals"),
             (6, "Gate 3: open-set results\nper held-out class"), (8, "Gate 4: all experiments\nrun or documented")]
    for k, t in gates:
        x = 14 + k * (w + g) + w / 2
        D.raw(f'<polygon points="{x},{146} {x + 9},{155} {x},{164} {x - 9},{155}" fill="#FBF1DF" stroke="{AMBER}"/>')
        D.text(x, 182, t, size=7.6, color=AMBER)
    D.text(400, 236, "Each gate must be passed before claims built on it are made; negative results are recorded, not discarded.", size=8.4, color=GRAY)
    D.text(160, 56, "core research milestones →", size=8, color=GRAY)
    D.text(637, 56, "optional (core if time) ↓", size=8, color=GRAY)
    D.save(os.path.join(OUT, "dia_09_workflow.svg"))


def dia_gantt():
    D = Diagram(800, 60 + 26 * len(ROADMAP) + 40, "Implementation roadmap (40 weeks)")
    x0, x1 = 250, 780
    scale = (x1 - x0) / 40
    for wk in range(0, 41, 4):
        x = x0 + wk * scale
        D.raw(f'<line x1="{x:.1f}" y1="40" x2="{x:.1f}" y2="{50 + 26 * len(ROADMAP)}" stroke="#E3E7ED"/>')
        D.text(x, 36, f"w{wk}", size=7.6, color=GRAY)
    for k, r in enumerate(ROADMAP):
        y = 50 + k * 26
        a, b = [int(v) for v in r["weeks"].split("–")]
        D.text(240, y + 14, f"{r['n']}. {r['phase']}", size=8.6, anchor="end")
        fill = TEAL if r["core"] else AMBER
        D.raw(f'<rect x="{x0 + (a - 1) * scale:.1f}" y="{y + 3}" width="{(b - a + 1) * scale:.1f}" height="16" rx="3" fill="{fill}" opacity="0.85"/>')
    y = 60 + 26 * len(ROADMAP)
    D.raw(f'<rect x="300" y="{y}" width="14" height="10" fill="{TEAL}"/>')
    D.text(320, y + 9, "core milestone", size=8, anchor="start")
    D.raw(f'<rect x="440" y="{y}" width="14" height="10" fill="{AMBER}"/>')
    D.text(460, y + 9, "core-if-time / advanced (feedback)", size=8, anchor="start")
    D.save(os.path.join(OUT, "dia_10_gantt.svg"))


def dia_triage():
    D = Diagram(780, 250, "Three-way triage of a suspicious region (Stage 8)")
    D.box(16, 90, 140, 64, "Region r with\nhigh anomaly score", None, "navy", size=9.6)
    D.box(196, 90, 150, 64, "Is A(r) > τ_n ?", "distance to NORMAL\nmemory M_N", "white", size=10, subsize=8)
    D.arrow(156, 122, 194, 122)
    D.box(196, 190, 150, 44, "NORMAL", "no action", "teal", size=10, subsize=8)
    D.arrow(271, 154, 271, 188, label="no", lx=280, ly=175, anchor="start")
    D.box(392, 90, 170, 64, "d_c = distance to each\nknown-defect prototype", "nearest class c*, margin\nto 2nd nearest", "white", size=9.4, subsize=8)
    D.arrow(346, 122, 390, 122, label="yes", ly=114)
    D.box(608, 30, 160, 58, "KNOWN defect c*", "if d_c* < τ_k and margin\nis large", "amber", size=10, subsize=8)
    D.box(608, 110, 160, 58, "AMBIGUOUS", "close to 2+ classes →\nreview with top-2 labels", "gray", size=10, subsize=8)
    D.box(608, 190, 160, 50, "UNKNOWN anomaly", "far from all known\nclasses → investigate", "red", size=10, subsize=8)
    D.arrow(562, 112, 606, 62, color=AMBER)
    D.arrow(562, 122, 606, 138)
    D.arrow(562, 134, 606, 212, color=RED)
    D.text(480, 210, "The normal-reference test always runs first,\nso an unfamiliar defect can never be\nhidden by forcing it into a known class.", size=8.2, color=GRAY)
    D.save(os.path.join(OUT, "dia_11_triage.svg"))


def dia_alignment():
    D = Diagram(780, 230, "Defect-preserving alignment: two ways to align, one recommended")
    D.box(16, 50, 170, 60, "Target die x", "native pixel grid", "navy", size=10, subsize=8)
    D.box(16, 140, 170, 60, "Reference dies R", "K normal images", "teal", size=10, subsize=8)
    D.box(240, 95, 150, 60, "Estimate T", "coarse: 0/90/180/270 +\nFourier–Mellin; fine: ECC", "white", size=10, subsize=7.8)
    D.arrow(186, 80, 238, 115); D.arrow(186, 170, 238, 135, color=TEAL)
    D.box(440, 30, 320, 74, "Option A (NOT recommended): warp the target", "T⁻¹(x) resamples the die under inspection: a 1–2 px\ndefect is interpolated, blurred or partly cut at borders", "red", size=9.6, subsize=8)
    D.box(440, 126, 320, 84, "Option B (recommended): warp the references", "T(R) brings references into the target's frame; target\npixels are never resampled; invalid border regions are\nmasked; references are clean, so interpolation is harmless", "teal", size=9.6, subsize=8)
    D.arrow(390, 115, 438, 70, color=RED, dash="4,3")
    D.arrow(390, 135, 438, 165, color=TEAL)
    D.save(os.path.join(OUT, "dia_12_alignment_options.svg"))


if __name__ == "__main__":
    fig_data_types(); fig_wafer_die(); fig_normal_vs_defect(); fig_rotations(); fig_refs_targets()
    fig_localisation(); fig_rotation_diagram(); fig_wafermap(); fig_feedback_ui()
    dia_concept(); dia_architecture(); dia_same_wafer(); dia_cross_wafer(); dia_feedback(); dia_train_infer()
    dia_workflow(); dia_gantt(); dia_triage(); dia_alignment()
    print("figures written to", OUT)
