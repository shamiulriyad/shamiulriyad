"""Render assets/telemetry.svg from GitHub's API and public contribution calendar.

Runs in GitHub Actions (see .github/workflows/telemetry.yml) so the profile
does not depend on rate-limited public stats services.
"""

import datetime as dt
import html
import json
import os
import re
import sys
import urllib.request

USER = os.environ.get("GH_USER", "shamiulriyad")
OUT = os.environ.get("OUT", os.path.join(os.path.dirname(__file__), "..", "assets", "telemetry.svg"))

EMERALD = "#10b981"
EMERALD_SOFT = "#6ee7b7"
GOLD = "#d4af37"
TEXT = "#e6edf3"
MUTED = "#8b949e"
BG = "#050807"
HEAT = ["#0f1714", "#064e3b", "#047857", "#10b981", "#d4af37"]
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "Segoe UI,Helvetica Neue,Helvetica,Arial,sans-serif"


def request(url, token=True, data=None, accept="application/vnd.github+json"):
    headers = {"Accept": accept, "User-Agent": f"{USER}-profile-telemetry"}
    if token:
        headers["Authorization"] = f"bearer {os.environ['GITHUB_TOKEN']}"
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers), timeout=60) as resp:
        return resp.read().decode()


def rest(path):
    return json.loads(request(f"https://api.github.com/{path}"))


def gql(query, variables=None):
    body = json.loads(request("https://api.github.com/graphql", data={"query": query, "variables": variables or {}}))
    if body.get("errors"):
        raise RuntimeError(body["errors"])
    return body["data"]


def calendar_year(year):
    """Daily counts from the public contributions page.

    The Actions token cannot read contributionsCollection for a user (it
    returns zeros), but the public calendar is available without auth.
    """
    page = request(
        f"https://github.com/users/{USER}/contributions?from={year}-01-01&to={year}-12-31",
        token=False, accept="text/html",
    )
    tips = {}
    for tip_for, body in re.findall(r'<tool-tip[^>]*\bfor="([^"]+)"[^>]*>(.*?)</tool-tip>', page, re.S):
        m = re.match(r"\s*([\d,]+|No) contributions?", body)
        if m:
            tips[tip_for] = 0 if m.group(1) == "No" else int(m.group(1).replace(",", ""))
    days = {}
    for cell in re.findall(r"<td\b[^>]*\bdata-date=[^>]*>", page):
        date = re.search(r'data-date="([^"]+)"', cell).group(1)
        cid = re.search(r'\bid="([^"]+)"', cell)
        if cid and cid.group(1) in tips:
            days[date] = tips[cid.group(1)]
    return days


def fetch():
    now = dt.datetime.now(dt.timezone.utc)
    profile = rest(f"users/{USER}")
    repos = gql(
        """query($login: String!) {
          user(login: $login) {
            repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
              totalCount
              nodes {
                stargazerCount
                languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                  edges { size node { name color } }
                }
              }
            }
          }
        }""",
        {"login": USER},
    )["user"]["repositories"]

    days = {}
    for year in range(int(profile["created_at"][:4]), now.year + 1):
        days.update(calendar_year(year))
    if not days:
        raise RuntimeError("could not parse the contribution calendar; refusing to render zeros")

    langs = {}
    for repo in repos["nodes"]:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            size, _ = langs.get(name, (0, None))
            langs[name] = (size + e["size"], e["node"]["color"] or MUTED)

    year = [n for d, n in days.items() if d.startswith(str(now.year))]
    return {
        "today": now.date(),
        "days": days,
        "langs": langs,
        "year_total": sum(year),
        "active_days": sum(1 for n in year if n),
        "best_day": max(year, default=0),
        "repos": repos["totalCount"],
        "stars": sum(r["stargazerCount"] for r in repos["nodes"]),
        "followers": profile["followers"],
    }


def streaks(days, today):
    dates = sorted(dt.date.fromisoformat(d) for d in days if dt.date.fromisoformat(d) <= today)
    longest, longest_range, run, run_start = 0, None, 0, None
    for d in dates:
        if days[d.isoformat()] > 0:
            run_start = d if run == 0 else run_start
            run += 1
            if run > longest:
                longest, longest_range = run, (run_start, d)
        else:
            run = 0

    # Today without contributions yet does not break the current streak.
    cursor = today if days.get(today.isoformat(), 0) > 0 else today - dt.timedelta(days=1)
    current, current_start = 0, None
    while days.get(cursor.isoformat(), 0) > 0:
        current, current_start = current + 1, cursor
        cursor -= dt.timedelta(days=1)
    return current, current_start, longest, longest_range


def fmt_date(d):
    return d.strftime("%b %-d, %Y") if d else "—"


def render(data):
    today = data["today"]
    days = data["days"]
    total = sum(days.values())
    first = min(days) if days else today.isoformat()
    current, current_start, longest, longest_range = streaks(days, today)

    W, H = 900, 600
    s = []
    a = s.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
      f'aria-label="GitHub telemetry for {USER}: {total} contributions, current streak {current} days, longest streak {longest} days">')
    a(f"""<defs>
  <radialGradient id="glow" cx="0.5" cy="0" r="0.8"><stop offset="0" stop-color="{EMERALD}" stop-opacity="0.18"/><stop offset="1" stop-color="{EMERALD}" stop-opacity="0"/></radialGradient>
  <linearGradient id="rule" x1="0" x2="1"><stop offset="0" stop-color="{EMERALD}" stop-opacity="0"/><stop offset="0.5" stop-color="{EMERALD}" stop-opacity="0.5"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>
  <style>.p{{animation:p 2.4s ease-in-out infinite}}@keyframes p{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}</style>
</defs>""")
    a(f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/><rect width="{W}" height="{H}" rx="14" fill="url(#glow)"/>')
    a(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{EMERALD}" stroke-opacity="0.25"/>')
    a(f'<g stroke="{GOLD}" stroke-width="2" fill="none" stroke-linecap="round"><path d="M18 40V18H40"/><path d="M{W-40} 18H{W-18}V40"/>'
      f'<path d="M18 {H-40}V{H-18}H40"/><path d="M{W-40} {H-18}H{W-18}V{H-40}"/></g>')

    def text(x, y, body, size, fill, family=SANS, weight=400, anchor="start", extra=""):
        a(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
          f'text-anchor="{anchor}" {extra}>{html.escape(str(body))}</text>')

    # Streak trio
    cols = [150, 450, 750]
    text(cols[0], 98, f"{total:,}", 38, TEXT, weight=700, anchor="middle")
    text(cols[0], 128, "TOTAL CONTRIBUTIONS", 11.5, GOLD, MONO, anchor="middle", extra='letter-spacing="1.5"')
    text(cols[0], 150, f"{fmt_date(dt.date.fromisoformat(first))} – Present", 12, MUTED, anchor="middle")

    a(f'<circle cx="{cols[1]}" cy="86" r="44" fill="none" stroke="#1f2a24" stroke-width="5"/>')
    a(f'<circle cx="{cols[1]}" cy="86" r="44" fill="none" stroke="{EMERALD}" stroke-width="5"/>')
    a(f'<circle cx="{cols[1]}" cy="42" r="5" fill="{GOLD}" class="p"/>')
    text(cols[1], 99, current, 36, TEXT, weight=700, anchor="middle")
    text(cols[1], 154, "CURRENT STREAK", 11.5, EMERALD, MONO, weight=700, anchor="middle", extra='letter-spacing="1.5"')
    cur_label = f"{fmt_date(current_start)} – {fmt_date(today)}" if current else "start one today"
    text(cols[1], 174, cur_label, 12, MUTED, anchor="middle")

    text(cols[2], 98, longest, 38, TEXT, weight=700, anchor="middle")
    text(cols[2], 128, "LONGEST STREAK", 11.5, GOLD, MONO, anchor="middle", extra='letter-spacing="1.5"')
    lr = f"{fmt_date(longest_range[0])} – {fmt_date(longest_range[1])}" if longest_range else "—"
    text(cols[2], 150, lr, 12, MUTED, anchor="middle")
    for x in (300, 600):
        a(f'<rect x="{x}" y="50" width="1" height="120" fill="#1f2a24"/>')

    a(f'<rect x="40" y="200" width="{W-80}" height="1" fill="url(#rule)"/>')

    # Counters
    text(40, 236, f"// {today.year}", 12, MUTED, MONO)
    rows = [("Contributions", data["year_total"]), ("Active days", data["active_days"]), ("Best day", data["best_day"]),
            ("Public repos", data["repos"]), ("Stars earned", data["stars"]), ("Followers", data["followers"])]
    for i, (label, value) in enumerate(rows):
        y = 266 + i * 24
        a(f'<circle cx="46" cy="{y-4}" r="3" fill="{EMERALD if i < 3 else GOLD}"/>')
        text(60, y, label, 13.5, "#c9d1d9")
        text(330, y, f"{value:,}", 13.5, TEXT, MONO, weight=700, anchor="end")

    # Languages
    lx, lw = 400, 460
    text(lx, 236, "// languages · public repos", 12, MUTED, MONO)
    ranked = sorted(data["langs"].items(), key=lambda kv: -kv[1][0])
    lang_total = sum(v[0] for _, v in ranked) or 1
    top = ranked[:8]
    a(f'<clipPath id="bar"><rect x="{lx}" y="252" width="{lw}" height="8" rx="4"/></clipPath><g clip-path="url(#bar)">')
    a(f'<rect x="{lx}" y="252" width="{lw}" height="8" fill="#1f2a24"/>')
    x = lx
    for name, (size, color) in top:
        w = lw * size / lang_total
        a(f'<rect x="{x:.2f}" y="252" width="{w:.2f}" height="8" fill="{color}"/>')
        x += w
    a("</g>")
    for i, (name, (size, color)) in enumerate(top):
        cx = lx + (i % 2) * 235
        cy = 286 + (i // 2) * 24
        a(f'<circle cx="{cx+5}" cy="{cy-4}" r="4.5" fill="{color}"/>')
        text(cx + 16, cy, name, 13, "#c9d1d9")
        text(cx + 215, cy, f"{100 * size / lang_total:.1f}%", 12, MUTED, MONO, anchor="end")

    a(f'<rect x="40" y="420" width="{W-80}" height="1" fill="url(#rule)"/>')

    # Last 53 weeks heatmap, columns are weeks starting on Sunday
    start = today - dt.timedelta(days=(today.weekday() + 1) % 7 + 52 * 7)
    cell, gap = 11, 3
    gx = (W - 53 * (cell + gap) + gap) / 2
    peak = max([days.get((start + dt.timedelta(i)).isoformat(), 0) for i in range(53 * 7)] + [1])
    for i in range((today - start).days + 1):
        d = start + dt.timedelta(i)
        n = days.get(d.isoformat(), 0)
        level = 0 if n == 0 else 1 + min(3, int(4 * n / (peak + 1)))
        a(f'<rect x="{gx + (i // 7) * (cell + gap):.1f}" y="{436 + (i % 7) * (cell + gap)}" width="{cell}" height="{cell}" rx="2.5" fill="{HEAT[level]}"/>')

    text(W - 60, H - 30, f"synced {today.isoformat()}", 10.5, "#4b5563", MONO, anchor="end")
    a("</svg>")
    return "\n".join(s) + "\n"


def main():
    svg = render(fetch())
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
