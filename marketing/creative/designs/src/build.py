"""Builds the Sportzy core marketing designs as HTML (rendered to PNG by render.js).

Run:  python3 build.py && node render.js
Sample data (venue names, times, prices, teams) is marked SAMPLE in ../README.md and
must be replaced with real, consented data before anything is published.
"""
import pathlib

HERE = pathlib.Path(__file__).parent
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
<body data-size="{w}x{h}" data-scale="{scale}"><div class="canvas">{body}<div class="grain"></div></div></body></html>"""
    (HERE / f"{name}.html").write_text(html, encoding="utf-8")


PAY = '<div class="pay"><span>bKash</span><span>Nagad</span><span>QR Pay BD</span></div>'

# ---------------------------------------------------------------- DES-04 launch post 1080x1350
page("DES-04_launch_post", 1080, 1350, atmosphere() + f"""
<div style="position:absolute;left:72px;top:64px">{brand()}</div>
<div style="position:absolute;right:72px;top:70px"><span class="tag">ঢাকায় লাইভ</span></div>
<div style="position:absolute;left:72px;top:190px;width:940px">
  <div class="mono g" style="font-size:24px;letter-spacing:4px;margin-bottom:22px">SPORTZY IS LIVE · DHAKA</div>
  <div class="bn" style="font-size:132px">টার্ফ বুকিং</div>
  <div class="bn g glow" style="font-size:132px">এখন এক ট্যাপে</div>
</div>
<div style="position:absolute;left:72px;top:560px;width:520px">
  <p class="bn-body" style="font-size:31px;color:var(--muted2)">ঢাকার খালি স্লট আর দাম এক জায়গায়। বুক করো, পে করো, টিমকে লিংক পাঠাও।</p>
  <div style="margin-top:40px;display:grid;gap:18px">
    {''.join(f'<div class="card" style="display:flex;align-items:center;gap:18px;padding:18px 22px"><span class="mono" style="font-size:22px;color:var(--ink);background:var(--yellow);border-radius:10px;padding:6px 10px">0{i}</span><span class="bn" style="font-size:36px;font-weight:700">{t}</span></div>' for i, t in enumerate(["এলাকা আর সময় বাছো", "খালি স্লট হোল্ড করো", "bKash/Nagad-এ পে করো"], 1))}
  </div>
</div>
{phone("main-mobile.png", 640, 540, 400, 6)}
<div style="position:absolute;left:72px;bottom:64px;display:grid;gap:20px;justify-items:start"><span class="cta">এখনই বুক করো {ARROW}</span><span class="url" style="padding-left:8px">sportzy.live</span></div>
""")

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


# ---------------------------------------------------------------- DES-05 Facebook cover 1640x624 (safe area: centre 1000x400)
page("DES-05_facebook_cover", 1640, 624, atmosphere() + f"""
{phone("discover-mobile.png", 70, 120, 300, -10)}
{phone("main-mobile.png", 1270, 110, 300, 10)}
<div style="position:absolute;left:320px;width:1000px;top:112px;text-align:center;display:grid;justify-items:center;gap:20px">
  {brand(46, 34)}
  <div class="bn" style="font-size:86px;white-space:nowrap">পরের ম্যাচ, <span class="g glow">এক ট্যাপ দূরে</span></div>
  <div class="en" style="font-size:40px;color:var(--muted2);letter-spacing:2px">Turf booking · Tournaments · Live streams</div>
  <div style="display:flex;gap:18px;align-items:center;margin-top:6px"><span class="url">sportzy.live</span>{PAY}</div>
</div>
""")

# ---------------------------------------------------------------- DES-06 live thumbnail 1280x720 (SAMPLE teams)
page("DES-06_live_thumbnail_sample", 1280, 720, atmosphere() + f"""
<div style="position:absolute;left:60px;top:52px">{brand(46, 34)}</div>
<div style="position:absolute;left:60px;top:150px">
  <span class="badge" style="font-size:34px;padding:10px 20px;font-family:Anton;letter-spacing:2px">● LIVE</span>
  <div class="en" style="font-size:150px;margin-top:26px">LIONS</div>
  <div class="en y" style="font-size:70px;margin:6px 0 6px 6px">VS</div>
  <div class="en g glow" style="font-size:150px">STRIKERS</div>
</div>
<div class="card" style="position:absolute;right:70px;top:170px;width:430px;padding:34px;text-align:center;box-shadow:0 30px 80px rgba(0,0,0,.5)">
  <div class="bn" style="font-size:44px">ফাইনাল</div>
  <div style="background:var(--paper);color:var(--ink);border-radius:22px;margin:22px 0;padding:18px 0" class="mono"><span style="font-size:130px;line-height:1">2–1</span></div>
  <div class="mono m" style="font-size:24px">FLOODLIT FUTSAL CUP</div>
</div>
""")

# ---------------------------------------------------------------- DES-07 venue QR poster, A3 ratio (1191x1684 @2x)
page("DES-07_venue_qr_poster_sample", 1191, 1684, atmosphere() + f"""
<div style="position:absolute;left:90px;top:84px">{brand(64, 46)}</div>
<div style="position:absolute;right:90px;top:94px"><span class="tag" style="font-size:22px">পার্টনার টার্ফ</span></div>
<div style="position:absolute;left:90px;right:90px;top:230px;text-align:center">
  <div class="bn" style="font-size:116px;white-space:nowrap">এই টার্ফ বুক করো</div>
  <div class="bn g glow" style="font-size:150px">অনলাইনে</div>
  <p class="bn-body" style="font-size:34px;color:var(--muted2);margin-top:22px">খালি স্লট দেখো, bKash বা Nagad-এ পে করো, পে করলেই বুকিং কনফার্ম।</p>
</div>
<div style="position:absolute;left:50%;top:690px;transform:translateX(-50%);background:var(--paper);border-radius:40px;padding:44px 44px 30px;text-align:center;box-shadow:0 0 0 10px rgba(47,214,123,.35),0 40px 120px rgba(0,0,0,.6)">
  {qr_svg("https://sportzy.live", 380)}
  <div class="bn" style="color:var(--ink);font-size:48px;margin-top:22px">স্ক্যান করে বুক করো</div>
</div>
<div style="position:absolute;left:90px;right:90px;top:1300px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px">
  {''.join(f'<div class="card" style="padding:24px;text-align:center"><div class="mono y" style="font-size:30px">0{i}</div><div class="bn" style="font-size:40px;font-weight:700;margin-top:8px">{t}</div></div>' for i, t in enumerate(["স্ক্যান করো", "স্লট বাছো", "পে করো"], 1))}
</div>
<div style="position:absolute;left:90px;right:90px;bottom:70px;display:flex;justify-content:space-between;align-items:center">
  <span class="url" style="font-size:32px">sportzy.live</span>{PAY}
</div>
""", scale=2)

# ---------------------------------------------------------------- DES-08 turf spotlight 1080x1350 (SAMPLE venue)
page("DES-08_turf_spotlight_sample", 1080, 1350, atmosphere() + head('<span class="tag">টার্ফ স্পটলাইট</span>') + f"""
<div style="position:absolute;left:72px;top:190px">
  <div class="mono g" style="font-size:24px;letter-spacing:4px;margin-bottom:18px">TURF OF THE WEEK · WARI</div>
  <div class="en" style="font-size:150px">WARI</div>
  <div class="en g glow" style="font-size:150px">FLOODLIT</div>
</div>
<div style="position:absolute;left:72px;top:620px;width:500px;display:grid;gap:16px">
  {''.join(f'<div class="card" style="padding:20px 24px"><div class="bn-body m" style="font-size:24px">{a}</div><div class="{c}" style="font-size:{fs}px;margin-top:4px">{b}</div></div>' for a, b, c, fs in [("খেলা", "ফুটবল · ৫ ও ৭ জন", "bn", 40), ("ফ্লাডলাইট", "রাত ১টা পর্যন্ত", "bn", 40), ("দাম শুরু", "৳1,500 / ঘণ্টা", "mono y", 44)])}
  <div><span style="display:inline-flex;gap:10px;align-items:center;border:1.5px solid rgba(47,214,123,.6);border-radius:99px;padding:10px 18px;font:700 22px Manrope;color:var(--green)">{CHECK.replace('<svg', '<svg width="22" height="22"')} ভেরিফায়েড ভেন্যু</span></div>
</div>
{phone("turfdetail-mobile.png", 640, 470, 390, 5)}
{cta_block("এখানে বুক করো")}
""")

# ---------------------------------------------------------------- DES-09 tournament announcement 1080x1350 (SAMPLE event)
page("DES-09_tournament_announcement_sample", 1080, 1350, atmosphere() + head('<span class="tag">রেজিস্ট্রেশন চলছে</span>') + f"""
<div style="position:absolute;left:72px;right:72px;top:180px;text-align:center">
  <div class="mono y" style="font-size:26px;letter-spacing:6px">DHAKA · 5-A-SIDE · 2026</div>
  <div class="en" style="font-size:190px;margin-top:20px">WINTER</div>
  <div class="en g glow" style="font-size:190px">FUTSAL CUP</div>
</div>
<div class="card" style="position:absolute;left:72px;right:72px;top:640px;display:grid;grid-template-columns:repeat(3,1fr);text-align:center">
  {''.join(f'<div style="padding:30px 10px;{bd}"><div class="bn-body m" style="font-size:24px">{a}</div><div class="{c}" style="font-size:38px;margin-top:6px">{b}</div></div>' for a, b, c, bd in [("তারিখ", "১২–১৪ ডিসেম্বর", "bn", ""), ("ভেন্যু", "Pitch 9 Arena", "bn", "border-left:1.5px solid var(--line);border-right:1.5px solid var(--line)"), ("এন্ট্রি ফি", "৳3,000/টিম", "mono y", "")])}
</div>
<div style="position:absolute;left:0;right:0;top:850px;text-align:center"><span class="badge" style="font-size:44px;padding:14px 30px;transform:rotate(-2deg);display:inline-block">মাত্র ৪টি স্পট বাকি</span></div>
<div style="position:absolute;left:72px;right:72px;top:990px;display:flex;justify-content:center;gap:14px;flex-wrap:wrap">
  {''.join(f'<span style="display:inline-flex;gap:10px;align-items:center;background:rgba(255,255,255,.05);border:1.5px solid var(--line);border-radius:99px;padding:12px 20px" class="bn-body"><span style="font-size:26px">{CHECK.replace("<svg", "<svg width=22 height=22")} {t}</span></span>' for t in ["অনলাইনে রেজিস্ট্রেশন", "QR Pay BD-তে পেমেন্ট", "ফাইনাল লাইভ"])}
</div>
<div style="position:absolute;left:72px;right:72px;bottom:64px;display:flex;justify-content:space-between;align-items:flex-end">
  <div style="display:grid;gap:20px;justify-items:start"><span class="cta">টিম রেজিস্টার করো {ARROW}</span><span class="url" style="padding-left:8px">sportzy.live</span></div>
  <div style="text-align:center"><div style="width:120px;height:120px;border-radius:50%;border:2px dashed rgba(255,255,255,.35);display:grid;place-items:center" class="bn-body m"><span style="font-size:20px">আয়োজকের<br>লোগো</span></div></div>
</div>
""")

# ---------------------------------------------------------------- DES-11 owner one-pager, A4 ratio (1240x1754 @2x)
BEN = [("ফ্রি লিস্টিং", "খালি স্লট আর দাম ঢাকার খেলোয়াড়দের সামনে"),
       ("টাকা আমরা সংগ্রহ করি", "প্রতি সপ্তাহে আপনার ব্যাংক, bKash বা Nagad-এ"),
       ("টুর্নামেন্ট বুকিং", "অর্গানাইজাররা টানা কয়েক রাত আপনার মাঠ বুক করে"),
       ("ওনার ড্যাশবোর্ড", "বুকিং, ওয়াক-ইন, ব্লক স্লট, ডিসকাউন্ট আর আয়"),
       ("ফ্রি মার্কেটিং", "স্পটলাইট পোস্ট আর মাঠের জন্য পোস্টার")]
page("DES-11_owner_one_pager", 1240, 1754, atmosphere(floor=False) + f"""
<div style="position:absolute;left:90px;top:80px">{brand(60, 44)}</div>
<div style="position:absolute;right:90px;top:90px"><span class="tag" style="font-size:22px">টার্ফ মালিকদের জন্য</span></div>
<div style="position:absolute;left:90px;top:220px;width:700px">
  <div class="bn" style="font-size:118px">আপনার টার্ফ,</div>
  <div class="bn g glow" style="font-size:118px">আরও বুকিং</div>
  <p class="bn-body" style="font-size:34px;color:var(--muted2);margin-top:26px">ঢাকার খেলোয়াড়রা Sportzy-তে আপনার খালি স্লট আর দাম দেখে, অনলাইনে বুক আর পে করে।</p>
</div>
{phone("turfdetail-mobile.png", 860, 230, 270, 6)}
<div style="position:absolute;left:90px;right:90px;top:800px;display:grid;grid-template-columns:1fr 1fr;gap:18px">
  {''.join(f'<div class="card" style="padding:20px 26px;display:flex;gap:20px;align-items:flex-start{";grid-column:span 2" if i == 5 else ""}"><span class="mono" style="font-size:24px;color:var(--ink);background:var(--green);border-radius:10px;padding:6px 11px">0{i}</span><div><div class="bn" style="font-size:40px;font-weight:700">{a}</div><div class="bn-body m" style="font-size:25px;margin-top:2px">{b}</div></div></div>' for i, (a, b) in enumerate(BEN, 1))}
</div>
<div style="position:absolute;left:90px;right:90px;top:1370px;display:flex;align-items:center;gap:40px;padding:26px 44px;border-radius:30px;background:var(--paper);color:var(--ink)">
  <div class="mono" style="font-size:116px;line-height:1">8%</div>
  <div><div class="bn" style="font-size:42px">শুধু Sportzy-র আনা বুকিংয়ে</div>
  <div class="bn-body" style="font-size:28px;color:#2a4a36;margin-top:6px">লিস্টিং ফ্রি। আপনার নিজের ওয়াক-ইনে কোনো কমিশন নেই।</div></div>
</div>
<div style="position:absolute;left:90px;right:90px;bottom:76px;display:flex;justify-content:space-between;align-items:center">
  <div><div class="bn" style="font-size:44px">১০ মিনিটে সেটআপ, <span class="g">আপনার ফোনেই</span></div>
  <div class="mono m" style="font-size:28px;margin-top:10px">WhatsApp 01XXX-XXXXXX · sportzy.live</div></div>
  <span class="cta" style="font-size:32px">যোগাযোগ করুন {ARROW}</span>
</div>
""", scale=2)

# ---------------------------------------------------------------- DES-12 organiser social card 1080x1350
ORG = ["অনলাইনে টিম রেজিস্ট্রেশন", "QR Pay BD-তে এন্ট্রি ফি", "পে করার সময় স্পট হোল্ড", "রিফান্ড আমরা সামলাই", "ফিক্সচার আর মাঠের স্লট এক জায়গায়", "ফাইনাল ফেসবুক-ইউটিউবে লাইভ"]
page("DES-12_organiser_card", 1080, 1350, atmosphere() + head('<span class="tag">অর্গানাইজারদের জন্য</span>') + f"""
<div style="position:absolute;left:72px;top:190px;width:940px">
  <div class="bn-body y" style="font-size:32px;margin-bottom:14px">১২টা bKash স্ক্রিনশট মেলানো আর না।</div>
  <div class="bn" style="font-size:86px;white-space:nowrap">টুর্নামেন্ট আপনি চালান,</div>
  <div class="bn g glow" style="font-size:86px;white-space:nowrap">টাকার হিসাব আমাদের</div>
</div>
<div style="position:absolute;left:72px;top:470px;width:600px;display:grid;gap:14px">
  {''.join(f'<div style="display:flex;gap:16px;align-items:center" class="card"><div style="padding:18px 0 18px 22px">{CHECK.replace("<svg", "<svg width=34 height=34")}</div><div class="bn" style="font-size:31px;font-weight:700;padding-right:18px;white-space:nowrap">{t}</div></div>' for t in ORG)}
</div>
{phone("managematch-mobile.png", 700, 500, 350, 6)}
{cta_block("মেসেজ করুন")}
""")

# ---------------------------------------------------------------- DES-13 open slots story 1080x1920 (SAMPLE slots)
SLOTS = [("Pitch 9 Arena", "মিরপুর", "8:00 PM", "৳1,800", ""), ("Wari Floodlit Field", "ওয়ারী", "9:00 PM", "৳1,500", "শেষ স্লট"),
         ("Banani Sports Field", "বনানী", "9:30 PM", "৳2,200", ""), ("Uttara Box Cricket", "উত্তরা", "10:00 PM", "৳1,600", ""),
         ("Mirpur Night Turf", "মিরপুর", "11:00 PM", "৳1,200", "")]
page("DES-13_open_slots_story_sample", 1080, 1920, atmosphere() + f"""
<div style="position:absolute;left:72px;top:270px">{brand()}</div>
<div style="position:absolute;right:72px;top:276px"><span class="tag">আজ রাত</span></div>
<div style="position:absolute;left:72px;top:390px">
  <div class="mono g" style="font-size:26px;letter-spacing:5px;margin-bottom:16px">TONIGHT IN DHAKA</div>
  <div class="bn" style="font-size:150px">আজ রাতে</div>
  <div class="bn g glow" style="font-size:150px">খালি স্লট</div>
</div>
<div class="card" style="position:absolute;left:72px;right:72px;top:800px;padding:10px 0;box-shadow:0 30px 90px rgba(0,0,0,.5)">
  {''.join(f'<div style="display:flex;align-items:center;justify-content:space-between;padding:22px 34px;{"border-top:1.5px solid var(--line)" if i else ""}"><div><div style="font:800 34px Manrope">{v}</div><div class="bn-body m" style="font-size:26px">{a}{(" &nbsp;<span class=badge style=font-size:20px;padding:3px 10px>" + b + "</span>") if b else ""}</div></div><div style="text-align:right"><div class="mono y" style="font-size:40px">{t}</div><div class="mono" style="font-size:28px;color:var(--text)">{pr}</div></div></div>' for i, (v, a, t, pr, b) in enumerate(SLOTS))}
</div>
<div style="position:absolute;left:72px;right:72px;top:1560px;display:flex;justify-content:space-between;align-items:center">
  <span class="cta">এখনই বুক করো {ARROW}</span><span class="url">sportzy.live</span>
</div>
""")

# ---------------------------------------------------------------- DES-17 paid ad static, C2 "tonight" angle 1080x1080
page("DES-17_ad_tonight", 1080, 1080, atmosphere() + head() + f"""
<div style="position:absolute;left:72px;top:190px;width:560px">
  <div class="bn" style="font-size:122px;white-space:nowrap">আজ রাতে</div>
  <div class="bn g glow" style="font-size:122px">খেলবে?</div>
  <p class="bn-body" style="font-size:34px;color:var(--muted2);margin-top:26px">ঢাকার খালি স্লট আর দাম, এক সার্চে। বুক করো মিনিটেই।</p>
  <div style="margin-top:30px">{PAY}</div>
</div>
{phone("main-mobile.png", 650, 170, 360, 7, 90)}
{cta_block("স্লট খোঁজো")}
""")


if __name__ == "__main__":
    print("built", len(list(HERE.glob("*.html"))), "designs")
