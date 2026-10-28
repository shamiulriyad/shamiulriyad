# Implications of Advanced Statistics in Business and Research

A 16:9 university presentation in three versions: a **6-slide deck** that keeps every topic of the full deck with less text, a **short deck (title + 5 slides)** and a full 8-slide deck with a supplementary reference slide.

| File | Use it for |
| --- | --- |
| `Advanced_Statistics_Presentation_6_Slides.pptx` | **Recommended:** the full deck's topics on 6 uncluttered slides. Each slide has a short spoken explanation in its speaker notes. |
| `Advanced_Statistics_Presentation_6_Slides.pdf` | PDF copy of the 6-slide version. |
| `Advanced_Statistics_Short_Presentation.pptx` | **Short version:** a title slide plus 5 content slides, with little text. Each slide has a short spoken explanation in its speaker notes. |
| `Advanced_Statistics_Short_Presentation.pdf` | PDF copy of the short version. |
| `Advanced_Statistics_Presentation.pptx` | The editable deck: PowerPoint, Keynote or Google Slides. Speaker notes on every slide hold the full explanations and calculations. |
| `Advanced_Statistics_Presentation.pdf` | A quick-review copy with all animated content shown. |
| `build/` | Scripts that rebuild the deck (`build.sh`). |

## 6-slide version

| # | Slide | What it says |
| --- | --- | --- |
| 1 | Title | Topic, team members, course details |
| 2 | Why it matters & key methods | Data → description → prediction → inference → decision; six methods in one line each; 5–6% productivity evidence |
| 3 | Business & research implications | Business uses + Bing A/B test (+12% revenue); research uses + RECOVERY trial (deaths 41.4% → 29.3%) |
| 4 | A/B test case (**illustrative data**) | 4.20% vs 4.80%; +0.60 pp, 95% CI +0.19 to +1.01 pp, p = 0.004; launch B |
| 5 | Challenges & ethics | Six risks in one line each; five-step responsible practice |
| 6 | Conclusion | Four takeaways, closing quote, key references |

## Short version (title + 5 slides)

| # | Slide | What it says |
| --- | --- | --- |
| 1 | Title | Topic, team members, course details |
| 2 | Statistics turns data into decisions | Data → patterns → uncertainty → decision; four key methods (regression, hypothesis testing, forecasting, A/B testing) |
| 3 | Better decisions in business and research | Four uses in each field, plus two real cases: Bing A/B test (+12% revenue) and the RECOVERY trial (deaths 41.4% → 29.3% in ventilated patients) |
| 4 | A/B test case (**illustrative data**) | Old page 4.20% vs new page 4.80%; difference +0.60 pp, 95% CI +0.19 to +1.01 pp, p = 0.004; decision: launch B |
| 5 | Challenges | Four cautions (biased data, correlation ≠ causation, significant ≠ important, privacy & fairness) and a note on AI |
| 6 | Conclusion | Three takeaways, closing quote, thank you, key references |

Team and course details are edited the same way as in the full version (see below).

## Full version: slide plan

| # | Slide | Main visual | Animation |
| --- | --- | --- | --- |
| 1 | Title and team details | Original data visual: data → fitted model with uncertainty → forecast → decision | – |
| 2 | Why advanced statistics matters | Five-stage data-to-decision flow; limits of intuition; Brynjolfsson et al. (2011) evidence | 5 clicks: stages appear one at a time |
| 3 | Key advanced statistical methods | Six method cards (what each asks, where it is applied, its main caveat) | – |
| 4 | Business decision-making | Bing experiment chain: question → data → method → insight → decision → outcome; table of business functions | 6 clicks: one per chain step |
| 5 | Scientific and academic research | Six-step research workflow; RECOVERY forest plot; reproducibility evidence | 6 clicks: one per workflow step |
| 6 | Case study: product-page A/B test (**illustrative data**) | Experiment diagram, native bar chart, confidence-interval diagram, decision | 3 clicks: results, then inference, then decision |
| 7 | Challenges, ethics and future implications | Risk and safeguard table; ML/AI note; five-step responsible-practice framework | – |
| 8 | Conclusion, takeaways and key references | Four takeaways and the closing statement | – |
| A | Appendix: full references and visual sources | Two-column APA reference list | – |

Every slide uses a medium-speed **Fade** transition.

## Editing the team and course details (slide 1)

All details are ordinary PowerPoint text. None of them is part of an image.

* **Team name:** click `[Team Name]` next to "PRESENTED BY".
* **Members:** names and student IDs sit in a borderless two-column table.
  * Replace `[Member 1 Full Name]` and `[Student ID]` in each row.
  * To add a member, click the last cell and press **Tab**.
  * To remove a member, right-click the row and choose **Delete → Delete Rows**.
* **Course, instructor, department, university, date:** click each bracketed value and type over it. The orange labels stay as they are.
* **Footer:** the footer text and slide numbers come from the slide layouts. To change them, go to **View → Slide Master**.
* **Colours and fonts:** they come from the deck theme ("Evidence Navy": Cambria headings, Calibri body). Use **Design → Variants** to restyle the whole deck in one place.

## References

1. Amrhein, V., Greenland, S., & McShane, B. (2019). Scientists rise up against statistical significance. *Nature, 567*, 305–307. https://doi.org/10.1038/d41586-019-00857-9
2. Brynjolfsson, E., Hitt, L. M., & Kim, H. H. (2011). *Strength in numbers: How does data-driven decisionmaking affect firm performance?* SSRN. https://doi.org/10.2139/ssrn.1819486
3. Button, K. S., Ioannidis, J. P. A., Mokrysz, C., Nosek, B. A., Flint, J., Robinson, E. S. J., & Munafò, M. R. (2013). Power failure: Why small sample size undermines the reliability of neuroscience. *Nature Reviews Neuroscience, 14*(5), 365–376. https://doi.org/10.1038/nrn3475
4. Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). *Bayesian data analysis* (3rd ed.). CRC Press.
5. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The elements of statistical learning* (2nd ed.). Springer.
6. Hernán, M. A., & Robins, J. M. (2020). *Causal inference: What if.* Chapman & Hall/CRC.
7. Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and practice* (3rd ed.). OTexts. https://otexts.com/fpp3/
8. Kohavi, R., Tang, D., & Xu, Y. (2020). *Trustworthy online controlled experiments: A practical guide to A/B testing.* Cambridge University Press. https://doi.org/10.1017/9781108653985
9. Kohavi, R., & Thomke, S. (2017). The surprising power of online experiments. *Harvard Business Review, 95*(5), 74–82. https://hbr.org/2017/09/the-surprising-power-of-online-experiments
10. Montgomery, D. C. (2017). *Design and analysis of experiments* (9th ed.). Wiley.
11. Obermeyer, Z., Powers, B., Vogeli, C., & Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. *Science, 366*(6464), 447–453. https://doi.org/10.1126/science.aax2342
12. Open Science Collaboration. (2015). Estimating the reproducibility of psychological science. *Science, 349*(6251), aac4716. https://doi.org/10.1126/science.aac4716
13. RECOVERY Collaborative Group. (2021). Dexamethasone in hospitalized patients with Covid-19. *New England Journal of Medicine, 384*(8), 693–704. https://doi.org/10.1056/NEJMoa2021436
14. Shmueli, G. (2010). To explain or to predict? *Statistical Science, 25*(3), 289–310. https://doi.org/10.1214/10-STS330
15. Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-positive psychology. *Psychological Science, 22*(11), 1359–1366. https://doi.org/10.1177/0956797611417632
16. Wasserstein, R. L., & Lazar, N. A. (2016). The ASA statement on p-values: Context, process, and purpose. *The American Statistician, 70*(2), 129–133. https://doi.org/10.1080/00031305.2016.1154108

## Visual sources

* **Title visual and the six method diagrams (slide 3):** original artwork made from simulated data (`build/build_visuals.py`, fixed random seed). The title slide labels it "Illustrative visual · simulated data".
* **Slide 5 forest plot:** redrawn as editable shapes from the published RECOVERY results (rates, age-adjusted rate ratios and 95% CIs, NEJM 2021). The bar chart and the other diagrams use no external figures.
* **Slide 6 data:** hypothetical, and labelled that way on the slide.
* **Icons (slide 2):** Font Awesome glyphs from the `react-icons` package (free icons, CC BY 4.0).
* **No third-party photographs are used.** See the notes below.

## Slide 6 calculations (illustrative data)

| Quantity | Value |
| --- | --- |
| A (current page) | 840 / 20,000 = 4.20% |
| B (redesign) | 960 / 20,000 = 4.80% |
| Difference | +0.60 pp; relative lift 0.60 / 4.20 = 14.3% |
| Pooled proportion | 1,800 / 40,000 = 0.045 |
| SE under H0 | √(0.045 × 0.955 × (1/20,000 + 1/20,000)) = 0.002073 |
| z | 0.006 / 0.002073 = 2.89, two-sided p = 0.0038 |
| 95% CI (unpooled SE 0.002073) | 0.006 ± 1.96 × 0.002073 = +0.19 to +1.01 pp |
| Planned sample size | 80% power, α = 0.05 two-sided, 4.2% → 4.8%: ≈ 18,738 per arm, so 20,000 were planned |

## Notes and limitations

* **Animations:** these are native PowerPoint entrance effects (Fade) and slide transitions, written into the slide XML. The file passes OOXML schema validation, and LibreOffice Impress reads back every effect. They have **not** been played in Microsoft PowerPoint's slideshow mode, so run the deck once (**Slide Show → From Beginning**) before presenting. To remove an effect, use **Animations → Animation Pane**.
* **Photographs:** this build environment's network policy blocked image hosts such as Wikimedia Commons, so no authentic photographs could be downloaded and checked. The deck uses original diagrams and charts instead. To add a photo, put it on a slide and give it a source caption.
* **PDF fonts:** the PDF was rendered with LibreOffice using metric-compatible substitutes for Cambria and Calibri. PowerPoint will show the true fonts, and line breaks may differ very slightly.
* **Appendix slide:** it sits after slide 8 and is outside the eight-slide main deck. If your course needs exactly eight slides in slideshow mode, right-click it and choose **Hide Slide**.

## Rebuilding

```bash
PPTX_SKILL=<path to the pptx skill> \
NODE_PATH=<node_modules with pptxgenjs react-icons react react-dom sharp> \
./build/build.sh
```

The build needs Python 3 with matplotlib, numpy, scipy and lxml, plus LibreOffice for the PDF.
