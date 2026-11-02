# Research problem definition (Artifact 1)

**Sample-Guided Semiconductor Wafer Die Inspection: Few-Shot, Rotation-Robust Anomaly Detection, Localisation and Verified Feedback Adaptation**

## Informal statement

Given a small set of reference die images from one product (and, optionally, a few verified defect examples), build an inspector that, for any new die of the same product, possibly from another wafer and in any orientation, outputs:

- whether the die is normal, contains a known defect type, or contains an unknown anomaly;
- where the abnormal regions are, how large they are and how severe they are;
- how confident it is.

It must improve over time from engineer-verified feedback, without retraining the network and without getting worse on cases it already handled.

## Formal definition

Let

- `R = {r_1, …, r_K}` be K normal reference images of die type `d`;
- `D = {(x_j, c_j)}` be an optional small set of verified defect images with labels `c_j ∈ C_known`;
- a target die image `x ∈ R^(H×W)` be observed as `x = g(T(x*))`, where:
  - `x*` is the die in canonical pose;
  - `T` is an unknown geometric transform (rotation θ, translation t, scale s);
  - `g` is an unknown photometric change.

Learn, **without updating encoder weights**, a function

```
F(x; R, D) → ( S ∈ R^(H×W),  A ∈ R,  y ∈ {normal, known:c, unknown},  u ∈ [0, 1] )
```

where

- `S` is a pixel anomaly map in the coordinates of `x`;
- `A` is an image anomaly score;
- `y` is the triage decision;
- `u` is a confidence.

`F` must meet three requirements:

1. Its decisions are invariant to `T` and `g` within stated ranges.
2. It never assigns a region that lies outside all known classes to a known class with high confidence.
3. It admits an update operator `M_(t+1) = U(M_t, verified feedback)` that does not reduce performance on a held-out set.

Performance is evaluated separately for target dies from the **same wafer**, from **other wafers** of the same design, and from **other die types**.

## Scope

**In scope:**

- visual anomaly detection and localisation on die images;
- geometric and photometric robustness;
- known/unknown triage;
- memory-based feedback adaptation;
- optional wafer-level aggregation.

**Out of scope:**

- root-cause analysis;
- electrical failure prediction;
- production deployment, user interfaces and tool integration.

See Section 6 of `Sample_Guided_Die_Inspection_Research_Dossier.pdf` for the full discussion.
