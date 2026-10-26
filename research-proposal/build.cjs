// Renders proposal.html to a one-page A4 PDF (plus a PNG preview) with headless Chromium.
// Usage: node research-proposal/build.cjs   (needs the `playwright` package)
// Exits with an error if the content no longer fits on one A4 page.
const { chromium } = require('playwright');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const name = 'Defect_Aware_MultiDie_Fusion_Proposal';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await page.goto(pathToFileURL(path.join(__dirname, 'proposal.html')).href, { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'print' });
  await page.evaluate(() => document.fonts.ready);

  // Text that does not fit flows into a third column (horizontal overflow) or pushes
  // the references past the bottom margin.
  const issues = await page.evaluate(() => {
    const out = [];
    const pg = document.querySelector('.page');
    const cols = document.querySelector('.cols');
    if (cols.scrollWidth > cols.clientWidth + 1) out.push('body text overflows the two columns');
    const limit = pg.getBoundingClientRect().bottom - parseFloat(getComputedStyle(pg).paddingBottom);
    if (document.querySelector('footer.refs').getBoundingClientRect().bottom > limit + 1) out.push('references run past the bottom margin');
    return out;
  });
  if (issues.length) {
    await browser.close();
    console.error('Layout does not fit one page: ' + issues.join('; '));
    process.exit(1);
  }

  await page.pdf({
    path: path.join(__dirname, `${name}.pdf`),
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
    tagged: true,
  });
  await page.screenshot({ path: path.join(__dirname, 'preview.png'), fullPage: true });
  await browser.close();
  console.log(`Wrote research-proposal/${name}.pdf and preview.png`);
})();
