# I. Training and experimentation protocol

## I.1 Data preprocessing and annotation format

**Images.**

- Keep the original bit depth (8- or 16-bit TIFF/PNG) on disk.
- Convert to float32 in [0, 1] at load time, using the dataset's documented maximum (not per-image min–max, which hides contrast changes).
- Crop to the ROI after stage 1; never resize differently across dies of one group.

**Masks.** Single-channel PNG, 0 = background and 255 = defect. A separate "ignore" value (e.g. 128) marks uncertain annotation, excluded from losses.

**Group manifest (JSON).**

```json
{
  "group_id": "syn-L03-g0147",
  "split": "test",
  "design_id": "L03",
  "source": "synthetic-v1",
  "images": [{"path": "img_1.tif", "sha256": "…", "die_id": "1",
              "mask": "mask_1.png", "T_true": [[1,0,2.4],[0,1,-1.1]]}],
  "reference": {"path": "R.tif", "kind": "synthetic|reviewed-die|design-render"},
  "generator": {"version": "1.0", "seed": 9182, "params": {"N": 5, "overlap": "all-N:1"}}
}
```

## I.2 Synthetic defect generation and controlled transformations

- **Defect library.** Defect patches are cut from Carinthia-S masks (dilated by 2 px for context) and from MVTec, with source and licence recorded per patch. Procedural defects are bridge, open/break, particle, scratch, residue, missing via and line-edge bump.
- **Insertion.** Random scale (0.5–2×), rotation, intensity matching to the local background, then alpha or Poisson blending. The binary mask is the blended region above a set opacity.
- **Overlap control.** For each group, draw the number of dies sharing each defect location from {1, 2, …, N}. Include all-N cases at a set rate (initial 10% of defect sites) to populate $Z$.
- **Transformations.** Translation, rotation and scale ranges are swept in ablations (Section J.5). Use bicubic resampling with anti-aliasing when scaling down.
- **Imaging variation.** Gain/offset, low-order illumination gradient, Gaussian plus Poisson-like noise, mild defocus blur, and optional SEM-like edge brightening and charging streaks.
- **Augmentation for learned models (training only).** Flips, 90° rotations, brightness/contrast, noise and blur, via Albumentations. No augmentation is applied to validation or test data.

## I.3 Objectives and losses

| Model | Loss | Notes |
|---|---|---|
| U-Net segmentation | BCE + Dice (Equation G.7) | Optional positive-class weight if defects are < 1% of pixels |
| PatchCore / PaDiM | None (fitted, not trained) | Fit on defect-free images of the training split only |
| Masked reconstruction | Heteroscedastic L1 + gradient + SSIM (Equation G.7) | Holes simulated with the same overlap generator |
| Calibration | Temperature scaling or isotonic regression on validation | Never on test [42] |

## I.4 Hyper-parameter starting points (initial values, not optima)

| Parameter | Start | Search range |
|---|---|---|
| U-Net depth / base channels | 4 levels / 32 | 3–5 / 16–64 |
| Patch size | 256 px | 128–512 |
| Batch size | 8 | as memory allows |
| Optimiser | AdamW, lr 1e-3, weight decay 1e-4 | lr 3e-4 – 3e-3 |
| Schedule | cosine decay, 5% warm-up | — |
| Epochs | 100 with early stopping (patience 15) | — |
| PatchCore backbone / layers | WideResNet-50, layers 2+3 (Anomalib default) | ResNet-18 for speed |
| PatchCore coreset ratio | 0.1 | 0.01–0.25 |
| Fusion thresholds $\tau_d, \tau_r$ | 0.5, 0.5 | 0.3–0.7 |
| $\kappa$ (consistency) | 3 | 2–5 |
| $s_{\min}$ | 2 | 1–3 |

## I.5 Checkpoints, seeds, logging and tracking

- Fix and log seeds for Python, NumPy and PyTorch, plus the data-generator seed per group. Enable deterministic cuDNN settings for final runs, noting the slowdown.
- Save checkpoints at each validation improvement and at the end. Store the configuration file, git commit hash, lock-file hash, data-manifest hash, driver and CUDA versions with each run.
- Track with MLflow or TensorBoard: losses, validation metrics, learning rate, peak memory, wall-clock time.
- **Failure-case logging.** For every test group, save a panel (inputs, masks, $\hat R$, $U$, $A$, error map). Automatically tag the worst 5% by each primary metric for review.

## I.6 Validation, early stopping and profiling

- Use validation groups (separate designs) for early stopping, threshold tuning and calibration.
- Test once, after freezing all choices; repeat test evaluation only for reported ablations, not for tuning.
- **Profiling run (before any hardware decision).** Run one epoch at the intended patch size and batch on the target machine. Record `torch.cuda.max_memory_allocated()`, peak RSS (psutil) and time per iteration, then scale estimates from these measurements rather than from Section H.

## I.7 Leakage controls

These are the Section D.6 controls enforced in code:

- split by design or acquisition group;
- hash-checked manifests;
- thresholds chosen on validation only;
- no test-time augmentation tuned on test;
- defect patches used for synthetic *test* groups come from a held-out part of the defect library.

# J. Evaluation framework

![Figure 6. Experimental evaluation pipeline. Schematic of the planned protocol; no results exist yet.](figures/fig6_evaluation.svg){#fig:eval width=100%}

## J.1 Evaluation sets

**Valid pixels.** For a group, let $\Omega_v = \{\mathbf{x} : V_k(\mathbf{x}) = 1 \text{ for all } k\}$ (the common field of view). Unless stated otherwise, fidelity metrics are computed over $\mathcal{E} = \Omega_v \backslash A$, the pixels where the method made an estimate. **Coverage** is reported alongside every metric so that a method cannot look accurate by abstaining everywhere:

$$\mathrm{cov} = \frac{|\Omega_v \backslash A|}{|\Omega_v|} .$$

**Unrecoverable set.** $Z = \{\mathbf{x} \in \Omega_v : \sum_k (1 - M_k(\mathbf{x})) < s_{\min}\}$: pixels without enough clean observations. Computable only where true masks exist (synthetic data, annotated real data).

## J.2 Metrics

**Reconstruction fidelity** (requires a verified clean reference $R$; intensities in [0, 1], so the peak value is $L = 1$):

$$\mathrm{MSE} = \frac{1}{|\mathcal{E}|}\sum_{\mathbf{x}\in\mathcal{E}} \big(\hat R(\mathbf{x}) - R(\mathbf{x})\big)^2, \qquad \mathrm{PSNR} = 10\log_{10}\frac{L^2}{\mathrm{MSE}}, \qquad \mathrm{MAE} = \frac{1}{|\mathcal{E}|}\sum_{\mathbf{x}\in\mathcal{E}} \left|\hat R - R\right| .$$

$$\mathrm{SSIM}(u, v) = \frac{(2\mu_u\mu_v + C_1)(2\sigma_{uv} + C_2)}{(\mu_u^2 + \mu_v^2 + C_1)(\sigma_u^2 + \sigma_v^2 + C_2)}, \quad C_1 = (0.01L)^2,\; C_2 = (0.03L)^2,$$

computed in local Gaussian windows and averaged over windows fully inside $\mathcal{E}$ [45]. $\mu$, $\sigma^2$ and $\sigma_{uv}$ are the local means, variances and covariance. **Normalised MAE** (NMAE) divides MAE by the 1st–99th percentile range of $R$, to compare across layouts.

*Limitations:*

- PSNR and MAE reward smooth averages and do not distinguish a blurred edge from a missing feature.
- SSIM depends on window size.
- None of them detects a *plausible but wrong* structure if it is close in intensity.

That is why structure and leakage metrics are primary.

**Defect leakage.** Let $M_\cup = \bigcup_k M_k$ be every pixel that is defective in at least one input. The recoverable, non-abstained defect pixels are $\mathcal{D} = (M_\cup \cap \mathcal{E}) \backslash Z$. With a tolerance $\tau_\ell$ (initial $3\,s_0$):

$$\mathrm{DLR} = \frac{\left|\{\mathbf{x}\in\mathcal{D} : |\hat R(\mathbf{x}) - R(\mathbf{x})| > \tau_\ell\}\right|}{|\mathcal{D}|} .$$

**Instance leakage** is the fraction of defect instances (connected components) in which at least $a_{\min}$ pixels leak.

**Silent pass-through** is the most safety-relevant failure: unrecoverable pixels that were *not* abstained:

$$\mathrm{SPR} = \frac{|Z \backslash A|}{|Z|} .$$

*Limitation:* both depend on $\tau_\ell$, so report curves over $\tau_\ell$.

**Structural and edge preservation.** Edge maps $E(\hat R)$ and $E(R)$ come from the same Canny settings. With matching tolerance $r_t$ (initial 1.5 px):

- $P_e$ = fraction of predicted edge pixels within $r_t$ of a true edge;
- $R_e$ = the converse;
- $F_e = 2P_eR_e/(P_e + R_e)$.

**Gradient error** is $\frac{1}{|\mathcal{E}|}\sum \|\nabla\hat R - \nabla R\|_1$. On procedural layouts, also report line-width (critical-dimension proxy) error measured on profiles across lines.

*Limitation:* edge detectors depend on their thresholds, which must be fixed in advance.

**Registration error** (requires known transforms or fiducials). Target registration error, in pixels, over a grid $G$ of points in the ROI:

$$\mathrm{TRE}_k = \frac{1}{|G|}\sum_{\mathbf{x}\in G} \big\| \hat{\mathbf{T}}_k(\mathbf{x}) - \mathbf{T}_k(\mathbf{x}) \big\|_2 .$$

Report the mean and maximum per image, and the failure rate (TRE above a pre-set limit, e.g. 1 px, or a one-pitch error). On real data, TRE uses manually marked fiducials and is limited by their marking accuracy.

**Defect segmentation** (where true masks exist), from true positives (TP), false positives (FP) and false negatives (FN) at the pixel level:

$$\mathrm{Precision} = \frac{TP}{TP+FP}, \quad \mathrm{Recall} = \frac{TP}{TP+FN}, \quad \mathrm{IoU} = \frac{TP}{TP+FP+FN} .$$

Also report AU-PRO (per-region overlap integrated up to 30% false-positive rate, as defined for MVTec AD [2]) for threshold-free comparison.

*Limitation:* pixel metrics favour large defects; PRO weights each region equally.

**Uncertainty quality.**

- *Sparsification* [43]: sort pixels in $\mathcal{E}$ by $U$, descending. Remove the most uncertain fraction $f$ and compute the MAE of the remainder, $\mathrm{MAE}_U(f)$. The oracle removes pixels by true error, $\mathrm{MAE}_{\text{oracle}}(f)$. Then $\mathrm{AUSE} = \int_0^1 \big(\mathrm{MAE}_U(f) - \mathrm{MAE}_{\text{oracle}}(f)\big)\,df$; lower is better, and 0 means perfect ranking.
- *Selective risk* [41]: risk at coverage $c$ is the MAE over the fraction $c$ of pixels with the lowest $U$. **AURC** is the area under risk versus coverage.
- *Abstention quality:* the precision and recall of $A$ against $Z$.
- *Calibration of $\hat p_k$:* expected calibration error with 15 bins [42].

*Limitation:* $U$ cannot see errors that every reliable die shares; all uncertainty metrics are conditional on the evidence available.

**Runtime and peak memory.**

- Wall-clock time per group: median of 5 runs after one warm-up, with hardware recorded.
- Peak RSS (psutil) and `torch.cuda.max_memory_allocated()`.
- Reported per stage.

## J.3 Methods compared

| ID | Method | Purpose |
|---|---|---|
| M1 | **Single-image reference:** one registered die (random, and best-quality) used directly | Lower bound; mirrors one-neighbour die-to-die practice |
| M2 | **Classical registration + robust fusion:** unweighted median and trimmed mean over all dies | Standard multi-die reference [15] |
| M3 | **Defect-mask-aware fusion:** weights $w_k$, weighted median, abstention | Proposed core (H1–H3) |
| M4 | **M3 + learned reconstruction** for validated hole classes | Tests whether learned fill adds value without hallucination |
| (B) | RASL joint alignment and low-rank fusion [31] | Strong external baseline |

## J.4 Fair-comparison protocol

- All methods receive identical inputs, ROI, registration (unless registration is what is compared) and photometric correction.
- All thresholds are tuned on validation designs and frozen before test evaluation.
- **Coverage-matched comparison.** M3 and M4 abstain and M1 and M2 do not. Report each metric on (i) the pixels where all methods produce estimates, and (ii) each method's own covered pixels, together with coverage. Also report M2 restricted to M3's covered pixels.
- **Primary metrics (pre-registered):** DLR, SPR, and $F_e$ together with PSNR on the common pixels. Other metrics are secondary.
- **Statistics.** The unit of analysis is the *group*, nested in *designs*. Report per-group paired differences, 95% bootstrap confidence intervals (resampling designs, then groups), and a Wilcoxon signed-rank test as secondary. Use Holm correction for multiple comparisons. No method is "better" unless the interval excludes zero; effect sizes are reported either way.

## J.5 Ablation studies

| Factor | Levels (initial plan) | Question |
|---|---|---|
| Number of inputs $N$ | 2, 3, 4, 5 | How fast do leakage and coverage improve with more dies? |
| Defect overlap | independent; pairwise 10/30/50%; all-N 0/10/30% of sites | Where does robust fusion break down, and does abstention catch it? |
| Rotation | 0°, ±0.5°, ±2°, ±5° | Registration capture range |
| Scale | 1, ±1%, ±3% | Magnification drift |
| Illumination | none; gain ±10/25%; gradient; local charging streaks | Normalisation adequacy |
| Injected registration error | 0, 0.25, 0.5, 1, 2 px after registration | H4: sensitivity of fusion to misalignment |
| Missing evidence | random holes; systematic all-N defects | Abstention recall; SPR |
| Evidence source | consistency only; learned only; both | H3 |
| $s_{\min}$ | 1, 2, 3 | Coverage–accuracy trade-off |

## J.6 What cannot be validated without clean references or real same-design data

- **Without a verified clean reference,** PSNR, SSIM, MAE, DLR and edge metrics cannot be computed on real images. Only self-consistency checks remain, such as leave-one-die-out prediction (predict die $k$ from the other dies and compare outside its defects). These indicate agreement, not correctness.
- **Without real same-design groups,** no claim about real-world performance, registration difficulty or synthetic-to-real transfer (H5) can be made. Results remain synthetic.
- **Without design data,** a defect repeated in all dies cannot be distinguished from intended structure, so its recall is unmeasurable on real data.
- **Electrical function** is never validated by this project.
