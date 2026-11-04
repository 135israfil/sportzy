// Renders motion HTML (build/*.html) to MP4 frame by frame: seek(t) -> JPEG -> ffmpeg (H.264, yuv420p, 30 fps).
// Usage: node render_videos.js [name ...]     Output: ../renders/<name>.mp4 + poster PNG (out__* names go to ../out/)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
const FPS = 30, BUILD = path.join(__dirname, 'build');
(async () => {
  const only = process.argv.slice(2);
  const files = fs.readdirSync(BUILD).filter(f => f.endsWith('.html') && (only.length ? only.includes(f.replace('.html', '')) : !f.startsWith('out__')));
  const browser = await chromium.launch();
  for (const f of files) {
    const html = fs.readFileSync(path.join(BUILD, f), 'utf8');
    const [, w, h] = html.match(/data-size="(\d+)x(\d+)"/);
    const dur = +html.match(/data-duration="([\d.]+)"/)[1];
    const poster = +((html.match(/data-poster="([\d.]+)"/) || [0, dur / 2])[1]);
    const name = f.replace('.html', '');
    const dir = name.startsWith('out__') ? path.join(__dirname, '..', 'out') : path.join(__dirname, '..', 'renders');
    const base = path.join(dir, name.replace(/^out__/, ''));
    fs.mkdirSync(dir, { recursive: true });
    const page = await browser.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 1 });
    await page.goto('file://' + path.join(BUILD, f));
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(() => window.fitText && window.fitText());
    await page.waitForTimeout(300);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', base + '.mp4']);
    const done = new Promise((res, rej) => ff.on('close', c => (c ? rej(new Error('ffmpeg ' + c)) : res())));
    const canvas = page.locator('.canvas');
    const n = Math.round(dur * FPS);
    for (let i = 0; i < n; i++) {
      await page.evaluate(t => window.seek(t), i / FPS);
      const buf = await canvas.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await done;
    await page.evaluate(t => window.seek(t), poster);
    await canvas.screenshot({ path: base + '_poster.png' });
    console.log('rendered', path.basename(base) + '.mp4', w + 'x' + h, dur + 's');
    await page.close();
  }
  await browser.close();
})();
