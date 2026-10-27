# E. Proposed system architecture

![Figure 2. Modular pipeline. Stages 6 and 8 are the core of the proposed method; stage 7 is optional and skipped by default. Schematic, not experimental data.](figures/fig1_architecture.svg){#fig:arch width=100%}

![Figure 3. Conceptual example (synthetic, not experimental data). One layout is used throughout. (A) Five misaligned dies, each with its own defect a–e, and defect f repeated in all five. (B) Registration into one frame. (C) Estimated defect maps. (D) Which die supplies each region, and how many reliable dies support it. (E) Candidate reference and uncertainty map; f has no reliable source and is flagged, not filled.](figures/fig2_example.svg){#fig:example width=100%}

## E.1 Stage specifications

Each stage below lists its inputs, outputs, candidate methods, assumptions, failure modes and the **recommended baseline** to build first.

**Stage 1. Image quality checks and ROI extraction.**

- *Inputs:* raw images $I_k$ and metadata.
- *Outputs:* accepted images, ROI, quality report.
- *Methods:*
  - focus measure (variance of Laplacian);
  - saturation fraction;
  - noise estimate (median absolute deviation of a high-pass residual);
  - coverage of the shared ROI after coarse alignment.
- *Assumptions:* metadata identifies layer and design.
- *Failure modes:* thresholds rejecting usable images; charging artefacts passing.
- *Baseline:* fixed thresholds set on validation data; reject an image only with a logged reason; require at least 3 accepted images.

**Stage 2. Illumination and contrast normalisation (only when justified).**

- *Inputs:* accepted images.
- *Outputs:* $y_k$ on a common intensity scale, plus fitted $\hat a_k, \hat b_k$.
- *Methods:*
  - robust affine gain/offset to the group median (least trimmed squares);
  - histogram matching;
  - low-order background (illumination gradient) removal.
- *Assumptions:* A5 (mostly global photometric differences).
- *Failure modes:* histogram matching can make a large defect look normal or vice versa, or create false structure.
- *Baseline:* robust gain/offset only. Use histogram matching only if validation shows the gain/offset model leaves systematic residuals. **Normalisation is fitted after coarse registration**, using only pixels with low cross-die deviation.

**Stage 3. Geometric registration.**

- *Inputs:* images, ROI.
- *Outputs:* $\hat{\mathbf{T}}_k$, registered $\tilde I_k$, validity $V_k$, residual and confidence maps $c_k$.
- *Methods:* phase correlation [29]; Fourier–Mellin [28]; ECC [27]; SIFT/ORB + RANSAC [24–26]; optional regularised dense residual flow; joint alignment by RASL [31] as a comparison.
- *Assumptions:* A4; enough non-periodic structure, or fiducials, to resolve pitch ambiguity.
- *Failure modes:*
  - one-pitch shifts in periodic arrays;
  - defects pulling the alignment;
  - over-flexible models absorbing defects;
  - interpolation blur.
- *Baseline:* the reference frame is the median-quality image (or the design rendering if available). Phase correlation for translation, then ECC Euclidean refinement, with defect-likely pixels masked out of the ECC objective in a second pass.

**Stage 4. Defect segmentation and anomaly scoring.**

- *Inputs:* registered, normalised images.
- *Outputs:* $\hat p_k(\mathbf{x})$, defect probability per image.
- *Methods:* supervised U-Net [22] (Mask R-CNN [12] if instance counts matter); one-class PatchCore [18] / PaDiM [19]; cross-die robust deviation.
- *Assumptions:* training domain resembles test domain (H5).
- *Failure modes:*
  - false positives on process variation;
  - false negatives on low-contrast defects;
  - miscalibrated scores.
- *Baseline:* cross-die robust z-score (no learning). Learned models are added in Stage 2 of the strategy, with temperature or isotonic calibration on validation data [42].

**Stage 5. Reliability and confidence estimation.**

- *Inputs:* $\hat p_k$, deviation $z_k$, registration confidence $c_k$, validity $V_k$.
- *Outputs:* weights $w_k(\mathbf{x})$, states (reliable / defective / uncertain), support $S(\mathbf{x})$.
- *Methods:* product-of-evidence weight (Equation G.3); optionally a small learned fusion of the evidence channels.
- *Assumptions:* evidence sources are not all wrong at once.
- *Failure modes:* with two coincident defects at $N = 4$ the median breaks down and the consistency term points the wrong way.
- *Baseline:* the product weight with thresholds tuned on validation groups.

**Stage 6. Defect-aware fusion.**

- *Inputs:* $y_k$, $w_k$.
- *Outputs:* $\hat R$, provenance map.
- *Methods:* weighted median; Huber M-estimator via iteratively reweighted least squares; region-level source selection where reliable observations disagree structurally.
- *Assumptions:* reliable observations show the same structure up to noise.
- *Failure modes:* edge blur from residual misregistration; seams between regions from different sources; mixing of distinct structures (Section G.4).
- *Baseline:* weighted median over observations with $w_k \ge \tau_r$.

**Stage 7. Optional learned reconstruction.**

- *Inputs:* stack of $y_k$, $w_k$, and the abstention mask $A$.
- *Outputs:* a fill for some abstained pixels, the model-filled mask $F$, and predicted uncertainty.
- *Methods:* masked U-Net with partial convolutions [34]; pretrained LaMa [35]; RePaint [36] as an experiment only.
- *Assumptions:* the layout is locally predictable from context (often false for unique structures).
- *Failure modes:* hallucinated circuitry [44].
- *Baseline:* **none: skipped by default.** Enabled only after it passes the checks in Section K.

**Stage 8. Uncertainty estimation and abstention.**

- *Inputs:* $S$, the weighted spread, $n_\text{eff}$, the region consistency flag and $F$.
- *Outputs:* $U$, $A$.
- *Methods:* analytic spread and support (Section G.5); ensembles or MC dropout for learned stages [39, 40].
- *Assumptions:* calibration on validation groups transfers to test.
- *Failure modes:* overconfidence when every reliable die shares an undetected defect (unobservable from the images).
- *Baseline:* $A = [S < s_{\min}] \lor [\mathrm{SE} > \tau_u]$.

**Stage 9. Evaluation and result export.**

- *Inputs:* all maps, ground truth where available.
- *Outputs:* metrics (Section J), report, failure gallery, files.
- *Format:* 32-bit float TIFF for $\hat R$ (NaN where abstained); PNG/TIFF masks; JSON metrics; YAML copy of the configuration; provenance as a compact index map.

# F. Model selection and technical justification

![Figure 4. Decision diagram for choosing registration, defect-evidence and reconstruction methods. Recommendations, not results.](figures/fig4_decisions.svg){#fig:decisions width=100%}

## F.1 Registration

| Option | Handles | Pros | Cons | Recommendation |
|---|---|---|---|---|
| Phase correlation (sub-pixel) [29] | Translation | Fast, accurate, global, intensity-robust | Translation only; periodic ambiguity | **Default first step** |
| Fourier–Mellin [28] | Translation, rotation, scale | No features needed | Less accurate; boundary effects | Coarse alignment if rotation is unknown |
| ECC [27] (OpenCV) | Translation to homography | Sub-pixel; gain/offset invariant; supports masks | Needs initialisation; local optimum | **Default refinement** (Euclidean, then affine if needed) |
| SIFT / ORB + RANSAC [24–26] | Large rotation and scale | Wide capture range | Repetitive layouts give wrong matches; ORB less precise | Only with distinctive structures or fiducials |
| Learned registration | Anything learned | Can handle complex distortion | Needs training data; opaque failure | Not recommended for this data scale |
| RASL [31] | Joint align and separate | Uses all images together | Heavier; assumptions on correlation | **Comparison baseline** |

## F.2 Defect evidence

| Option | Supervision | Output | Pros | Cons | Recommendation |
|---|---|---|---|---|---|
| Cross-die robust z-score | None | Per-pixel deviation | No training; uses the group itself | Breaks at ≥ 50% co-located defects | **Stage-1 baseline** |
| U-Net [22] | Pixel masks | Per-pixel probability | Precise; data-efficient | Needs masks (Carinthia-S, synthetic) | **Stage-2 main** |
| PatchCore [18] | Defect-free only | Patch anomaly score (upsampled) | No defect labels; strong localisation | Uncalibrated; memory bank grows | **Stage-2 alternative** |
| PaDiM [19] | Defect-free only | Position-wise Mahalanobis score | Uses alignment; simple | Per-position covariance memory | Stage-2 alternative for aligned data |
| DRAEM [20] | Synthetic anomalies | Mask | No real labels | Synthetic-to-real gap | Optional |
| ResNet classifier | Image labels | One label per image | Simple | **No pixel mask, no reconstruction** | Not sufficient (below) |

**Why a classification-only model cannot do this task.** A classifier such as a ResNet maps an entire image to one label ("bridge", "particle", "clean"). Fusion needs to know *which pixels* of *which image* are untrustworthy, and reconstruction needs pixel values. Class activation maps from a classifier are coarse (at the resolution of the last feature map), uncalibrated and not trained to delineate defect boundaries. They cannot replace a segmentation mask. A classifier can still serve as a quality gate (e.g. rejecting a badly charged image) or route groups to defect-specific settings.

## F.3 Fusion and reconstruction

| Option | Pros | Cons | Recommendation |
|---|---|---|---|
| Pixel-wise median (unweighted) | Simple; robust below 50% outliers | Ignores defect evidence; blurs edges under misregistration; mixes structures; fails at ≥ 50% | Baseline M2 |
| Trimmed mean | Lower variance than median | Same failure modes | Baseline M2 variant |
| Weighted median / Huber (proposed) | Uses evidence; robust; provenance is traceable | Depends on weight quality | **Stage-1 core (M3)** |
| Region-level source selection | Keeps edges sharp; no mixing | Seams; depends on region definition | Used where structure disagrees |
| Masked U-Net / partial conv [34] | Fills gaps from context | Can hallucinate; needs training data | Stage 3, optional, flagged |
| LaMa [35] (pretrained) | Strong on periodic texture | Domain gap; convincing hallucinations | Comparison only |
| Diffusion inpainting [36] | Diverse samples, usable for uncertainty | Slow; stochastic; data-hungry | **Pretrained only; never trained from scratch here** |

**Why not train a large diffusion model from scratch.** The expected data (a few thousand SEM images at most, plus synthetic data) is far too small to train a large generative model well. Training cost is high. More importantly, a generative model is designed to produce *plausible* content, which is the opposite of what an inspection reference needs where evidence is missing. If used at all, pretrained diffusion inpainting is an experiment whose outputs are labelled as samples, and whose spread across samples may serve as an uncertainty signal.

## F.4 Staged strategy

1. **Stage 1: classical.** Phase correlation + ECC registration; robust gain/offset; cross-die z-score; weighted-median fusion; support-based abstention. Deliverable: a complete, reproducible baseline pipeline (M2 and M3 in Section J).
2. **Stage 2: learned evidence.** U-Net on Carinthia-S and synthetic masks; PatchCore/PaDiM on defect-free data; calibrated probabilities feeding $w_k$. Deliverable: ablation H3.
3. **Stage 3: optional reconstruction.** Masked U-Net for abstained regions, only if hallucination checks pass on held-out designs. Outputs stay flagged (M4).
