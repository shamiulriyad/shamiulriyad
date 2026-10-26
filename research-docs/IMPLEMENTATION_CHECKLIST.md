# Implementation checklist

A compact companion to the technical document. Section references (B–N) point to it. Tick items in order; a milestone is done only when all its items are ticked.

## L1. Literature review and dataset audit
- [ ] Write the review protocol: databases (IEEE Xplore, SPIE, Scopus, arXiv, Google Patents), search strings, inclusion rules.
- [ ] Screen and log the counts; search patents for multi-die and computed references (see [15–17]).
- [ ] Confirm or revise the gap statement (C.8). If items 2–5 already exist together, refocus the project.
- [ ] Open every dataset record and confirm content and licence (N.1 open items); write dataset cards.

## L2. Data and synthetic benchmark
- [ ] Download the Level-1 data; record licences per dataset and per defect patch.
- [ ] Build the defect library from Carinthia-S and MVTec masks, with a held-out test portion.
- [ ] Generator v1: layouts, transforms, photometrics, noise, overlap policy including all-N (D.4).
- [ ] Store R, Mₖ, Tₖ, Z, parameters and seed for every group; test that regenerating from the seed reproduces the same hashes.
- [ ] Split by design or layout family; write hashed manifests; add a leakage guard to the evaluator (D.6).
- [ ] Compare synthetic and real statistics (histograms, noise spectra, edge profiles).

## L3. Registration baseline
- [ ] Quality checks and ROI (E, stage 1).
- [ ] Phase correlation, then ECC Euclidean/affine; defect-masked second pass (G.1).
- [ ] Residual and confidence maps; pitch-ambiguity test; image rejection with logged reasons.
- [ ] Measure TRE per test level; add unit tests on known shifts and rotations.

## L4. Defect masks, fusion and abstention (core method M3)
- [ ] Robust gain/offset normalisation after coarse registration.
- [ ] Cross-die z-score (with a noise floor s₀), mask post-processing (G.2).
- [ ] Weights wₖ, states, support S (G.3).
- [ ] Weighted median and Huber fusion; structure-aware region safeguard; provenance map (G.4).
- [ ] Uncertainty U and abstention A, with NaN in R̂ wherever A = 1 (G.5).
- [ ] Baselines M1 (single image) and M2 (median, trimmed mean) on the same inputs.
- [ ] Export: float32 TIFF, masks, JSON metrics, configuration copy.

## L5. Learned evidence and optional reconstruction
- [ ] U-Net (BCE + Dice) trained on train designs only; calibrate on validation (G.7, I.3).
- [ ] PatchCore and PaDiM via Anomalib, fitted on defect-free training images only.
- [ ] Noisy-OR combination with the consistency evidence; H3 ablation.
- [ ] Optional masked U-Net (M4): hallucination tests (K) and validation criteria (G.6) must pass before enabling.

## L6. Evaluation
- [ ] Implement all J.2 metrics, with unit tests on toy cases where the answer is known.
- [ ] Coverage-matched comparison; pre-registered primary metrics DLR, SPR, F_e and PSNR (J.4).
- [ ] Bootstrap CIs over designs; Holm correction.
- [ ] Ablations: N, overlap, rotation, scale, illumination, injected registration error, missing evidence, evidence source, s_min (J.5).
- [ ] Runtime and peak memory per stage, with hardware recorded.
- [ ] Failure gallery: worst 5% per primary metric.

## L7. Report and release
- [ ] Report synthetic and real results separately; state the J.6 limits.
- [ ] Release code, configs, lock file and generator; respect NC licences when redistributing data.
- [ ] Second person reproduces one main table from a clean checkout.

## Always
- [ ] Fixed seeds; log the git hash, lock-file hash, data-manifest hash, driver and CUDA version.
- [ ] Tune thresholds on validation only; touch the test set only for final runs.
- [ ] Never fill an abstained pixel without the model-filled flag F; never present synthetic results as real-world performance.
- [ ] Never claim electrical function or physical repair.
