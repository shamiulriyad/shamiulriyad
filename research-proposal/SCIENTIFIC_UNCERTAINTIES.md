# Open points that still need checking

These items could not be fully verified while preparing the proposal, or they are assumptions the research itself must test. Check them before you submit, or raise them with the supervisor.

## How the sources were checked
- The build environment could not open zenodo.org, mvtec.com, link.springer.com or doi.org directly; the network policy blocked them. Every bibliographic and dataset fact below was checked through web-search results that quote those pages, and through repository or mirror listings. **Open each of the 8 links in the PDF once by hand.**

## References and datasets
1. **Carinthia (Zenodo 10715190), licence.** Not found in any accessible source, so the table says "not verified".
2. **Carinthia, record identity.** One secondary listing gives the original dataset as 10.5281/zenodo.10696644. Another, using the citation format Zenodo generates, gives 10715190 as version v2. 10696644 is probably the concept DOI covering all versions, but this is unconfirmed.
3. **Carinthia, annotation type and "unstructured wafers".** The image-level class labels (6 classes, CSV) and the phrase "one production layer of unstructured wafers" come from secondary descriptions of the record, not from reading the record itself.
4. **Carinthia-S (Zenodo 16895427).** The details below come only from third-party repositories and listings:
   - authors: C. Kofler and V. Hasić
   - published 20 August 2025
   - licence: CC BY 4.0
   - binary masks
   One listing calls the record classification-only. Others say some masks contain anti-aliased grey values, and that class 6 ("no visible defect") includes misaligned captures. Confirm all of this on Zenodo.
5. **MVTec AD 2 [2], journal details.** The IJCV 2026 DOI comes from MVTec's dataset page as quoted in search results. A volume and issue (134(4)) were also reported but are left out of the reference until confirmed.
6. **Taha [4].** The publication year, volume and pages could not be confirmed, so the reference shows only the journal and DOI. The arXiv preprint (2310.10705) has changed title between versions.
7. **MVTec page URLs.** MVTec serves its dataset pages under both `/research-teaching/datasets/` and `/company/research/datasets/`. The PDF uses the `/research-teaching/` form you supplied; check that it does not redirect somewhere unexpected.

## Statements without a citation
8. **"Inspection often compares a die image with a reference."** Die-to-die and die-to-database comparison is standard practice, but the page cites no source for it. Add a textbook or review citation if a reviewer asks.
9. **"Random defects usually fall in different places."** This is the core premise. It holds for random particle-type defects. It fails for systematic, design-related or reticle (mask-level) defects that repeat on every die. The proposal names this limit, but how often each type occurs in a given process is unknown.

## Possible prior art (novelty)
10. Commercial die-to-die inspection already uses several dies at once. Examples include arbitration with a third die, and median or "golden" computed reference images. Patents may already cover defect-aware weighting with explicit uncertainty. **The novelty of the combination is unverified until the literature and patent review is done.** The proposal says so; do not strengthen that claim.

## Technical assumptions the project must test
11. **Registration accuracy.** It is unknown whether sub-pixel registration is reachable on real SEM or optical images under charging, drift, distortion and focus differences between dies.
12. **Process variation versus defects.** Legitimate die-to-die variation (critical-dimension variation, line-edge roughness) may be flagged as a defect, or may blur the fused reference.
13. **Detector transfer.** Anomaly detectors trained on natural or industrial images (MVTec) may not transfer to SEM inspection images.
14. **Is 4–5 dies enough?** Whether 4–5 dies give enough support where defects overlap is unknown. The ablation over the number of dies is meant to measure this.
15. **Do the metrics predict usefulness?** Higher PSNR or SSIM against a clean reference may not mean better downstream defect detection. That is why downstream detection should be measured directly.
16. **Synthetic-to-real transfer.** Pasting real defect appearances into copies of one clean layout leaves out real imaging physics. Results may not transfer without real same-design groups.

## What the page does not claim
- No experimental result, accuracy figure or performance target appears in the proposal.
- Fig. 1 is a hand-built schematic and is labelled as not experimental data.
