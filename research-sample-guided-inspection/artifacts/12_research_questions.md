# Research questions and hypotheses (Artifact 12)

Numerical targets are hypotheses to be revised after the pilot study, not predicted results.

## RQ1

**Question.** How does reference-based anomaly detection performance change with K = 1, 2, 5, 10 normal reference dies?

**Hypothesis.** H1: Image-level AUROC and pixel AUPRO increase monotonically with K, with diminishing gains after K = 5. Rejected if the K = 10 result is within the 95% confidence interval of K = 1 for most classes.

**Measured by.** Image AUROC, AUPRC, pixel AUROC, AUPRO; 5 random reference draws per K

**Experiment.** A

## RQ2

**Question.** Does explicit alignment of reference memory to the target die reduce rotation-induced false alarms compared with (a) no alignment and (b) rotation-augmented memory, without weakening true defects?

**Hypothesis.** H2: Alignment-based inspection keeps AUROC within 2 points of the 0° result across a full 0–360° sweep, while the unaligned baseline degrades; defect preservation ratio (DPR) stays ≥ 0.9 for alignment and is lower for target-warping pipelines.

**Measured by.** AUROC vs angle curve; DPR; false alarms on normal dies per angle

**Experiment.** B

## RQ3

**Question.** Do references enrolled from some dies of a wafer transfer to the remaining dies of the same wafer, and to dies of other wafers or other die types?

**Hypothesis.** H3: Same-wafer transfer is within 3 AUROC points of in-sample performance; cross-wafer transfer loses more; cross-type transfer without new references fails (near chance), and is recovered by enrolling K ≥ 2 references of the new type.

**Measured by.** AUROC / AUPRO per split type; performance gap

**Experiment.** C, D

## RQ4

**Question.** Can a reference memory plus a small known-defect memory separate normal, known-class and unknown anomalies at pixel / region level?

**Hypothesis.** H4: In leave-one-class-out tests on Carinthia-S, held-out classes are flagged as anomalous (detection AUROC ≥ 0.85, target to be calibrated in the pilot) and are labelled 'unknown' more often than they are forced into a known class.

**Measured by.** Unknown-detection AUROC; open-set F1; known-class accuracy; forced-assignment rate

**Experiment.** E

## RQ5

**Question.** How accurately do reference-based anomaly maps localise defects compared with expert masks?

**Hypothesis.** H5: Multi-scale patch features localise better than single-scale features, especially for defects smaller than one patch.

**Measured by.** Pixel AUROC, AUPRO, Dice/IoU at the validation threshold, by defect-size bin

**Experiment.** F, H

## RQ6

**Question.** Do verified feedback updates of the reference memory improve later inspection on held-out dies, without contamination or forgetting?

**Hypothesis.** H6: Gated memory updates improve held-out AUROC and reduce false alarms; with 10% wrong feedback, quarantine + gate limits degradation to below 1 AUROC point; ungated updates degrade more.

**Measured by.** ΔAUROC on held-out set; false-alarm rate; forgetting rate; contamination rate

**Experiment.** G

## RQ7 (optional)

**Question.** Does combining per-die anomaly scores with wafer-level spatial context improve the ranking of truly defective dies?

**Hypothesis.** H7: Adding a spatial-neighbourhood term improves die-level AUPRC on synthetic wafers with clustered defects, and does not harm it on wafers with random defects.

**Measured by.** Die-level AUPRC; per-pattern breakdown

**Experiment.** H (wafer-context ablation)

