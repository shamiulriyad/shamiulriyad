# Technical notes (supplement to the one-page proposal)

This file holds the details that were moved off the one-page proposal to keep it readable. Everything here is a plan, not a result.

## 1. Inputs and assumptions
- A **group** is N = 4–5 images of dies sharing the same intended layout, taken with the same layer, tool and imaging settings.
- Random defects are assumed to occur independently between dies. Systematic or mask-level defects break this assumption and are treated as a known failure mode (region *f* in Fig. 1).

## 2. Pipeline (Fig. 1, panels A–E)
1. **Pre-processing.** Intensity normalisation (per-image histogram matching to the group median) and mild denoising.
2. **Registration (B).**
   - Global alignment by phase correlation (translation), then estimation of rotation and scale (e.g. log-polar phase correlation or a feature-based homography).
   - Local refinement, either classical (optical flow or B-spline free-form deformation) or learning-based.
   - The per-pixel registration residual lowers that pixel's weight.
3. **Reliability estimation (C).** Each pixel or region *x* of die *k* gets a weight w_k(x) from three evidence sources:
   - an anomaly score from a detector trained on defect-free data, such as PatchCore- or PaDiM-style feature models (to be chosen after the literature review);
   - deviation from a robust cross-die estimate (the median, with median absolute deviation);
   - registration confidence.

   Thresholds turn the weights into three states: reliable, uncertain or defective. Region-level estimates (connected components, superpixels) are compared with pixel-level ones.
4. **Fusion (D).**
   - Core method: a weighted robust estimate per pixel, such as a weighted median or a Huber M-estimator, computed over reliable observations only.
   - Optional extension: a learned fusion network trained on synthetic groups.
   - Provenance (which die contributed where) is stored so that every output pixel can be traced back.
5. **Uncertainty (E).** The support count, i.e. the number of reliable dies per pixel, plus the weighted dispersion of those observations. Pixels below a support threshold (e.g. fewer than 2 reliable dies) are flagged and left unreconstructed. Generative inpainting is deliberately not used for these pixels, because it can invent circuit structure.

## 3. Baselines (Objective O3)
| Baseline | Description |
| --- | --- |
| Single image | One randomly chosen registered die used as the reference |
| Mean | Pixel-wise mean of the registered dies |
| Median | Pixel-wise median of the registered dies |
| Anomaly-masked mean | Mean after removing pixels whose anomaly score exceeds a threshold |

## 4. Controlled synthetic benchmark
- Start from a clean pattern image: synthetic layouts at first, real defect-free crops later where licensing allows.
- Make N copies. Apply known sub-pixel shifts and rotations, Gaussian or Poisson noise, intensity drift and slight blur.
- Paste real defect appearances into the copies at known positions. Patches are cut out with the Carinthia-S or MVTec masks and blended (e.g. Poisson blending).
- Control the overlap between dies: how often the same location is defective in 0, 1, …, N dies. This includes "all-N" cases that simulate systematic defects.
- Because the clean image is known, the true reference, defect masks and unrecoverable regions are all exact.
- Licences: MVTec AD and AD 2 are CC BY-NC-SA 4.0 (non-commercial only). Check the Carinthia licences before redistributing any derived benchmark.

## 5. Metrics (Objective O4)
- **Fidelity:** PSNR and SSIM against the true clean reference, inside and outside defect regions.
- **Structure:** edge-map F-score (Canny or learned edges against ground-truth edges), line-width (critical-dimension proxy) error and edge-placement error on synthetic layouts.
- **Defect leakage:** the fraction of inserted-defect pixels whose reconstruction error stays above a threshold. Also measured downstream: detection AUROC and AU-PRO when each reference is used for die-to-reference comparison.
- **Registration:** mean and maximum displacement error in pixels against the known transforms.
- **Uncertainty quality:**
  - Spearman correlation between uncertainty and absolute error;
  - sparsification curves and AUSE;
  - precision and recall of flagged pixels against truly unrecoverable pixels (support 0 by construction).
- **Ablations:** number of dies (2–5), inter-die defect overlap, noise level, registration error, and reliability source (anomaly score only, cross-die deviation only, both).

## 6. What would count as evidence (from the proposal)
On held-out synthetic groups, and on real paired data if it can be obtained, the method is considered useful only if all three hold:
1. it leaks fewer defects than mean or median fusion at comparable structural fidelity;
2. it beats the single-image reference;
3. its uncertainty flags concentrate on truly unrecoverable regions.

A negative or mixed result will be reported as such.

## 7. Indicative work plan
1. Systematic literature and patent review; confirm or refocus the claimed gap.
2. Synthetic benchmark generator and baselines.
3. Registration and reliability estimation.
4. Defect-aware fusion and uncertainty; ablations.
5. Real-data validation if same-design groups become available through collaboration; write-up.
