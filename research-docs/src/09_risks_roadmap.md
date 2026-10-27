# K. Risk analysis and limitations

| Risk | Effect | Detection | Mitigation |
|---|---|---|---|
| **Repeated defects at the same location** (systematic, mask/reticle-level) | Unrecoverable from images; undetected cases pass silently into $\hat R$ | SPR on synthetic all-N cases; on real data only via design data or a golden die | Abstain where learned evidence flags all dies; compare with design rendering or verified golden image where possible [17]; report SPR prominently |
| **Incorrect registration** (incl. one-pitch shifts) | Blurred edges, mixed structures, false defect flags | Residual maps, pitch-ambiguity test, TRE on synthetic | Least flexible model; defect-masked second pass; fiducials or design anchoring; reject images above a residual limit |
| **False-positive defect masks** | Good evidence discarded; lower support; more abstention | Precision on annotated data; coverage drop | Calibrate on validation; require consistency *and* learned evidence for exclusion where support is low |
| **False-negative masks** | Defects leak into $\hat R$ | DLR | Noisy-OR combination; dilation; ensembles |
| **Missing circuit structures** (feature absent in all reliable dies due to a shared defect, or occluded) | Reference lacks a real feature; silent if undetected | Edge recall; comparison with design | Same as repeated defects; never "complete" structures from priors without flagging |
| **Texture and illumination variation** (charging, detector differences) | Photometric model fails; spurious deviations | Residual statistics after normalisation | Robust gain/offset; local normalisation only if validated; ablation |
| **False confidence and hallucination** | Plausible but wrong patterns trusted | Hallucination tests (below); AUSE | Abstain by default; learned fill flagged in $F$; never shown as verified |
| **Dataset domain shift** | Learned detectors underperform on target SEM | Performance gap between sources | Fine-tune on target data; report per-source metrics |
| **Synthetic-to-real gap** | Benchmark results do not transfer | Level-3 comparison; realism statistics | Present synthetic results as such; prioritise Level-3 acquisition |
| **Licensing and confidentiality** | Legal or contractual breach; unpublishable results | Licence register per dataset and patch | Respect NC licences (MVTec, KolektorSDD2); NDA for partner data; publish only aggregate metrics or approved images; keep partner data off public repositories |

**Hallucination checks for any learned fill.**

1. *Known-truth test:* on held-out designs, compare the fill with $R$ inside holes. Count *hallucinated edges*: edges in the fill farther than $r_t$ from any true edge, per unit area.
2. *Counterfactual test:* change the hidden content (e.g. remove a via in $R$ under the hole). A trustworthy model should not confidently restore the via.
3. *Context-swap test:* fill the same hole with context from a different design. Similar fills indicate the model is copying priors, not evidence.
4. *Design comparison:* where layout data exists, compare fills with the design rendering.

**Rule.** Uncertain regions stay explicitly marked in every output, figure and report. A plausible but unverified pattern is never shown without its flag.

# L. Implementation roadmap

**Effort assumptions.** One researcher at about 0.8 full-time equivalent, with Python and PyTorch experience, access to the entry-level GPU configuration, and public datasets downloadable at the start. Level-3 data depends on a partner and is *not* on the critical path. Estimates are in person-weeks and are planning figures, not commitments. No calendar dates are given, because the start date and partner timelines are unknown.

| Milestone | Deliverables | Depends on | Acceptance criteria (process-based) | Effort |
|---|---|---|---|---|
| **L1. Literature review and dataset audit** | Systematic review protocol and log (incl. patents); dataset cards with verified licences; refined gap statement | — | Search strings, databases and screening counts documented; every dataset fact linked to the official record; gap statement revised or confirmed | 3–4 |
| **L2. Data preparation and synthetic benchmark** | Generator v1 with seeds; defect library with provenance; split manifests; realism report | L1 | Same seed regenerates identical groups (hash check); splits by design with no hash overlap; realism statistics reported | 3–5 |
| **L3. Registration baseline** | Phase correlation + ECC module; diagnostics; tests | L2 | Recovers synthetic transforms with TRE reported for each test level; unit tests pass; failure cases logged | 2–3 |
| **L4. Defect-mask and fusion baseline** | Cross-die z-score; weights; weighted-median fusion; abstention; M1–M3 results | L3 | Full pipeline runs end to end on test groups; all Section J metrics computed with coverage; deterministic re-run | 3–4 |
| **L5. Learned model experiments** | U-Net, PatchCore/PaDiM evidence; calibration; optional masked U-Net (M4) with hallucination tests | L4 | Trained on train designs only; calibration on validation; H3 ablation complete; M4 enabled only if Section G.6 criteria are met | 4–6 |
| **L6. Evaluation and ablation** | All Section J.5 ablations; statistics; failure gallery; RASL baseline | L4 (L5 for learned rows) | Pre-registered primary metrics reported with CIs; every ablation level has ≥ the planned number of groups | 3–4 |
| **L7. Final report and demonstration** | Paper/report, slides, demo notebook, released code and benchmark (where licences allow) | L6 | Results reproducible from the repository by a second person; limitations section complete | 2–3 |
| (Parallel) **Level-3 data acquisition** | Data agreement; real groups; annotations | Partner | Annotation QC (Section D.5) passed | Partner-dependent |

**Total for L1–L7:** about 20–29 person-weeks, plus partner-dependent real-data work and writing time for any publication.

# M. Expected outputs

| Output | Content | Form |
|---|---|---|
| Research proposal | One-page faculty proposal and this document | PDF, DOCX, Markdown sources |
| Dataset audit | Dataset cards, licence register, suitability matrix (Figure 1), verification log | Markdown + CSV |
| Reproducible code repository | Modules for stages 1–9; configs; tests; lock file; Dockerfile; generator | Git repository |
| Trained checkpoints (if feasible) | U-Net, PatchCore memory banks, optional reconstruction model, each with training config and data-manifest hash | Files + model cards |
| Evaluation scripts | Metric implementations (Section J) with unit tests on toy cases with known answers | Python package + CLI |
| Qualitative and quantitative results | Metric tables with CIs; ablation curves; failure gallery, synthetic and real reported separately | Report figures, CSV |
| Limitations and future work | What was not validated (Section J.6); open questions (one-page summary) | Report section |
| Final paper/report and presentation | Written report; slides; optional short animation (Appendix N.6) | PDF, PPTX |

**Not an output:** any claim of physical die repair, electrical functionality, or real-world accuracy without Level-3 data.
