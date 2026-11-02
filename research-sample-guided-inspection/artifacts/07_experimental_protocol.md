# Experimental protocol (Artifact 7)

This is a planned protocol. **No experiments have been run and no results exist yet.** The full version, with rationale, is in Sections 20–22 of the dossier PDF.

## 1. General rules

- **Reference draws.** Each few-shot setting uses 5 independent random draws of the reference set. Seeds are fixed and logged.
- **Reporting.** Report mean ± standard deviation and 95% bootstrap confidence intervals over test images.
- **Paired comparisons.** Comparisons between methods use the same reference draws. Test with a Wilcoxon signed-rank test and apply a Holm correction.
- **Tuning.** Thresholds and hyper-parameters (τ, window size, coreset ratio, q) are chosen on validation data only, then frozen.
- **Data tiers.** Every table states its data tier. Synthetic results are never merged with real-data results.

| Tier | Data | Purpose |
| --- | --- | --- |
| T0 | MVTec AD, MVTec AD 2, VisA | Method check |
| T1 | Carinthia / Carinthia-S | Real SEM |
| T2 | Wafer Surface Defect | Real die images |
| T3 | Synthetic patterned wafers | Controlled ground truth |
| T4 | Partner data, if obtained | External validity |

## 2. Leak-free splits

Each split is defined by a manifest of file hashes. The evaluation script refuses to run if any test hash appears in a reference, calibration or feedback set.

| Dataset | Split rule |
| --- | --- |
| MVTec AD / VisA | Official split. References and calibration normals come only from the normal training set. |
| Carinthia-S | Stratified by class: reference-source / validation / test (≈ 20 / 20 / 60%), after near-duplicate clustering by perceptual hash. References are taken from defect-free regions of reference-source images only. |
| Wafer Surface Defect | Normal dies are split into reference pool / calibration / test. Defective dies appear only in validation and test. |
| Synthetic (T3) | Split by wafer and by design. Same-wafer tests never reuse a reference die. Cross-wafer tests use disjoint wafers. Cross-type tests use an unseen design. |
| Partner (T4) | Split by lot and wafer, in time order: earlier data for tuning, later data for testing. |
| Feedback | Three disjoint pools: feedback stream, held-out evaluation (never fed back), canary set. |

## 3. Experiments

| Exp. | RQ | Data | Procedure | Primary metrics |
| --- | --- | --- | --- | --- |
| A Few-shot | RQ1 | T0, T1, T2 | K ∈ {1, 2, 5, 10} × 5 draws; WRN-50 and DINOv2 encoders; with and without memory QC | Image AUROC, AUPRC; pixel AUROC, AUPRO |
| B Rotation | RQ2 | T0, T1, T2, T3 | Rotation 0–360° in 15° steps; translation ±10%; scale ±10%; illumination gradients. Five pipelines: none, warp-target, warp-reference, rotation-augmented memory, invariant features. Injected defects of 1–20 px for DPR | AUROC vs angle; false alarms; DPR; TRE |
| C Cross-die | RQ3 | T3 (T4) | Enrol K dies of one wafer; test the other dies of the same wafer. Compare spread vs clustered reference selection | AUROC, AUPRO; gap to the in-sample result |
| D Cross-wafer / type | RQ3 | T3, T4, T2→T1 | Enrol on wafer A; test on wafers B…; then a new design with 0, 1, 2, 5 new references | Per-split AUROC/AUPRO; references needed to recover |
| E Unknown | RQ4 | T1, T2, T3 | Leave-one-class-out over every class | Unknown-detection AUROC; open-set F1; forced-assignment rate |
| F Localisation | RQ5 | T0, T1, T2, T3 | Single- vs multi-scale features; native tiles vs resizing | Pixel AUROC, AUPRO, Dice, IoU (box IoU/AP on T2); by defect size |
| G Feedback | RQ6 | T0, T1, T3 | Simulated stream with 0/5/10/20% wrong labels and 10% wrong locations. Arms: none, ungated, gated, gated + 2nd review, gated + rollback. Negative control: random normal patches | ΔAUROC and false-alarm rate on held-out data; forgetting; contamination |
| H Ablations | all | best tier | Remove one component at a time (list below) | As in the affected experiment |

**Ablations (Experiment H):**

- without alignment;
- warp target instead of references;
- without reference memory (reference-free score);
- without multi-scale features;
- without unknown handling;
- without feedback;
- without feedback gate or rollback;
- without wafer context;
- without memory QC.

## 4. Baselines

- PatchCore
- AnomalyDINO
- RegAD
- GraphCore, or Augmentation + PatchCore
- WinCLIP
- Classical die-to-die difference
- Supervised U-Net (upper bound)
- Reverse Distillation / EfficientAD (full-data upper bound, optional)
- Abbas et al. memory correction (feedback)

## 5. Metrics

| Task | Metrics |
| --- | --- |
| Detection | AUROC, AUPRC, precision/recall/F1 at τ, recall at 1% false-alarm rate |
| Localisation | pixel AUROC, AUPRO (30% FPR), Dice, IoU, box IoU/AP |
| Unknowns | unknown-detection AUROC, open-set F1, forced-assignment rate |
| Alignment | DPR, target registration error |
| Efficiency | ms per die, memory size (MB, number of vectors), peak RAM |
| Feedback | held-out gain, forgetting rate (canary set), contamination rate |

## 6. Experiment G step by step

1. Build the initial memory M_0 from K references.
2. Stream the feedback dies in batches.
3. Simulate engineer decisions from ground truth, then corrupt a controlled fraction of them.
4. Apply the update arm.
5. Evaluate on the held-out set and the canary set only.
6. Report learning curves, the worst-case dip and the rollback count.
