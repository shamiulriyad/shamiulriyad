# Research and implementation documentation

Full technical documentation for *Defect-Aware Multi-Die Image Fusion for Semiconductor Reference Reconstruction*: problem formulation, literature review, dataset audit, architecture, algorithms, hardware, training and evaluation protocol, risks, roadmap and references.

This is a **planning document**. No experiments have been run, and it contains no results, accuracy figures or hardware benchmarks. All figures are synthetic schematics generated from code.

## Deliverables

| File | Contents |
| --- | --- |
| `Defect_Aware_MultiDie_Fusion_Technical_Document.pdf` | Main document: 35 pages, A4, clickable links and bookmarks, vector figures. |
| `Defect_Aware_MultiDie_Fusion_Technical_Document.docx` | Editable Word version with native equations. Word refreshes the table of contents when the file is opened. |
| `REFERENCES.md` | The 50 references with working links, plus the verification log. |
| `IMPLEMENTATION_CHECKLIST.md` | Compact milestone-by-milestone checklist. |
| `Decisions_and_Open_Questions.pdf` | One-page summary of technical decisions and unresolved questions (source: `decisions_summary.html`). |

## Editing and rebuilding

- **Text:** edit the section files in `src/`. They are combined in file-name order.
- **Figures:** edit `make_figures.py`, then run `python3 research-docs/make_figures.py`. Figure 3 is generated from `../research-proposal/make_figure.py`, so the proposal and this document always show the same example.
- **Build:** run `python3 research-docs/build.py`. This writes the PDF, the DOCX and the one-page summary.

Requirements:

- pandoc 3
- Python with `python-docx` and `lxml`
- Node with `playwright`
- MathJax 3 installed locally: `cd research-docs/build && npm install mathjax@3.2.2`

The build is fully offline.

## What the build does to the DOCX

Pandoc's DOCX output places some XML elements in an order the Office schema does not allow. `build.py` reorders them, so the file passes the Office XML schema validator. LibreOffice's round trip was not used, because it drops the equations.
