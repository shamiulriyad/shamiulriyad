# Change log

## Revision 2 (October 2026): restructured around one explanatory figure

This revision follows a review of the rendered version 1 PDF. The research idea, the author line, the one-page format and the four references are kept.

### Figure
- **Replaced both figures.** Version 1 had a generic six-box flow chart and a small 4-die sketch about 26 mm tall. The sketch had no registration step, no per-die maps and no record of which die supplied which region. Fig. 1 is now a single figure about 87 mm tall with panels A–E.
  - A: five misaligned inputs.
  - B: registration into one common frame.
  - C: estimated defect/reliability maps.
  - D: an evidence matrix showing which die is used for each region, with the count of reliable dies per region.
  - E: the candidate reference and the uncertainty map side by side.
- **One layout everywhere.** `make_figure.py` draws every panel from a single layout definition and a single defect list. The circuit pattern, defect positions, maps, matrix and outputs therefore cannot drift apart.
- **Each die has a different defect:** a particle, a bridge, an open, a scratch and residue. Defect **f** repeats in all five dies, which shows what happens when every input is defective at the same place. Region f is marked uncertain, not filled in.
- **The three states are shown separately.** The scratch on die 4 is marked *uncertain* rather than *defective*, so the figure shows reliable, defective and uncertain regions with one legend used in C, D and E.
- **Maps are labelled as estimates.** Panel C is labelled "estimates only" and the caption says "not ground-truth labels", so anomaly scores are not presented as confirmed defects.
- **The uncertainty map has a concrete meaning:** the number of reliable dies supporting each pixel (5, 4 or 0).
- **"Conceptual example — not experimental data"** appears on the figure itself and in its caption.
- **Text inside the figure was cut** and label sizes raised to about 6–7.5 pt at print size.

### Narrative
- **Research question added** in the exact wording requested, labelled as a hypothesis.
- **Problem section rewritten** to explain four points in order: why one real reference image is risky, why several same-design images hold complementary evidence, why registration must come before fusion, and what is produced. It also states that the output is a digital image, not a repaired die, and that a clean image does not imply electrical function.
- **Research gap made precise.** It no longer claims that detection, fusion or reconstruction is new. The contribution is framed as a testable combination of four elements (registration, region-level reliability, evidence-weighted reconstruction, explicit uncertainty). The section also states how this differs from classification or segmentation, and requires a literature and patent review before any novelty claim.
- **Objectives reduced to the four requested.** No accuracy targets.
- **Evaluation now says what would count as evidence:** fewer leaked defects than mean or median fusion at similar fidelity, better than a single-image reference, and uncertainty flags that land on truly unrecoverable regions. Negative results will be reported.
- **The limit of the method is stated:** a region defective in every die can only be flagged, and passes into the reference if it is not detected.
- **Detail moved off the page.** Method specifics, the synthetic benchmark protocol, metric definitions and the work plan are now in `TECHNICAL_NOTES.md`.

### Data and references
- **The dataset table now has annotation and licence columns,** and lists Carinthia and Carinthia-S as separate rows. The note under it says that anomaly-detection datasets do not provide multi-die reconstruction ground truth, and explains why a synthetic benchmark and real same-design groups are both needed.
- **[2] updated** from the arXiv preprint to the journal version, *International Journal of Computer Vision* (2026, doi:10.1007/s11263-026-02743-0). MVTec's dataset page lists that DOI. The arXiv link is kept.
- **[3] now names the first three Carinthia authors** (Kofler, Strauß, Zernig et al.) and the record version (v2).
- **Unverified licences are no longer stated as fact.** The original Carinthia licence could not be confirmed, so the table says "not verified". Carinthia-S says "CC BY 4.0 (unverified)" because that licence comes only from secondary listings.

### Layout and production
- Single-column narrative with short paragraphs. Only the short gap and evaluation blocks sit side by side.
- Fonts switched from Inter (CFF, which Chromium embeds as Type 3 fonts) to Liberation Serif and Liberation Sans. These are TrueType, so every font embeds cleanly and renders sharply in any PDF viewer.
- `build.cjs` now checks for overflow on the new layout, waits for the figure to load, and refuses to write a PDF that does not fit one page.
