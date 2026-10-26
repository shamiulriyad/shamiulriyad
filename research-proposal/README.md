# Defect-Aware Multi-Die Image Fusion for Semiconductor Reference Reconstruction

A one-page (A4) research proposal written for a university faculty member. It describes a proposed direction: the method has not been built or validated, and the figure is a conceptual example, not experimental data.

![Preview](preview.png)

| File | Use it for |
| --- | --- |
| `Defect_Aware_MultiDie_Fusion_Proposal.pdf` | The final one-page PDF. All 8 reference links are clickable, and the figure is vector. |
| `proposal.html` | Editable source for the page text and layout. |
| `make_figure.py` | Generates `figure.svg` (Fig. 1) from one layout and defect definition, so all panels stay consistent. Run `python3 research-proposal/make_figure.py` after editing it. |
| `figure.svg` | The generated figure, which `proposal.html` embeds. |
| `build.cjs` | Rebuilds the PDF and `preview.png`: `node research-proposal/build.cjs` (needs the `playwright` package). It stops with an error if the page no longer fits on one sheet. |
| `CHANGELOG.md` | What changed from version 1 and why. |
| `SCIENTIFIC_UNCERTAINTIES.md` | Facts and assumptions that still need checking. |
| `TECHNICAL_NOTES.md` | Method details, synthetic benchmark, metrics and work plan that did not fit on the page. |

## References used

1. P. Bergmann, M. Fauser, D. Sattlegger, C. Steger, "MVTec AD — A comprehensive real-world dataset for unsupervised anomaly detection," CVPR 2019, pp. 9584–9592.
   - Paper: <https://doi.org/10.1109/CVPR.2019.00982>
   - Dataset: <https://www.mvtec.com/research-teaching/datasets/mvtec-ad>
2. L. Heckler-Kram, J.-H. Neudeck, U. Scheler, R. König, C. Steger, "The MVTec AD 2 dataset: Advanced scenarios for unsupervised anomaly detection," International Journal of Computer Vision, 2026.
   - Paper: <https://doi.org/10.1007/s11263-026-02743-0>
   - Preprint: <https://arxiv.org/abs/2503.21622>
   - Dataset: <https://www.mvtec.com/research-teaching/datasets/mvtec-ad-2>
3. Two Zenodo dataset records:
   - C. Kofler, S. Strauß, A. Zernig et al., "Carinthia dataset," v2, Zenodo, 2024. <https://zenodo.org/records/10715190>
   - C. Kofler, V. Hasić, "Carinthia-S," Zenodo, 2025. <https://zenodo.org/records/16895427>
4. K. Taha, "Observational and experimental insights into machine learning-based defect classification in wafers," Journal of Intelligent Manufacturing (Springer). <https://doi.org/10.1007/s10845-024-02521-0>

See `SCIENTIFIC_UNCERTAINTIES.md` for the details of these references that could not be fully confirmed: licences, the journal volume, and dataset record identity.
