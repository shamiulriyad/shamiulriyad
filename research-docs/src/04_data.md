# D. Dataset investigation and data strategy

## D.1 Summary

**Fact.** None of the investigated public datasets contains groups of same-design die images with complementary defects *and* a clean reference of the same die. None therefore supports direct evaluation of registration plus reconstruction against ground truth.

The public data is useful for two things:

1. **training and calibrating defect evidence** (segmentation and anomaly scoring);
2. **supplying realistic defect appearances** for a synthetic benchmark.

![Figure 1. Dataset suitability for each requirement of the task. Public datasets above the dashed line are rated from their providers' descriptions; rows below are the planned data levels. Schematic table, not experimental data.](figures/fig3_datasets.svg){#fig:datasets width=100%}

## D.2 Public datasets investigated

Sources: providers' pages and papers [1–9], read through search-result quotations (see Appendix N.1). "Third-party" marks details found only in secondary listings.

| Dataset | What it contains | Patterned dies? | Same-design groups / clean ref.? | Direct evaluation of alignment or reconstruction? | Access and licence | Suitability |
|---|---|---|---|---|---|---|
| **Carinthia** [4] (Zenodo 10715190, v2, 2024) | 4,591 grayscale SEM images of defects from one production layer; 6 classes; CSV with image path and label (image-level labels). | No: described as *unstructured* wafers. | No / No | No | Open download from Zenodo. Licence **not verified**; record also reported under another DOI (concept vs. version). | Real SEM defect appearance; classification pre-training. |
| **Carinthia-S** [5] (Zenodo 16895427, 2025) | Same 4,591 images with binary segmentation masks; CSV maps image, mask and label. Third-party: 480×480 px, class 6 = "no visible defect" incl. misaligned captures, some masks anti-aliased. | No | No / No | No | Open download; **CC BY 4.0 according to third-party listings** (confirm on record). | Best public source of *real SEM defect masks* for cut-and-paste synthesis and U-Net training. |
| **MVTec AD** [1, 2] | 5,354 high-resolution colour images, 15 object and texture categories, >70 defect types; defect-free training set; pixel-precise anomaly masks. | No (industrial objects/textures) | No / No (defect-free images are other instances) | No | Official download; **CC BY-NC-SA 4.0**, non-commercial. | Anomaly-detection baselines; defect masks for synthesis; not die imagery. |
| **MVTec AD 2** [3] | >8,000 high-resolution images, 8 scenarios incl. lighting changes, transparent and overlapping objects, very small defects; public test set with masks plus a private test set (ground truth withheld, evaluation server). | No | No / No | No | Official download; **CC BY-NC-SA 4.0**. | Robustness to lighting; small-defect behaviour. |
| **KolektorSDD2** [6] | 3,335 images (356 with visible defects, 2,979 defect-free), about 230×630 px, from production items captured in a controlled industrial setting; pixel-level defect annotations. | No (surface images) | No / No | No | Download from ViCoS; **CC BY-NC-SA 4.0** per the ViCoS page (a mirror lists CC BY-SA, so use the ViCoS terms); commercial use by agreement. | Mixed and weak supervision; surface-defect segmentation. |
| **VisA**, PCB subsets [7] | 10,821 images (9,621 normal, 1,200 anomalous) in 12 subsets, 4 of them printed circuit boards; pixel masks. | **Partly**: PCB boards of one design are patterned, but not semiconductor dies. | Partial: many instances of the same PCB design; not paired, not aligned / No | Partly, as a proxy: groups of normal boards can be registered, but the boards are physically different instances. | GitHub release; **licence conflicting** (CC BY 4.0 in the repository vs CC BY-NC-SA 4.0 in Anomalib docs). | Best public *patterned same-design proxy*; useful to test registration on real repeated layouts. |
| **WM-811K** [8] | 811,457 wafer maps (die-level categorical grids); a labelled subset with failure-pattern classes (secondary sources: about 172,950 labelled). | No (maps, not images) | No / No | No | Widely mirrored; licence unclear. | Not usable for reconstruction (scenario S4). |
| **MixedWM38** [9] | More than 38,000 wafer maps with 1 normal, 8 single and 29 mixed defect patterns. | No (maps) | No / No | No | IEEE DataPort; licence unclear. | Not usable for reconstruction (S4). |

**Other semiconductor literature.** The SEM studies [11–13] use proprietary or partner data; most are not public. The systematic review [11] should be used in L1 to search for any public patterned-die SEM data.

## D.3 Data plan: three levels

**Level 1: public data for defect evidence (pre-training and baselines).**

- Carinthia-S masks → supervised U-Net defect segmentation on real SEM texture (unpatterned background).
- MVTec AD, MVTec AD 2, KolektorSDD2 → PatchCore/PaDiM baselines and segmentation pre-training.
- VisA PCB → registration and fusion sanity checks on real repeated layouts.

None of these is used as reconstruction ground truth.

**Level 2: controlled synthetic benchmark (main quantitative evaluation).** Groups are generated from known clean references, so $R$, $M_k$, $\mathbf{T}_k$ and the unrecoverable set $Z$ are known exactly (Section D.4).

**Level 3: real same-design die groups (external validity).** Real SEM or optical images of 4–5 dies of the same design and layer, ideally with a verified clean reference: a die confirmed defect-free by review, a design-rendered image, or a high-dose re-scan. These are obtained through a university fab, laboratory or industry partner under a data agreement. **Without Level 3, the project cannot claim real-world validity** (Section J.6).

## D.4 Synthetic benchmark design (Level 2)

**Clean references.** Three sources are planned:

- (a) procedurally generated layouts (lines, vias, contacts, pads) rendered with an SEM-like appearance model: edge brightening, blur, shot-like noise;
- (b) defect-free crops of real patterned images where licensing allows (e.g. VisA PCB normal images, *only* as a proxy);
- (c) Level-3 verified references when available.

**Group generation** (all parameters drawn from seeded distributions and logged):

1. Choose a clean reference $R$ and $N \in \{2,\dots,5\}$.
2. For each die $k$, sample a transform $\mathbf{T}_k$:
   - translation up to a few pixels to tens of pixels;
   - rotation within ±θ_max;
   - scale within $1 \pm s_\text{max}$;
   - optional smooth distortion $\mathbf{u}$.
3. Sample a photometric map $g_k$ (gain, offset, slow illumination gradient) and noise $\varepsilon_k$ (Gaussian plus Poisson-like; optional blur).
4. Sample defects: type, size, count and location, under a **controlled overlap** policy:
   - *independent* (random positions);
   - *pairwise overlap* at a set rate;
   - *all-N* (the same location in every die, simulating systematic or mask-level defects).
5. Insert defects. Defect appearances are cut from Carinthia-S or MVTec masks and blended (alpha or Poisson blending), or drawn procedurally (bridge, open, particle, scratch, residue).
6. Render $I_k$ by applying $g_k$, $\mathbf{T}_k^{-1}$, defects and noise. Store $R$, $M_k$, $\mathbf{T}_k$, all parameters and the derived $Z = \{\mathbf{x} : \sum_k (1 - M_k(\mathbf{x})) < s_{\min}\}$.

**Realism controls.**

- Compare intensity histograms, noise power spectra and edge profiles of synthetic images with real SEM images (Carinthia, and Level 3 when available).
- Report every metric separately for procedural versus cut-and-paste defects.
- **Synthetic results are never reported as real-world performance.**

## D.5 Annotation requirements (Level 3 and any real masks)

| Item | Requirement |
|---|---|
| Defect masks | Polygon or pixel masks per die; class label; annotator ID; confidence (certain / probable / unsure). |
| Clean reference | Source (reviewed die, design rendering, re-scan); reviewer; date; known caveats. |
| Correspondence | Die IDs, wafer, lot, layer, tool, recipe, magnification, timestamp. |
| Registration truth | Optional fiducial points (≥ 4 per image) for target-registration error on real data. |
| Format | PNG/TIFF images (16-bit if available), PNG masks, one JSON or CSV manifest per group with SHA-256 hashes. |

**Quality control.**

- Double annotation of at least a random subset, reporting inter-annotator IoU.
- Adjudication of disagreements.
- An "unsure" class that is excluded from precision and recall but reported separately.
- Periodic audit of 5–10% of masks.

## D.6 Splits and leakage prevention

**Recommendation.** Split by **design or reference identity and acquisition group**, never by individual image.

- **Synthetic data.** Each clean reference (layout) belongs to exactly one split: train, validation or test. All groups generated from one reference stay in that split. The test split also holds out at least one *layout family* never seen in training, to measure generalisation.
- **Real data.** Split by wafer or lot and, where possible, by layer or design. Never place dies from the same wafer region in both train and test. Near-duplicate images (re-scans, overlapping fields of view) are clustered by perceptual hash and kept in one split.
- **Public datasets.** Keep providers' official train/test splits; never tune thresholds on test images.
- **Thresholds and hyper-parameters** ($\tau_d$, $\tau_r$, $s_{\min}$, $\kappa$) are chosen on validation groups only, then frozen before test evaluation.
- **Manifest hashing.** Every split is defined by a versioned manifest of file hashes; the evaluation script refuses to run if a test hash appears in the training manifest.
