// Deterministic keyframe engine for Sportzy motion videos.
// Elements carry data-k='[[t,{o,x,y,s,r,b},ease], ...]' (t in seconds). window.seek(t) sets the exact state for time t.
// data-count='{"t0":0,"t1":45,"a":60,"b":15,"fmt":"m:ss"}' renders a counter.
(function () {
  const D = { o: 1, x: 0, y: 0, s: 1, r: 0, b: 0, sx: 1 };
  const E = {
    out: t => 1 - Math.pow(1 - t, 3),
    inout: t => (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
    lin: t => t,
    back: t => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); },
    step: t => (t < 1 ? 0 : 1),
  };
  let items = null, counters = null;
  function init() {
    items = [...document.querySelectorAll('[data-k]')].map(el => {
      const tracks = {};
      JSON.parse(el.dataset.k).forEach(([t, p, e]) => { for (const k in p) (tracks[k] = tracks[k] || []).push([t, p[k], e || 'out']); });
      for (const k in tracks) tracks[k].sort((a, b) => a[0] - b[0]);
      return [el, tracks, el.style.transform || ''];
    });
    counters = [...document.querySelectorAll('[data-count]')].map(el => [el, JSON.parse(el.dataset.count)]);
  }
  function val(tr, t) {
    if (t <= tr[0][0]) return tr[0][1];
    for (let i = 1; i < tr.length; i++) {
      if (t <= tr[i][0]) {
        const [t0, v0] = tr[i - 1], [t1, v1, e] = tr[i];
        return v0 + (v1 - v0) * E[e]((t - t0) / ((t1 - t0) || 1));
      }
    }
    return tr[tr.length - 1][1];
  }
  const BN = '০১২৩৪৫৬৭৮৯';
  window.seek = function (t) {
    if (!items) init();
    for (const [el, tr, base] of items) {
      const g = k => (tr[k] ? val(tr[k], t) : D[k]);
      el.style.opacity = g('o');
      el.style.transform = `${base} translate(${g('x')}px,${g('y')}px) scale(${g('s')}) rotate(${g('r')}deg) scaleX(${g('sx')})`;
      const b = g('b'); el.style.filter = b > 0.05 ? `blur(${b}px)` : '';
    }
    for (const [el, c] of counters) {
      const u = Math.min(1, Math.max(0, (t - c.t0) / (c.t1 - c.t0)));
      let v = Math.round(c.a + (c.b - c.a) * u), s;
      if (c.fmt === 'm:ss') s = Math.floor(v / 60) + ':' + String(v % 60).padStart(2, '0');
      else s = String(v);
      if (c.bn) s = s.replace(/[0-9]/g, d => BN[+d]);
      el.textContent = (c.pre || '') + s + (c.suf || '');
    }
  };
})();
