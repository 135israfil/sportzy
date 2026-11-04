"""Builds the Sportzy marketing designs as HTML; render.js turns them into PNGs.

  python3 build.py                              # all designs + template samples -> ../*.png (after: node render.js)
  python3 build.py fill <template> <data.json>  # one real post from your data -> ../out/ (renders it too)

Templates and their sample data live in templates.py and ../data/*.json.
Anything built from sample data is marked SAMPLE and must not be published as-is.
"""
import json, subprocess, sys, datetime, re
from kit import *
from templates import TEMPLATES

DATA = HERE.parent / "data"

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


# ================================================================ new designs (Nov 2026)
# LAUNCH_DATE_* live in kit.py (shared with the videos)

SWIPE = '<div style="position:absolute;left:72px;bottom:72px;display:flex;align-items:center;gap:14px" class="mono m"><span style="font-size:24px">{n}/{t}</span><span style="width:64px;height:64px;border-radius:50%;border:2px solid var(--green);display:grid;place-items:center;color:var(--green)">' + ARROW.replace("<svg", "<svg width=28 height=28") + '</span></div>'
RAIL = '<div style="position:absolute;left:0;right:0;top:1176px;height:3px;background:linear-gradient(90deg,rgba(47,214,123,.0),rgba(47,214,123,.7),rgba(47,214,123,.0))"></div>'
BETA = '<span style="display:inline-block;border:1.5px solid var(--yellow);color:var(--yellow);border-radius:8px;padding:4px 10px;font:700 20px Manrope;letter-spacing:2px;vertical-align:middle;margin-left:12px">BETA</span>'

# ---------------------------------------------------------------- DES-01 brand intro carousel, 6 slides 1080x1350
CAROUSEL = [
    ("BOOK", "YOUR TURF.", "খালি স্লট আর আসল দাম, এক জায়গায়। বুক করো, bKash বা Nagad-এ পে করো।", ("main-mobile.png", 0), ""),
    ("PLAY", "TONIGHT.", "খেলোয়াড় কম? ম্যাচে স্পট খুলে দাও, খেলোয়াড় নিজেই রিকোয়েস্ট পাঠাবে।", ("discover-mobile.png", 0), ""),
    ("SCORE", "EVERY GOAL.", "Scorezy-তে লাইভ স্কোর, পুরো ম্যাচ জুড়ে।", ("matchroster-mobile.png", 0), BETA),
    ("STREAM", "THE FINAL.", "Streemzy দিয়ে ফাইনাল লাইভ, ফেসবুক আর ইউটিউবে একসাথে।", None, BETA),
    ("SHARE", "ONE LINK.", "একটা লিংকে পুরো টিম। কারও অ্যাপ নামাতে হবে না।", ("managematch-mobile.png", 0), ""),
]
for i, (w1, w2, bn, scr, tag) in enumerate(CAROUSEL, 1):
    visual = phone(scr[0], 600, 560, 400, 6, scr[1]) if scr else f"""
<div class="card" style="position:absolute;left:560px;top:600px;width:450px;padding:36px;box-shadow:0 40px 100px rgba(0,0,0,.6)">
  <span class="badge" style="font-family:Anton;font-size:30px;letter-spacing:2px">● LIVE</span>
  <div class="en" style="font-size:64px;margin-top:26px">LIONS <span class="y">vs</span><br>STRIKERS</div>
  <div class="mono" style="font-size:96px;margin-top:18px;background:var(--paper);color:var(--ink);border-radius:18px;text-align:center;padding:8px 0">2–1</div>
  <div style="display:flex;gap:10px;margin-top:24px">{''.join(f'<span style="padding:10px 16px;border-radius:10px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.16);font:700 22px Manrope">{p}</span>' for p in ["Facebook", "YouTube"])}</div>
</div>"""
    page(f"DES-01_brand_carousel_0{i}", 1080, 1350, atmosphere() + RAIL + f"""
<div style="position:absolute;left:72px;top:72px" class="mono g"><span style="font-size:24px;letter-spacing:4px">SPORTZY · 0{i}</span></div>
<div style="position:absolute;left:72px;top:150px">
  <div class="en" style="font-size:190px">{w1}</div>
  <div class="en g glow" style="font-size:150px">{w2}</div>
  <p class="bn-body" style="font-size:36px;color:var(--muted2);margin-top:34px;width:470px">{bn}{tag}</p>
</div>
{visual}
{SWIPE.format(n=i, t=6)}""")

page("DES-01_brand_carousel_06", 1080, 1350, atmosphere() + RAIL + f"""
<div style="position:absolute;left:0;right:0;top:250px;text-align:center;display:grid;justify-items:center;gap:30px">
  <img src="{LOGO}" style="width:200px;height:200px;filter:drop-shadow(0 0 50px rgba(47,214,123,.5))">
  <div class="en" style="font-size:150px;letter-spacing:4px">SPORTZY</div>
  <div class="bn" style="font-size:64px">বুক · খেলা · স্কোর · লাইভ · শেয়ার</div>
  <div class="mono y" style="font-size:34px;letter-spacing:4px">LAUNCHING {LAUNCH_DATE_EN.upper()} · DHAKA</div>
</div>
<div style="position:absolute;left:0;right:0;top:880px;display:grid;justify-items:center;gap:22px">
  <span class="cta">পোস্টটা সেভ করে রাখো {ARROW}</span><span class="url">sportzy.live</span>
</div>""")

# ---------------------------------------------------------------- DES-02 "7 stages of booking a turf" carousel, 7 slides
def bub(text, out=False, t=""):
    side = "justify-self:end;background:var(--green);color:var(--ink);border-bottom-right-radius:8px" if out else "justify-self:start;background:#16301F;color:var(--text);border-bottom-left-radius:8px"
    ts = f'<div class="mono" style="font-size:22px;opacity:.6;margin-top:8px;text-align:right">{t}</div>' if t else ""
    return f'<div style="max-width:82%;padding:24px 32px;border-radius:34px;{side}"><div class="bn-body" style="font-size:44px;line-height:1.35">{text}</div>{ts}</div>'


def note(text):
    return f'<div class="bn-body m" style="justify-self:center;font-size:30px;padding:10px 22px;border-radius:99px;background:rgba(255,255,255,.06)">{text}</div>'


STAGES = [
    ("স্লট খোঁজা", "টার্ফ ম্যানেজার", [bub("ভাই, আজ রাতে স্লট আছে?", True, "8:02 PM"), bub("দেখে জানাচ্ছি ভাই", False, "8:10 PM")]),
    ("অপেক্ষা", "টার্ফ ম্যানেজার", [bub("ভাই?", True, "8:40 PM"), bub("৮টা বা ৯টা, যেকোনো একটা হলেই হবে", True, "9:05 PM"), note("Seen 9:06 PM")]),
    ("আরেক টার্ফে ফোন", "আরেক টার্ফ", [note("মিসড কল ×৩"), bub("সন্ধ্যা সব বুকড ভাই। সাড়ে ১১টা খালি আছে।", False, "9:31 PM")]),
    ("টিম জোগাড়", "ফুটবল গ্রুপ", [bub("আজ রাত সাড়ে ১১টা, কে কে আসবি?", True, "9:35 PM"), bub("আসছি", False), bub("আমিও আসছি", False), note("১৪ জন বলল 'আসছি'। কনফার্ম: ৬ জন")]),
    ("অ্যাডভান্স", "আরেক টার্ফ", [bub("অ্যাডভান্স ৫০০ টাকা পাঠান, স্ক্রিনশট দিয়েন", False, "9:50 PM"), bub("পাঠালাম ভাই, স্ক্রিনশট দিলাম", True, "9:58 PM"), bub("পাইনি ভাই, আবার দেন", False, "10:20 PM")]),
    ("টাকা তোলা", "ফুটবল গ্রুপ", [bub("সবাই ২০০ করে পাঠাও", True, "10:25 PM"), bub("কাল দিব", False), bub("নগদে নিবি?", False), bub("আমি তো আজ খেলবই না", False)]),
]
for i, (title, who, msgs) in enumerate(STAGES, 1):
    page(f"DES-02_seven_stages_0{i}", 1080, 1350, atmosphere(floor=False) + f"""
<div style="position:absolute;left:72px;top:80px">
  <div class="en y" style="font-size:150px">STAGE {i}</div>
  <div class="bn" style="font-size:72px;margin-top:6px">{title}</div>
</div>
<div class="card" style="position:absolute;left:72px;right:72px;top:420px;height:760px;overflow:hidden;box-shadow:0 40px 100px rgba(0,0,0,.5)">
  <div style="display:flex;align-items:center;gap:18px;padding:24px 30px;border-bottom:1.5px solid var(--line)">
    <div style="width:64px;height:64px;border-radius:50%;background:#1E3829;display:grid;place-items:center" class="bn"><span style="font-size:30px">{who[0]}</span></div>
    <div><div class="bn" style="font-size:34px;font-weight:700">{who}</div><div class="mono m" style="font-size:18px">online</div></div>
  </div>
  <div style="display:grid;gap:30px;padding:44px 34px">{''.join(msgs)}</div>
</div>
<div style="position:absolute;right:72px;bottom:86px" class="bn-body m"><span style="font-size:30px">তুমি কোন স্টেজে? কমেন্ট করো।</span></div>
{SWIPE.format(n=i, t=7)}""")

page("DES-02_seven_stages_07", 1080, 1350, atmosphere() + f"""
<div style="position:absolute;left:72px;top:80px">
  <div class="en y" style="font-size:150px">STAGE 7</div>
  <div class="bn" style="font-size:66px;margin-top:6px;width:930px">রাত সাড়ে ১১টায় খেলা, কারণ শুধু ওটাই বাকি ছিল।</div>
</div>
<div class="card" style="position:absolute;left:72px;right:72px;top:560px;padding:44px 48px;border-color:rgba(47,214,123,.5);box-shadow:0 0 80px rgba(47,214,123,.18)">
  {brand()}
  <div class="bn" style="font-size:68px;margin-top:30px">এবার থেকে <span class="g">এক জায়গায়:</span></div>
  <div style="display:grid;gap:20px;margin-top:30px">{''.join(f'<div style="display:flex;gap:18px;align-items:center">{CHECK.replace("<svg", "<svg width=42 height=42")}<span class="bn" style="font-size:46px;font-weight:700">{t}</span></div>' for t in ["খালি স্লট আর দাম দেখো", "বুক করো, bKash বা Nagad-এ পে করো", "টিমকে একটা লিংক পাঠাও"])}</div>
</div>
<div style="position:absolute;left:72px;right:72px;bottom:80px;display:flex;justify-content:space-between;align-items:center">
  <span class="cta">আসছে {LAUNCH_DATE_BN} {ARROW}</span><span class="url">sportzy.live</span>
</div>""")

# ---------------------------------------------------------------- DES-03 launch countdown, 7 story frames 1080x1920 + feed 1080x1080
COUNT = {7: "ঢাকার টার্ফ, খালি স্লট এক জায়গায়", 6: "দাম আগে দেখো, তারপর বুক করো", 5: "bKash, Nagad বা QR Pay BD", 4: "পে করার সময় স্লট তোমার জন্য হোল্ড",
         3: "একটা লিংকে পুরো টিম", 2: "টুর্নামেন্ট রেজিস্ট্রেশনও এখানেই", 1: LAUNCH_DAY_BN}
BN_DIGIT = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
for n, line in COUNT.items():
    days = "কাল লঞ্চ" if n == 1 else f"{str(n).translate(BN_DIGIT)} দিন বাকি"
    page(f"DES-03_countdown_story_{n}", 1080, 1920, atmosphere() + f"""
<div style="position:absolute;left:72px;top:270px">{brand()}</div>
<div style="position:absolute;right:72px;top:276px"><span class="tag">{LAUNCH_DATE_BN}</span></div>
<div style="position:absolute;left:0;right:0;top:430px;text-align:center">
  <div class="en g glow" style="font-size:680px;line-height:.9">{n}</div>
  <div class="bn" style="font-size:96px;margin-top:10px">{days}</div>
  <div class="bn-body" style="font-size:44px;color:var(--muted2);margin:30px auto 0;width:860px">{line}</div>
</div>
<div style="position:absolute;left:0;right:0;top:1440px;display:grid;justify-items:center;gap:22px">
  <span class="cta">নোটিফিকেশন অন করো {ARROW}</span><span class="url">sportzy.live</span>
</div>""")

page("DES-03_countdown_feed", 1080, 1080, atmosphere() + head(f'<span class="tag">{LAUNCH_DATE_BN}</span>') + f"""
<div style="position:absolute;left:72px;top:200px">
  <div class="mono y" style="font-size:26px;letter-spacing:5px">LAUNCHING IN DHAKA</div>
  <div class="en" style="font-size:210px;margin-top:16px">{LAUNCH_DATE_EN.upper()}</div>
  <div class="bn g glow" style="font-size:84px;margin-top:4px">{LAUNCH_DAY_BN}</div>
  <p class="bn-body" style="font-size:36px;color:var(--muted2);margin-top:22px">টার্ফ বুকিং, টুর্নামেন্ট আর লাইভ ম্যাচ, এক জায়গায়।</p>
</div>
{cta_block("নোটিফিকেশন অন করো")}""")

# ---------------------------------------------------------------- DES-16 corporate league: LinkedIn 1200x627 + feed 1080x1350
CORP = ["Fixtures and booked turf slots", "Online team registration", "Live-streamed final with your branding", "Standings, MVP and certificates", "Photo and highlight pack"]
corp_list = lambda fs: "".join(f'<div style="display:flex;gap:16px;align-items:center">{CHECK.replace("<svg", f"<svg width={fs} height={fs}")}<span style="font:700 {fs}px Manrope">{t}</span></div>' for t in CORP)
page("DES-16_corporate_league_linkedin", 1200, 627, atmosphere() + f"""
<div style="position:absolute;left:60px;top:48px">{brand(44, 32)}</div>
<div style="position:absolute;right:60px;top:52px"><span class="tag" style="font-size:16px">For HR and sports clubs</span></div>
<div style="position:absolute;left:60px;top:130px;width:620px">
  <div class="en" style="font-size:78px">A LEAGUE YOUR TEAM</div>
  <div class="en g glow" style="font-size:78px">WILL TURN UP FOR</div>
  <div class="mono y" style="font-size:20px;margin-top:22px;letter-spacing:1px">6–12 TEAMS · 4–8 WEEKS · FUTSAL / 5-A-SIDE / BOX CRICKET</div>
</div>
<div class="card" style="position:absolute;right:60px;top:130px;width:450px;padding:28px 30px;display:grid;gap:14px">{corp_list(22)}</div>
<div style="position:absolute;left:60px;bottom:48px;display:flex;align-items:center;gap:24px"><span class="cta" style="font-family:Manrope;font-size:24px;padding:16px 26px">Ask for a one-page plan {ARROW}</span><span class="url" style="font-size:22px">sportzy.live</span></div>
""")

page("DES-16_corporate_league_feed", 1080, 1350, atmosphere() + head('<span class="tag">For HR and sports clubs</span>') + f"""
<div style="position:absolute;left:72px;top:190px">
  <div class="mono y" style="font-size:24px;letter-spacing:4px">INTER-DEPARTMENT LEAGUES · DHAKA</div>
  <div class="en" style="font-size:118px;margin-top:20px">A LEAGUE</div>
  <div class="en" style="font-size:118px">YOUR TEAM</div>
  <div class="en g glow" style="font-size:118px">WILL TURN UP FOR</div>
</div>
<div class="card" style="position:absolute;left:72px;right:72px;top:640px;padding:36px 40px;display:grid;gap:20px">{corp_list(32)}</div>
<div style="position:absolute;left:72px;top:1060px" class="mono m"><span style="font-size:24px">6–12 teams · 4–8 weeks · weeknight evenings at partner turfs</span></div>
<div style="position:absolute;left:72px;bottom:64px;display:grid;gap:20px;justify-items:start"><span class="cta" style="font-family:Manrope;font-size:30px">Ask for a one-page plan {ARROW}</span><span class="url" style="padding-left:8px">sportzy.live</span></div>
""")


def build_template(name, data, out_name):
    fn, _ = TEMPLATES[name]
    w, h, body, scale = fn(data)
    page(out_name, w, h, body, scale=scale)


SAMPLES = {"live_thumbnail": "live_thumbnail", "turf_spotlight": "turf_spotlight", "tournament": "tournament", "fixtures": "fixtures",
           "standings": "fixtures", "open_slots": "open_slots", "captain": "captain", "ramadan": "ramadan"}

if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "fill":
        name, path = sys.argv[2], sys.argv[3]
        if name not in TEMPLATES:
            sys.exit("unknown template; choose one of: " + ", ".join(TEMPLATES))
        data = json.loads(open(path, encoding="utf-8").read())
        stamp = re.sub(r"[^A-Za-z0-9_-]", "", data.get("_label", "")) or datetime.date.today().isoformat()
        out = f"out__{TEMPLATES[name][1]}_{stamp}"
        build_template(name, data, out)
        subprocess.run(["node", str(HERE / "render.js"), out], check=True)
        sys.exit(0)
    for name, file in SAMPLES.items():
        d = json.loads((DATA / f"{file}.json").read_text(encoding="utf-8"))
        build_template(name, d, TEMPLATES[name][1] + "_sample")
    d = json.loads((DATA / "ramadan.json").read_text(encoding="utf-8")); d["format"] = "a3"
    build_template("ramadan", d, "DES-15_ramadan_nights_poster_sample")
    print("built", len([p for p in HERE.glob("*.html") if not p.name.startswith("out__")]), "designs")
