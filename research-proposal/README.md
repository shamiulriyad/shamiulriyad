# One-page research proposal: wafer die defect inspection

| File | Purpose |
| --- | --- |
| `wafer-defect-proposal.pdf` | Final one-page A4 proposal (portrait) |
| `wafer-defect-proposal.html` | Editable source: text, layout and both figures |
| `wafer-defect-proposal-preview.png` | Screen preview of the page |
| `build_pdf.cjs` | Renders the HTML to PDF with Chromium (Playwright) |
| `fonts/` | Embedded fonts (Charter, Inter) as TrueType |

## Editing

1. Replace the placeholders in `[square brackets]`: researcher name, student ID, supervisor, institution and date.
2. Edit any text directly in `wafer-defect-proposal.html`. Figure 1 (the wafer) is inline SVG; its die grid and failure patterns are drawn by the short script at the bottom of the file.
3. Rebuild from the repository root:

   ```bash
   node research-proposal/build_pdf.cjs
   ```

   The script prints a warning if the content no longer fits on one page.

## Notes

- Figure 1 is a schematic, not real data. No experiments or results are claimed.
- All four DOIs are live links in the PDF.
- Fonts: Inter (SIL Open Font License, see `fonts/OFL-inter.txt`) and Bitstream Charter (Bitstream/X Consortium free license), converted to TrueType so they embed cleanly in the PDF.
