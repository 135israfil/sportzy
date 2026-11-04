// Quick layout check without a full render: node preview.js <name> <out.png> t1 t2 ...  (frames tiled side by side, 560 px tall)
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');
(async () => {
  const [name, out, ...times] = process.argv.slice(2);
  const html = fs.readFileSync(path.join(__dirname, 'build', name + '.html'), 'utf8');
  const [, w, h] = html.match(/data-size="(\d+)x(\d+)"/);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +w, height: +h } });
  await p.goto('file://' + path.join(__dirname, 'build', name + '.html'));
  await p.evaluate(() => document.fonts.ready); await p.evaluate(() => window.fitText && window.fitText()); await p.waitForTimeout(300);
  const d = fs.mkdtempSync(path.join(os.tmpdir(), 'pv'));
  for (const [i, t] of times.entries()) { await p.evaluate(t => seek(t), +t); await p.locator('.canvas').screenshot({ path: path.join(d, String(i).padStart(2, '0') + '.png') }); }
  await b.close();
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', path.join(d, '%02d.png'), '-vf', `scale=-2:560,tile=${times.length}x1:padding=8:color=white`, '-frames:v', '1', out]);
})();
