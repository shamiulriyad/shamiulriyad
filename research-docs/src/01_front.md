---
title: "Defect-Aware Multi-Die Image Fusion for Semiconductor Reference Reconstruction"
subtitle: "Research and implementation documentation"
author: "Md Shamiul Islam Riyad · B.Sc. CSE, United International University"
date: "October 2026 · Version 1.0 · Planning document: no experiments have been run"
lang: en-GB
---

# How to read this document {.unnumbered}

This document plans a research project. It does not report results. No model has been trained, no dataset has been processed, and no hardware has been benchmarked. Every number in it is one of three things: a property of a published dataset or paper, with a link; a stated starting value for an experiment; or a calculation shown in full.

Key statements carry one of four labels:

| Label | Meaning |
|---|---|
| **Fact** | Supported by a cited source or by a calculation shown here. |
| **Recommendation** | A design choice made for this project, with the reason given. It can be changed. |
| **Hypothesis** | A claim the project will test. It may turn out to be false. |
| **Assumption** | A condition the method needs. If it fails, the method's guarantees fail with it. |

**Figures.** Figures 1–6 are schematics drawn from code (`make_figures.py`). None shows real inspection data. Figure 3 is a conceptual example and is labelled as one. No third-party images are reproduced, because none of the reviewed datasets clearly permits redistribution in a document of this kind.

**Verification.** The build environment could not open publisher and dataset websites directly. Bibliographic details were checked through search results that quote those pages. Appendix N.1 lists which details were confirmed this way and which still need a manual check.

# A. Executive summary and research motivation {.break}

## A.1 Problem

Automated inspection of semiconductor dies often compares an image of a die with a **reference image** of what the die should look like. The reference can be a neighbouring die (die-to-die comparison), a rendering of the design (die-to-database), or a stored "golden" image [11, 15]. If the reference is itself a real inspection image, any particle, scratch, bridge, missing feature, noise or imaging artefact in it enters the comparison. The result is missed defects or false alarms.

**Fact.** Commercial inspection already derives references from several dies, for example a per-pixel median or mean over about five to eight dies [15] or a computed reference fitted to a set of dies [16]. The same patent literature notes a known failure: a median cannot serve as the reference when systematic defects are widespread, because the median itself is then defective [17].

## A.2 Proposed research

This project studies how to build a **candidate defect-free reference image** from 4–5 images of dies that share one intended design. Each image may carry defects in different places. The system should:

1. align the images into one coordinate frame;
2. estimate, for every image and region, whether it is reliable, defective or uncertain;
3. compare corresponding regions across images;
4. fuse only trustworthy evidence;
5. reconstruct the reference where enough evidence exists;
6. explicitly flag regions where all observations are defective or the evidence is insufficient.

**The output is a digital image plus maps:** a candidate reference, per-image defect and reliability masks, an uncertainty map, an abstention mask and an evaluation report. It is not a fabricated or repaired die. A clean-looking reconstruction says nothing about electrical function.

## A.3 Intended application and potential benefit

- **Cleaner references for comparison-based inspection.** A reference that excludes defects seen in individual dies could reduce false alarms and missed detections compared with using one neighbouring image (Hypothesis H1).
- **Visible reliability.** An explicit uncertainty or abstention map tells an engineer where the reference can be trusted, instead of hiding gaps behind plausible-looking pixels.
- **A reproducible open benchmark.** A synthetic same-design benchmark with exact ground truth would let methods be compared fairly. To our knowledge no public dataset supports this today (Section D).

## A.4 Hypotheses to be tested

| ID | Hypothesis | Main measurement (Section J) |
|---|---|---|
| H1 | Defect-aware fusion leaks fewer defects into the reference than unweighted median or mean fusion, at comparable structural fidelity, when defects are mostly random. | Defect leakage rate, edge F-score |
| H2 | Support-based abstention flags regions that cannot be recovered (for example, defects shared by all dies) with high recall. | Abstention recall on the unrecoverable set *Z* |
| H3 | Reliability that combines learned defect scores with cross-die consistency beats either source alone. | Leakage and PSNR ablation |
| H4 | Residual registration error is a major driver of reconstruction error. The threshold at which it dominates is unknown and will be measured. | Error versus injected registration error |
| H5 | Detectors trained or calibrated on synthetic and public data transfer only partly to real same-design SEM groups. The gap can be quantified only with real data. | Synthetic versus real metrics |

## A.5 Major technical risks

1. **Repeated defects.** A systematic or mask-level defect at the same location in every die cannot be recovered by fusion. It can only be flagged, and it passes into the reference if it goes undetected.
2. **Registration error.** Misalignment blurs edges or mixes structures. Periodic layouts can cause shifts of exactly one pattern pitch.
3. **False-positive defect masks.** Normal process variation flagged as a defect removes good evidence.
4. **Hallucination.** Learned reconstruction can invent plausible but wrong circuitry.
5. **Data.** No public dataset supplies same-design die groups with verified clean references. Real validation depends on industry or laboratory collaboration, and synthetic results may not transfer.
6. **Prior art.** Multi-die reference generation already exists in industry [15–17]. The research contribution must be stated narrowly (Section C.8).

## A.6 Recommended strategy

**Recommendation.** Proceed in stages:

1. **Stage 1:** classical registration, robust statistics and mask-weighted fusion with abstention, built and evaluated first.
2. **Stage 2:** learned defect segmentation and reliability estimation (U-Net, PatchCore or PaDiM).
3. **Stage 3:** a learned reconstruction model, only for unresolved regions and only if it passes hallucination checks.

Diffusion models are optional, pretrained only, and never presented as verified patterns.
