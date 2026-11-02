# Sample-Guided Semiconductor Wafer Die Inspection: research dossier

**Topic:** few-shot, rotation-robust anomaly detection, defect localisation and verified feedback adaptation for semiconductor die images.

**The idea:** give the system a few sample dies, let it learn their patterns, show it new dies, let it locate defects, and improve it using verified feedback.

**Status:** this is a research proposal and technical explanation.

- No experiments have been run.
- The document reports no results.
- Every die image in it is a synthetic illustration, labelled as such.

## Deliverables

| File | What it is |
| --- | --- |
| [`Sample_Guided_Die_Inspection_Research_Dossier.pdf`](Sample_Guided_Die_Inspection_Research_Dossier.pdf) | **Main document** (A4). Contents with page numbers, PDF bookmarks, clickable citations and DOI links, vector figures, 30 sections. |
| [`artifacts/01_problem_definition.md`](artifacts/01_problem_definition.md) | Artifact 1: formal problem statement |
| [`artifacts/02_novelty_matrix.csv`](artifacts/02_novelty_matrix.csv) | Artifact 2: novelty matrix |
| [`artifacts/03_literature_review.xlsx`](artifacts/03_literature_review.xlsx) | Artifact 3: literature spreadsheet (see contents below) |
| [`artifacts/03_literature_review.csv`](artifacts/03_literature_review.csv) | Artifact 3: CSV version of the literature sheet |
| [`artifacts/04_dataset_inventory.csv`](artifacts/04_dataset_inventory.csv) | Artifact 4: dataset comparison |
| [`figures/dia_02_architecture.svg`](figures/dia_02_architecture.svg), [`diagrams/02_architecture.mmd`](diagrams/02_architecture.mmd) | Artifact 5: architecture diagram (SVG + editable Mermaid) |
| [`figures/dia_09_workflow.svg`](figures/dia_09_workflow.svg), [`diagrams/09_research_workflow.mmd`](diagrams/09_research_workflow.mmd) | Artifact 6: end-to-end workflow |
| [`artifacts/07_experimental_protocol.md`](artifacts/07_experimental_protocol.md), [`artifacts/example_experiment_config.yaml`](artifacts/example_experiment_config.yaml) | Artifact 7: experimental protocol and an example config |
| [`artifacts/08_risk_register.csv`](artifacts/08_risk_register.csv) | Artifact 8: risk register |
| [`artifacts/09_roadmap.csv`](artifacts/09_roadmap.csv), [`figures/dia_10_gantt.svg`](figures/dia_10_gantt.svg) | Artifact 9: implementation roadmap |
| [`artifacts/10_glossary.md`](artifacts/10_glossary.md) | Artifact 10: glossary (63 terms) |
| [`figures/`](figures/) | Artifact 11: visual gallery and all diagrams, as editable SVG |
| [`artifacts/12_research_questions.md`](artifacts/12_research_questions.md) | Artifact 12: research questions and falsifiable hypotheses |
| [`diagrams/*.mmd`](diagrams/) | Mermaid sources of Diagrams 1–8 and the research workflow. All nine were checked to render with Mermaid 10.9. |
| [`prototype/toy_reference_memory.py`](prototype/toy_reference_memory.py) | Runnable CPU toy of the pipeline (see below) |
| [`artifacts/references.json`](artifacts/references.json) | Bibliography with verification codes |

The literature spreadsheet has these sheets:

- 34 papers, with the 15 requested fields
- comparison matrix
- datasets
- novelty
- research questions
- risks
- roadmap
- references
- glossary

The toy prototype covers enrolment, alignment, the reference memory, anomaly maps and the threshold.

## What the dossier concludes

**Literature.** The building blocks exist separately in published work:

- memory-based few-shot anomaly detection (PatchCore, AnomalyDINO);
- registration and rotation invariance (RegAD, GraphCore);
- open-set recognition for wafer maps;
- continual learning on fab SEM data;
- human-in-the-loop memory correction (a 2026 preprint).

**Gap.** We found no study that tests the following on semiconductor die images:

- defect-preserving alignment;
- pixel-level known/unknown triage;
- feedback updates when some feedback is wrong;
- separate same-wafer, cross-wafer and cross-type splits.

This is a gap in evaluated combinations and protocols. It is not a claim that any single component is new.

**Recommended core contributions:**

- C2: defect-preserving alignment, measured with a defect preservation ratio (DPR);
- C3: reference-guided unknown-anomaly localisation;
- C5: safe feedback adaptation, if time allows.

**Data.** No public dataset combines patterned dies, pixel masks and wafer coordinates. The plan therefore combines several sources:

| Data | Role |
| --- | --- |
| Carinthia-S | 4,591 SEM images with expert masks |
| Wafer Surface Defect | 500 optical single-die images with boxes |
| MVTec AD | Method check |
| WM-811K | Wafer maps only |
| Labelled synthetic patterned-wafer benchmark | Same-wafer, cross-wafer and cross-type tests |

## Verification of facts

Direct access to arXiv, Zenodo and Crossref was blocked in the build environment. Paper and dataset facts were checked through search results that quote the official records: publisher, CVF, ACL Anthology, arXiv, Zenodo and IEEE DataPort pages.

Each reference in the PDF carries a code:

- **S:** checked in this session.
- **P:** checked in an earlier verification log in this repository (`research-docs/REFERENCES.md`).
- **K:** standard bibliographic knowledge, used only for background references such as backbones and registration.

Quoted numbers come from abstracts or official records only.

These items are **not verified** and are marked as such in the PDF:

- dataset licences (Carinthia, Carinthia-S, Wafer Surface Defect, WM-811K);
- image resolutions and class names of Carinthia;
- MixedWM38 and MPDD counts.

Open every link once before you share the document outside the project.

## Rebuilding

```bash
pip install numpy scipy matplotlib openpyxl pypdf
```

```bash
python3 research-sample-guided-inspection/build.py
```

- The build also needs Node with `playwright` and its Chromium.
- `build.py` regenerates the figures (`src/figures.py`) and assembles `src/sections/*.html`.
- It numbers figures, tables and citations, renders the A4 PDF in two passes so the contents show page numbers, and stamps the page header and page numbers.
- It then writes the XLSX, CSV and Markdown artifacts.
- Paper, dataset, risk and roadmap data each live in one place (`src/papers.py`, `src/tables.py`, `src/refs.py`), so the PDF and the spreadsheets cannot disagree.

To run the toy pipeline (about 10 s on a CPU):

```bash
python3 research-sample-guided-inspection/prototype/toy_reference_memory.py
```

The prototype uses synthetic dies and simple patch descriptors in place of a deep encoder. Its numbers illustrate how the pipeline works; they are not experimental results.
