"""Build the research dossier: figures -> HTML -> PDF (A4) + spreadsheets/CSV artifacts.

    python3 build.py            # full build
    python3 build.py --no-figs  # reuse existing figures

Requirements: Python 3 with numpy, scipy, matplotlib, openpyxl, pypdf;
Node with the `playwright` package and its Chromium.
"""
import csv
import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
BUILD = os.path.join(ROOT, "build")
ART = os.path.join(ROOT, "artifacts")
sys.path.insert(0, SRC)

from refs import REFS  # noqa: E402
from papers import PAPERS, SHORT  # noqa: E402
from tables import DATASETS, NOVELTY, RQS, RISKS, ROADMAP, GLOSSARY, CLOSEST  # noqa: E402

PDF_NAME = "Sample_Guided_Die_Inspection_Research_Dossier.pdf"
RUNNING_TITLE = "Sample-Guided Semiconductor Wafer Die Inspection · Research Dossier"
PAPER_BY_ID = {p["id"]: p for p in PAPERS}


def esc(s):
    return html.escape(s, quote=False)


# ---------------------------------------------------------------------------
# Generated HTML blocks
# ---------------------------------------------------------------------------
def rq_table():
    rows = "".join(
        f"<tr><td><b>{r['id']}</b></td><td>{r['q']}</td><td>{r['h']}</td><td>{r['m']}</td><td>{r['exp']}</td></tr>"
        for r in RQS)
    return ("<table class='small'><caption>Research questions, hypotheses, measurements and experiments (Artifact 12).</caption>"
            "<thead><tr><th style='width:7%'>ID</th><th style='width:27%'>Research question</th><th style='width:38%'>Hypothesis (falsifiable)</th>"
            "<th>Measured by</th><th style='width:6%'>Exp.</th></tr></thead><tbody>" + rows + "</tbody></table>")


def vcell(v):
    return f"<td class='v {v.replace(' ', '')}'>{v}</td>"


def paper_matrix():
    rows = []
    for p in PAPERS:
        rows.append(
            f"<tr><td>{esc(p['short'])} [[{p['id']}]]</td><td>{p['year']}</td><td>{esc(SHORT[p['id']][0])}</td><td>{esc(SHORT[p['id']][1])}</td>"
            + vcell(p["fewshot"]) + vcell(p["rotation"]) + vcell(p["localization"]) + vcell(p["unknown"]) + vcell(p["feedback"])
            + f"<td>{esc(p['limit_short'])}</td></tr>")
    return ("<table class='small matrix'><caption>Paper comparison matrix (34 papers). Values: Yes / Partial / No / Not evaluated / Unclear.</caption>"
            "<thead><tr><th style='width:14%'>Paper</th><th style='width:5%'>Year</th><th style='width:12%'>Dataset</th><th style='width:17%'>Method</th>"
            "<th style='width:7%'>Few-shot</th><th style='width:7%'>Rotation</th><th style='width:7%'>Localisation</th><th style='width:7%'>Unknown defects</th><th style='width:7%'>Feedback learning</th><th>Limitation</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table>")


def paper_cards():
    out, group = [], None
    for k, p in enumerate(PAPERS, 1):
        if p["group"] != group:
            group = p["group"]
            out.append(f"<h2>{esc(group)}</h2>")
        stars = "★" * p["closeness"] + "☆" * (5 - p["closeness"])
        url = REFS[p["id"]][1]
        rows = [("1. Title", f"{esc(p['title'])}"), ("2. Authors", esc(p["authors"])), ("3. Year", str(p["year"])),
                ("4. Venue", esc(p["venue"])), ("5. DOI / URL", f"<a href='{url}'>{esc(url)}</a>"),
                ("6. Research problem", esc(p["problem"])), ("7. Dataset", esc(p["dataset"])), ("8. Input modality", esc(p["modality"])),
                ("9. Proposed method", esc(p["method"])), ("10. Architecture", esc(p["architecture"])),
                ("11. What it achieved", esc(p["achieved"])), ("12. Limitations", esc(p["limitations"])),
                ("13. What to learn", esc(p["learn"])), ("14. Relation to this research", esc(p["relation"])),
                ("15. Unexplored", esc(p["unexplored"]))]
        tr1 = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows[:6])
        tr2 = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows[6:])
        out.append(
            f"<div class='paper' id='paper-{p['id']}'><div class='phead'><div class='ph'><div class='pt'>P{k}. {esc(p['short'])} [[{p['id']}]]</div>"
            f"<div class='pm'>{esc(p['authors'])} · {esc(p['venue'])} · closeness <span class='stars'>{stars}</span></div></div>"
            f"<div class='simple'><b>In simple words.</b> {esc(p['simple'])}</div>"
            f"<table><tbody>{tr1}</tbody></table></div><table><tbody>{tr2}</tbody></table>"
            f"<div class='flags'>Matrix: few-shot {p['fewshot']} · rotation {p['rotation']} · localisation {p['localization']} · unknown {p['unknown']} · feedback {p['feedback']}</div></div>")
    return "\n".join(out)


def closest():
    out = []
    for c in CLOSEST:
        out.append(
            f"<h3>{esc(c['name'])} [[{c['id']}]]</h3><table class='kv'><tbody>"
            f"<tr><td>Overlap</td><td>{esc(c['overlap'])}</td></tr><tr><td>Difference</td><td>{esc(c['difference'])}</td></tr>"
            f"<tr><td>Already accomplished</td><td>{esc(c['done'])}</td></tr><tr><td>Remaining gap</td><td>{esc(c['gap'])}</td></tr>"
            f"<tr><td>How this work extends it</td><td>{esc(c['extend'])}</td></tr></tbody></table>")
    return "\n".join(out)


def novelty():
    def bar(n):
        return "<span class='stars'>" + "■" * n + "□" * (5 - n) + "</span>"
    rows = "".join(
        f"<tr><td><b>{n['c']}</b></td><td><b>{n['name']}</b></td><td>{n['prior']}</td><td>{n['covered']}</td><td>{n['open']}</td>"
        f"<td>{n['kind']}</td><td>{n['status']}<br>{bar(n['strength'])}</td></tr>" for n in NOVELTY)
    return ("<table class='small'><caption>Novelty matrix: proposed contributions vs closest existing research. The bar shows how strong and testable the remaining gap is (■ = 1 point of 5), as judged from the reviewed literature.</caption>"
            "<thead><tr><th>ID</th><th style='width:12%'>Contribution</th><th style='width:19%'>Closest prior work</th><th style='width:19%'>Already covered</th>"
            "<th style='width:21%'>Still open</th><th style='width:11%'>Type of claim</th><th style='width:12%'>Status / gap</th></tr></thead><tbody>" + rows + "</tbody></table>")


def datasets():
    rows = "".join(
        f"<tr><td><b>{d['name']}</b> [[{d['ref']}]]</td><td>{d['modality']}</td><td>{d['samples']}</td><td>{d['labels']}</td><td>{d['masks']}</td>"
        f"<td><a href='{d['link']}'>{esc(d['link'].replace('https://', ''))}</a></td><td>{d['use']}</td><td>{d['limits']}</td></tr>" for d in DATASETS)
    return ("<table class='small'><caption>Dataset comparison (Artifact 4). Figures as stated in official records; unverified items are marked.</caption>"
            "<thead><tr><th style='width:9%'>Dataset</th><th style='width:13%'>Modality</th><th style='width:9%'>Samples</th><th style='width:12%'>Labels</th>"
            "<th style='width:9%'>Segmentation masks</th><th style='width:11%'>Official link</th><th style='width:15%'>Intended use here</th><th>Limitations</th></tr></thead><tbody>"
            + rows + "</tbody></table>")


def roadmap():
    rows = "".join(
        f"<tr><td><b>{r['n']}</b></td><td><b>{r['phase']}</b><br><span class='small-note'>{'core' if r['core'] else 'core-if-time'} · weeks {r['weeks']} · depends on {r['dep']}</span></td>"
        f"<td>{r['tasks']}</td><td>{r['out']}</td><td>{r['challenge']}</td><td>{r['done']}</td></tr>" for r in ROADMAP)
    return ("<table class='small'><caption>Research execution roadmap: tasks, outputs, challenges and completion criteria per phase (Artifact 9).</caption>"
            "<thead><tr><th>#</th><th style='width:17%'>Phase</th><th style='width:26%'>Main tasks</th><th style='width:17%'>Expected output</th><th style='width:15%'>Technical challenges</th><th>Completion criteria</th></tr></thead><tbody>"
            + rows + "</tbody></table>")


def risks():
    rows = "".join(f"<tr><td>{k}</td><td><b>{r[0]}</b></td><td>{r[1]}</td><td class='v {r[2]}'>{r[2]}</td><td class='v {r[3]}'>{r[3]}</td><td>{r[4]}</td></tr>"
                   for k, r in enumerate(RISKS, 1))
    rows = rows.replace("class='v High'", "class='v No'").replace("class='v Medium'", "class='v Partial'").replace("class='v Low'", "class='v Yes'")
    return ("<table class='small matrix'><caption>Risk register (Artifact 8). Probability and impact: High / Medium / Low.</caption>"
            "<thead><tr><th>#</th><th style='width:20%'>Risk</th><th style='width:22%'>Why it matters</th><th>Probability</th><th>Impact</th><th>Mitigation</th></tr></thead><tbody>"
            + rows + "</tbody></table>")


def glossary():
    return "<dl class='gloss'>" + "".join(f"<div><dt>{esc(t)}</dt><dd>{esc(d)}</dd></div>" for t, d in GLOSSARY) + "</dl>"


# ---------------------------------------------------------------------------
# Markup transforms
# ---------------------------------------------------------------------------
def concepts(s):
    def rep(m):
        n, title, body = m.group(1), m.group(2), m.group(3)
        parts = {k: re.search(fr"<{k}>(.*?)</{k}>", body, re.S).group(1).strip() for k in "setw"}
        return (f"<div class='concept'><h4><span class='n'>Concept {n}</span>{title}</h4>"
                f"<div class='row'><div class='k'>Simple</div><div class='v'>{parts['s']}</div></div>"
                f"<div class='row ex'><div class='k'>Example</div><div class='v'>{parts['e']}</div></div>"
                f"<div class='row tech'><div class='k'>Technical</div><div class='v'>{parts['t']}</div></div>"
                f"<div class='row why'><div class='k'>Why it matters</div><div class='v'>{parts['w']}</div></div></div>")
    return re.sub(r'<concept n="(\d+)" title="([^"]+)">(.*?)</concept>', rep, s, flags=re.S)


def figures(s):
    figs = {}

    def rep(m):
        fid, src, w, cap = m.group(1), m.group(2), m.group(3), m.group(4)
        n = len(figs) + 1
        figs[fid] = n
        return (f"<figure id='fig-{fid}' class='{w}'><img src='../figures/{src}' alt='Figure {n}'>"
                f"<figcaption><span class='fn'>Figure {n}.</span> {cap.strip()}</figcaption></figure>")
    s = re.sub(r'<fig id="([^"]+)" src="([^"]+)" w="([^"]+)">(.*?)</fig>', rep, s, flags=re.S)
    s = re.sub(r"\{\{fig:([^}]+)\}\}", lambda m: f"<a href='#fig-{m.group(1)}'>{figs[m.group(1)]}</a>", s)
    return s


def tables(s):
    n = [0]

    def rep(m):
        n[0] += 1
        return f"{m.group(1)}<span class='tn'>Table {n[0]}.</span> "
    return re.sub(r"(<caption>)", rep, s)


def citations(s):
    order = []

    def num(key):
        if key not in REFS:
            raise KeyError(f"unknown reference key: {key}")
        if key not in order:
            order.append(key)
        return order.index(key) + 1

    def rep(m):
        keys = [k.strip() for k in m.group(1).split(",")]
        nums = [num(k) for k in keys]
        return "[" + ", ".join(f"<a href='#ref-{n}'>{n}</a>" for n in nums) + "]"
    s = re.sub(r"\[\[([a-z0-9_,\s]+)\]\]", rep, s)
    reflist = "".join(f"<p id='ref-{i}'>[{i}] {REFS[k][0]} <a href='{REFS[k][1]}'>{esc(REFS[k][1])}</a> <span class='vf'>[{REFS[k][2]}]</span></p>"
                      for i, k in enumerate(order, 1))
    unused = [k for k in REFS if k not in order]
    if unused:
        print("note: references never cited:", unused)
    return s.replace("<!--REFERENCES-->", reflist), order


def toc(s, pages=None):
    items = []
    for m in re.finditer(r"<h([12]) id=['\"]([^'\"]+)['\"]>(.*?)</h\1>", s):
        lvl, hid, text = m.group(1), m.group(2), re.sub(r"<[^>]+>", " ", m.group(3))
        text = re.sub(r"\s+", " ", text).strip()
        if hid == "contents":
            continue
        pg = pages.get(hid, "") if pages else ""
        items.append(f"<li class='l{lvl}'><span class='t'><a href='#{hid}'>{esc(text)}</a></span><span class='pg'>{pg}</span></li>")
    return s.replace("<!--TOC-->", "<ol>" + "".join(items) + "</ol>")


def add_h2_ids(s):
    k = [0]

    def rep(m):
        k[0] += 1
        return f"<h2 id='h2-{k[0]}'>{m.group(1)}</h2>"
    return re.sub(r"<h2>(.*?)</h2>", rep, s)


def assemble():
    parts = []
    for f in sorted(os.listdir(os.path.join(SRC, "sections"))):
        if f.endswith(".html"):
            parts.append(open(os.path.join(SRC, "sections", f), encoding="utf-8").read())
    body = "\n".join(parts)
    for key, fn in [("RQ_TABLE", rq_table), ("PAPER_MATRIX", paper_matrix), ("PAPER_CARDS", paper_cards), ("CLOSEST", closest),
                    ("NOVELTY", novelty), ("DATASETS", datasets), ("ROADMAP", roadmap), ("RISKS", risks), ("GLOSSARY", glossary)]:
        assert f"<!--{key}-->" in body, key
        body = body.replace(f"<!--{key}-->", fn())
    body = concepts(body)
    body = figures(body)
    body = tables(body)
    body = add_h2_ids(body)
    body, order = citations(body)
    return body, order


def page_html(body):
    css = open(os.path.join(SRC, "style.css"), encoding="utf-8").read()
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Sample-Guided Die Inspection — Research Dossier</title>"
            f"<style>{css}</style></head><body>{body}</body></html>")


# ---------------------------------------------------------------------------
# PDF rendering
# ---------------------------------------------------------------------------
NODE = r"""
const { chromium } = require('playwright');
(async () => {
  const [inp, out, mode] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + inp, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const opts = { path: out, format: 'A4', printBackground: true, preferCSSPageSize: true };
  if (mode === 'doc') { opts.outline = true; opts.tagged = true; }
  await p.pdf(opts);
  await b.close();
})();
"""


def render(html_path, pdf_path, mode="doc"):
    js = os.path.join(BUILD, "render.cjs")
    open(js, "w").write(NODE)
    subprocess.run(["node", js, html_path, pdf_path, mode], check=True)


def heading_pages(pdf_path, body):
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())  # noqa: E731
    texts = [norm(pg.extract_text() or "") for pg in reader.pages]
    pages, start = {}, 2
    for m in re.finditer(r"<h([12]) id=['\"]([^'\"]+)['\"]>(.*?)</h\1>", body):
        hid = m.group(2)
        if hid == "contents":
            continue
        key = norm(html.unescape(re.sub(r"<[^>]+>", "", m.group(3))))[:40]
        for i in range(start, len(texts)):
            if key and key in texts[i]:
                pages[hid] = i + 1
                start = i
                break
    return pages, len(reader.pages)


def stamp_page_numbers(pdf_path, n_pages):
    """Overlay running header + page numbers on every page except the cover."""
    from pypdf import PdfReader, PdfWriter
    pages = "".join(
        "<div class='pg'>" + ("" if i == 1 else
                              f"<div class='hd'>{esc(RUNNING_TITLE)}</div><div class='ft'>{i} / {n_pages}</div>") + "</div>"
        for i in range(1, n_pages + 1))
    h = ("<!doctype html><html><head><meta charset='utf-8'><style>@page{size:A4;margin:0}body{margin:0}"
         ".pg{width:210mm;height:297mm;position:relative;break-after:page}"
         ".hd{position:absolute;top:8mm;left:16mm;right:16mm;font:7.5pt 'Liberation Sans',Arial;color:#5B6573;border-bottom:0.5pt solid #C9D1DB;padding-bottom:1mm}"
         ".ft{position:absolute;bottom:8mm;right:16mm;font:8pt 'Liberation Sans',Arial;color:#1F3A5F}"
         f"</style></head><body>{pages}</body></html>")
    hp = os.path.join(BUILD, "overlay.html")
    op = os.path.join(BUILD, "overlay.pdf")
    open(hp, "w", encoding="utf-8").write(h)
    render(hp, op, mode="overlay")
    overlay = PdfReader(op)
    writer = PdfWriter(clone_from=pdf_path)
    for i, page in enumerate(writer.pages):
        if i > 0:
            page.merge_page(overlay.pages[i])
    for page in writer.pages:
        page.compress_content_streams(level=9)
    writer.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
    writer.add_metadata({"/Title": "Sample-Guided Semiconductor Wafer Die Inspection — Research Dossier",
                         "/Author": "Md Shamiul Islam Riyad", "/Subject": "Exploratory research proposal and technical explanation"})
    writer.write(pdf_path)


# ---------------------------------------------------------------------------
# Artifacts (spreadsheets, CSV, markdown)
# ---------------------------------------------------------------------------
def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def artifacts(order):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    os.makedirs(ART, exist_ok=True)
    num = {k: i for i, k in enumerate(order, 1)}

    lit_header = ["Ref no.", "Paper", "Title", "Authors", "Year", "Venue", "DOI / URL", "Group", "Plain-language summary", "Research problem",
                  "Dataset", "Input modality", "Method", "Architecture", "What it achieved", "Limitations", "What to learn",
                  "Relation to this research", "Unexplored", "Few-shot", "Rotation", "Localisation", "Unknown defects", "Feedback learning",
                  "Closeness (1-5)", "Verification"]
    lit_rows = [[num[p["id"]], p["short"], p["title"], p["authors"], p["year"], p["venue"], REFS[p["id"]][1], p["group"], p["simple"],
                 p["problem"], p["dataset"], p["modality"], p["method"], p["architecture"], p["achieved"], p["limitations"], p["learn"],
                 p["relation"], p["unexplored"], p["fewshot"], p["rotation"], p["localization"], p["unknown"], p["feedback"],
                 p["closeness"], REFS[p["id"]][2]] for p in PAPERS]
    ds_header = ["Dataset", "Modality", "Samples", "Labels", "Segmentation masks", "Official link", "Intended use", "Limitations", "Verification"]
    ds_rows = [[d["name"], strip(d["modality"]), d["samples"], d["labels"], d["masks"], d["link"], strip(d["use"]), strip(d["limits"]), d["verified"]] for d in DATASETS]
    nov_header = ["ID", "Contribution", "Closest prior work", "Already covered", "Still open", "Type of claim", "Status", "Gap strength (1-5)"]
    nov_rows = [[n["c"], n["name"], strip(n["prior"]), strip(n["covered"]), strip(n["open"]), n["kind"], n["status"], n["strength"]] for n in NOVELTY]
    risk_header = ["#", "Risk", "Why it matters", "Probability", "Impact", "Mitigation"]
    risk_rows = [[k] + list(r) for k, r in enumerate(RISKS, 1)]
    rm_header = ["Phase", "Name", "Weeks", "Core", "Main tasks", "Expected output", "Technical challenges", "Completion criteria", "Depends on"]
    rm_rows = [[r["n"], r["phase"], r["weeks"], "core" if r["core"] else "core-if-time", r["tasks"], r["out"], r["challenge"], r["done"], r["dep"]] for r in ROADMAP]
    rq_header = ["ID", "Research question", "Hypothesis", "Measured by", "Experiment"]
    rq_rows = [[r["id"], r["q"], r["h"], r["m"], r["exp"]] for r in RQS]
    ref_header = ["No.", "Key", "Citation", "URL", "Verification"]
    ref_rows = [[i, k, strip(REFS[k][0]), REFS[k][1], REFS[k][2]] for i, k in enumerate(order, 1)]

    write_csv(os.path.join(ART, "03_literature_review.csv"), lit_header, lit_rows)
    write_csv(os.path.join(ART, "04_dataset_inventory.csv"), ds_header, ds_rows)
    write_csv(os.path.join(ART, "02_novelty_matrix.csv"), nov_header, nov_rows)
    write_csv(os.path.join(ART, "08_risk_register.csv"), risk_header, risk_rows)
    write_csv(os.path.join(ART, "09_roadmap.csv"), rm_header, rm_rows)

    wb = Workbook()
    sheets = [("Literature review", lit_header, lit_rows), ("Comparison matrix", ["Paper", "Year", "Dataset", "Few-shot", "Rotation", "Localisation", "Unknown defects", "Feedback learning", "Limitation"],
               [[p["short"], p["year"], p["dataset"], p["fewshot"], p["rotation"], p["localization"], p["unknown"], p["feedback"], p["limit_short"]] for p in PAPERS]),
              ("Datasets", ds_header, ds_rows), ("Novelty matrix", nov_header, nov_rows), ("Research questions", rq_header, rq_rows),
              ("Risk register", risk_header, risk_rows), ("Roadmap", rm_header, rm_rows), ("References", ref_header, ref_rows),
              ("Glossary", ["Term", "Definition"], [list(g) for g in GLOSSARY])]
    fills = {"Yes": "D9EEEE", "Partial": "FAEFD9", "No": "F6E1DE", "Not evaluated": "EEF0F3", "Unclear": "EEF0F3"}
    for idx, (name, header, rows) in enumerate(sheets):
        ws = wb.active if idx == 0 else wb.create_sheet()
        ws.title = name
        ws.append(header)
        for r in rows:
            ws.append(r)
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="1F3A5F")
            c.alignment = Alignment(wrap_text=True, vertical="top")
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
                if isinstance(c.value, str) and c.value in fills:
                    c.fill = PatternFill("solid", fgColor=fills[c.value])
                if isinstance(c.value, str) and c.value.startswith("https://"):
                    c.hyperlink = c.value
                    c.font = Font(color="0F7C80", underline="single")
        for i, col in enumerate(header, 1):
            longest = max([len(str(col))] + [len(str(r[i - 1])) for r in rows])
            ws.column_dimensions[get_column_letter(i)].width = max(8, min(60, longest * 0.9 if longest < 30 else 45))
        ws.freeze_panes = "B2"
        ws.auto_filter.ref = ws.dimensions
    wb.save(os.path.join(ART, "03_literature_review.xlsx"))

    with open(os.path.join(ART, "12_research_questions.md"), "w", encoding="utf-8") as f:
        f.write("# Research questions and hypotheses (Artifact 12)\n\nNumerical targets are hypotheses to be revised after the pilot study, not predicted results.\n\n")
        for r in RQS:
            f.write(f"## {r['id']}\n\n**Question.** {r['q']}\n\n**Hypothesis.** {r['h']}\n\n**Measured by.** {r['m']}\n\n**Experiment.** {r['exp']}\n\n")
    with open(os.path.join(ART, "10_glossary.md"), "w", encoding="utf-8") as f:
        f.write("# Glossary (Artifact 10)\n\n| Term | Definition |\n| --- | --- |\n")
        for t, d in GLOSSARY:
            f.write(f"| {t} | {d} |\n")
    with open(os.path.join(ART, "references.json"), "w", encoding="utf-8") as f:
        json.dump([{"no": i, "key": k, "citation": strip(REFS[k][0]), "url": REFS[k][1], "verification": REFS[k][2]} for i, k in enumerate(order, 1)], f, indent=1, ensure_ascii=False)


def main():
    os.makedirs(BUILD, exist_ok=True)
    if "--no-figs" not in sys.argv:
        subprocess.run([sys.executable, os.path.join(SRC, "figures.py")], check=True)
    body, order = assemble()
    html_path = os.path.join(BUILD, "dossier.html")
    pdf_path = os.path.join(ROOT, PDF_NAME)
    # pass 1: no page numbers in the contents
    open(html_path, "w", encoding="utf-8").write(page_html(toc(body)))
    render(html_path, pdf_path)
    pages, n = heading_pages(pdf_path, body)
    # pass 2: contents with page numbers
    open(html_path, "w", encoding="utf-8").write(page_html(toc(body, pages)))
    render(html_path, pdf_path)
    pages2, n2 = heading_pages(pdf_path, body)
    if pages2 != pages:
        open(html_path, "w", encoding="utf-8").write(page_html(toc(body, pages2)))
        render(html_path, pdf_path)
    stamp_page_numbers(pdf_path, n2)
    missing = [m.group(2) for m in re.finditer(r"<h([12]) id=['\"]([^'\"]+)['\"]>", body) if m.group(2) not in pages2 and m.group(2) != "contents"]
    if missing:
        print("warning: headings not located in PDF:", missing)
    artifacts(order)
    print(f"built {PDF_NAME}: {n2} pages, {len(order)} references, {len(PAPERS)} papers")


if __name__ == "__main__":
    main()
