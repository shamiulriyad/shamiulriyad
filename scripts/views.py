"""Render assets/views-<hash>.svg from the komarev.com profile views counter.

komarev.com still counts the views: the README loads its badge as a hidden 1px
image. But it is sometimes too slow for GitHub's image proxy, which then shows
a broken image. So the visible badge is this file, served from the repo, and
it always loads. Runs in GitHub Actions (see .github/workflows/telemetry.yml).

Every fetch here is itself counted as a view, so assets/views.json keeps how
many times this script has hit the counter and subtracts that.
"""

import json
import os
import re
import sys
import time
import urllib.request

from brand import EMERALD, SANS, publish_versioned
from typeset import Doc

USER = os.environ.get("GH_USER", "shamiulriyad")
ROOT = os.path.join(os.path.dirname(__file__), "..")
STATE = os.path.join(ROOT, "assets", "views.json")
OUT = os.path.join(ROOT, "assets", "views.svg")  # published as views-<hash>.svg
URL = f"https://komarev.com/ghpvc/?username={USER}&label=PROFILE%20VIEWS&color=10b981&style=flat-square"

LABEL = "PROFILE VIEWS"
LABEL_BG = "#555555"
SIZE, H, PAD = 11, 20, 6


def fetch_count():
    """The counter's current total, or None if komarev.com did not answer."""
    req = urllib.request.Request(URL, headers={"User-Agent": f"{USER}-profile-views", "Cache-Control": "no-cache"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                svg = resp.read().decode()
            numbers = [t for t in re.findall(r"<text[^>]*>([^<]*)</text>", svg) if re.fullmatch(r"[\d,.\s]+", t.strip())]
            if numbers:
                return int(re.sub(r"\D", "", numbers[-1]))
            print(f"no count in komarev response: {svg[:200]!r}", file=sys.stderr)
            return None
        except Exception as e:  # noqa: BLE001 - any failure just keeps the last badge
            print(f"komarev fetch {attempt + 1} failed: {e}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    return None


def render(count):
    value = "—" if count is None else f"{count:,}"
    lw = SANS.width(LABEL, SIZE, 0.6) + 2 * PAD
    vw = SANS.width(value, SIZE) + 2 * PAD
    doc = Doc(round(lw + vw), H, f"Profile views: {value}")
    doc.add(f'<rect width="{lw:.2f}" height="{H}" fill="{LABEL_BG}"/>')
    doc.add(f'<rect x="{lw:.2f}" width="{vw:.2f}" height="{H}" fill="{EMERALD}"/>')
    doc.text(SANS, LABEL, PAD, 14, SIZE, "#ffffff", tracking=0.6)
    doc.text(SANS, value, lw + PAD, 14, SIZE, "#ffffff")
    return doc.render()


def main():
    try:
        with open(STATE, encoding="utf-8") as f:
            state = json.load(f)
    except FileNotFoundError:
        state = {"views": None, "own_hits": 0}

    total = fetch_count()
    if total is not None:
        state["own_hits"] += 1  # the fetch above was counted too
        views = total - state["own_hits"]
        # never go backwards on a bad read
        state["views"] = views if state["views"] is None else max(views, state["views"])
        with open(STATE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
            f.write("\n")
    else:
        print("komarev.com unreachable; keeping the last count", file=sys.stderr)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(render(state["views"]))
    # a new name per count, or GitHub and browsers keep showing a cached badge
    publish_versioned("views.svg")
    print(f"views badge: {state['views']} views", file=sys.stderr)


if __name__ == "__main__":
    main()
