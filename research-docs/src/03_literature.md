# C. Literature review and research gap

**Scope.** This review covers the six areas the project builds on. It is a starting point, not the systematic review that milestone L1 requires, which must also search patents and SPIE/JM3 inspection literature in a documented way. Each table summarises the objective and method, the data used, strengths and limitations, and relevance to this project. Dataset papers are covered in Section D.

## C.1 Semiconductor wafer and die defect inspection

| Work | Objective and method | Data | Strengths / limitations | Relevance |
|---|---|---|---|---|
| Dehaerne et al., systematic review [11] | Systematic review of SEM-based automatic defect inspection; 103 papers screened from four databases (Jan 2024). | Published SEM inspection studies | Broad, recent; reports that reference-based detection was the most common approach until 2020, after which deep learning dominated, especially for classification. Review only. | Confirms the place of reference-based methods and the shift to learning; entry point for L1. |
| Zontak & Cohen [14] | Defect detection in patterned wafers *without registration*: anisotropic-kernel reconstruction of the source image from a reference image; features that cannot be reconstructed from the reference are flagged. | Patterned-wafer SEM images | Handles misalignment implicitly; reference-based. Assumes the reference itself is clean. | Closest academic precedent for "reconstruct from a reference". This project instead reconstructs the *reference* from several imperfect dies. |
| Dey et al. [12] | Instance segmentation (Mask R-CNN) of SEM defects: bridges, breaks, line collapses; per-defect masks for counting and area. | SEM images of patterned resist structures | Pixel-level masks on real SEM; supervised, needs annotations. | Candidate learned defect-evidence model (Stage 2). |
| De Ridder et al., SEMI-DiffusionInst [13] | Diffusion-based detection and instance segmentation of SEM defects. | SEM defect images | Reports mAP gains over the authors' earlier work; heavier inference. | Shows diffusion used for *segmentation*, not reconstruction; a Stage-2 alternative if compute allows. |
| Taha, survey [10] | Taxonomy and experimental comparison of ML methods for wafer-defect classification. | Wafer maps | Broad comparison; classification of maps, not die images. | Background: classification is well studied. Image-level labels are not enough here (Section F.2). |
| KLA-Tencor patents [15–17] | Standard reference die from mean/median of about 5–8 dies [15]; computed reference minimising difference-image norm [16]; median unusable when systematic defects are widespread, use a verified template [17]. | Industrial wafer inspection | Show multi-die references are established industrial practice. Patents disclose claims, not reproducible benchmarks. | **Directly limits the novelty claim** (Section C.8). |

## C.2 Industrial anomaly detection and segmentation

| Work | Objective and method | Data | Strengths / limitations | Relevance |
|---|---|---|---|---|
| PatchCore, Roth et al. [18] | One-class anomaly detection and localisation: memory bank of pretrained CNN patch features from defect-free images, reduced by greedy coreset subsampling; nearest-neighbour distance gives a per-patch anomaly score. | MVTec AD and two further datasets | Strong localisation, no defect labels needed. Memory bank grows with data; scores are uncalibrated distances; backbone is pretrained on natural images. | Stage-2 defect evidence when only defect-free images exist. |
| PaDiM, Defard et al. [19] | Gaussian model of pretrained-CNN patch embeddings at each position; Mahalanobis distance as anomaly score. | MVTec AD, STC | Simple and fast; position-specific models suit *aligned* images. Needs good alignment; covariance per position costs memory. | Well matched to registered same-design images; Stage-2 baseline. |
| DRAEM, Zavrtanik et al. [20] | Reconstructive plus discriminative sub-networks trained on synthetic anomalies pasted onto normal images. | MVTec AD | Learns segmentation without real defect labels. Synthetic anomaly realism limits transfer. | Template for synthetic defect generation (Section D.6) and a learned reconstruction idea. |
| Anomalib, Akcay et al. [21] | Open-source library implementing PatchCore, PaDiM and other methods with benchmarking tools. | Several public datasets | Reproducible reference implementations. Library defaults are not tuned for SEM. | Recommended implementation source for Stage-2 baselines. |
| U-Net, Ronneberger et al. [22] | Encoder–decoder with skip connections for dense segmentation from few annotated images. | Biomedical microscopy | Strong with small datasets; needs pixel labels. | Stage-2 supervised segmentation and Stage-3 masked reconstruction backbone. |
| MVTec AD (extended), Bergmann et al. [2] | Dataset paper, plus the per-region-overlap (PRO) metric for localisation. | MVTec AD | Standard benchmark and metric. Industrial objects, not dies. | AU-PRO for segmentation evaluation (Section J.2). |

## C.3 Image registration and geometric alignment

| Work | Objective and method | Data | Strengths / limitations | Relevance |
|---|---|---|---|---|
| Zitová & Flusser [23] | Survey: area-based versus feature-based registration; four steps (features, matching, mapping model, resampling). | Survey | Standard taxonomy. Predates learned registration. | Structures the registration design (Section E, stage 3). |
| Reddy & Chatterji [28] | FFT-based registration of translation, rotation and scale (Fourier–Mellin, log-polar). | General images | Global, fast, no features needed. Sensitive to large non-overlapping content. | Coarse alignment when rotation or scale is unknown. |
| Guizar-Sicairos et al. [29] | Efficient sub-pixel translation registration by matrix-multiply DFT upsampling. | Phase-retrieval images | Accurate to a fraction of a pixel at low cost; translation only. Basis of scikit-image `phase_cross_correlation`. | Stage-1 translation registration and initialisation. |
| Evangelidis & Psarakis, ECC [27] | Iterative parametric alignment maximising the enhanced correlation coefficient; invariant to global brightness and contrast. | General images | Sub-pixel, robust to gain/offset; needs a reasonable initialisation; local optimum. Implemented as OpenCV `findTransformECC`. | Stage-1 refinement for Euclidean/affine models. |
| Lowe, SIFT [24]; Rublee et al., ORB [25] | Keypoint detection and description (SIFT: scale-invariant gradients; ORB: fast binary features). | General images | Handles large rotation or scale. Repetitive layouts produce ambiguous matches. | Coarse alignment when transforms are large and features are distinctive. |
| Fischler & Bolles, RANSAC [26] | Robust model fitting from matches containing outliers. | General | Standard outlier rejection. Fails when most matches are wrong (periodic patterns). | Pairs with SIFT/ORB. |

## C.4 Robust multi-image fusion

| Work | Objective and method | Data | Strengths / limitations | Relevance |
|---|---|---|---|---|
| Candès et al., Robust PCA [30] | Decompose a data matrix into low-rank plus sparse parts (Principal Component Pursuit) with exact-recovery guarantees under conditions. | Video surveillance, faces | Principled separation of a shared component from sparse corruptions. Needs many observations; *N* = 4–5 is very few. | Conceptual model: aligned dies ≈ shared pattern + sparse defects. |
| Peng et al., RASL [31] | Jointly solves for alignment transforms and a low-rank plus sparse decomposition of a batch of images. | Faces, digits, video frames | Unifies registration and robust fusion. Convex relaxation per iteration; assumes linearly correlated images and moderate misalignment. | **Strong baseline** for joint alignment and defect separation; compare with the staged pipeline. |
| Farsiu et al. [32] | Multi-frame super-resolution with L1 data term and robust regularisation, giving median-like fusion that resists outliers. | Video sequences | Shows the robustness of L1/median estimators to outliers and misregistration. Targets resolution, not defects. | Justifies L1/weighted-median fusion (Section G.4). |

## C.5 Masked image reconstruction and inpainting

| Work | Objective and method | Data | Strengths / limitations | Relevance |
|---|---|---|---|---|
| Telea [33] | Fast-marching inpainting propagating smooth information into holes. | General images | Simple, deterministic; blurs structure in large holes. In OpenCV. | Visual comparison only; must never be shown as recovered structure. |
| Liu et al., partial convolutions [34] | Convolutions conditioned only on valid pixels, with automatic mask update. | Natural-image benchmarks | Handles irregular masks. Learns plausible fills, not verified ones. | Masked U-Net building block for Stage 3. |
| Suvorov et al., LaMa [35] | Large-mask inpainting with fast Fourier convolutions for a global receptive field. | Natural-image benchmarks | Good at repetitive, periodic structure, which is relevant to layouts. Can hallucinate convincingly. | Candidate pretrained comparison for Stage 3, strictly flagged. |
| Lugmayr et al., RePaint [36] | Inpainting with a pretrained unconditional diffusion model, changing only the reverse sampling. | Faces and general images | Any mask shape. Stochastic; slow; outputs are samples, not estimates. | Only an optional experiment; samples could feed an uncertainty estimate. |
| He et al., masked autoencoders [37] | Self-supervised pre-training by reconstructing masked patches. | ImageNet | Learns structure from unlabelled data. Reconstructions are blurry and not meant as outputs. | Possible self-supervised pre-training on unlabelled SEM images. |

## C.6 Uncertainty estimation and hallucination control

| Work | Objective and method | Data | Strengths / limitations | Relevance |
|---|---|---|---|---|
| Kendall & Gal [38] | Separates aleatoric (data) and epistemic (model) uncertainty in dense prediction; heteroscedastic loss. | Segmentation and depth | Per-pixel uncertainty in one framework. Heteroscedastic variance can be miscalibrated. | Loss for the Stage-3 model (Section G.7). |
| Lakshminarayanan et al. [39]; Gal & Ghahramani [40] | Deep ensembles; Monte Carlo dropout as approximate Bayesian inference. | Various | Practical epistemic uncertainty. Ensembles cost *M*× compute; MC dropout often underestimates. | Uncertainty for learned stages. |
| Geifman & El-Yaniv [41] | Selective classification: abstain to guarantee risk at a chosen coverage. | Image classification | Formalises risk-coverage trade-offs. | Selective-risk and AURC metrics (Section J.2). |
| Guo et al. [42] | Modern networks are often miscalibrated; temperature scaling fixes much of it. | Image classification | Simple post-hoc calibration. | Calibrating defect probabilities $\hat p_k$. |
| Ilg et al. [43] | Uncertainty for optical flow; sparsification curves and AUSE. | Sintel, KITTI | Dense-uncertainty evaluation without calibration assumptions. | AUSE metric (Section J.2). |
| Bhadra et al. [44] | Defines and maps hallucinations in learned image reconstruction (measurement versus null-space components). | Stylised tomography | Shows learned reconstructions can add false structure. | Motivates abstention by default and hallucination checks (Section K). |

## C.7 Established methods versus the proposed contribution

**Established (not claimed).**

- Die-to-die and multi-die median references [15–17].
- Reference-based detection [11, 14].
- Supervised and one-class defect segmentation [12, 18–22].
- Translation, rigid, affine and feature-based registration [23–29].
- Low-rank plus sparse and robust fusion [30–32].
- Learned inpainting [33–37].
- Uncertainty and selective prediction [38–44].

## C.8 Research gap: stated narrowly

**What may be open.** This is a hypothesis to confirm in the systematic review. Defect *detection* and median references exist. What we have not found is a published, reproducible study that combines and evaluates all of the following:

1. same-design multi-die registration;
2. *per-image, region-level* defect and reliability estimates combining learned evidence with cross-die consistency;
3. evidence-weighted reconstruction with recorded provenance;
4. *explicit abstention and uncertainty* for regions without sufficient evidence;
5. an open benchmark with exact ground truth that measures defect leakage, structural fidelity and abstention quality.

**What would remove the gap.** Any prior work found in L1 that already does items 2–5 together. If found, the project should become a reproduction and comparison study, or narrow its focus to the benchmark or to abstention.

**Recommendation.** Present the work as a test of whether this combination helps, never as a new kind of inspection.
