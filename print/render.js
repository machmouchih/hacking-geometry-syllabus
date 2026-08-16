// Renders print/syllabus.html to the PDF at the repo root.
// Requires playwright-core and a Chromium binary.
const { chromium } = require('playwright-core');

const OUT = 'DME2100_Hacking_Geometry_Fall2026.pdf';
const SRC = 'print/syllabus.html';

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium',
  });
  const page = await browser.newPage();
  await page.goto('file://' + process.cwd() + '/' + SRC, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: OUT,
    format: 'Letter',
    printBackground: true,
    margin: { top: '0.8in', right: '0.9in', bottom: '0.75in', left: '0.9in' },
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate:
      '<div style="width:100%;font-family:Roboto,Arial;font-size:9pt;color:#000;padding:0 0.9in;">' +
      '<span class="pageNumber"></span></div>',
  });
  await browser.close();
  console.log('wrote ' + OUT);
})();
