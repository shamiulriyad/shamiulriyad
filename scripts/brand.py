"""Generate the profile's visual assets (assets/*.svg).

    pip install fonttools
    python scripts/brand.py                                # hero without a photo
    python scripts/brand.py --photo assets/hero-photo.jpg  # hero with the photo embedded

The hero photo is embedded as a data URI because GitHub blocks external
images inside SVGs. The brand workflow does this whenever
assets/hero-photo.jpg (or .png) is added or changed.
"""

import argparse
import base64
import hashlib
import os
import re

from typeset import Doc, Font

ROOT = os.path.join(os.path.dirname(__file__), "..")

BG = "#0a0a0b"
LINE = "#232327"
OFF = "#f2efe8"
MUTED = "#a1a1a6"
DIM = "#6b6b70"
EMERALD = "#10b981"
EMERALD_SOFT = "#34d399"
GOLD = "#c8a96a"

DISPLAY = Font("InterDisplay-Light.otf", "dl")
DISPLAY_MED = Font("InterDisplay-Medium.otf", "dm")
SANS = Font("Inter-Regular.otf", "ir")
MONO = Font("IBMPlexMono-Regular.ttf", "pm")
SERIF = Font("InstrumentSerif-Regular.ttf", "sr")
SERIF_IT = Font("InstrumentSerif-Italic.ttf", "si")

W = 1200
PAD = 80


def panel(doc, h, rx=18):
    doc.add(f'<rect width="{doc.w}" height="{h}" rx="{rx}" fill="{BG}"/>')
    doc.add(f'<rect x="0.5" y="0.5" width="{doc.w - 1}" height="{h - 1}" rx="{rx}" fill="none" stroke="{LINE}"/>')


def hairline(doc, x1, y, x2, color=LINE, width=1):
    doc.add(f'<rect x="{x1}" y="{y}" width="{x2 - x1}" height="{width}" fill="{color}"/>')


def fit(font, s, size, max_width, tracking=0):
    while font.width(s, size, tracking) > max_width:
        size -= 0.5
    return size


def save(doc, name, out):
    with open(os.path.join(out, name), "w", encoding="utf-8") as f:
        f.write(doc.render())


# ─────────────────────────────── hero ───────────────────────────────

# Framing for the current hero photo (a square shot with a quote on its left):
# scale the photo up, anchor it top-right and fade further so the quote sinks
# into the black and the player fills the column.
PHOTO_ZOOM = 1.75
PHOTO_FADE = 0.5


def hero(out, photo):
    H = 660
    doc = Doc(W, H, "Md Shamiul Islam Riyad — AI/ML Engineer · Software Engineer · CSE Student. "
                    "Building intelligent systems. Solving real-world problems.")

    px = 620  # photo column starts here
    doc.define(f'<clipPath id="card"><rect width="{W}" height="{H}" rx="20"/></clipPath>')
    doc.define(f'<linearGradient id="fadeX" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
               f'<stop offset="{PHOTO_FADE if photo else 0.38}" stop-color="#fff" stop-opacity="1"/></linearGradient>')
    doc.define('<linearGradient id="fadeY" x1="0" y1="0" x2="0" y2="1"><stop offset="0.62" stop-color="#fff" stop-opacity="1"/>'
               '<stop offset="1" stop-color="#fff" stop-opacity="0.05"/></linearGradient>')
    doc.define(f'<mask id="mX"><rect x="{px}" width="{W - px}" height="{H}" fill="url(#fadeX)"/></mask>')
    doc.define(f'<mask id="mY"><rect x="{px}" width="{W - px}" height="{H}" fill="url(#fadeY)"/></mask>')
    doc.define(f'<radialGradient id="glow" cx="0.08" cy="1" r="0.75"><stop offset="0" stop-color="{EMERALD}" stop-opacity="0.13"/>'
               f'<stop offset="1" stop-color="{EMERALD}" stop-opacity="0"/></radialGradient>')
    doc.define('<linearGradient id="topshade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.55"/>'
               '<stop offset="0.22" stop-color="#000" stop-opacity="0"/></linearGradient>')
    doc.define(f'<linearGradient id="grade" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{EMERALD}" stop-opacity="0.16"/>'
               f'<stop offset="1" stop-color="#000" stop-opacity="0.35"/></linearGradient>')

    doc.add('<g clip-path="url(#card)">')
    doc.add(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    if photo:
        with open(photo, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        mime = "image/png" if photo.lower().endswith(".png") else "image/jpeg"
        doc.add(f'<g mask="url(#mY)"><g mask="url(#mX)">'
                f'<image x="{W - (W - px) * PHOTO_ZOOM:.0f}" y="0" width="{(W - px) * PHOTO_ZOOM:.0f}" '
                f'height="{H * PHOTO_ZOOM:.0f}" preserveAspectRatio="xMaxYMin slice" '
                f'xlink:href="data:{mime};base64,{data}"/>'
                f'<rect x="{px}" width="{W - px}" height="{H}" fill="url(#grade)"/></g></g>')
        # The photo has a quote printed on it; one closing mark survives the fade.
        doc.define(f'<radialGradient id="hush"><stop offset="0.35" stop-color="{BG}" stop-opacity="0.95"/>'
                   f'<stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>')
        doc.add('<ellipse cx="655" cy="548" rx="70" ry="55" fill="url(#hush)"/>')
    else:
        # No photo yet: an outlined numeral holds the right side of the frame.
        doc.add(f'<g mask="url(#mY)"><g mask="url(#mX)"><rect x="{px}" width="{W - px}" height="{H}" fill="url(#grade)"/></g></g>')
        doc.text(SERIF, "10", W - 40, H - 70, 560, "none", anchor="end", stroke=EMERALD, stroke_width=1.2, opacity=0.55)
    doc.add(f'<rect width="{W}" height="{H}" fill="url(#topshade)"/>')
    doc.add(f'<rect width="{W}" height="{H}" fill="url(#glow)"/>')
    doc.add("</g>")
    doc.add(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="20" fill="none" stroke="{LINE}"/>')

    # top bar
    doc.text(SERIF, "MSIR", PAD, 64, 22, OFF, tracking=2)
    doc.text(MONO, "GITHUB.COM/SHAMIULRIYAD", W - PAD + 20, 62, 11, OFF, anchor="end", tracking=2.4, opacity=0.75)

    # eyebrow
    doc.add(f'<circle cx="{PAD + 4}" cy="146" r="3.5" fill="{EMERALD}"/>')
    doc.text(MONO, "PROFILE  ·  Nº 10  ·  2026", PAD + 18, 150, 12, MUTED, tracking=3)

    # name
    max_w = px - PAD - 40
    size = fit(DISPLAY, "MD SHAMIUL", 80, max_w, 1)
    line2_islam = DISPLAY.width("ISLAM ", size, 1)
    while line2_islam + DISPLAY_MED.width("RIYAD", size, 1) > max_w:
        size -= 0.5
        line2_islam = DISPLAY.width("ISLAM ", size, 1)
    doc.text(DISPLAY, "MD SHAMIUL", PAD - 4, 246, size, OFF, tracking=1)
    doc.text(DISPLAY, "ISLAM", PAD - 4, 246 + size * 1.04, size, OFF, tracking=1)
    doc.text(DISPLAY_MED, "RIYAD", PAD - 4 + line2_islam, 246 + size * 1.04, size, EMERALD_SOFT, tracking=1)

    y = 246 + size * 1.04 + 48
    hairline(doc, PAD, y, PAD + 56, EMERALD, 1.5)
    doc.add(f'<circle cx="{PAD + 66}" cy="{y + 0.75}" r="2" fill="{GOLD}"/>')

    roles = "AI/ML ENGINEER  ·  SOFTWARE ENGINEER  ·  CSE STUDENT"
    doc.text(MONO, roles, PAD, y + 40, fit(MONO, roles, 13.5, max_w, 2.2), MUTED, tracking=2.2)

    doc.text(SERIF, "Building intelligent systems.", PAD, y + 104, 34, OFF)
    doc.text(SERIF_IT, "Solving real-world problems.", PAD, y + 144, 34, MUTED)

    # spec strip
    sy = H - 112
    hairline(doc, PAD, sy, px - 20)
    specs = [("POSITION", "AI/ML Engineer"), ("CLUB", "UIU · CSE"), ("BASE", "Bangladesh"), ("FOCUS", "NLP · RAG")]
    colw = (px - 20 - PAD) / len(specs)
    for i, (k, v) in enumerate(specs):
        x = PAD + i * colw
        doc.text(MONO, k, x, sy + 34, 10, DIM, tracking=2.4)
        doc.text(SANS, v, x, sy + 62, 15.5, OFF)

    # photo caption
    if photo:
        doc.text(SERIF_IT, "“1% chance, 99% faith.”", W - PAD + 20, H - 74, 26, GOLD, anchor="end")
        doc.text(MONO, "—  NEYMAR JR", W - PAD + 20, H - 48, 9.5, OFF, anchor="end", tracking=2.4, opacity=0.7)
    else:
        doc.text(MONO, "FLAIR IN THE IDEA · DISCIPLINE IN THE BUILD", W - PAD + 20, H - 48, 9.5, OFF,
                 anchor="end", tracking=2, opacity=0.7)
    save(doc, "hero.svg", out)


# ─────────────────────────────── section band ───────────────────────────────

def band(out, slug, num, title, note):
    H = 108
    doc = Doc(W, H, f"{num} — {title}")
    panel(doc, H, 16)
    doc.text(SERIF, num, PAD - 6, 72, 52, EMERALD_SOFT)
    nx = PAD - 6 + SERIF.width(num, 52) + 22
    hairline(doc, nx, 55, nx + 28, DIM)
    doc.text(DISPLAY, title, nx + 50, 66, 25, OFF, tracking=8)
    doc.text(MONO, note, W - PAD, 64, 11, DIM, anchor="end", tracking=2.4)
    save(doc, f"s-{slug}.svg", out)


def subband(out, slug, label, note):
    H = 76
    doc = Doc(W, H, f"{label.title()} — {note.lower()}")
    panel(doc, H, 14)
    doc.add(f'<circle cx="{PAD + 4}" cy="38" r="3.5" fill="{GOLD}"/>')
    doc.text(MONO, label, PAD + 20, 43, 13, OFF, tracking=4)
    doc.text(MONO, note, W - PAD, 43, 10.5, DIM, anchor="end", tracking=2.4)
    save(doc, f"sub-{slug}.svg", out)


# ─────────────────────────────── 01 identity ───────────────────────────────

def identity(out):
    H = 420
    doc = Doc(W, H, "Identity: AI/ML and software engineer building AI systems end to end.")
    panel(doc, H)
    doc.text(MONO, "STATEMENT", PAD, 92, 10.5, DIM, tracking=2.4)
    statement = ("I build AI systems end to end — retrieval pipelines, agents and vision models, "
                 "shipped as products people actually use.")
    last = doc.paragraph(SERIF, statement, PAD, 148, 36, OFF, 560, leading=1.22)
    doc.text(SANS, "Python handles the intelligence; ASP.NET Core and React carry it to users.",
             PAD, last + 62, 15, MUTED)

    fx, fw = 720, W - PAD
    facts = [
        ("DISCIPLINE", "AI/ML · Software Engineering"),
        ("STUDY", "BSc CSE · United International University"),
        ("BASE", "Bangladesh"),
        ("NOW", "Multi-tenant RAG and LLM agents"),
        ("TRAINING", "Daily DSA · Codeforces · LeetCode"),
    ]
    for i, (k, v) in enumerate(facts):
        y = 92 + i * 58
        doc.text(MONO, k, fx, y, 10.5, DIM, tracking=2.4)
        doc.text(SANS, v, fx, y + 26, 16, OFF)
        hairline(doc, fx, y + 42, fw)
    save(doc, "identity.svg", out)


# ─────────────────────────────── 02 current form ───────────────────────────────

FORM = [
    ("AI/ML", "Models that see, classify and decide under real constraints.", "Mango Fraud · Smart Shelf"),
    ("NLP", "Bangla-first generation with voice in and voice out.", "Chokh · Study Assistant"),
    ("RAG", "Chunking, embeddings, vector search and cited answers.", "rag-kit · rag-learning"),
    ("Full-Stack", "React and Next.js over ASP.NET Core or Node, Python for the ML.", "TakaRunway · ShilpoHubBD"),
    ("Research", "Agents that reason over conflicting real-world signals.", "NogorSathi AI"),
]


def form(out):
    H = 330
    doc = Doc(W, H, "Current form: " + ", ".join(f[0] for f in FORM))
    panel(doc, H)
    gap = 28
    colw = (W - 2 * PAD - gap * (len(FORM) - 1)) / len(FORM)
    for i, (title, desc, proof) in enumerate(FORM):
        x = PAD + i * (colw + gap)
        hairline(doc, x, 72, x + colw, EMERALD if i == 0 else LINE, 1.5 if i == 0 else 1)
        doc.text(MONO, f"0{i + 1}", x, 106, 11, EMERALD_SOFT, tracking=2)
        doc.text(DISPLAY, title, x, 146, fit(DISPLAY, title, 27, colw), OFF)
        doc.paragraph(SANS, desc, x, 184, 14, MUTED, colw, leading=1.55)
        doc.text(MONO, "IN PLAY", x, 268, 9.5, DIM, tracking=2.4)
        doc.text(SANS, proof, x, 290, fit(SANS, proof, 13, colw), EMERALD_SOFT)
    save(doc, "form.svg", out)


# ─────────────────────────────── 03 selected work ───────────────────────────────

PROJECTS = [
    ("rag-kit", "rag-kit", "RAG PLATFORM",
     "Multi-tenant RAG SaaS with knowledge bases, PDF ingestion, cited chat, teams, usage limits and an operator admin panel.",
     "React · TypeScript · ASP.NET Core · FastAPI · Qdrant · Gemini · Postgres", False),
    ("nogorsathi", "NogorSathi AI", "AUTONOMOUS AGENT",
     "A Gemma 4 function-calling agent that weighs traffic, waterlogging, night safety and fare to pick the right Dhaka commute.",
     "Gemma 4 · Function Calling · Gemini API · Python", False),
    ("chokh", "Chokh", "VISION · ACCESSIBILITY",
     "AI eyes for the visually impaired. It narrates surroundings and reads printed text aloud in Bengali, hazards first.",
     "React · ASP.NET Core · Gemini Vision · Web Speech API", True),
    ("takarunway", "TakaRunway", "FINTECH · FULL-STACK",
     "Personal ledger and cashflow-runway manager for salaried professionals in Dhaka: burn rate, surplus and goals, live.",
     "Next.js 15 · React 19 · TypeScript · Supabase · Tailwind CSS", True),
    ("mango", "Mango Fraud Detection", "COMPUTER VISION",
     "Identifies a mango's true variety from a photo and scores fraud against the seller's claimed variety and price.",
     "PyTorch · FastAPI · ASP.NET Core 8 · React · PostgreSQL", False),
    ("queuestorm", "QueueStorm Investigator", "AI SUPPORT COPILOT",
     "Checks each support complaint against the customer's transactions, routes it and drafts a safety-checked reply.",
     "ASP.NET Core 8 · Minimal API · Claude API · Docker", False),
    ("english-rag", "English Learning RAG", "RAG · NLP",
     "Ask a grammar book anything and get grounded answers with page-level citations, from PDF pipeline to chat UI.",
     "FastAPI · Qdrant · Gemini · ASP.NET Core · React · Supabase", False),
    ("shilpohub", "ShilpoHubBD", "FULL-STACK PLATFORM",
     "A heritage marketplace connecting Bangladeshi artisans with buyers: commerce, live auctions, realtime chat, traceability.",
     "React 19 · ASP.NET Core 8 · SignalR · PostgreSQL · Supabase", False),
]


def project_card(out, idx, slug, name, kind, desc, tech, live):
    CW, CH = 580, 344
    doc = Doc(CW, CH, f"{name} — {kind.lower()}. {desc}")
    panel(doc, CH, 16)
    x = 44
    doc.text(SERIF, f"{idx:02d}", x - 2, 76, 44, OFF, opacity=0.9)
    doc.text(MONO, kind, CW - x, 64, 10.5, EMERALD_SOFT, anchor="end", tracking=2.2)
    if live:
        lw = MONO.width("LIVE", 9.5, 2.2) + 26
        lx = CW - x - lw
        doc.add(f'<rect x="{lx}" y="78" width="{lw}" height="22" rx="11" fill="none" stroke="{EMERALD}" stroke-opacity="0.7"/>')
        doc.add(f'<circle cx="{lx + 11}" cy="89" r="2.5" fill="{EMERALD}"/>')
        doc.text(MONO, "LIVE", lx + 19, 92.5, 9.5, OFF, tracking=2.2)
    doc.text(DISPLAY, name, x, 150, fit(DISPLAY, name, 38, CW - 2 * x), OFF)
    doc.paragraph(SANS, desc, x, 192, 17, MUTED, CW - 2 * x, leading=1.5)
    hairline(doc, x, 278, CW - x)
    doc.text(MONO, tech, x, 310, fit(MONO, tech, 12.5, CW - 2 * x - 30, 0.4), DIM, tracking=0.4)
    doc.text(SANS, "↗", CW - x, 312, 19, EMERALD_SOFT, anchor="end")
    save(doc, f"work-{slug}.svg", out)


# ─────────────────────────────── 04 toolkit ───────────────────────────────

TOOLKIT = [
    ("INTELLIGENCE", ["Python", "PyTorch", "OpenCV", "Gemini · Gemma", "Qdrant", "FastAPI"]),
    ("SYSTEMS", ["C# · ASP.NET Core", "Node.js · Express", "Spring Boot", "PostgreSQL · MySQL", "Supabase", "Docker"]),
    ("INTERFACE", ["React", "Next.js", "TypeScript", "JavaScript", "Tailwind CSS", "Vite"]),
    ("FOUNDATIONS", ["C++", "C", "Java", "Algorithms & DS", "Git"]),
]


def toolkit(out):
    H = 400
    doc = Doc(W, H, "Toolkit: " + "; ".join(f"{k}: {', '.join(v)}" for k, v in TOOLKIT))
    panel(doc, H)
    gap = 40
    colw = (W - 2 * PAD - gap * 3) / 4
    for i, (cat, items) in enumerate(TOOLKIT):
        x = PAD + i * (colw + gap)
        doc.text(MONO, cat, x, 90, 10.5, EMERALD_SOFT, tracking=2.6)
        hairline(doc, x, 108, x + colw)
        for j, item in enumerate(items):
            y = 152 + j * 38
            doc.text(MONO, f"{j + 1:02d}", x, y - 1, 9.5, DIM, tracking=1)
            doc.text(SANS, item, x + 34, y, 17, OFF)
    save(doc, "toolkit.svg", out)


# ─────────────────────────────── 05 achievements ───────────────────────────────

TROPHIES = [
    ("gemma", "2026", "Gemma Hackathon", "United International University", "Autonomous Agent Track", "NOGORSATHI AI"),
    ("ictfest", "2026", "IUT 12th ICT Fest", "Bdapps Agentic AI Hackathon", "Preliminary round entry", "COWORK BOOKING API"),
    ("techathon", "2026", "IUT Techathon", "Nationals & Rover Summit", "Team build · IoT + Discord", "SMART OFFICE MONITOR"),
    ("mlbd", "2026", "ML Bangladesh Hackathon", "Accessibility · Computer vision", "Deployed live", "CHOKH"),
    ("sust", "2026", "bKash SUST CSE Carnival", "Codex Community Hackathon", "Online preliminary", "QUEUESTORM INVESTIGATOR"),
    ("lsh26", "2026", "LSH26 Build Event", "Team T035 · two problem tracks", "Problems P01 + P12", "TAKARUNWAY · LOADSHED"),
]


def trophy_icon(doc, cx, cy):
    s = f'fill="none" stroke="{GOLD}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"'
    doc.add(f'<g transform="translate({cx} {cy})" {s}>'
            '<path d="M-17 -26H17V-8C17 3 9 11 0 11C-9 11 -17 3 -17 -8Z"/>'
            '<path d="M-17 -20H-25C-25 -10 -21 -5 -15 -4"/><path d="M17 -20H25C25 -10 21 -5 15 -4"/>'
            '<path d="M0 11V21"/><path d="M-11 27H11"/><path d="M-7 21H7V27H-7Z"/></g>')


def plaque(out, slug, year, event, sub, detail, project):
    PW, PH = 580, 210
    doc = Doc(PW, PH, f"{year} — {event}, {sub}. {detail}. Project: {project.title()}")
    panel(doc, PH, 16)
    doc.add(f'<circle cx="92" cy="105" r="46" fill="none" stroke="{GOLD}" stroke-opacity="0.25"/>')
    trophy_icon(doc, 92, 104)
    x = 176
    doc.text(MONO, year, x, 62, 10.5, GOLD, tracking=2.6)
    doc.text(DISPLAY, event, x, 100, fit(DISPLAY, event, 27, PW - x - 40), OFF)
    doc.text(SANS, sub, x, 128, 14.5, MUTED)
    hairline(doc, x, 148, PW - 40)
    doc.text(MONO, project, x, 176, 10.5, EMERALD_SOFT, tracking=2.2)
    doc.text(SANS, detail, PW - 40, 176, 12.5, DIM, anchor="end")
    save(doc, f"trophy-{slug}.svg", out)


# ─────────────────────────────── 07 connect ───────────────────────────────

CONTACTS = [
    ("github", "GITHUB", "shamiulriyad"),
    ("linkedin", "LINKEDIN", "Md Shamiul Islam Riyad"),
    ("codeforces", "CODEFORCES", "Riyad_shamiul"),
    ("leetcode", "LEETCODE", "shamiulislamriyad"),
    ("youtube", "YOUTUBE", "@ZeroTo420perfect"),
]


def contact(out, slug, label, handle):
    CW, CH = 300, 170
    doc = Doc(CW, CH, f"{label.title()}: {handle}")
    panel(doc, CH, 16)
    doc.text(MONO, label, 28, 52, 15, EMERALD_SOFT, tracking=2.4)
    doc.text(SANS, "↗", CW - 28, 56, 26, OFF, anchor="end")
    doc.text(DISPLAY, handle, 28, 130, fit(DISPLAY, handle, 30, CW - 56), OFF)
    save(doc, f"connect-{slug}.svg", out)


def footer(out):
    H = 120
    doc = Doc(W, H, "Md Shamiul Islam Riyad — AI/ML and Software Engineering")
    hairline(doc, PAD, 30, W - PAD, LINE)
    doc.text(SERIF, "MSIR", PAD, 82, 26, OFF)
    doc.text(MONO, "AI/ML  ·  SOFTWARE ENGINEERING  ·  BANGLADESH", W - PAD, 78, 10.5, DIM, anchor="end", tracking=2.6)
    save(doc, "footer.svg", out)


def publish_versioned(name):
    """Rename assets/<stem>.svg to <stem>-<content hash>.svg and point the README at it.

    GitHub redirects README images to raw.githubusercontent.com and drops any
    query string, so browsers kept showing a cached old hero. A new file name
    per version is the only reliable cache buster.
    """
    stem = name[:-len(".svg")]
    assets = os.path.join(ROOT, "assets")
    src = os.path.join(assets, name)
    with open(src, "rb") as f:
        version = hashlib.sha256(f.read()).hexdigest()[:10]
    versioned = f"{stem}-{version}.svg"
    for old in os.listdir(assets):
        if re.fullmatch(rf"{re.escape(stem)}-[0-9a-f]{{10}}\.svg", old) and old != versioned:
            os.remove(os.path.join(assets, old))
    os.replace(src, os.path.join(assets, versioned))

    path = os.path.join(ROOT, "README.md")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = re.sub(rf"\./assets/{re.escape(stem)}(-[0-9a-f]{{10}})?\.svg(\?v=[0-9a-f]+)?\"", f'./assets/{versioned}"', text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo", help="hero photo to embed (JPEG or PNG)")
    ap.add_argument("--out", default=os.path.join(ROOT, "assets"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    hero(args.out, args.photo)
    if os.path.abspath(args.out) == os.path.abspath(os.path.join(ROOT, "assets")):
        publish_versioned("hero.svg")
    for slug, num, title, note in [
        ("identity", "01", "IDENTITY", "WHO · WHAT · HOW"),
        ("form", "02", "CURRENT FORM", "WHERE THE WORK IS"),
        ("work", "03", "SELECTED WORK", "REAL REPOSITORIES"),
        ("toolkit", "04", "TOOLKIT", "INSTRUMENTS OF CHOICE"),
        ("achievements", "05", "ACHIEVEMENTS", "THE CABINET"),
        ("performance", "06", "PERFORMANCE", "LIVE · REFRESHED EVERY 6H"),
        ("connect", "07", "CONNECT", "OPEN CHANNEL"),
    ]:
        band(args.out, slug, num, title, note)
    subband(args.out, "squad", "THE FULL SQUAD", "EVERY OTHER PROJECT")
    subband(args.out, "practice", "TRAINING GROUND", "PROBLEM-SOLVING ARCHIVES")
    identity(args.out)
    form(args.out)
    for i, p in enumerate(PROJECTS, 1):
        project_card(args.out, i, *p)
    toolkit(args.out)
    for t in TROPHIES:
        plaque(args.out, *t)
    for c in CONTACTS:
        contact(args.out, *c)
    footer(args.out)


if __name__ == "__main__":
    main()
