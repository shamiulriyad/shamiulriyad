# B. Problem formulation

## B.1 Scenarios that must not be confused

| Scenario | What the images are | Addressed here? |
|---|---|---|
| **S1. Same-design dies, complementary defects** | Images of *different physical dies* printed from the same design (same layer, same process step), taken with the same tool settings. Random defects differ between dies. | **Yes. This is the target scenario.** |
| S2. Multiple views of one physical die | Repeated images of the *same* die (re-scans, frame averaging, multiple detectors). A defect appears in every view. | No. Fusion would reproduce the defect. S2 helps only with noise, not defects. |
| S3. Different lighting or imaging conditions | Same or different dies under different illumination, detector, beam energy or focus. | Only as a nuisance variable inside S1 (Section B.6). Strong changes break the shared-appearance assumption. |
| S4. Wafer maps | Grids of categorical labels per die (for example pass/fail or failure-pattern class), as in WM-811K [8] and MixedWM38 [9]. | No. Wafer maps contain no die-surface images, so nothing can be reconstructed from them. |

**Assumptions for S1.** The method is only valid under the following conditions:

- **A1:** all dies share one intended layout in the region of interest (ROI).
- **A2:** the images come from the same layer and process step, with the same nominal magnification and detector.
- **A3:** at most locations, the majority of dies are defect-free; defects are not systematically co-located.
- **A4:** geometric differences between images can be modelled by a low-dimensional transform plus small residual distortion.
- **A5:** appearance differences between dies are mostly a global gain and offset plus noise.

When A3 fails locally (repeated defects), the correct output is abstention, not reconstruction.

## B.2 Notation

| Symbol | Plain-English meaning |
|---|---|
| $N$ | Number of images in a group (planned: 4–5; ablated: 2–5). |
| $k = 1,\dots,N$ | Index of an image (one die). |
| $\Omega \subset \mathbb{Z}^2$ | Pixel grid of the common reference frame (the ROI). |
| $\mathbf{x} \in \Omega$ | A pixel position in that frame. |
| $I_k$ | Raw image of die $k$, defined on its own grid $\Omega_k$. |
| $R(\mathbf{x})$ | The unknown clean reference: the intended pattern as this tool would image it. |
| $\mathbf{T}_k$ | Geometric transform mapping reference coordinates to image-$k$ coordinates. |
| $g_k$ | Photometric map for image $k$ (brightness and contrast). |
| $M_k(\mathbf{x}) \in \{0,1\}$ | True defect mask of die $k$ (1 = defective). Unknown in real data. |
| $D_k(\mathbf{x})$ | Appearance of the defect where $M_k = 1$. |
| $\varepsilon_k(\mathbf{x})$ | Noise. |

## B.3 Observation model

$$
I_k\big(\mathbf{T}_k(\mathbf{x})\big) \;=\; \big(1 - M_k(\mathbf{x})\big)\, g_k\big(R(\mathbf{x})\big) \;+\; M_k(\mathbf{x})\, D_k(\mathbf{x}) \;+\; \varepsilon_k(\mathbf{x}), \qquad \mathbf{x} \in \Omega .
$$

In words, at every reference position die $k$ shows either the intended pattern (after a brightness and contrast change $g_k$) or a defect, plus noise. The baseline photometric model is affine, $g_k(r) = a_k r + b_k$ with gain $a_k > 0$ and offset $b_k$. **Assumption.** Charging, edge effects and detector non-linearity in SEM images can violate this model; that is tested as a nuisance factor.

## B.4 Registration transformations

Registration estimates $\hat{\mathbf{T}}_k$ for each image. The candidate families, from most to least constrained, are:

| Family | Form | Degrees of freedom | When to use |
|---|---|---|---|
| Translation | $\mathbf{T}(\mathbf{x}) = \mathbf{x} + \mathbf{t}$ | 2 | Stage-aligned images, same magnification |
| Euclidean (rigid) | $\mathbf{T}(\mathbf{x}) = \mathbf{R}_\theta \mathbf{x} + \mathbf{t}$ | 3 | Small rotations |
| Similarity | $\mathbf{T}(\mathbf{x}) = s\,\mathbf{R}_\theta \mathbf{x} + \mathbf{t}$ | 4 | Rotation plus magnification drift |
| Affine | $\mathbf{T}(\mathbf{x}) = \mathbf{A}\mathbf{x} + \mathbf{t}$ | 6 | Shear or anisotropic scale (e.g. scan distortion) |
| Residual field | $\mathbf{T}(\mathbf{x}) = \mathbf{A}\mathbf{x} + \mathbf{t} + \mathbf{u}(\mathbf{x})$ | dense | Small non-rigid distortion (optional, regularised) |

Here $\mathbf{R}_\theta$ is a 2-D rotation by angle $\theta$, $s$ is a scale factor, $\mathbf{A}$ is a 2×2 matrix and $\mathbf{u}$ is a smooth displacement field.

**Recommendation.** Use the least flexible family that explains the data. Extra freedom lets the registration "explain away" real defects.

The **registered image** is $\tilde{I}_k(\mathbf{x}) = I_k(\hat{\mathbf{T}}_k(\mathbf{x}))$, computed by bilinear or bicubic interpolation. A validity mask $V_k(\mathbf{x}) \in \{0,1\}$ marks pixels whose source position lies inside image $k$.

**Photometric correction** puts all images on a common scale:

$$y_k(\mathbf{x}) = \big(\tilde{I}_k(\mathbf{x}) - \hat b_k\big) / \hat a_k ,$$

where $\hat a_k, \hat b_k$ are fitted robustly (for example by least trimmed squares against the group median), so that defects do not bias the fit.

## B.5 Defect masks, reliability and the three states

For every image and pixel the system estimates the following quantities:

- **Defect probability** $\hat p_k(\mathbf{x}) \in [0,1]$: from a segmentation network, or from a calibrated anomaly score (Section G.2).
- **Reliability weight** $w_k(\mathbf{x}) \in [0,1]$: how much observation $y_k(\mathbf{x})$ should count in fusion. It combines defect probability, cross-die consistency, registration confidence and validity (Section G.3).
- **State**, for display and counting only:
  - *defective* if $\hat p_k(\mathbf{x}) \ge \tau_d$;
  - *reliable* if $w_k(\mathbf{x}) \ge \tau_r$ and not defective;
  - *uncertain* otherwise.

**These are estimates.** In real data the true mask $M_k$ is unknown, so a high anomaly score is evidence of a defect, not a confirmed defect.

**Support** is the number of reliable observations at a pixel:

$$S(\mathbf{x}) = \sum_{k=1}^{N} \mathbb{1}\big[w_k(\mathbf{x}) \ge \tau_r\big].$$

## B.6 Fusion function and outputs

A **fusion function** $F$ maps the stack of observations and weights to an estimate:

$$\hat R(\mathbf{x}) = F\big(\{y_k(\mathbf{x}), w_k(\mathbf{x})\}_{k=1}^{N}\big), \quad \text{defined only where } \mathbf{x} \notin A .$$

The **abstention mask** $A(\mathbf{x}) \in \{0,1\}$ marks pixels where no trustworthy estimate exists, for example $S(\mathbf{x}) < s_{\min}$. At those pixels $\hat R$ is stored as "not a number" (NaN) and is never silently filled.

The **uncertainty map** $U(\mathbf{x}) \ge 0$ summarises how unreliable $\hat R(\mathbf{x})$ is, from the support and the spread of the reliable observations (Section G.5).

The deliverables per group are:

- $\hat R$;
- $\{\hat p_k, w_k\}$;
- $S$, $U$ and $A$;
- a **provenance map** recording which dies contributed to each pixel;
- an evaluation record.

## B.7 What the formulation implies

- **Fact (from the model).** Where every die is defective at $\mathbf{x}$, no observation carries information about $R(\mathbf{x})$, so the reference there is unidentifiable from the images alone. Only external information (a verified golden die or design data) can resolve it.
- **Fact (robust statistics).** The pixel-wise median has a 50% breakdown point. If half or more of the observations at a pixel are defective, the median can be arbitrarily wrong. With $N = 4$, two coinciding defects already reach that limit.
- **Hypothesis.** Learned defect evidence can identify defective observations even when they are the majority at a pixel, which pure cross-die statistics cannot. This is tested in the overlap ablation (Section J.5).
