// Renders wafer-defect-proposal.html to a one-page A4 PDF (and a PNG preview)
// with the pre-installed Chromium. Usage: node research-proposal/build_pdf.cjs
const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const dir = __dirname;
  const html = path.join(dir, "wafer-defect-proposal.html");
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await page.goto("file://" + html);
  await page.evaluate(() => document.fonts.ready);

  const overflow = await page.evaluate(() => {
    const p = document.querySelector(".page");
    return p.scrollHeight - p.clientHeight;
  });
  if (overflow > 0) console.warn(`WARNING: content overflows the page by ${overflow}px`);

  await page.pdf({
    path: path.join(dir, "wafer-defect-proposal.pdf"),
    format: "A4",
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });
  await page.screenshot({ path: path.join(dir, "wafer-defect-proposal-preview.png"), fullPage: false });
  await browser.close();
  console.log("Wrote wafer-defect-proposal.pdf and preview PNG");
})();
