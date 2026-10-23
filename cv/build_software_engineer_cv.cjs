// Renders the Software Engineer Intern CV HTML to an A4 PDF with headless Chromium.
// Usage: node cv/build_software_engineer_cv.cjs   (needs the `playwright` package)
const { chromium } = require('playwright');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const name = 'Md_Shamiul_Islam_Riyad_Software_Engineer_Intern_CV';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(pathToFileURL(path.join(__dirname, `${name}.html`)).href, { waitUntil: 'networkidle' });
  await page.pdf({
    path: path.join(__dirname, `${name}.pdf`),
    format: 'A4',
    printBackground: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
    tagged: true,
  });
  await browser.close();
  console.log(`Wrote cv/${name}.pdf`);
})();
