"""Builds the Sportzy motion-graphics videos as HTML timelines; render_videos.js turns them into MP4.

  python3 build_videos.py                            # all videos -> build/*.html, then: node render_videos.js
  python3 build_videos.py fill <video> <data.json>   # VID-09 / VID-12 / VID-13 from real data -> ../out/ (renders too)

Reuses the static design system (creative/designs/src: base.css, kit.py, data/*.json).
Videos are silent masters; captions (.srt) are written next to each MP4.
"""
import datetime, json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).parent
DESIGN_SRC = HERE.parents[1] / "creative" / "designs" / "src"
sys.path.insert(0, str(DESIGN_SRC))
from kit import ARROW, CHECK, LOGO, PAY, LAUNCH_DATE_BN, LAUNCH_DATE_EN, atmosphere, brand  # noqa: E402

BUILD = HERE / "build"
RENDERS = HERE.parent / "renders"
DATA = DESIGN_SRC.parent / "data"
ENGINE = (HERE / "timeline.js").read_text(encoding="utf-8")
FIT = re.search(r"<script>function fitText.*?</script>", (DESIGN_SRC / "kit.py").read_text(encoding="utf-8"), re.S).group(0).replace("{{", "{").replace("}}", "}")
SCR_W = 1170  # width of the approved mobile screenshots (px)


# ---------------------------------------------------------------- keyframe helpers
def K(*frames):
    return "data-k='" + json.dumps([list(f) for f in frames], ensure_ascii=False) + "'"


ENTER = {"up": ({"o": 0, "y": 70}, "out"), "down": ({"o": 0, "y": -70}, "out"), "left": ({"o": 0, "x": -90}, "out"),
         "right": ({"o": 0, "x": 90}, "out"), "fade": ({"o": 0}, "out"), "pop": ({"o": 0, "s": .6}, "back"),
         "slam": ({"o": 0, "s": 1.8, "b": 14}, "out"), "zoom": ({"o": 0, "s": .85}, "out")}


def anim(t0, t1=None, kind="up", d=.5, exit_kind="fade"):
    """Enter at t0 (duration d), hold, exit at t1."""
    start, ease = ENTER[kind]
    rest = {k: (1 if k in ("o", "s") else 0) for k in start}
    fr = [(t0, start), (t0 + d, rest, ease)]
    if t1 is not None:
        end = {"o": 0, "y": -40} if exit_kind == "up" else {"o": 0}
        fr += [(t1 - .3, {**rest}), (t1, {**{k: v for k, v in rest.items()}, **end}, "inout")]
    return K(*fr)


def at(x, y, inner, k="", w=None, extra=""):
    ws = f"width:{w}px;" if w else ""
    return f'<div style="position:absolute;left:{x}px;top:{y}px;{ws}{extra}" {k}>{inner}</div>'


def center(y, inner, k="", W=1080, extra=""):
    return f'<div style="position:absolute;left:0;width:{W}px;top:{y}px;text-align:center;{extra}" {k}>{inner}</div>'


def scene(t0, t1, inner):
    return f'<div style="position:absolute;inset:0" {K((t0 - .01, {"o": 0}), (t0, {"o": 1}, "step"), (t1, {"o": 1}), (t1 + .25, {"o": 0}, "lin"))}>{inner}</div>'


def phone_v(left, top, width, screens, taps=(), rot=0, k=""):
    """Phone frame with timed screen changes. screens: [(img, t_in, t_out, y_offset_px)], taps: [(t, x_px, y_px)] in screenshot px."""
    h = int(width * 2.05)
    sc = (width - 30) / SCR_W
    layers = ""
    for img, t_in, t_out, yoff in screens:
        fr = [(t_in - .01, {"o": 0, "x": 60}), (t_in + .35, {"o": 1, "x": 0})]
        if t_out is not None:
            fr += [(t_out - .01, {"o": 1, "x": 0}), (t_out + .35, {"o": 0, "x": -60})]
        layers += f'<div style="position:absolute;left:0;right:0;top:62px;bottom:0;overflow:hidden" {K(*fr)}><img src="../../product_screens/{img}" style="width:100%;display:block;margin-top:-{yoff * sc:.0f}px"></div>'
    for t, x, y in taps:
        yoff = next((s[3] for s in screens if s[1] <= t and (s[2] is None or t < s[2])), 0)
        cx, cy = x * sc, 62 + (y - yoff) * sc
        layers += (f'<span style="position:absolute;left:{cx - 40:.0f}px;top:{cy - 40:.0f}px;width:80px;height:80px;border-radius:50%;'
                   f'border:5px solid #fff;background:rgba(255,255,255,.25);z-index:5" {K((t - .01, {"o": 0, "s": .4}), (t, {"o": 1, "s": .4}, "step"), (t + .55, {"o": 0, "s": 1.7}, "out"))}></span>')
    return (f'<div style="position:absolute;left:{left}px;top:{top}px" {k}><div class="phone" style="position:relative;width:{width}px;height:{h}px;transform:rotate({rot}deg)">'
            f'<div class="notch"></div><div class="scr" style="padding-top:0"><div class="sb"><span>9:41</span><i></i></div>{layers}</div></div></div>')


def lamps(t_on, W):
    """Four floodlight banks that switch on one by one (VID-01 hook)."""
    xs = [W * .08, W * .30, W * .62, W * .84]
    out = ""
    for i, x in enumerate(xs):
        t = t_on + i * .55
        out += (f'<div class="lamp" style="left:{x - 40:.0f}px;top:40px" {K((t - .01, {"o": .12}), (t, {"o": 1}, "step"))}>' + "<i></i>" * 8 + "</div>")
    return out


def counter(t0, t1, a, b, fmt="", cls="mono y", size=60, pre="", suf="", bn=False):
    c = json.dumps({"t0": t0, "t1": t1, "a": a, "b": b, "fmt": fmt, "pre": pre, "suf": suf, "bn": bn})
    return f"<span class='{cls}' style='font-size:{size}px' data-count='{c}'>{a}</span>"


def cta(label, size=34):
    return f'<span class="cta" style="font-size:{size}px">{label} {ARROW}</span>'


def chip(text, size=30, hl=False):
    col = "border-color:rgba(47,214,123,.7);color:var(--green)" if hl else ""
    return (f'<span style="display:inline-flex;gap:10px;align-items:center;background:rgba(255,255,255,.06);border:1.5px solid var(--line);'
            f'border-radius:99px;padding:14px 24px;{col}" class="bn-body"><span style="font-size:{size}px">{CHECK.replace("<svg", f"<svg width={size} height={size}")} {text}</span></span>')


def step_tag(n, bn, en, t0, t1, y=290, W=1080, size=84):
    tag = f"{n} · {en}" if n else en
    return center(y, f'<span class="mono y" style="font-size:30px;letter-spacing:5px">{tag}</span><div class="bn" data-fit="{W - 120}" style="font-size:{size}px;margin:10px auto 0">{bn}</div>', anim(t0, t1, "up"), W)


def end_card(t0, W, H, line1, line2, cta_label, sub=""):
    y = H * .27 if H > 1300 else H * .12
    return scene(t0, 999, f"""
{center(y, f'<img src="{LOGO}" style="width:{170 if H > 1300 else 130}px;height:{170 if H > 1300 else 130}px;filter:drop-shadow(0 0 40px rgba(47,214,123,.55))">', anim(t0, None, "pop", .6), W)}
{center(y + 190, f'<div class="bn" data-fit="{W - 120}" style="font-size:{140 if H > 1300 else 96}px;margin:0 auto">{line1}</div><div class="bn g glow" data-fit="{W - 120}" style="font-size:{140 if H > 1300 else 96}px;margin:0 auto">{line2}</div>', anim(t0 + .25, None, "up"), W)}
{center(y + (600 if H > 1300 else 470), (f'<div class="mono y" style="font-size:30px;letter-spacing:4px;margin-bottom:30px">{sub}</div>' if sub else '') + cta(cta_label) + '<div class="url" style="margin-top:24px">sportzy.live</div>', anim(t0 + .5, None, "up"), W)}""")


def vpage(name, W, H, dur, body, captions, poster=None, kb=True):
    """Write build/<name>.html. captions: [(t0, t1, bn, en)] -> .srt files beside the MP4."""
    BUILD.mkdir(exist_ok=True)
    zoom = K((0, {"s": 1}), (dur, {"s": 1.06}, "lin")) if kb else ""
    html = f"""<!doctype html><html><head><meta charset="utf-8"><base href="{DESIGN_SRC.as_uri()}/">
<link rel="stylesheet" href="base.css"><style>.canvas{{width:{W}px;height:{H}px}} .lamp{{position:absolute}}</style>{FIT}</head>
<body data-size="{W}x{H}" data-duration="{dur}" data-poster="{poster if poster is not None else dur - 1}">
<div class="canvas"><div style="position:absolute;inset:0" {zoom}>{atmosphere()}</div>{body}<div class="grain"></div></div>
<script>{ENGINE}</script><script>seek(0)</script></body></html>"""
    (BUILD / f"{name}.html").write_text(html, encoding="utf-8")
    if captions and not name.startswith("out__"):
        RENDERS.mkdir(exist_ok=True)
        for lang, idx in (("bn", 2), ("en", 3)):
            srt = "".join(f"{i}\n{ts(c[0])} --> {ts(c[1])}\n{c[idx]}\n\n" for i, c in enumerate([c for c in captions if c[idx]], 1))
            (RENDERS / f"{name}_{lang}.srt").write_text(srt, encoding="utf-8")


def ts(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def load(name):
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))


# ================================================================ VID-12 Tonight in Dhaka (15 s, 9:16) from open_slots.json
def vid12(d, name="VID-12_tonight_in_dhaka_9x16_sample"):
    W, H, dur = 1080, 1920, 15
    slots = d["slots"][:5]
    rows = ""
    for i, s in enumerate(slots):
        t = 3.2 + i * 1.5
        badge = f' &nbsp;<span class=badge style="font-size:22px;padding:3px 12px">{s["badge_bn"]}</span>' if s.get("badge_bn") else ""
        rows += (f'<div class="card" style="display:flex;justify-content:space-between;align-items:center;padding:30px 36px;margin-bottom:22px" {anim(t, 12.2, "right", .45)}>'
                 f'<div><div data-fit="560" style="font:800 36px Manrope">{s["venue"]}</div><div class="bn-body m" style="font-size:28px">{s["area_bn"]}{badge}</div></div>'
                 f'<div style="text-align:right;white-space:nowrap"><div class="mono y" style="font-size:44px">{s["time"]}</div><div class="mono" style="font-size:30px">{s["price"]}</div></div></div>')
    body = f"""
{scene(0, 3, f'''
{center(520, '<div style="position:relative;height:200px"><div class="mono y glow" style="font-size:190px;position:absolute;left:0;right:0" ' + K((0, {"o": 1}), (1.3, {"o": 0}, "step")) + '>6:59<span style="font-size:90px"> PM</span></div><div class="mono y glow" style="font-size:190px;position:absolute;left:0;right:0" ' + K((0, {"o": 0}), (1.3, {"o": 1}, "step")) + '>7:00<span style="font-size:90px"> PM</span></div></div>', anim(0, None, "zoom", .5))}
{center(800, '<div class="mono g" style="font-size:30px;letter-spacing:6px">' + d.get("kicker_en", "TONIGHT IN DHAKA").upper() + '</div><div class="bn" style="font-size:130px;margin-top:10px">' + d.get("title_line1_bn", "আজ রাতে") + '</div><div class="bn g glow" style="font-size:130px">' + d.get("title_line2_bn", "খালি স্লট") + '</div>', anim(1.3, None, "slam", .45))}''')}
{scene(3, 12.2, at(72, 270, brand()) + center(420, '<div class="bn" style="font-size:104px">' + d.get("title_line1_bn", "আজ রাতে") + ' <span class="g">' + d.get("title_line2_bn", "খালি স্লট") + '</span></div>', anim(3, None, "down", .4)) + at(72, 640, rows, w=936))}
{end_card(12.2, W, H, "এখনই", "বুক করো", "স্লট দেখো", "TONIGHT IN DHAKA")}"""
    caps = [(0, 3, "আজ রাতে ঢাকায়।", "Tonight in Dhaka.")] + \
           [(3.2 + i * 1.5, 3.2 + (i + 1) * 1.5, f'{s["area_bn"]}, রাত {s["time"]}', f'{s["venue"]}, {s["time"]}') for i, s in enumerate(slots)] + \
           [(12.2, 15, "এখনই বুক করো।", "Book now.")]
    vpage(name, W, H, dur, body, caps, poster=9.5)


# ================================================================ shared layout per format
def L(W, H):
    if H > 1300:   # 9:16
        return dict(head=290, ph=(270, 560, 540), big=150, mid=96, step=84)
    return dict(head=80, ph=(375, 330, 330), big=110, mid=72, step=64)   # 1:1


def slam2(t, l1, l2, W, y, size, en=""):
    k = f'<div class="mono g" style="font-size:30px;letter-spacing:6px;margin-bottom:14px">{en}</div>' if en else ""
    return (center(y, k + f'<div class="bn" data-fit="{W - 120}" style="font-size:{size}px;margin:0 auto">{l1}</div>', anim(t, None, "slam", .45), W)
            + center(y + int(size * 1.05) + (50 if en else 0), f'<div class="bn g glow" data-fit="{W - 120}" style="font-size:{size}px;margin:0 auto">{l2}</div>', anim(t + .5, None, "slam", .45), W))


def toast(t0, t1, text, y, W, ok=True):
    ic = CHECK.replace("<svg", "<svg width=38 height=38") if ok else ""
    return center(y, f'<span class="card" style="display:inline-flex;gap:16px;align-items:center;padding:22px 34px;border-color:rgba(47,214,123,.6);box-shadow:0 20px 60px rgba(0,0,0,.6)">{ic}<span class="bn" style="font-size:38px;font-weight:700">{text}</span></span>', anim(t0, t1, "pop", .4), W)


def pay_chips(t0, W, y, tap_t=None):
    out = ""
    for i, p in enumerate(["bKash", "Nagad", "QR Pay BD"]):
        hl = "border-color:var(--green);box-shadow:0 0 30px rgba(47,214,123,.4)" if i == 0 and tap_t else ""
        out += f'<span style="display:inline-block;margin:0 10px;padding:18px 30px;border-radius:16px;background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.16);font:800 34px Manrope;{hl}" {anim(t0 + i * .3, None, "pop", .35)}>{p}</span>'
    return center(y, out, "", W)


# ================================================================ VID-01 brand intro (animated cut)
def vid01(W, H, name, cut=False):
    l = L(W, H)
    T = dict(s1=(0, 2), s2=(2, 5), s4=(5, 11), s5=(11, 15), dur=15) if cut else dict(s1=(0, 3), s2=(3, 8), s3=(8, 16), s4=(16, 24), s5=(24, 30), dur=30)
    a, b = T["s1"]
    dark = f'<div style="position:absolute;inset:0;background:#020604" {K((0, {"o": .94}), (a + .35, {"o": .94}), (a + .4, {"o": .7}, "step"), (a + .95, {"o": .48}, "step"), (a + 1.5, {"o": .26}, "step"), (a + 2.05 if not cut else a + 1.7, {"o": 0}, "step"))}></div>'
    body = dark + f'<div {K((b, {"o": 1}), (b + .4, {"o": 0}))}>' + lamps(a + .4, W) + "</div>"
    # S2
    a, b = T["s2"]
    areas = ["মিরপুর", "বসুন্ধরা", "উত্তরা", "ধানমন্ডি", "ওয়ারী", "বনানী"]
    tick = "".join(f'<span class="tag" style="margin:10px;font-size:{34 if H > 1300 else 26}px" {anim(a + 1.2 + i * .25, None, "pop", .3)}>{x}</span>' for i, x in enumerate(areas))
    body += scene(a, b, slam2(a + .1, "প্রতি সন্ধ্যায়", "ঢাকা খেলে।", W, l["head"] + (240 if H > 1300 else 120), l["big"], "EVERY EVENING, DHAKA PLAYS")
                  + center(l["head"] + (760 if H > 1300 else 520), f'<div style="width:{W - 160}px;margin:0 auto">{tick}</div>', "", W))
    caps = [(T["s2"][0], T["s2"][1], "প্রতি সন্ধ্যায় ঢাকা খেলে।", "Every evening, Dhaka plays.")]
    # S3 (full version only)
    if not cut:
        a, b = T["s3"]
        scores = ["2–1", "0–0", "3–2", "1–1", "4–3", "2–0"]
        cols = 3
        tw = 260 if H > 1300 else 220
        tiles = "".join(f'<div class="card mono" style="position:absolute;left:{(W - cols * tw - 40) // 2 + (i % cols) * (tw + 20)}px;top:{(820 if H > 1300 else 480) + (i // cols) * (tw * .62 + 20):.0f}px;width:{tw}px;padding:26px 0;text-align:center;font-size:{64 if H > 1300 else 52}px" '
                        f'{K((a + .8 + i * .2, {"o": 0, "s": .6}), (a + 1.1 + i * .2, {"o": 1, "s": 1}, "back"), (a + 4, {"o": 1, "b": 0}), (a + 4.8, {"o": .18, "b": 6}))}>{sc}</div>' for i, sc in enumerate(scores))
        body += scene(a, b, center(l["head"] + (60 if H > 1300 else 0), f'<div class="bn" style="font-size:{l["mid"]}px">হাজারো ম্যাচ হয়।</div>', anim(a + .2, None, "up"), W)
                      + tiles + center((1300 if H > 1300 else 830), f'<div class="bn y" style="font-size:{l["mid"]}px">কেউ দেখে না।</div>', anim(a + 4, None, "slam", .5), W))
        caps += [(a, a + 4, "হাজারো ম্যাচ হয়।", "Thousands of matches."), (a + 4, b, "কেউ দেখে না।", "Nobody sees them.")]
    # S4
    a, b = T["s4"]
    cw = 620 if H > 1300 else 480
    card = (f'<div class="card" style="width:{cw}px;margin:0 auto;padding:34px;text-align:left;box-shadow:0 40px 100px rgba(0,0,0,.6)">'
            f'<span class="badge" style="font-family:Anton;font-size:30px;letter-spacing:2px">● LIVE</span>'
            f'<div class="en" style="font-size:{70 if H > 1300 else 56}px;margin-top:22px">LIONS <span class="y">vs</span> STRIKERS</div>'
            f'<div class="mono" style="font-size:{110 if H > 1300 else 80}px;margin-top:16px;background:var(--paper);color:var(--ink);border-radius:18px;text-align:center;padding:6px 0">2–1</div>'
            f'<div style="display:flex;gap:12px;margin-top:22px">' + "".join(f'<span style="padding:10px 18px;border-radius:10px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.16);font:700 24px Manrope">{p}</span>' for p in ["Facebook", "YouTube"]) + "</div></div>")
    ey = 1340 if H > 1300 else 850
    body += scene(a, b, slam2(a + .1, "এখন থেকে", "দেখবে।", W, l["head"] + (20 if H > 1300 else 0), l["mid"])
                  + center((620 if H > 1300 else 330), card, anim(a + 1.6, None, "pop", .5), W)
                  + center(ey, f'<div class="en" style="font-size:{72 if H > 1300 else 52}px">EVERY MATCH</div><div class="en g glow" style="font-size:{72 if H > 1300 else 52}px">DESERVES A BROADCAST.</div>', anim(a + 3.2, None, "up"), W))
    caps += [(a, b, "এখন থেকে দেখবে।", "Now they will.")]
    a, b = T["s5"]
    body += end_card(a, W, H, "Sportzy", "শিগগিরই আসছে", "WhatsApp-এ আপডেট পাও", f"LAUNCHING {LAUNCH_DATE_EN.upper()} · DHAKA")
    caps += [(a, b, "Sportzy। শিগগিরই আসছে।", "Sportzy. Coming soon.")]
    vpage(name, W, H, T["dur"], body, caps, poster=T["s4"][0] + 4)


# ================================================================ VID-02 launch announcement
def vid02(W, H, name, teaser=False):
    l = L(W, H); x, y, pw = l["ph"]
    body = lamps(0, W) if False else ""
    body += scene(0, 3, slam2(.3, "Sportzy", "এখন লাইভ", W, (700 if H > 1300 else 330), l["big"], "SPORTZY IS LIVE"))
    caps = [(0, 3, "Sportzy এখন লাইভ।", "Sportzy is live.")]
    if teaser:
        body += end_card(3, W, H, "লঞ্চ", LAUNCH_DATE_BN, "নোটিফিকেশন অন করো", "SPORTZY · DHAKA")
        vpage(name, W, H, 10, body, caps + [(3, 10, f"আসছে {LAUNCH_DATE_BN}।", f"Launching {LAUNCH_DATE_EN}.")], poster=1.5)
        return
    body += scene(3, 10, step_tag("", "আজ রাতের খালি স্লট দেখো", "TONIGHT'S OPEN SLOTS", 3, None, l["head"], W, l["step"])
                  + phone_v(x, y, pw, [("main-mobile.png", 3, 6.2, 300), ("turfdetail-mobile.png", 6.2, None, 0)], [(5.3, 870, 2490), (7.4, 400, 1131)], k=anim(3, None, "up", .5))
                  + center((1180 if H > 1300 else 700), f'<div class="card" style="display:inline-block;padding:28px 40px;border-color:rgba(47,214,123,.6);box-shadow:0 30px 90px rgba(0,0,0,.8)"><div style="display:flex;gap:16px;align-items:center;justify-content:center">{CHECK.replace("<svg", "<svg width=44 height=44")}<span class="bn" style="font-size:{48 if H > 1300 else 38}px">বুকিং কনফার্ম</span></div><div class="mono m" style="font-size:24px;margin-top:12px">bKash · Nagad · QR Pay BD</div></div>', anim(8.4, None, "pop", .4), W))
    body += scene(10, 16, step_tag("", "একটা লিংক, পুরো স্কোয়াড", "ONE LINK. WHOLE SQUAD.", 10, None, l["head"], W, l["step"])
                  + phone_v(x, y, pw, [("matchroster-mobile.png", 10, None, 0)], [(12, 255, 348)], k=anim(10, None, "up", .5))
                  + toast(12.5, None, "ম্যাচ লিংক কপি হয়েছে", (1500 if H > 1300 else 920), W))
    body += end_card(16, W, H, "পরের ম্যাচ,", "এক ট্যাপ দূরে", "এখনই বুক করো", "SPORTZY.LIVE")
    caps += [(3, 10, "আজ রাতের খালি স্লট দেখো, মিনিটেই বুক করো।", "See tonight's open slots, book in a minute."),
             (10, 16, "স্কোয়াডকে একটা লিংক পাঠাও।", "Send your squad one link."), (16, 20, "পরের ম্যাচ, এক ট্যাপ দূরে।", "Your next match is one tap away.")]
    vpage(name, W, H, 20, body, caps, poster=8.8)


# ================================================================ VID-03 how to book (45 s, 9:16)
def vid03(name="VID-03_how_to_book_9x16"):
    W, H = 1080, 1920
    x, y, pw = 270, 600, 540
    body = scene(0, 3, center(560, counter(0, 3, 60, 57, "m:ss", "mono y glow", 240), anim(0, None, "zoom", .4))
                 + slam2(1, "৬০ সেকেন্ডে", "টার্ফ বুক", W, 900, 130))
    screens = [("main-mobile.png", 3, 12.5, 300), ("turfdetail-mobile.png", 12.5, 38, 0), ("matchroster-mobile.png", 38, None, 0)]
    taps = [(5.5, 240, 2295), (7.2, 810, 2295), (8.9, 240, 2505), (10.8, 870, 2490), (14.2, 400, 1131), (40.4, 255, 348)]
    body += phone_v(x, y, pw, screens, taps, k=K((2.9, {"o": 0, "y": 120}), (3.4, {"o": 1, "y": 0}), (27, {"o": 1, "y": 0}), (27.4, {"o": .35, "y": 0}), (38, {"o": .35}), (38.4, {"o": 1}), (41.7, {"o": 1}), (42, {"o": 0})))
    body += step_tag("১", "এলাকা, সময় আর খেলা বাছো", "SEARCH", 3, 15, 290)
    body += step_tag("২", "খালি স্লট বাছো", "PICK A SLOT", 15, 27, 290)
    slots = [("7:00 PM", "বুকড", False), ("8:00 PM", "খালি", True), ("9:00 PM", "খালি", True), ("10:00 PM", "খালি", True)]
    chips = ""
    for i, (tm, st, free) in enumerate(slots):
        sel = K((16.5 + i * .3, {"o": 0, "s": .7}), (16.9 + i * .3, {"o": 1, "s": 1}, "back"))
        style = "border:2.5px solid var(--green);color:var(--text)" if free else "border:2.5px solid #2a3a30;color:#5d7466;text-decoration:line-through"
        chips += f'<div style="position:relative;display:inline-block;margin:10px;padding:22px 30px;border-radius:18px;background:#0b1a11;{style}" {sel}><div class="mono" style="font-size:40px">{tm}</div><div class="bn-body" style="font-size:24px">{st}</div>'
        if tm == "9:00 PM":
            chips += f'<div style="position:absolute;inset:-3px;border-radius:18px;background:var(--green);display:grid;place-items:center;color:var(--ink)" {K((20.5, {"o": 0}), (20.6, {"o": 1}, "step"))}><div><div class="mono" style="font-size:40px">9:00 PM</div><div class="bn" style="font-size:24px">বাছাই করা</div></div></div>'
        chips += "</div>"
    body += scene(15, 27, center(1180, f'<div class="card" style="display:inline-block;padding:24px;width:960px;box-shadow:0 30px 90px rgba(0,0,0,.7)">{chips}</div>', anim(15.5, None, "up"), W)
                  + f'<span style="position:absolute;left:{540 + 122}px;top:{1230}px;width:80px;height:80px;border-radius:50%;border:5px solid #fff;background:rgba(255,255,255,.25)" {K((20.39, {"o": 0, "s": .4}), (20.4, {"o": 1, "s": .4}, "step"), (20.95, {"o": 0, "s": 1.7}))}></span>'
                  + toast(22.5, None, "সবুজ = খালি স্লট", 1560, W))
    body += step_tag("৩", "পে করার সময় স্লট তোমার জন্য হোল্ড", "PAY", 27, 38, 290)
    hold = (f'<div class="card" style="display:inline-block;width:900px;padding:40px;text-align:left;box-shadow:0 30px 90px rgba(0,0,0,.7)">'
            f'<div class="bn" style="font-size:44px">9:00 PM · স্লট হোল্ড চলছে</div>'
            f'<div style="margin-top:24px;height:22px;border-radius:99px;background:#1E3829;overflow:hidden"><div style="height:100%;background:var(--yellow);transform-origin:left" {K((27.5, {"sx": 1}), (38, {"sx": .7}, "lin"))}></div></div>'
            f'<div class="bn-body m" style="font-size:28px;margin-top:16px">পে করার আগ পর্যন্ত অন্য কেউ এই স্লট নিতে পারবে না</div></div>')
    body += scene(27, 38, center(820, hold, anim(27.4, None, "up"), W) + pay_chips(29.5, W, 1200, tap_t=33) + toast(34.5, None, "পেমেন্ট সফল", 1400, W))
    body += step_tag("৪", "বুকিং কনফার্ম, টিমকে লিংক পাঠাও", "PLAY", 38, 42, 290) + toast(40.9, 42, "ম্যাচ লিংক কপি হয়েছে", 1450, W)
    body += end_card(42, W, H, "টার্ফ বুকিং,", "এখন সহজ", "এখনই বুক করো", "SPORTZY.LIVE")
    caps = [(0, 3, "৬০ সেকেন্ডে টার্ফ বুক।", "Book a turf in 60 seconds."), (3, 15, "এলাকা, সময় আর খেলা বেছে নাও।", "Pick area, time and sport."),
            (15, 27, "খালি স্লট সবুজ। একটা বাছো।", "Open slots are green. Pick one."), (27, 38, "পে করার সময় স্লটটা তোমার জন্য হোল্ড থাকে।", "Your slot is held while you pay."),
            (38, 45, "বুকিং কনফার্ম। টিমকে লিংক পাঠাও।", "Booking confirmed. Send your team the link.")]
    vpage(name, W, H, 45, body, caps, poster=20.8)


# ================================================================ VID-05 organiser tournaments (45 s, 9:16)
def vid05(name="VID-05_organiser_tournaments_9x16"):
    W, H = 1080, 1920
    shots = ""
    import random
    rnd = random.Random(7)
    for i in range(12):
        sx, sy, rot = rnd.randint(40, 760), rnd.randint(260, 1360), rnd.randint(-18, 18)
        shots += (f'<div style="position:absolute;left:{sx}px;top:{sy}px;width:260px;height:420px;border-radius:26px;background:#14261b;border:2px solid #24402f;transform:rotate({rot}deg);padding:22px" '
                  f'{K((i * .18, {"o": 0, "s": 1.4}), (i * .18 + .25, {"o": 1, "s": 1}, "out"))}><div style="font:800 30px Manrope;color:#e2136e">bKash</div>'
                  f'<div class="mono m" style="font-size:22px;margin-top:20px">Send Money</div><div class="mono" style="font-size:40px;margin-top:10px">৳3,000</div><div style="height:12px;background:#24402f;border-radius:6px;margin-top:30px"></div><div style="height:12px;width:70%;background:#24402f;border-radius:6px;margin-top:14px"></div></div>')
    body = scene(0, 3, shots + f'<div style="position:absolute;inset:0;background:rgba(6,16,10,.55)" {K((1, {"o": 0}), (1.3, {"o": 1}))}></div>' + slam2(1.2, "১২ জন ক্যাপ্টেন,", "১২টা স্ক্রিনশট।", W, 760, 120))
    # S2 create
    fields = ["টুর্নামেন্টের নাম", "খেলা আর ফরম্যাট", "এন্ট্রি ফি", "সর্বোচ্চ টিম", "রেজিস্ট্রেশন ডেডলাইন"]
    rows = "".join(f'<div style="margin:14px 0" {anim(4.5 + i * .9, None, "left", .4)}>{chip(t, 38)}</div>' for i, t in enumerate(fields))
    body += scene(3, 15, step_tag("১", "টুর্নামেন্ট বানাও", "CREATE", 3, None, 290) + center(620, f'<div style="display:inline-block;text-align:left">{rows}</div>', "", W) + toast(10.5, None, "রেজিস্ট্রেশন খোলা হয়েছে", 1450, W))
    # S3 teams pay
    body += scene(15, 27, step_tag("২", "ক্যাপ্টেনরা QR Pay BD-তে পে করে", "TEAMS PAY", 15, None, 290)
                  + center(640, f'<div class="card" style="display:inline-block;width:900px;padding:44px;text-align:left"><div class="bn-body m" style="font-size:30px">পেইড টিম</div>'
                           f'<div style="margin-top:6px">{counter(16, 24, 0, 12, "", "en", 200)}<span class="en m" style="font-size:110px"> / 16</span></div>'
                           f'<div style="margin-top:24px;height:24px;border-radius:99px;background:#1E3829;overflow:hidden"><div style="height:100%;background:var(--green);transform-origin:left" {K((16, {"sx": 0}), (24, {"sx": .75}, "inout"))}></div></div>'
                           f'<div class="mono m" style="font-size:22px;margin-top:14px">SAMPLE NUMBERS</div></div>', anim(15.4, None, "up"), W)
                  + center(1200, chip("পে করার সময় স্পট হোল্ড", 34), anim(18, None, "pop", .4), W)
                  + center(1310, chip("রিজেক্ট হলে রিফান্ড আমরা দিই", 34), anim(19.5, None, "pop", .4), W)
                  + center(1420, chip("টাকা আসে এক জায়গায়", 34), anim(21, None, "pop", .4), W))
    # S4 fixtures
    fx = [("7:00 PM", "Lions", "Strikers"), ("7:00 PM", "Rangers", "Falcons"), ("8:00 PM", "Titans", "United")]
    fr = "".join(f'<div class="card" style="display:grid;grid-template-columns:170px 1fr;align-items:center;padding:22px 30px;margin-bottom:14px" {anim(33.2 + i * .4, None, "right", .4)}><span class="mono y" style="font-size:32px">{a}</span><span style="font:800 34px Manrope">{b} <span class="mono m" style="font-size:24px">vs</span> {c}</span></div>' for i, (a, b, c) in enumerate(fx))
    body += scene(27, 38, step_tag("৩", "ফিক্সচার, মাঠের স্লট, পয়েন্ট টেবিল", "FIXTURES", 27, None, 290)
                  + phone_v(270, 600, 540, [("managematch-mobile.png", 27, None, 0)], [(30.5, 342, 2052)], k=K((27, {"o": 0, "y": 120}), (27.5, {"o": 1, "y": 0}), (32.6, {"o": 1}), (33, {"o": .25})))
                  + at(110, 900, fr, w=860))
    # S5 live + end
    body += scene(38, 41.5, center(760, '<span class="badge" style="font-family:Anton;font-size:60px;padding:16px 34px;letter-spacing:3px">● LIVE</span>', anim(38.2, None, "slam", .4), W)
                  + slam2(38.9, "ফাইনাল", "লাইভ করো", W, 950, 140) + center(1340, '<div style="display:flex;gap:14px;justify-content:center">' + "".join(f'<span style="padding:14px 24px;border-radius:12px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.16);font:700 30px Manrope">{p}</span>' for p in ["Facebook", "YouTube"]) + "</div>", anim(40, None, "up"), W))
    body += end_card(41.5, W, H, "টুর্নামেন্ট আপনি চালান,", "টাকার হিসাব আমাদের", "মেসেজ করুন", "RUN THE TOURNAMENT. WE'LL HANDLE THE MONEY.")
    caps = [(0, 3, "১২ জন ক্যাপ্টেন, ১২টা স্ক্রিনশট।", "12 captains, 12 screenshots."), (3, 15, "টুর্নামেন্ট বানাও: ফি, টিম সংখ্যা, ডেডলাইন।", "Create the tournament: fee, teams, deadline."),
            (15, 27, "ক্যাপ্টেনরা QR Pay BD-তে পে করে, স্পট হোল্ড থাকে।", "Captains pay by QR Pay BD; spots are held."), (27, 38, "ফিক্সচার, মাঠের স্লট, পয়েন্ট টেবিল।", "Fixtures, turf slots, standings."),
            (38, 45, "ফাইনাল লাইভ করো।", "Stream the final live.")]
    vpage(name, W, H, 45, body, caps, poster=20)


# ================================================================ VID-06 find a game (25 s, 9:16)
def vid06(name="VID-06_find_a_game_9x16"):
    W, H = 1080, 1920
    body = scene(0, 3, slam2(.2, "ঢাকায় নতুন?", "টিম নেই?", W, 760, 140))
    body += phone_v(270, 600, 540, [("discover-mobile.png", 3, 8.6, 0), ("matchroster-mobile.png", 8.6, None, 0)], [(5.4, 450, 1539), (7.1, 855, 2019), (10.6, 510, 2235)],
                    k=K((2.9, {"o": 0, "y": 120}), (3.4, {"o": 1, "y": 0}), (15.3, {"o": 1}), (15.8, {"o": .28}), (20.7, {"o": .28}), (21, {"o": 0})))
    body += step_tag("", "ফাইন্ড আ গেম খোলো, স্পট রিকোয়েস্ট করো", "REQUEST A SPOT", 3, 14, 290)
    body += toast(11.2, 14, "স্পট রিকোয়েস্ট পাঠানো হয়েছে", 1450, W)
    body += center(640, f'<div class="card" style="display:inline-flex;gap:18px;align-items:center;padding:26px 34px;width:900px;text-align:left;border-color:rgba(47,214,123,.6);box-shadow:0 30px 80px rgba(0,0,0,.7)">{CHECK.replace("<svg", "<svg width=48 height=48")}<div><div style="font:800 30px Manrope">Sportzy</div><div class="bn-body" style="font-size:32px">অর্গানাইজার তোমার রিকোয়েস্ট অ্যাকসেপ্ট করেছে</div></div></div>', K((14, {"o": 0, "y": -160}), (14.5, {"o": 1, "y": 0}), (20.7, {"o": 1}), (21, {"o": 0})), W)
    body += step_tag("", "অ্যাকসেপ্ট করলেই তুমি মাঠে", "YOU'RE IN", 14, 21, 290)
    body += center(1380, '<div class="en g glow" style="font-size:170px">YOU\'RE IN</div>', anim(15.6, 21, "slam", .45), W)
    body += end_card(21, W, H, "আজ রাতেই", "খেলো।", "গেম খোঁজো", "FIND A GAME")
    caps = [(0, 3, "ঢাকায় নতুন? টিম নেই?", "New to Dhaka? No team?"), (3, 14, "ফাইন্ড আ গেম খোলো, স্পট রিকোয়েস্ট করো।", "Open Find a game and request a spot."),
            (14, 21, "অর্গানাইজার অ্যাকসেপ্ট করলেই তুমি মাঠে।", "Once the organiser accepts, you're on the pitch."), (21, 25, "আজ রাতেই খেলো।", "Play tonight.")]
    vpage(name, W, H, 25, body, caps, poster=16.5)


# ================================================================ VID-09 tournament promo (15 s) from tournament.json
def vid09(d, name, W=1080, H=1920):
    l = L(W, H)
    big = 190 if H > 1300 else 150
    y0 = 560 if H > 1300 else 170
    body = scene(0, 3, center(y0 - 60, f'<div class="mono y" style="font-size:28px;letter-spacing:6px">{d["kicker_en"].upper()}</div>', anim(.2, None, "fade"), W)
                 + center(y0, f'<div class="en" data-fit="{W - 120}" style="font-size:{big}px;margin:0 auto">{d["title_line1"].upper()}</div>', anim(.4, None, "slam", .45), W)
                 + center(y0 + int(big * .95), f'<div class="en g glow" data-fit="{W - 120}" style="font-size:{big}px;margin:0 auto">{d["title_line2"].upper()}</div>', anim(1, None, "slam", .45), W))
    info = [("তারিখ", d["dates_bn"], "bn"), ("ভেন্যু", d["venue"], "bn"), ("এন্ট্রি ফি", d["fee"], "mono y")]
    cards = "".join(f'<div class="card" style="padding:28px 36px;margin-bottom:18px;text-align:left" {anim(3.3 + i * .8, None, "left", .45)}><div class="bn-body m" style="font-size:28px">{a}</div><div class="{c}" style="font-size:{50 if H > 1300 else 40}px">{b}</div></div>' for i, (a, b, c) in enumerate(info))
    feats = "".join(f'<span style="display:inline-block;margin:8px" {anim(7.6 + i * .3, None, "pop", .35)}>{chip(t, 28)}</span>' for i, t in enumerate(d["features_bn"]))
    badge = center((1260 if H > 1300 else 700), f'<span class="badge" style="font-size:54px;padding:16px 34px;transform:rotate(-2deg);display:inline-block">{d["spots_badge_bn"]}</span>', anim(6.4, None, "slam", .4), W) if d.get("spots_badge_bn") else ""
    body += scene(3, 10, center(l["head"] - (0 if H > 1300 else 0), f'<div class="en" data-fit="{W - 120}" style="font-size:{l["mid"]}px;margin:0 auto">{d["title_line1"].upper()} <span class="g">{d["title_line2"].upper()}</span></div>', anim(3, None, "down", .4), W)
                  + at(90, (480 if H > 1300 else 190), cards, w=W - 180) + badge + center((1420 if H > 1300 else 850), f'<div style="width:{W - 120}px;margin:0 auto">{feats}</div>', "", W))
    body += end_card(10, W, H, "Sportzy-তে", "রেজিস্টার করো", "টিম রেজিস্টার করো", d["kicker_en"].upper())
    caps = [(0, 3, "", f'{d["title_line1"]} {d["title_line2"]}'), (3, 10, f'{d["dates_bn"]}, {d["venue"]}', f'{d["venue"]} · {d["fee"]}'), (10, 15, "Sportzy-তে রেজিস্টার করো।", "Register on Sportzy.")]
    vpage(name, W, H, 15, body, caps, poster=7)


# ================================================================ VID-13 match of the week bumper (5 s) from live_thumbnail.json
def vid13(d, name="VID-13_match_of_the_week_bumper_9x16_sample"):
    W, H = 1080, 1920
    body = (center(420, '<div class="mono y" style="font-size:32px;letter-spacing:8px">MATCH OF THE WEEK</div>', anim(.1, None, "fade"), W)
            + center(520, f'<div class="en" data-fit="940" style="font-size:170px;margin:0 auto">{d["team_a"].upper()}</div>', anim(.4, None, "slam", .4), W)
            + center(720, '<div class="en y" style="font-size:90px">VS</div>', anim(.8, None, "pop", .3), W)
            + center(840, f'<div class="en g glow" data-fit="940" style="font-size:170px;margin:0 auto">{d["team_b"].upper()}</div>', anim(1.1, None, "slam", .4), W)
            + center(1110, f'<div class="card" style="display:inline-block;padding:30px 60px"><div class="bn" style="font-size:44px">{d["stage_bn"]}</div><div class="mono" style="font-size:150px;background:var(--paper);color:var(--ink);border-radius:20px;padding:4px 40px;margin-top:14px">{d["score"]}</div></div>', anim(2.1, None, "pop", .45), W)
            + center(1560, '<div style="display:inline-flex;gap:16px;align-items:center"><img src="' + LOGO + '" style="width:60px;height:60px"><span class="en" style="font-size:48px">STREAMED ON SPORTZY</span></div>', anim(3.2, None, "up"), W))
    vpage(name, W, H, 5, body, [(0, 5, "", f'{d["team_a"]} vs {d["team_b"]} · {d["score"]}')], poster=3.8)


VIDEOS = {
    "VID-01": lambda: (vid01(1080, 1920, "VID-01_brand_intro_animated_9x16"), vid01(1080, 1080, "VID-01_brand_intro_animated_1x1"), vid01(1080, 1920, "VID-01_brand_intro_animated_15s_9x16", cut=True)),
    "VID-02": lambda: (vid02(1080, 1920, "VID-02_launch_announcement_9x16"), vid02(1080, 1080, "VID-02_launch_announcement_1x1"), vid02(1080, 1920, "VID-02_launch_teaser_10s_9x16", teaser=True)),
    "VID-03": lambda: vid03(),
    "VID-05": lambda: vid05(),
    "VID-06": lambda: vid06(),
    "VID-09": lambda: (vid09(load("tournament"), "VID-09_tournament_promo_9x16_sample"), vid09(load("tournament"), "VID-09_tournament_promo_1x1_sample", 1080, 1080)),
    "VID-12": lambda: vid12(load("open_slots")),
    "VID-13": lambda: vid13(load("live_thumbnail")),
}
FILL = {"VID-12": (vid12, "VID-12_tonight_in_dhaka_9x16"), "VID-09": (vid09, "VID-09_tournament_promo_9x16"),
        "VID-13": (vid13, "VID-13_match_of_the_week_bumper_9x16")}

if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "fill":
        vid, path = sys.argv[2], sys.argv[3]
        if vid not in FILL:
            sys.exit("fill works for: " + ", ".join(FILL))
        d = json.loads(open(path, encoding="utf-8").read())
        stamp = re.sub(r"[^A-Za-z0-9_-]", "", d.get("_label", "")) or datetime.date.today().isoformat()
        fn, base = FILL[vid]
        out = f"out__{base}_{stamp}"
        fn(d, out)
        subprocess.run(["node", str(HERE / "render_videos.js"), out], check=True)
        sys.exit(0)
    only = sys.argv[1:]
    for k, fn in VIDEOS.items():
        if not only or k in only:
            fn()
    print("built", len(list(BUILD.glob("*.html"))), "video timelines")
