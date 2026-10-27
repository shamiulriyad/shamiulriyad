# G. Detailed algorithm, equations and pseudocode

All thresholds below are **initial values to be tuned on validation groups**. None is a proven optimum.

## G.1 Registration to a common frame

```text
procedure REGISTER_GROUP(images I[1..N], roi, model ∈ {translation, euclidean, affine})
    ref ← argmax_k quality(I[k])                 # or a design rendering, if available
    for k in 1..N:
        # 1. coarse: translation by sub-pixel phase correlation on windowed, high-passed images
        t0[k] ← phase_cross_correlation(hp(I[ref]), hp(I[k]), upsample=20)
        if model ≠ translation and rotation/scale unknown:
            (θ0, s0) ← fourier_mellin(I[ref], I[k])
        # 2. refine: ECC with the chosen motion model, initialised from step 1
        T[k] ← findTransformECC(I[ref], I[k], init=(t0, θ0, s0), model, mask=roi)
    # 3. second pass: recompute after masking likely defects (pixels with high cross-die deviation)
    D ← robust_deviation_mask(warp_all(I, T))
    for k in 1..N:
        T[k] ← findTransformECC(I[ref], I[k], init=T[k], model, mask=roi ∧ ¬D[k])
    # 4. diagnostics
    for k in 1..N:
        Ĩ[k], V[k] ← warp(I[k], T[k]), valid_mask(T[k])
        ρ[k] ← 1 − local_ncc(Ĩ[k], median_k(Ĩ), window=w)   # local residual
        c[k] ← exp(−ρ[k]² / (2 σρ²))
        if pitch_ambiguity(I[ref], T[k]) or mean(ρ[k]) > ρ_max: flag image k (exclude or review)
    return T, Ĩ, V, c
```

Notes:

- `hp` is a high-pass filter that suppresses illumination gradients.
- `pitch_ambiguity` tests whether shifting by one layout period gives a near-equal correlation peak. If so, the group needs fiducials or a design-anchored reference.
- *Initial values:* upsample factor 20 (1/20 px), window *w* = 15 px, σ_ρ = 0.2.

## G.2 Defect probabilities from each evidence source

**Cross-die robust deviation (no learning).** With registered, photometrically corrected observations $y_k(\mathbf{x})$:

$$m(\mathbf{x}) = \operatorname*{median}_{k:\,V_k(\mathbf{x})=1} y_k(\mathbf{x}), \qquad s(\mathbf{x}) = 1.4826\,\operatorname*{median}_{k}\left|y_k(\mathbf{x}) - m(\mathbf{x})\right|,$$

$$z_k(\mathbf{x}) = \frac{\left|y_k(\mathbf{x}) - m(\mathbf{x})\right|}{\max\big(s(\mathbf{x}),\, s_0\big)} .$$

What the symbols mean:

- $m$ is the per-pixel median over the dies.
- $s$ is the median absolute deviation (MAD). The factor 1.4826 makes it estimate a standard deviation for Gaussian noise.
- $s_0$ is a floor equal to the global noise level, so that flat regions (where $s \approx 0$) do not inflate $z_k$.
- $z_k$ says how many noise-units die $k$ is away from the consensus.

**Recommendation.** Compute $z_k$ on lightly smoothed images, or as a patch-level statistic, so that sub-pixel misregistration at edges is not mistaken for a defect.

**Learned evidence.** $\hat p^{\text{seg}}_k(\mathbf{x})$ from a U-Net, or an anomaly score $a_k(\mathbf{x})$ from PatchCore/PaDiM mapped to a probability by a calibration function fitted on validation data:

$$\hat p^{\text{anom}}_k(\mathbf{x}) = \sigma\!\big((a_k(\mathbf{x}) - \mu_a)/\tau_a\big),$$

where $\sigma$ is the logistic function and $\mu_a, \tau_a$ are fitted. Isotonic regression is an alternative.

**Combined defect probability.** A noisy-OR keeps the most alarming source:

$$\hat p_k(\mathbf{x}) = 1 - \big(1 - \hat p^{\text{learn}}_k(\mathbf{x})\big)\big(1 - \hat p^{\text{cons}}_k(\mathbf{x})\big), \qquad \hat p^{\text{cons}}_k(\mathbf{x}) = 1 - \exp\!\big(-z_k(\mathbf{x})^2 / 2\kappa^2\big),$$

with $\kappa$ (initial value 3) controlling how many noise-units count as "inconsistent". Small mask post-processing follows: morphological opening to remove isolated pixels, and dilation by *r* px (initial 2) so that defect borders are excluded.

## G.3 Reliability weights and support

$$w_k(\mathbf{x}) = V_k(\mathbf{x}) \cdot \big(1 - \hat p_k(\mathbf{x})\big) \cdot c_k(\mathbf{x}) \cdot q_k ,$$

- $V_k$ is image validity (0 outside the warped image);
- $1 - \hat p_k$ is the probability that the pixel is *not* defective;
- $c_k$ is local registration confidence (Section G.1);
- $q_k \in [0,1]$ is a per-image quality score from stage 1 (initial: 1 for accepted images).

Reliability states: defective if $\hat p_k \ge \tau_d$ (initial 0.5); reliable if $w_k \ge \tau_r$ (initial 0.5) and not defective; otherwise uncertain. Support $S(\mathbf{x})$ is the count of reliable observations (Section B.5).

## G.4 Robust, defect-aware fusion

Let $\mathcal{K}(\mathbf{x}) = \{k : w_k(\mathbf{x}) \ge \tau_r\}$ be the reliable dies at $\mathbf{x}$.

**Weighted median (default).**

$$\hat R(\mathbf{x}) = \operatorname*{arg\,min}_{r} \sum_{k \in \mathcal{K}(\mathbf{x})} w_k(\mathbf{x})\, \left| y_k(\mathbf{x}) - r \right| .$$

Computed by sorting the $y_k$ and taking the value where the cumulative weight first reaches half the total weight.

**Huber M-estimator (variant).** Solved by iteratively reweighted least squares starting from the weighted median:

$$\hat R(\mathbf{x}) = \operatorname*{arg\,min}_{r} \sum_{k \in \mathcal{K}(\mathbf{x})} w_k(\mathbf{x})\, \rho_\delta\big(y_k(\mathbf{x}) - r\big), \qquad \rho_\delta(u) = \begin{cases} \tfrac12 u^2 & |u| \le \delta \\ \delta\,(|u| - \tfrac12 \delta) & |u| > \delta \end{cases}$$

with $\delta = 1.345\,s_0$ as an initial value. That is the classical tuning constant for 95% efficiency under Gaussian noise.

**Weighted mean** (only for comparison):

$$\hat R(\mathbf{x}) = \frac{\sum_{k \in \mathcal{K}} w_k y_k}{\sum_{k \in \mathcal{K}} w_k} .$$

**Why the pixel-wise median is not universally valid.**

1. *Residual misregistration.* If die $k$ is shifted by $\delta_k$, a sharp edge appears at different positions. The pixel-wise median places the edge near the median shift only when a majority agree. With $N = 4$ the median averages the two middle values, which blurs edges, and a mean blurs further.
2. *Mixing of distinct structures.* If reliable dies show genuinely different local structures (e.g. a one-pitch misregistration, or a design variant), choosing the median independently per pixel can stitch pieces of different structures into a pattern that exists in no die.
3. *Breakdown.* At 50% or more defective observations the median follows the defects.
4. *Photometric seams.* With imperfect gain correction, the median may switch source die from pixel to pixel, adding texture-like noise.

**Structure-aware safeguard.** Partition $\Omega$ into regions $r$: tiles of 16–32 px, or superpixels of $m(\mathbf{x})$. For each region, measure structural disagreement among reliable dies, $E_r$ (e.g. mean pairwise edge-map distance). If $E_r > \tau_e$:

- select one source $k^\star_r = \arg\max_k \frac{1}{|r|}\sum_{\mathbf{x}\in r} w_k(\mathbf{x})$;
- copy $y_{k^\star_r}$ into the region with feathered blending at the boundary;
- record the source in the provenance map;
- raise $U$ in that region.

```text
procedure FUSE(y[1..N], w[1..N], regions, τr, s_min)
    for each pixel x:
        K ← {k : w[k](x) ≥ τr}
        S(x) ← |K|
        if S(x) ≥ s_min:  R̂(x) ← weighted_median({y[k](x)}_{k∈K}, {w[k](x)}_{k∈K})
        else:             R̂(x) ← NaN                        # handled in G.5, never filled here
        provenance(x) ← bitmask(K)
    for each region r with S ≥ s_min on most pixels:
        if structural_disagreement(r, K) > τe:
            k* ← argmax_k mean_{x∈r} w[k](x)
            R̂|r ← feather_blend(R̂|r, y[k*]|r);  provenance|r ← {k*};  flag_region(r)
    return R̂, S, provenance, flagged_regions
```

## G.5 Pixels without reliable evidence, uncertainty and abstention

**Effective sample size and weighted spread.**

$$n_{\text{eff}}(\mathbf{x}) = \frac{\big(\sum_{k\in\mathcal{K}} w_k\big)^2}{\sum_{k\in\mathcal{K}} w_k^2}, \qquad \hat\sigma^2(\mathbf{x}) = \frac{\sum_{k\in\mathcal{K}} w_k \big(y_k - \hat R\big)^2}{\sum_{k\in\mathcal{K}} w_k} .$$

$n_\text{eff}$ is how many "full" observations the weights amount to. It equals $|\mathcal{K}|$ when all weights are equal and is smaller when one die dominates. $\hat\sigma^2$ is the spread of the reliable observations around the estimate.

**Approximate standard error.** This is exact for a weighted mean with independent noise. For a median it is approximate and should be checked by bootstrap on validation groups.

$$\mathrm{SE}(\mathbf{x}) = \sqrt{\frac{\max\big(\hat\sigma^2(\mathbf{x}),\, s_0^2\big)}{n_{\text{eff}}(\mathbf{x})}} .$$

**Uncertainty map.** $U = \mathrm{SE}/s_0$ (in noise units) for supported pixels; $U = +\infty$ (displayed as "unsupported") where $S < s_{\min}$; and $U \leftarrow \max(U, u_\text{flag})$ in structurally flagged regions.

**Abstention mask.**

$$A(\mathbf{x}) = \mathbb{1}\big[S(\mathbf{x}) < s_{\min}\big] \;\lor\; \mathbb{1}\big[\mathrm{SE}(\mathbf{x}) > \tau_u\big] \;\lor\; \mathbb{1}\big[\mathbf{x} \in \text{flagged region with no single reliable source}\big] .$$

Initial values are $s_{\min} = 2$ and $\tau_u = 2\,s_0$:

- $s_{\min} = 1$ would accept a single unchecked observation;
- $s_{\min} = 2$ requires two dies to agree;
- the ablation tests 1, 2 and 3.

```text
procedure ABSTAIN_AND_UNCERTAINTY(R̂, y, w, S, flagged, s_min, τu)
    for each pixel x:
        if S(x) < s_min:            A(x) ← 1; U(x) ← ∞; R̂(x) ← NaN; continue
        n_eff ← (Σ w)² / Σ w²;  σ̂² ← Σ w (y − R̂(x))² / Σ w
        SE ← sqrt(max(σ̂², s0²) / n_eff);  U(x) ← SE / s0
        if flagged(x):              U(x) ← max(U(x), u_flag)
        A(x) ← (SE > τu)
        if A(x): R̂(x) ← NaN
    return U, A                     # A is exported unchanged; no later stage may clear it silently
```

## G.6 Running reconstruction only when appropriate

```text
procedure OPTIONAL_FILL(R̂, A, y, w, model, validated: bool)
    if not validated: return R̂, F = 0                    # default: leave NaN, keep A
    candidates ← {x : A(x) = 1 and S(x) ≥ 1 and hole_size(x) ≤ h_max}
    if candidates = ∅: return R̂, F = 0
    R̃, b ← model(stack(y, w), mask = A)                  # prediction and predicted scale b
    for x in candidates:
        R̂(x) ← R̃(x);  F(x) ← 1;  U(x) ← max(U(x), b(x)/s0, u_model)   # stays high
    # Systematic-defect pixels (S(x) = 0) are never filled, so A(x) stays 1
    return R̂, F
```

The model is "validated" only if, on held-out *designs*, it meets every one of these conditions:

- it beats leaving the hole empty on the agreed error metric;
- its hallucination rate (Section K) is below a pre-set limit agreed with the supervisor;
- its predicted scale $b$ is calibrated: AUSE better than random ordering.

## G.7 Training losses

**Segmentation (U-Net).** Binary cross-entropy plus Dice, with predicted probability $p$ and ground truth $g$ over pixels $i$:

$$\mathcal{L}_{\text{seg}} = -\frac{1}{|\Omega|}\sum_i \big[g_i \log p_i + (1-g_i)\log(1-p_i)\big] \;+\; \Big(1 - \frac{2\sum_i p_i g_i + \epsilon}{\sum_i p_i + \sum_i g_i + \epsilon}\Big),$$

with $\epsilon = 1$ for stability. Dice counteracts the small fraction of defect pixels.

**Masked reconstruction (optional Stage 3).** The network predicts $\tilde R$ and a per-pixel Laplace scale $b > 0$, giving a heteroscedastic loss [38], plus gradient and SSIM terms over training pixels $\Omega_t$ (holes weighted by $\lambda_h$):

$$\mathcal{L}_{\text{rec}} = \frac{1}{|\Omega_t|}\sum_{\mathbf{x}\in\Omega_t} \omega(\mathbf{x}) \Big[\frac{|\tilde R(\mathbf{x}) - R(\mathbf{x})|}{b(\mathbf{x})} + \log b(\mathbf{x})\Big] + \lambda_g \big\|\nabla \tilde R - \nabla R\big\|_1 + \lambda_s \big(1 - \mathrm{SSIM}(\tilde R, R)\big),$$

with $\omega(\mathbf{x}) = \lambda_h$ inside simulated holes and 1 elsewhere. *Initial values:* $\lambda_h = 4$, $\lambda_g = 0.5$, $\lambda_s = 0.2$. The first term penalises error relative to the predicted scale and stops the network from shrinking $b$ everywhere. The gradient term protects edges. SSIM protects local structure [45].
