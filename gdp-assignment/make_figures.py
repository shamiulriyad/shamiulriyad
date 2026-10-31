# Builds every chart and the cover image for the GDP assignment.
# Single-colour (navy) scheme so the document prints cleanly in one colour.
# Usage: python3 gdp-assignment/make_figures.py
from pathlib import Path
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)

NAVY = "#1F3864"   # main ink
MID = "#4A6A9E"    # mid tint
LIGHT = "#A9BCDB"  # light tint
PALE = "#E3EAF5"
GREY = "#595959"
GRID = "#D9D9D9"

plt.rcParams.update({
    "font.family": "Liberation Serif",
    "font.size": 10.5,
    "axes.edgecolor": GREY,
    "axes.labelcolor": "#262626",
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.6,
    "axes.axisbelow": True,
    "xtick.color": GREY,
    "ytick.color": GREY,
    "legend.frameon": False,
    "savefig.dpi": 220,
    "savefig.bbox": "tight",
})


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", facecolor="white")
    plt.close(fig)


def bar_ends(ax):
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)


# ---------- Cover image (topic written on the front) ----------
def cover():
    W, H = 6.6, 4.3
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100); ax.set_ylim(0, 65); ax.axis("off")
    # vertical navy gradient
    grad = np.linspace(0, 1, 256).reshape(-1, 1)
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("n", ["#0E1E3D", NAVY, "#2E4C80"])
    ax.imshow(grad, extent=[0, 100, 0, 65], aspect="auto", cmap=cmap, origin="lower", zorder=0)
    # faint grid
    for x in range(0, 101, 5):
        ax.plot([x, x], [0, 65], color="white", alpha=0.05, lw=0.6, zorder=1)
    for y in range(0, 66, 5):
        ax.plot([0, 100], [y, y], color="white", alpha=0.05, lw=0.6, zorder=1)
    # rising bars (GDP)
    xs = np.arange(48, 98, 4.2)
    hs = 6 + 1.9 * np.arange(len(xs)) ** 1.25
    for x, h in zip(xs, hs):
        ax.add_patch(Rectangle((x, 4), 3.0, h, color="white", alpha=0.13, lw=0, zorder=2))
    # GDP line rising, well-being line flattening
    t = np.linspace(0, 1, 120)
    gx = 44 + 54 * t
    gdp = 8 + 34 * t ** 1.4
    wb = 8 + 18 * (1 - np.exp(-4 * t))
    ax.plot(gx, gdp + 4, color="white", lw=2.4, alpha=0.95, zorder=3)
    ax.plot(gx, wb + 4, color=LIGHT, lw=2.0, ls=(0, (5, 3)), alpha=0.95, zorder=3)
    ax.scatter([gx[-1]], [gdp[-1] + 4], s=28, color="white", zorder=4)
    ax.scatter([gx[-1]], [wb[-1] + 4], s=28, color=LIGHT, zorder=4)
    ax.text(gx[-1] - 1, gdp[-1] + 6.5, "GDP", color="white", ha="right", fontsize=9, fontweight="bold", zorder=4)
    ax.text(gx[-1] - 1, wb[-1] + 6.5, "Well-being", color=LIGHT, ha="right", fontsize=9, fontweight="bold", zorder=4)
    # text panel on the left
    ax.add_patch(Rectangle((0, 0), 52, 65, color="#0B1830", alpha=0.55, lw=0, zorder=2))
    ax.plot([5, 5], [16, 56], color=LIGHT, lw=2.2, zorder=5)
    ax.text(8, 55, "ASSIGNMENT ON", color=LIGHT, fontsize=10, fontweight="bold", zorder=5, va="top")
    ax.text(8, 49.5, "Is GDP Growth an\nAdequate Measure\nof Economic\nWell-Being?", color="white",
            fontsize=21, fontweight="bold", va="top", linespacing=1.12, zorder=5)
    ax.text(8, 18.5, "A critical evaluation with global\nevidence and a Bangladesh case study",
            color="#DCE4F2", fontsize=9.6, style="italic", va="top", linespacing=1.25, zorder=5)
    fig.savefig(OUT / "cover.png", dpi=300, facecolor=NAVY, bbox_inches=None)
    plt.close(fig)


# ---------- Figure 1: What GDP counts vs misses (concept diagram) ----------
def concept():
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.set_xlim(0, 100); ax.set_ylim(0, 60); ax.axis("off"); ax.grid(False)
    def box(x, y, w, h, fill, edge, title, items, tcolor):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.5",
                                    fc=fill, ec=edge, lw=1.3))
        ax.text(x + w / 2, y + h - 3.2, title, ha="center", va="top", fontsize=11.5, fontweight="bold", color=tcolor)
        for i, it in enumerate(items):
            ax.text(x + 3, y + h - 10.5 - i * 5.0, "■  " + it, va="top", fontsize=9.6, color="#262626")
    box(2, 4, 44, 52, PALE, NAVY, "Counted in GDP",
        ["Market goods and services", "Government services (at cost)", "Private investment",
         "Net exports", "Defensive spending (security, clean-up)",
         "Reconstruction after disasters", "Medical spending on pollution illness",
         "Resource extraction (as income)"], NAVY)
    box(54, 4, 44, 52, "white", GREY, "Missed or Mis-valued by GDP",
        ["Unpaid household and care work", "Volunteer work and leisure time",
         "Distribution of income and wealth", "Depletion of natural capital",
         "Pollution and climate damage", "Health, safety and life expectancy",
         "Informal and subsistence output", "Free digital goods, quality changes"], GREY)
    ax.annotate("", xy=(53, 30), xytext=(47, 30), arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.4))
    save(fig, "f01_concept")


# ---------- Figure 2: Bangladesh GDP growth ----------
def bd_growth():
    yrs = ["FY11", "FY12", "FY13", "FY14", "FY15", "FY16", "FY17", "FY18", "FY19", "FY20", "FY21", "FY22", "FY23", "FY24"]
    g = [6.46, 6.52, 6.01, 6.06, 6.55, 7.11, 7.28, 7.86, 7.88, 3.45, 6.94, 7.10, 5.78, 4.22]
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    cols = [LIGHT if v < 5 else NAVY for v in g]
    b = ax.bar(yrs, g, color=cols, width=0.62, edgecolor="white", linewidth=1.5)
    for rect, v in zip(b, g):
        ax.text(rect.get_x() + rect.get_width() / 2, v + 0.12, f"{v:.1f}", ha="center", fontsize=8.6, color="#262626")
    ax.axhline(np.mean(g), color=GREY, lw=1, ls="--")
    ax.text(13.45, np.mean(g) + 0.15, f"Average {np.mean(g):.1f}%", ha="right", fontsize=8.6, color=GREY)
    ax.set_ylabel("Real GDP growth (%)"); ax.set_ylim(0, 9.2)
    ax.grid(axis="x", visible=False); bar_ends(ax)
    ax.text(9, 1.2, "COVID-19", rotation=90, ha="center", color=NAVY, fontsize=8.5)
    save(fig, "f02_bd_growth")


# ---------- Figure 3: Preston curve ----------
COUNTRIES = {
    # name: (GDP per capita 2022 US$, life expectancy, HDI 2022, happiness WHR 2024 or None)
    "Norway": (108700, 83.1, 0.966, 7.30), "Switzerland": (92000, 83.5, 0.967, 7.06),
    "Qatar": (87700, 79.3, 0.875, None), "USA": (76300, 77.5, 0.927, 6.73),
    "Denmark": (67000, 81.4, 0.952, 7.58), "Finland": (50900, 81.2, 0.942, 7.74),
    "Germany": (48700, 80.7, 0.950, 6.72), "UK": (46100, 80.7, 0.940, 6.75),
    "Japan": (34000, 84.0, 0.920, 6.06), "Saudi Arabia": (30400, 77.0, 0.875, 6.59),
    "Russia": (15300, 72.0, 0.821, 5.79), "Costa Rica": (13200, 77.0, 0.806, 6.96),
    "China": (12700, 78.6, 0.788, 5.97), "Brazil": (8900, 73.4, 0.760, 6.27),
    "Eq. Guinea": (7500, 61.0, 0.650, None), "South Africa": (6700, 62.3, 0.717, 5.42),
    "Vietnam": (4200, 74.6, 0.726, 6.04), "Sri Lanka": (3350, 76.4, 0.780, 3.90),
    "Bangladesh": (2690, 73.4, 0.670, 3.89), "India": (2400, 67.7, 0.644, 4.05),
    "Nigeria": (2160, 53.6, 0.548, 4.88), "Pakistan": (1600, 66.4, 0.540, 4.66),
    "Ethiopia": (1030, 65.6, 0.492, None),
}
LABEL = {"Norway", "USA", "Japan", "Qatar", "Costa Rica", "China", "South Africa", "Eq. Guinea",
         "Sri Lanka", "Bangladesh", "India", "Nigeria", "Ethiopia", "Vietnam", "Finland", "Saudi Arabia", "Russia"}


OFFSETS = {(3, "Sri Lanka"): (6, -11), (3, "Bangladesh"): (-62, -3), (1, "Ethiopia"): (-4, 7),
           (1, "Bangladesh"): (-58, 6), (3, "India"): (-14, 7), (2, "Bangladesh"): (8, 3), (2, "India"): (-30, -4), (2, "Costa Rica"): (-60, -1), (2, "China"): (6, -9),
           (2, "Sri Lanka"): (-48, 4), (1, "Vietnam"): (5, -9)}


def scatter(name, idx, ylabel, fit=True, labels=LABEL, ylim=None):
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    pts = [(k, v[0], v[idx]) for k, v in COUNTRIES.items() if v[idx] is not None]
    x = np.array([p[1] for p in pts]); y = np.array([p[2] for p in pts])
    ax.scatter(x, y, s=46, color=NAVY, edgecolor="white", linewidth=1.2, zorder=3)
    hl = [p for p in pts if p[0] == "Bangladesh"]
    for k, xi, yi in hl:
        ax.scatter([xi], [yi], s=95, facecolor="none", edgecolor=NAVY, linewidth=1.4, zorder=4)
    if fit:
        c = np.polyfit(np.log(x), y, 1)
        xx = np.geomspace(x.min() * 0.9, x.max() * 1.1, 100)
        ax.plot(xx, c[0] * np.log(xx) + c[1], color=LIGHT, lw=2, zorder=2, label="Logarithmic trend")
        ax.legend(loc="lower right", fontsize=9)
    for k, xi, yi in pts:
        if k in labels:
            off = OFFSETS.get((idx, k), (5, 3))
            ax.annotate(k, (xi, yi), xytext=off, textcoords="offset points", fontsize=8.4, color="#262626",
                        fontweight="bold" if k == "Bangladesh" else "normal")
    ax.set_xscale("log")
    ax.set_xticks([1000, 2000, 5000, 10000, 20000, 50000, 100000])
    ax.set_xticklabels(["1k", "2k", "5k", "10k", "20k", "50k", "100k"])
    ax.set_xlabel("GDP per capita, 2022 (current US$, log scale)"); ax.set_ylabel(ylabel)
    if ylim: ax.set_ylim(*ylim)
    save(fig, name)


# ---------- Figure 4: Bangladesh poverty ----------
def bd_poverty():
    yrs = [2000, 2005, 2010, 2016, 2022]
    up = [48.9, 40.0, 31.5, 24.3, 18.7]
    lo = [34.3, 25.1, 17.6, 12.9, 5.6]
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(yrs, up, color=NAVY, lw=2.2, marker="o", ms=7, mec="white", mew=1.3, label="Upper poverty line")
    ax.plot(yrs, lo, color=MID, lw=2.2, ls="--", marker="s", ms=7, mec="white", mew=1.3, label="Lower (extreme) poverty line")
    for x, a, b in zip(yrs, up, lo):
        ax.text(x, a + 1.6, f"{a}%", ha="center", fontsize=8.6)
        ax.text(x, b - 3.6, f"{b}%", ha="center", fontsize=8.6, color=MID)
    ax.set_ylim(0, 55); ax.set_ylabel("Population below poverty line (%)")
    ax.set_xticks(yrs); ax.legend(loc="upper right")
    save(fig, "f04_bd_poverty")


# ---------- Figure 5: Gini ----------
def gini():
    d = [("South Africa", 63.0), ("Colombia", 54.8), ("Brazil", 52.0), ("USA", 41.3), ("China", 37.1),
         ("Bangladesh", 33.4), ("Japan", 32.9), ("India", 32.8), ("Germany", 31.7), ("Sweden", 29.8),
         ("Pakistan", 29.6), ("Norway", 27.7)]
    d = d[::-1]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    names = [a for a, _ in d]; vals = [b for _, b in d]
    cols = [NAVY if n == "Bangladesh" else MID if v >= 40 else LIGHT for n, v in d]
    ax.barh(names, vals, color=cols, height=0.62, edgecolor="white", linewidth=1.5)
    for i, v in enumerate(vals):
        ax.text(v + 0.8, i, f"{v:.1f}", va="center", fontsize=8.8)
    ax.set_xlabel("Gini index (0 = perfect equality, 100 = perfect inequality)")
    ax.set_xlim(0, 70); ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    save(fig, "f05_gini")


# ---------- Figure 6: global income vs wealth shares ----------
def wir():
    groups = ["Bottom 50%", "Middle 40%", "Top 10%"]
    pop = [50, 40, 10]; inc = [8.5, 39.5, 52.0]; wea = [2.0, 22.0, 76.0]
    x = np.arange(3); w = 0.26
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    sets = [(pop, PALE, "Share of population", None), (inc, LIGHT, "Share of income", None), (wea, NAVY, "Share of wealth", None)]
    for i, (v, c, lab, _) in enumerate(sets):
        bars = ax.bar(x + (i - 1) * w, v, w * 0.92, color=c, label=lab, edgecolor=NAVY if c == PALE else "white", linewidth=0.8)
        for r, val in zip(bars, v):
            ax.text(r.get_x() + r.get_width() / 2, val + 1.2, f"{val:g}%", ha="center", fontsize=8.6)
    ax.set_xticks(x); ax.set_xticklabels(groups); ax.set_ylim(0, 85); ax.set_ylabel("Per cent of global total")
    ax.legend(loc="upper left"); ax.grid(axis="x", visible=False); bar_ends(ax)
    save(fig, "f06_wir")


# ---------- Figure 7: demonstration, same GDP different distribution ----------
def demo_dist():
    q = ["Poorest 20%", "Second 20%", "Middle 20%", "Fourth 20%", "Richest 20%"]
    A = [6, 10, 15, 22, 47]; B = [9, 14, 18, 23, 36]
    mean = 5000
    a = [s / 100 * 5 * mean for s in A]; b = [s / 100 * 5 * mean for s in B]
    x = np.arange(5); w = 0.36
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    r1 = ax.bar(x - w / 2, a, w * 0.94, color=NAVY, label="Country A (unequal)", edgecolor="white")
    r2 = ax.bar(x + w / 2, b, w * 0.94, color="white", edgecolor=NAVY, hatch="////", linewidth=1.0, label="Country B (more equal)")
    for rs, vals in ((r1, a), (r2, b)):
        for r, v in zip(rs, vals):
            ax.text(r.get_x() + r.get_width() / 2, v + 180, f"${v:,.0f}", ha="center", fontsize=8.2)
    ax.axhline(mean, color=GREY, ls="--", lw=1)
    ax.text(-0.45, mean + 250, "Mean income in both countries = $5,000", fontsize=8.6, color=GREY)
    ax.set_xticks(x); ax.set_xticklabels(q); ax.set_ylabel("Average annual income (US$)")
    ax.set_ylim(0, 13500); ax.legend(loc="upper left", bbox_to_anchor=(0, 0.92)); ax.grid(axis="x", visible=False); bar_ends(ax)
    save(fig, "f07_demo_distribution")


# ---------- Figure 8: World GDP vs CO2 (indexed) ----------
def gdp_co2():
    yrs = [1990, 1995, 2000, 2005, 2010, 2015, 2019, 2020, 2022]
    gdp = [41.0, 45.5, 53.0, 61.0, 68.0, 77.0, 85.0, 82.0, 89.0]
    co2 = [22.7, 23.3, 25.5, 29.4, 33.4, 35.6, 37.0, 35.0, 37.2]
    gi = [v / gdp[0] * 100 for v in gdp]; ci = [v / co2[0] * 100 for v in co2]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.plot(yrs, gi, color=NAVY, lw=2.3, label="World real GDP")
    ax.plot(yrs, ci, color=MID, lw=2.3, ls="--", label="Global fossil CO₂ emissions")
    ax.fill_between(yrs, ci, 100, color=PALE, zorder=0)
    ax.text(2022.4, gi[-1], f"{gi[-1]:.0f}", va="center", fontsize=9, color=NAVY, fontweight="bold")
    ax.text(2022.4, ci[-1], f"{ci[-1]:.0f}", va="center", fontsize=9, color=MID, fontweight="bold")
    ax.set_ylabel("Index (1990 = 100)"); ax.set_xlim(1989, 2024.5); ax.legend(loc="upper left")
    save(fig, "f08_gdp_co2")


# ---------- Figure 9: Easterlin paradox (indexed, one axis) ----------
def easterlin():
    yrs = [1972, 1976, 1980, 1985, 1990, 1995, 2000, 2006, 2010, 2014, 2018]
    gdp = [100, 107, 117, 128, 143, 153, 177, 192, 188, 197, 211]
    happy = [30, 34, 34, 29, 33, 31, 32, 31, 29, 30, 31]
    hi = [h / happy[0] * 100 for h in happy]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.plot(yrs, gdp, color=NAVY, lw=2.3, marker="o", ms=5, mec="white", label="Real GDP per capita (index)")
    ax.plot(yrs, hi, color=MID, lw=2.3, ls="--", marker="s", ms=5, mec="white", label="Share 'very happy' (index)")
    ax.text(2018.6, gdp[-1], "211", va="center", fontsize=9, color=NAVY, fontweight="bold")
    ax.text(2018.6, hi[-1], "103", va="center", fontsize=9, color=MID, fontweight="bold")
    ax.set_ylabel("Index (1972 = 100)"); ax.set_ylim(60, 230); ax.set_xlim(1970, 2021.5)
    ax.legend(loc="upper left")
    save(fig, "f09_easterlin")


# ---------- Figure 11: health spending vs life expectancy ----------
def health():
    d = [("USA", 17.4, 76.4), ("Germany", 12.9, 80.9), ("France", 12.3, 82.3), ("UK", 12.4, 80.7),
         ("Canada", 12.3, 81.6), ("Japan", 10.8, 84.5), ("Costa Rica", 7.3, 77.0), ("Sri Lanka", 4.1, 76.4),
         ("Bangladesh", 2.4, 72.4)]
    fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.6), sharey=True)
    names = [a for a, _, _ in d][::-1]
    he = [b for _, b, _ in d][::-1]; le = [c for _, _, c in d][::-1]
    axs[0].barh(names, he, color=[NAVY if n == "USA" else LIGHT for n in names], height=0.6, edgecolor="white")
    for i, v in enumerate(he): axs[0].text(v + 0.3, i, f"{v}", va="center", fontsize=8.5)
    axs[0].set_title("Health spending (% of GDP)", fontsize=10.5); axs[0].set_xlim(0, 21)
    axs[1].barh(names, le, color=[NAVY if n == "USA" else LIGHT for n in names], height=0.6, edgecolor="white")
    for i, v in enumerate(le): axs[1].text(v + 0.3, i, f"{v}", va="center", fontsize=8.5)
    axs[1].set_title("Life expectancy (years)", fontsize=10.5); axs[1].set_xlim(60, 88)
    for a in axs:
        a.grid(axis="y", visible=False); a.spines["left"].set_visible(False); a.tick_params(axis="y", length=0)
    fig.tight_layout()
    save(fig, "f11_health")


# ---------- Figure 12: GDP vs GPI (stylised) ----------
def gpi():
    yrs = np.arange(1950, 2005)
    gdp = 100 * np.exp(0.0222 * (yrs - 1950))
    gpi = np.where(yrs <= 1978, 100 + 70 * (1 - np.exp(-(yrs - 1950) / 14)) / (1 - np.exp(-28 / 14)),
                   170 - 0.25 * (yrs - 1978))
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.plot(yrs, gdp, color=NAVY, lw=2.3, label="GDP per capita (index)")
    ax.plot(yrs, gpi, color=MID, lw=2.3, ls="--", label="Genuine Progress Indicator per capita (index)")
    ax.fill_between(yrs, gpi, gdp, where=yrs >= 1978, color=PALE, zorder=0)
    ax.axvline(1978, color=GREY, lw=0.9, ls=":")
    ax.text(1979, 112, "GPI peaks\n(c. 1978)", fontsize=8.8, color=GREY)
    ax.text(1990, 190, "Gap = uncounted\nsocial and\nenvironmental costs", fontsize=8.8, color=NAVY)
    ax.set_ylabel("Index (1950 = 100)"); ax.set_ylim(90, 345); ax.legend(loc="upper left")
    save(fig, "f12_gpi")


# ---------- Figure 14: Bangladesh HDI ----------
def bd_hdi():
    yrs = [1990, 1995, 2000, 2005, 2010, 2015, 2019, 2021, 2022]
    hdi = [0.394, 0.437, 0.485, 0.525, 0.557, 0.602, 0.662, 0.661, 0.670]
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(yrs, hdi, color=NAVY, lw=2.3, marker="o", ms=7, mec="white", mew=1.3)
    for x, v in zip(yrs, hdi):
        if x in (1990, 2000, 2010, 2015, 2022):
            ax.text(x, v + 0.012, f"{v:.3f}", ha="center", fontsize=8.6)
    ax.axhspan(0.55, 0.70, color=PALE, zorder=0)
    ax.text(1990.5, 0.69, "Medium human development band (0.550-0.699)", fontsize=8.6, color=NAVY, va="top")
    ax.set_ylim(0.35, 0.72); ax.set_ylabel("HDI value (0-1)")
    save(fig, "f14_bd_hdi")


# ---------- Figure 15: radar dashboard ----------
def radar():
    cats = ["GDP per\ncapita", "Income\nequality", "Health", "Education", "Environment", "Life\nsatisfaction", "Leisure &\nwork balance"]
    X = [80, 40, 60, 65, 35, 50, 45]; Y = [60, 75, 80, 75, 70, 72, 70]
    n = len(cats); ang = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist(); ang += ang[:1]
    fig = plt.figure(figsize=(6.0, 4.6)); ax = fig.add_subplot(111, polar=True)
    for vals, c, ls, lab, fill in ((X, NAVY, "-", "Country X (high GDP focus)", 0.22), (Y, MID, "--", "Country Y (balanced growth)", 0.0)):
        v = vals + vals[:1]
        ax.plot(ang, v, color=c, lw=2.2, ls=ls, label=lab)
        if fill: ax.fill(ang, v, color=c, alpha=fill)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(cats, fontsize=9)
    ax.set_yticks([20, 40, 60, 80, 100]); ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=7.5, color=GREY)
    ax.set_ylim(0, 100); ax.spines["polar"].set_color(GRID)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=2, fontsize=9)
    save(fig, "f15_radar")


# ---------- Figure 16: broken-window demonstration ----------
def broken_window():
    labels = ["GDP\n(flow)", "National wealth\n(stock)", "Household\nwell-being index"]
    base = [1000, 5000 / 5, 100 * 10]
    flood = [1050, 4700 / 5, 88 * 10]
    raw_b = ["$1,000 bn", "$5,000 bn", "100"]; raw_f = ["$1,050 bn", "$4,700 bn", "88"]
    x = np.arange(3); w = 0.34
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    r1 = ax.bar(x - w / 2, base, w * 0.94, color=LIGHT, label="Scenario 1: no flood", edgecolor="white")
    r2 = ax.bar(x + w / 2, flood, w * 0.94, color=NAVY, label="Scenario 2: flood + reconstruction", edgecolor="white")
    for rs, labs in ((r1, raw_b), (r2, raw_f)):
        for r, l in zip(rs, labs):
            ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 15, l, ha="center", fontsize=8.6)
    ax.text(0 + w / 2, 1150, "+5%", ha="center", fontsize=10, fontweight="bold", color=NAVY)
    ax.text(1 + w / 2, 1060, "-6%", ha="center", fontsize=10, fontweight="bold", color=NAVY)
    ax.text(2 + w / 2, 990, "-12%", ha="center", fontsize=10, fontweight="bold", color=NAVY)
    ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_yticks([]); ax.set_ylim(0, 1300)
    ax.spines["left"].set_visible(False); ax.grid(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=2, fontsize=9)
    ax.text(1, -260, "Bars are scaled within each measure for comparison; labels show actual values.", ha="center", fontsize=8.2, color=GREY, style="italic")
    save(fig, "f16_broken_window")


# ---------- Figure 17: framework of the study ----------
def framework():
    fig, ax = plt.subplots(figsize=(8.4, 2.4))
    ax.set_xlim(0, 100); ax.set_ylim(4, 26); ax.axis("off"); ax.grid(False)
    steps = ["Research\nquestion", "Literature &\ntheory review", "Secondary data\n(WB, UNDP, BBS)", "Comparative &\ncase analysis", "Findings &\nrecommendations"]
    for i, s in enumerate(steps):
        x = 1 + i * 20
        fc = NAVY if i in (0, 4) else PALE
        tc = "white" if i in (0, 4) else NAVY
        ax.add_patch(FancyBboxPatch((x, 8), 16, 14, boxstyle="round,pad=0.4,rounding_size=1.5", fc=fc, ec=NAVY, lw=1.2))
        ax.text(x + 8, 15, s, ha="center", va="center", fontsize=8.6, color=tc, fontweight="bold")
        if i < 4:
            ax.annotate("", xy=(x + 19.6, 15), xytext=(x + 16.6, 15), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.3))
    save(fig, "f00_framework")


if __name__ == "__main__":
    cover(); framework(); concept(); bd_growth()
    scatter("f03_preston", 1, "Life expectancy at birth (years)")
    bd_poverty(); gini(); wir(); demo_dist(); gdp_co2(); easterlin()
    scatter("f10_happiness", 3, "Life evaluation score (0-10), WHR 2024")
    health(); gpi()
    scatter("f13_hdi", 2, "Human Development Index (0-1), 2022")
    bd_hdi(); radar(); broken_window()
    print("figures written to", OUT)
