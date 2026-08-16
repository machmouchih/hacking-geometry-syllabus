// Renders print/syllabus.html to the PDF at the repo root.
// Page numbers sit bottom-right and are omitted on page 1, matching the
// Fall 2025 document. Chromium applies one footer to every page, so the
// document is rendered twice and page 1 is taken from the footerless pass.
const { chromium } = require('playwright-core');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');

const OUT = 'DME2100_Hacking_Geometry_Fall2026.pdf';
const SRC = 'print/syllabus.html';
const MARGIN = { top: '0.8in', right: '0.9in', bottom: '0.75in', left: '0.9in' };
const FOOTER =
  '<div style="width:100%;font-family:Roboto,Arial;font-size:9pt;color:#000;' +
  'padding:0 0.9in;text-align:right;"><span class="pageNumber"></span></div>';

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium',
  });
  const page = await browser.newPage();
  await page.goto('file://' + process.cwd() + '/' + SRC, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);

  const common = { format: 'Letter', printBackground: true, margin: MARGIN };
  const numbered = await page.pdf({
    ...common, displayHeaderFooter: true,
    headerTemplate: '<span></span>', footerTemplate: FOOTER,
  });
  const plain = await page.pdf(common);
  await browser.close();

  const src = await PDFDocument.load(numbered);
  const first = await PDFDocument.load(plain);
  const out = await PDFDocument.create();
  const [p1] = await out.copyPages(first, [0]);
  out.addPage(p1);
  const rest = await out.copyPages(src, src.getPageIndices().slice(1));
  rest.forEach((p) => out.addPage(p));
  fs.writeFileSync(OUT, await out.save());
  console.log('wrote ' + OUT + ' (' + out.getPageCount() + ' pages)');
})();
