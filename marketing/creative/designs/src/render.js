// Renders every design HTML in this folder to ../<name>.png at its exact pixel size.
// Usage: node render.js [name ...]   (needs Playwright + Chromium; fonts load from Google Fonts)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const only = process.argv.slice(2);
  const files = fs.readdirSync(__dirname).filter(f => f.endsWith('.html') && (!only.length || only.includes(f.replace('.html',''))));
  const browser = await chromium.launch();
  for (const f of files) {
    const html = fs.readFileSync(path.join(__dirname, f), 'utf8');
    const [, w, h] = html.match(/data-size="(\d+)x(\d+)"/);
    const sc = +((html.match(/data-scale="(\d+)"/) || [0, 1])[1]);
    const page = await browser.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: sc });
    await page.goto('file://' + path.join(__dirname, f));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);
    const out = path.join(__dirname, '..', f.replace('.html', '.png'));
    await page.locator('.canvas').screenshot({ path: out });
    console.log('rendered', path.basename(out), w + 'x' + h);
    await page.close();
  }
  await browser.close();
})();
