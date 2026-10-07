"""Render assets/telemetry.svg from GitHub's API and public contribution calendar.

Runs in GitHub Actions (see .github/workflows/telemetry.yml) so the profile
does not depend on rate-limited public stats services.
"""

import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request

USER = os.environ.get("GH_USER", "shamiulriyad")
TZ = dt.timezone(dt.timedelta(hours=float(os.environ.get("TZ_OFFSET_HOURS", "0"))))
OUT = os.environ.get("OUT", os.path.join(os.path.dirname(__file__), "..", "assets", "telemetry.svg"))

from brand import BG, DIM, DISPLAY, EMERALD, EMERALD_SOFT, GOLD, LINE, MONO, MUTED, OFF, SANS, SERIF_IT, fit, hairline, panel
from typeset import Doc

HEAT = ["#151517", "#0b3d2e", "#0f6b4c", "#10b981", GOLD]


def request(url, token=True, data=None, accept="application/vnd.github+json"):
    headers = {"Accept": accept, "User-Agent": f"{USER}-profile-telemetry"}
    if token:
        headers["Authorization"] = f"bearer {os.environ['GITHUB_TOKEN'] if token is True else token}"
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers), timeout=60) as resp:
        return resp.read().decode()


def rest(path):
    return json.loads(request(f"https://api.github.com/{path}"))


def gql(query, variables=None, token=True):
    body = json.loads(request("https://api.github.com/graphql", token=token, data={"query": query, "variables": variables or {}}))
    if body.get("errors"):
        raise RuntimeError(body["errors"])
    return body["data"]


def calendar_year_token(year, token):
    """Daily counts via GraphQL using the owner's own token.

    Needed when the profile is private: only the owner can see the calendar.
    """
    now = dt.datetime.now(dt.timezone.utc)
    end = min(dt.datetime(year, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc), now)
    cal = gql(
        """query($login: String!, $from: DateTime!, $to: DateTime!) {
          user(login: $login) {
            contributionsCollection(from: $from, to: $to) {
              contributionCalendar { weeks { contributionDays { date contributionCount } } }
            }
          }
        }""",
        {"login": USER, "from": f"{year}-01-01T00:00:00Z", "to": end.isoformat()},
        token=token,
    )["user"]["contributionsCollection"]["contributionCalendar"]
    return {d["date"]: d["contributionCount"] for w in cal["weeks"] for d in w["contributionDays"]}


def calendar_year(year):
    """Daily counts from the public contributions page.

    The Actions token cannot read contributionsCollection for a user (it
    returns zeros), but the public calendar is available without auth. A
    private profile shows an empty calendar here; set TELEMETRY_TOKEN then.
    """
    if os.environ.get("TELEMETRY_TOKEN"):
        return calendar_year_token(year, os.environ["TELEMETRY_TOKEN"])
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
    print(f"{year}: {len(days)} days, {sum(days.values())} contributions", file=sys.stderr)
    return days


def commit_days(repo_names):
    """Commits authored by USER per local day across public repos (default branches)."""
    days = {}
    for name in repo_names:
        page = 1
        while True:
            try:
                commits = rest(f"repos/{USER}/{name}/commits?author={USER}&per_page=100&page={page}")
            except urllib.error.HTTPError as e:
                if e.code == 409:  # empty repository
                    break
                raise
            for c in commits:
                when = dt.datetime.fromisoformat(c["commit"]["author"]["date"].replace("Z", "+00:00"))
                key = when.astimezone(TZ).date().isoformat()
                days[key] = days.get(key, 0) + 1
            if len(commits) < 100:
                break
            page += 1
    print(f"commit fallback: {sum(days.values())} commits on {len(days)} days", file=sys.stderr)
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
                name
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
    source = "contributions"
    if not any(days.values()):
        # Private profile: the calendar is hidden, so count commits in public repos instead.
        days, source = commit_days([r["name"] for r in repos["nodes"]]), "commits"

    langs = {}
    for repo in repos["nodes"]:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            size, _ = langs.get(name, (0, None))
            langs[name] = (size + e["size"], e["node"]["color"] or MUTED)

    today = now.astimezone(TZ).date()
    year = [n for d, n in days.items() if d.startswith(str(today.year))]
    return {
        "today": today,
        "source": source,
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
    dates = sorted(dt.date.fromisoformat(d) for d, n in days.items() if n > 0 and dt.date.fromisoformat(d) <= today)
    longest, longest_range, run, run_start, prev = 0, None, 0, None, None
    for d in dates:
        if prev is not None and d - prev == dt.timedelta(days=1):
            run += 1
        else:
            run, run_start = 1, d
        prev = d
        if run > longest:
            longest, longest_range = run, (run_start, d)

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
    unit = data.get("source", "contributions")
    total = sum(days.values())
    first = min(days) if days else today.isoformat()
    current, current_start, longest, longest_range = streaks(days, today)

    # A hidden calendar (or no activity) yields all zeros; show only repository data then.
    active = total > 0
    W, X = 1200, 80
    H = 820 if active else 340
    label = (f"{total} {unit}, current streak {current} days, longest streak {longest} days" if active
             else f"{data['repos']} public repositories, {data['stars']} stars")
    doc = Doc(W, H, f"GitHub performance for {USER}: {label}")
    panel(doc, H)

    top = 0
    if active:
        stats = [
            (f"TOTAL {unit.upper()}", f"{total:,}", f"{fmt_date(dt.date.fromisoformat(first))} — present"),
            ("CURRENT STREAK", str(current),
             f"{fmt_date(current_start)} — {fmt_date(today)}" if current else "Next commit starts it"),
            ("LONGEST STREAK", str(longest),
             f"{fmt_date(longest_range[0])} — {fmt_date(longest_range[1])}" if longest_range else "—"),
        ]
        colw = (W - 2 * X) / 3
        for i, (k, v, sub) in enumerate(stats):
            x = X + i * colw + (36 if i else 0)
            if i:
                doc.add(f'<rect x="{X + i * colw:.0f}" y="64" width="1" height="150" fill="{LINE}"/>')
            if i == 1:
                doc.add(f'<circle cx="{x + 4}" cy="86" r="3.5" fill="{EMERALD}"/>')
            doc.text(MONO, k, x + (16 if i == 1 else 0), 90, 10.5, EMERALD_SOFT if i == 1 else DIM, tracking=2.4)
            w = doc.text(DISPLAY, v, x - 3, 168, 76, OFF)
            if i:
                doc.text(SERIF_IT, "days", x + w + 8, 168, 26, MUTED)
            doc.text(SANS, sub, x, 204, 14, MUTED)
        hairline(doc, X, 252, W - X)
        top = 252

    # season counters
    y0 = top + 70
    doc.text(MONO, f"SEASON {today.year}" if active else "PUBLIC REPOSITORIES", X, y0, 10.5, DIM, tracking=2.4)
    rows = [(unit.capitalize(), data["year_total"]), ("Active days", data["active_days"]),
            ("Best day", data["best_day"])] if active else []
    rows += [("Public repos", data["repos"]), ("Stars earned", data["stars"])]
    if data["followers"]:
        rows.append(("Followers", data["followers"]))
    if not active:
        rows.append(("Languages", len(data["langs"])))
    rows = rows[:5]
    for i, (k, v) in enumerate(rows):
        y = y0 + 44 + i * 40
        doc.text(SANS, k, X, y, 15, MUTED)
        doc.text(DISPLAY, f"{v:,}", 520, y + 1, 19, OFF, anchor="end")
        hairline(doc, X, y + 15, 520)

    # languages
    lx, lw = 620, W - X - 620
    doc.text(MONO, "LANGUAGES  ·  PUBLIC REPOS", lx, y0, 10.5, DIM, tracking=2.4)
    ranked = sorted(data["langs"].items(), key=lambda kv: -kv[1][0])
    lang_total = sum(v[0] for _, v in ranked) or 1
    shown = ranked[:8]
    doc.define(f'<clipPath id="bar"><rect x="{lx}" y="{y0 + 24}" width="{lw}" height="6" rx="3"/></clipPath>')
    doc.add(f'<g clip-path="url(#bar)"><rect x="{lx}" y="{y0 + 24}" width="{lw}" height="6" fill="#1a1a1d"/>')
    x = lx
    for name, (size, color) in shown:
        w = lw * size / lang_total
        doc.add(f'<rect x="{x:.2f}" y="{y0 + 24}" width="{w:.2f}" height="6" fill="{color}"/>')
        x += w
    doc.add("</g>")
    half = lw / 2
    for i, (name, (size, color)) in enumerate(shown):
        cx = lx + (i % 2) * (half + 20)
        cy = y0 + 72 + (i // 2) * 40
        doc.add(f'<circle cx="{cx + 4}" cy="{cy - 5}" r="4" fill="{color}"/>')
        doc.text(SANS, name, cx + 18, cy, 15, OFF)
        doc.text(MONO, f"{100 * size / lang_total:.1f}%", cx + half - 20, cy, 12, DIM, anchor="end")

    if active:
        hy = top + 330
        hairline(doc, X, hy, W - X)
        doc.text(MONO, "LAST 53 WEEKS", X, hy + 44, 10.5, DIM, tracking=2.4)
        # columns are weeks starting on Sunday
        start = today - dt.timedelta(days=(today.weekday() + 1) % 7 + 52 * 7)
        cell, gap = 13, 4
        gx = W - X - 53 * (cell + gap) + gap
        # shade by quartile of active days so one huge day doesn't wash out the rest
        window = [days.get((start + dt.timedelta(i)).isoformat(), 0) for i in range(53 * 7)]
        active_counts = sorted(n for n in window if n)
        cuts = [active_counts[len(active_counts) * q // 4] for q in (1, 2, 3)] if active_counts else [1, 1, 1]
        for i in range((today - start).days + 1):
            n = days.get((start + dt.timedelta(i)).isoformat(), 0)
            level = 0 if n == 0 else 1 + sum(n >= c for c in cuts)
            doc.add(f'<rect x="{gx + (i // 7) * (cell + gap):.1f}" y="{hy + 70 + (i % 7) * (cell + gap)}" '
                    f'width="{cell}" height="{cell}" rx="3" fill="{HEAT[level]}"/>')
        for i, c in enumerate(HEAT):
            doc.add(f'<rect x="{X + i * 16}" y="{hy + 70 + 6 * (cell + gap)}" width="11" height="11" rx="2.5" fill="{c}"/>')
        doc.text(MONO, "LESS → MORE", X, hy + 70 + 5 * (cell + gap), 9, DIM, tracking=1.6)

    doc.text(MONO, f"SYNCED {today.isoformat()}", W - X, H - 34, 9.5, DIM, anchor="end", tracking=2)
    return doc.render()


def main():
    svg = render(fetch())
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
