"""Draws the original raster visuals for the deck (hero art and method glyphs).

All data here is simulated with a fixed seed and is used only as illustration.
Run: python3 build_visuals.py  ->  writes PNGs into ./assets
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import norm, beta

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

NAVY = "#0B1F33"
TEAL = "#14A3A5"
TEAL_DK = "#0F8B8D"
AMBER = "#E3A43B"
STEEL = "#2F5D8A"
CORAL = "#C4553B"
SLATE = "#5E6B7A"
ICE = "#CFE9E7"


def hero():
    """Raw data -> fitted model with uncertainty -> forecast fan -> decision density."""
    rng = np.random.default_rng(7)
    fig = plt.figure(figsize=(6.05, 7.5), dpi=300)
    fig.patch.set_facecolor(NAVY)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # faint measurement grid
    for g in np.arange(0.5, 10, 0.5):
        ax.plot([g, g], [0, 10], color="white", alpha=0.035, lw=0.6)
        ax.plot([0, 10], [g, g], color="white", alpha=0.035, lw=0.6)

    # raw observations (history), x in [0.6, 6.4]
    x = np.sort(rng.uniform(0.6, 6.4, 170))
    trend = lambda t: 1.7 + 0.5 * t + 0.35 * np.sin(1.3 * t)
    y = trend(x) + rng.normal(0, 0.55, x.size)
    ax.scatter(x, y, s=10, color="white", alpha=0.55, linewidths=0, zorder=3)

    # fitted curve with confidence band
    xf = np.linspace(0.6, 6.4, 200)
    yf = trend(xf)
    band = 0.28 + 0.06 * np.abs(xf - 3.5)
    ax.fill_between(xf, yf - band, yf + band, color=TEAL, alpha=0.28, lw=0, zorder=2)
    ax.plot(xf, yf, color=TEAL, lw=2.6, zorder=4)

    # forecast fan (80% and 95% intervals widen with horizon)
    xc = np.linspace(6.4, 9.3, 120)
    yc = trend(xc)
    h = xc - 6.4
    for z, a in ((1.96, 0.13), (1.28, 0.22)):
        w = band[-1] + z * 0.36 * np.sqrt(h + 0.02)
        ax.fill_between(xc, yc - w, yc + w, color=AMBER, alpha=a, lw=0, zorder=2)
        ax.plot(xc, yc + w, color=AMBER, alpha=0.45, lw=0.8)
        ax.plot(xc, yc - w, color=AMBER, alpha=0.45, lw=0.8)
    ax.plot(xc, yc, color=AMBER, lw=2.4, ls=(0, (4, 2.2)), zorder=4)
    ax.plot([6.4, 6.4], [0.9, 9.4], color="white", alpha=0.25, lw=0.9, ls=(0, (2, 3)))

    # decision density: predictive distribution at the horizon, drawn sideways
    yy = np.linspace(3.0, 9.4, 300)
    mu, sd = trend(9.3), 0.8
    dens = norm.pdf(yy, mu, sd)
    dens = dens / dens.max() * 0.5
    ax.fill_betweenx(yy, 9.38, 9.38 + dens, color=AMBER, alpha=0.55, lw=0)
    ax.plot(9.38 + dens, yy, color=AMBER, lw=1.4)
    thr = mu - 0.55
    ax.plot([9.3, 9.95], [thr, thr], color="white", lw=1.0, alpha=0.8)

    # small stage markers along the base
    for xm, col in ((1.2, "white"), (3.5, TEAL), (7.9, AMBER)):
        ax.scatter([xm], [0.9], s=46, color=col, zorder=5)
    ax.plot([1.2, 7.9], [0.9, 0.9], color="white", alpha=0.25, lw=1)

    fig.savefig(os.path.join(OUT, "hero.png"), facecolor=NAVY)
    plt.close(fig)


def glyph(name, draw):
    fig = plt.figure(figsize=(2, 2), dpi=300)
    ax = fig.add_axes([0.06, 0.06, 0.88, 0.88])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    draw(ax)
    fig.savefig(os.path.join(OUT, f"glyph_{name}.png"), transparent=True)
    plt.close(fig)


def g_regression(ax):
    rng = np.random.default_rng(3)
    x = rng.uniform(1, 9, 28)
    y = 1.5 + 0.8 * x + rng.normal(0, 0.9, x.size)
    t = np.linspace(0.5, 9.5, 50)
    ax.fill_between(t, 1.5 + 0.8 * t - 0.9, 1.5 + 0.8 * t + 0.9, color=TEAL, alpha=0.18, lw=0)
    ax.scatter(x, y, s=34, color=STEEL, alpha=0.85, linewidths=0)
    ax.plot(t, 1.5 + 0.8 * t, color=TEAL_DK, lw=4)
    ax.plot([0.5, 9.5], [0.4, 0.4], color=SLATE, lw=2)
    ax.plot([0.5, 0.5], [0.4, 9.8], color=SLATE, lw=2)


def g_hypothesis(ax):
    t = np.linspace(0.3, 9.7, 300)
    d = norm.pdf(t, 4.6, 1.2)
    d = 1 + d / d.max() * 7.4
    lo, hi = 4.6 - 1.96 * 1.2, 4.6 + 1.96 * 1.2
    ax.fill_between(t, 1, d, where=t <= lo, color=CORAL, alpha=0.9, lw=0)
    ax.fill_between(t, 1, d, where=t >= hi, color=CORAL, alpha=0.9, lw=0)
    ax.plot(t, d, color=STEEL, lw=4)
    for c in (lo, hi):
        ax.plot([c, c], [1, 4.2], color=CORAL, lw=2, ls=(0, (2, 1.5)))
    ax.plot([0.3, 9.7], [1, 1], color=SLATE, lw=2)
    ax.plot([8.6, 8.6], [1, 7.6], color=AMBER, lw=3.5)
    ax.scatter([8.6], [7.6], s=70, color=AMBER, zorder=5)


def g_bayes(ax):
    t = np.linspace(0.01, 0.99, 300)
    xs = 0.6 + t * 8.8
    prior = beta.pdf(t, 2, 2)
    post = beta.pdf(t, 18, 9)
    s = 7.6 / post.max()
    ax.fill_between(xs, 1, 1 + prior * s, color=SLATE, alpha=0.18, lw=0)
    ax.plot(xs, 1 + prior * s, color=SLATE, lw=3, ls=(0, (3, 2)))
    ax.fill_between(xs, 1, 1 + post * s, color=TEAL, alpha=0.30, lw=0)
    ax.plot(xs, 1 + post * s, color=TEAL_DK, lw=4)
    ax.plot([0.3, 9.7], [1, 1], color=SLATE, lw=2)


def g_timeseries(ax):
    rng = np.random.default_rng(11)
    t = np.arange(0, 26)
    y = 3 + 0.12 * t + 0.9 * np.sin(t / 1.6) + rng.normal(0, 0.25, t.size)
    xs = 0.4 + t * 0.26
    ax.plot(xs, y, color=STEEL, lw=3.5)
    tf = np.arange(25, 36)
    yf = 3 + 0.12 * tf + 0.9 * np.sin(tf / 1.6)
    xf = 0.4 + tf * 0.26
    w = 0.25 + 0.32 * np.sqrt(tf - 25)
    ax.fill_between(xf, yf - 1.6 * w, yf + 1.6 * w, color=AMBER, alpha=0.28, lw=0)
    ax.plot(xf, yf, color=AMBER, lw=3.5, ls=(0, (3, 1.6)))
    ax.plot([0.3, 9.7], [0.6, 0.6], color=SLATE, lw=2)


def g_experiment(ax):
    rng = np.random.default_rng(5)
    # pool of units on the left, split into two arms
    px = rng.uniform(0.6, 3.0, 16)
    py = rng.uniform(2.5, 7.5, 16)
    ax.scatter(px, py, s=40, color=SLATE, alpha=0.8, linewidths=0)
    ax.annotate("", xy=(5.6, 7.6), xytext=(3.4, 5.4), arrowprops=dict(arrowstyle="-|>", color=SLATE, lw=2.6, mutation_scale=18))
    ax.annotate("", xy=(5.6, 2.6), xytext=(3.4, 4.6), arrowprops=dict(arrowstyle="-|>", color=SLATE, lw=2.6, mutation_scale=18))
    ax.add_patch(plt.Rectangle((5.9, 6.3), 3.6, 2.6, color=STEEL, alpha=0.9, lw=0))
    ax.add_patch(plt.Rectangle((5.9, 1.2), 3.6, 2.6, color=TEAL, alpha=0.9, lw=0))
    ax.text(7.7, 7.6, "A", color="white", ha="center", va="center", fontsize=20, fontweight="bold")
    ax.text(7.7, 2.5, "B", color="white", ha="center", va="center", fontsize=20, fontweight="bold")


def g_cluster(ax):
    rng = np.random.default_rng(21)
    for (cx, cy, col) in ((2.8, 7.0, TEAL), (7.2, 6.6, AMBER), (4.8, 2.6, STEEL)):
        pts = rng.normal(0, 0.75, (18, 2))
        ax.scatter(cx + pts[:, 0], cy + pts[:, 1], s=34, color=col, alpha=0.9, linewidths=0)
        ax.add_patch(plt.Circle((cx, cy), 1.9, fill=False, color=col, lw=2.2, ls=(0, (3, 2))))


if __name__ == "__main__":
    hero()
    for n, f in (("regression", g_regression), ("hypothesis", g_hypothesis), ("bayes", g_bayes),
                 ("timeseries", g_timeseries), ("experiment", g_experiment), ("cluster", g_cluster)):
        glyph(n, f)
    print("wrote", sorted(os.listdir(OUT)))
