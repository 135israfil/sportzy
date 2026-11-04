"""Shared building blocks for the Sportzy designs (see build.py and templates.py)."""
import pathlib

HERE = pathlib.Path(__file__).parent

# [LAUNCH] slip rule: change here if go-live moves (used by designs and videos)
LAUNCH_DATE_BN = "১২ ডিসেম্বর"
LAUNCH_DATE_EN = "12 Dec"
LAUNCH_DAY_BN = "শনিবার, সন্ধ্যা ৭টা"
LOGO = "../../brand/sportzy-mark-pitchdeck.png"
SCR = "../../product_screens/"
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="#2FD67B" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 6.5"/></svg>'


def atmosphere(floor=True, lamps=False):
    s = '<div class="sky"></div><div class="beam l"></div><div class="beam r"></div>'
    if lamps:
        s += '<div class="lamp l">' + "<i></i>" * 8 + '</div><div class="lamp r">' + "<i></i>" * 8 + "</div>"
    if floor:
        s += '<div class="floor"><div class="turf"><div class="circle"></div></div></div>'
    return s + '<div class="vignette"></div>'


def brand(size=52, text=38):
    return f'<div class="brand"><img src="{LOGO}" style="width:{size}px;height:{size}px"><b style="font-size:{text}px">SPORTZY</b></div>'


def phone(img, left, top, width, rot=0, crop_top=0):
    h = int(width * 2.05)
    return (f'<div class="phone" style="left:{left}px;top:{top}px;width:{width}px;height:{h}px;transform:rotate({rot}deg)">'
            f'<div class="notch"></div><div class="scr"><div class="sb"><span>9:41</span><i></i></div><div style="height:100%;overflow:hidden"><img src="{SCR}{img}" style="margin-top:-{crop_top}px"></div></div></div>')


def page(name, w, h, body, extra_css="", scale=1):
    html = f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css">
<style>.canvas{{width:{w}px;height:{h}px}}{extra_css}</style></head>
<script>function fitText(){{document.querySelectorAll("[data-fit]").forEach(e=>{{e.style.whiteSpace="nowrap";e.style.width="max-content";let fs=parseFloat(getComputedStyle(e).fontSize);while(e.scrollWidth>+e.dataset.fit&&fs>16){{fs-=2;e.style.fontSize=fs+"px"}}}})}}</script>
<body data-size="{w}x{h}" data-scale="{scale}"><div class="canvas">{body}<div class="grain"></div></div></body></html>"""
    (HERE / f"{name}.html").write_text(html, encoding="utf-8")


PAY = '<div class="pay"><span>bKash</span><span>Nagad</span><span>QR Pay BD</span></div>'

# ---------------------------------------------------------------- QR helper (links to sportzy.live; per-venue link replaces it)
def qr_svg(url, size):
    import qrcode
    q = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_M); q.add_data(url); q.make()
    m = q.get_matrix(); n = len(m); c = size / n
    rects = "".join(f'<rect x="{x*c:.2f}" y="{y*c:.2f}" width="{c+.3:.2f}" height="{c+.3:.2f}"/>' for y, r in enumerate(m) for x, v in enumerate(r) if v)
    return f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" fill="#04110A">{rects}</svg>'


def head(right=""):
    return f'<div style="position:absolute;left:72px;top:64px">{brand()}</div><div style="position:absolute;right:72px;top:70px">{right}</div>'


def cta_block(label, left=72, bottom=64, url=True):
    u = '<span class="url" style="padding-left:8px">sportzy.live</span>' if url else ""
    return f'<div style="position:absolute;left:{left}px;bottom:{bottom}px;display:grid;gap:20px;justify-items:start"><span class="cta">{label} {ARROW}</span>{u}</div>'


