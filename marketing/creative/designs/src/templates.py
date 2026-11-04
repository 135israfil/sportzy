"""Data-driven Sportzy templates. Each function takes a dict (from ../data/<name>.json)
and returns (width, height, body_html, scale). build.py renders the sample data;
`python3 build.py fill <template> <file.json>` renders a real version into ../out/.
"""
from kit import ARROW, CHECK, PAY, atmosphere, brand, cta_block, head, phone


def chip(text, size=26):
    tick = CHECK.replace("<svg", f"<svg width={int(size*.85)} height={int(size*.85)}")
    return (f'<span style="display:inline-flex;gap:10px;align-items:center;background:rgba(255,255,255,.05);'
            f'border:1.5px solid var(--line);border-radius:99px;padding:12px 20px" class="bn-body">'
            f'<span style="font-size:{size}px">{tick} {text}</span></span>')


# ---------------------------------------------------------------- DES-06 live stream thumbnail 1280x720
def live_thumbnail(d):
    a, b = d["team_a"].upper(), d["team_b"].upper()
    body = atmosphere() + f"""
<div style="position:absolute;left:60px;top:52px">{brand(46, 34)}</div>
<div style="position:absolute;left:60px;top:150px">
  <span class="badge" style="font-size:34px;padding:10px 20px;font-family:Anton;letter-spacing:2px">● LIVE</span>
  <div class="en" data-fit="640" style="font-size:150px;margin-top:26px">{a}</div>
  <div class="en y" style="font-size:70px;margin:6px 0 6px 6px">VS</div>
  <div class="en g glow" data-fit="640" style="font-size:150px">{b}</div>
</div>
<div class="card" style="position:absolute;right:70px;top:170px;width:430px;padding:34px;text-align:center;box-shadow:0 30px 80px rgba(0,0,0,.5)">
  <div class="bn" style="font-size:44px">{d["stage_bn"]}</div>
  <div style="background:var(--paper);color:var(--ink);border-radius:22px;margin:22px 0;padding:18px 0" class="mono"><span style="font-size:130px;line-height:1">{d["score"]}</span></div>
  <div class="mono m" style="font-size:24px">{d["event"].upper()}</div>
</div>"""
    return 1280, 720, body, 1


# ---------------------------------------------------------------- DES-08 turf spotlight 1080x1350
def turf_spotlight(d):
    l1, l2 = d["title_line1"].upper(), d["title_line2"].upper()
    rows = [("খেলা", d["sports_bn"], "bn", 40), ("ফ্লাডলাইট", d["floodlit_until_bn"], "bn", 40), ("দাম শুরু", d["price_from"], "mono y", 44)]
    cards = "".join(f'<div class="card" style="padding:20px 24px"><div class="bn-body m" style="font-size:24px">{a}</div><div class="{c}" style="font-size:{fs_}px;margin-top:4px">{b}</div></div>' for a, b, c, fs_ in rows)
    verified = (f'<div><span style="display:inline-flex;gap:10px;align-items:center;border:1.5px solid rgba(47,214,123,.6);border-radius:99px;padding:10px 18px;font:700 22px Manrope;color:var(--green)">'
                f'{CHECK.replace("<svg", "<svg width=22 height=22")} ভেরিফায়েড ভেন্যু</span></div>') if d.get("verified") else ""
    body = atmosphere() + head('<span class="tag">টার্ফ স্পটলাইট</span>') + f"""
<div style="position:absolute;left:72px;top:190px">
  <div class="mono g" style="font-size:24px;letter-spacing:4px;margin-bottom:18px">TURF OF THE WEEK · {d["area_en"].upper()}</div>
  <div class="en" data-fit="920" style="font-size:150px">{l1}</div>
  <div class="en g glow" data-fit="920" style="font-size:150px">{l2}</div>
</div>
<div style="position:absolute;left:72px;top:620px;width:500px;display:grid;gap:16px">{cards}{verified}</div>
{phone(d.get("screen", "turfdetail-mobile.png"), 640, 470, 390, 5)}
{cta_block(d.get("cta_bn", "এখানে বুক করো"))}"""
    return 1080, 1350, body, 1


# ---------------------------------------------------------------- DES-09 tournament announcement 1080x1350
def tournament(d):
    l1, l2 = d["title_line1"].upper(), d["title_line2"].upper()
    info = [("তারিখ", d["dates_bn"], "bn", ""), ("ভেন্যু", d["venue"], "bn", "border-left:1.5px solid var(--line);border-right:1.5px solid var(--line)"), ("এন্ট্রি ফি", d["fee"], "mono y", "")]
    cells = "".join(f'<div style="padding:30px 10px;{bd}"><div class="bn-body m" style="font-size:24px">{a}</div><div class="{c}" style="font-size:38px;margin-top:6px">{b}</div></div>' for a, b, c, bd in info)
    badge = f'<div style="position:absolute;left:0;right:0;top:850px;text-align:center"><span class="badge" style="font-size:44px;padding:14px 30px;transform:rotate(-2deg);display:inline-block">{d["spots_badge_bn"]}</span></div>' if d.get("spots_badge_bn") else ""
    body = atmosphere() + head('<span class="tag">রেজিস্ট্রেশন চলছে</span>') + f"""
<div style="position:absolute;left:72px;right:72px;top:180px;text-align:center">
  <div class="mono y" style="font-size:26px;letter-spacing:6px">{d["kicker_en"].upper()}</div>
  <div class="en" data-fit="936" style="font-size:190px;margin:20px auto 0">{l1}</div>
  <div class="en g glow" data-fit="936" style="font-size:190px;margin:0 auto">{l2}</div>
</div>
<div class="card" style="position:absolute;left:72px;right:72px;top:640px;display:grid;grid-template-columns:repeat(3,1fr);text-align:center">{cells}</div>
{badge}
<div style="position:absolute;left:72px;right:72px;top:990px;display:flex;justify-content:center;gap:14px;flex-wrap:wrap">{"".join(chip(t) for t in d["features_bn"])}</div>
<div style="position:absolute;left:72px;right:72px;bottom:64px;display:flex;justify-content:space-between;align-items:flex-end">
  <div style="display:grid;gap:20px;justify-items:start"><span class="cta">টিম রেজিস্টার করো {ARROW}</span><span class="url" style="padding-left:8px">sportzy.live</span></div>
  <div style="width:120px;height:120px;border-radius:50%;border:2px dashed rgba(255,255,255,.35);display:grid;place-items:center;text-align:center" class="bn-body m"><span style="font-size:20px">আয়োজকের<br>লোগো</span></div>
</div>"""
    return 1080, 1350, body, 1


# ---------------------------------------------------------------- DES-13 open slots story 1080x1920 (max 5 rows)
def open_slots(d):
    slots = d["slots"][:5]
    rows = "".join(
        f'<div style="display:flex;align-items:center;justify-content:space-between;padding:22px 34px;{"border-top:1.5px solid var(--line)" if i else ""}">'
        f'<div><div data-fit="560" style="font:800 34px Manrope">{s["venue"]}</div><div class="bn-body m" style="font-size:26px">{s["area_bn"]}'
        f'{(" &nbsp;<span class=badge style=font-size:20px;padding:3px 10px>" + s["badge_bn"] + "</span>") if s.get("badge_bn") else ""}</div></div>'
        f'<div style="text-align:right;white-space:nowrap"><div class="mono y" style="font-size:40px">{s["time"]}</div><div class="mono" style="font-size:28px;color:var(--text)">{s["price"]}</div></div></div>'
        for i, s in enumerate(slots))
    body = atmosphere() + f"""
<div style="position:absolute;left:72px;top:270px">{brand()}</div>
<div style="position:absolute;right:72px;top:276px"><span class="tag">{d.get("tag_bn", "আজ রাত")}</span></div>
<div style="position:absolute;left:72px;top:390px">
  <div class="mono g" style="font-size:26px;letter-spacing:5px;margin-bottom:16px">{d.get("kicker_en", "TONIGHT IN DHAKA").upper()}</div>
  <div class="bn" data-fit="936" style="font-size:150px">{d.get("title_line1_bn", "আজ রাতে")}</div>
  <div class="bn g glow" data-fit="936" style="font-size:150px">{d.get("title_line2_bn", "খালি স্লট")}</div>
</div>
<div class="card" style="position:absolute;left:72px;right:72px;top:800px;padding:10px 0;box-shadow:0 30px 90px rgba(0,0,0,.5)">{rows}</div>
<div style="position:absolute;left:72px;right:72px;top:1560px;display:flex;justify-content:space-between;align-items:center">
  <span class="cta">এখনই বুক করো {ARROW}</span><span class="url">sportzy.live</span>
</div>"""
    return 1080, 1920, body, 1


# ---------------------------------------------------------------- DES-10 fixtures card 1080x1350 (max 6 fixtures)
def _event_head(d, tag):
    return atmosphere() + head(f'<span class="tag">{tag}</span>') + f"""
<div style="position:absolute;left:72px;top:180px">
  <div class="mono y" style="font-size:24px;letter-spacing:5px;margin-bottom:14px">{d["event"].upper()}</div>"""


def fixtures(d):
    rows = "".join(
        f'<div style="display:grid;grid-template-columns:150px 1fr 120px;align-items:center;padding:24px 30px;{"border-top:1.5px solid var(--line)" if i else ""}">'
        f'<div class="mono y" style="font-size:30px">{f["time"]}</div>'
        f'<div data-fit="560" style="font:800 32px Manrope">{f["home"]} <span class="mono m" style="font-size:24px;margin:0 10px">vs</span> {f["away"]}</div>'
        f'<div class="bn-body m" style="font-size:24px;text-align:right">{f["court_bn"]}</div></div>'
        for i, f in enumerate(d["fixtures"][:6]))
    body = _event_head(d, d.get("date_bn", "")) + f"""
  <div class="en" style="font-size:130px">ROUND {d["round"]}</div>
  <div class="en g glow" style="font-size:130px">FIXTURES</div>
</div>
<div class="card" style="position:absolute;left:72px;right:72px;top:560px;padding:6px 0">{rows}</div>
{cta_block("ফিক্সচার দেখো")}
<div style="position:absolute;right:72px;bottom:72px" class="bn-body m"><span style="font-size:26px">{d["venue"]}</span></div>"""
    return 1080, 1350, body, 1


def standings(d):
    head_row = "".join(f'<div class="mono m" style="font-size:22px;text-align:center">{h}</div>' for h in ["P", "W", "D", "L", "PTS"])
    rows = "".join(
        f'<div style="display:grid;grid-template-columns:60px 1fr repeat(5,72px);align-items:center;padding:13px 30px;{"border-top:1.5px solid var(--line)" if i else ""}{";background:rgba(47,214,123,.08)" if i < d.get("qualify", 0) else ""}">'
        f'<div class="mono {"g" if i < d.get("qualify", 0) else "m"}" style="font-size:28px">{i + 1}</div><div style="font:800 32px Manrope">{t["team"]}</div>'
        + "".join(f'<div class="mono" style="font-size:28px;text-align:center{";color:var(--yellow)" if k == "pts" else ""}">{t[k]}</div>' for k in ["p", "w", "d", "l", "pts"])
        + "</div>"
        for i, t in enumerate(d["table"][:8]))
    body = _event_head(d, d.get("date_bn", "")) + f"""
  <div class="en" style="font-size:110px">STANDINGS</div>
  <div class="en g glow" style="font-size:110px">AFTER ROUND {d["round"]}</div>
</div>
<div class="card" style="position:absolute;left:72px;right:72px;top:500px;padding:6px 0">
  <div style="display:grid;grid-template-columns:60px 1fr repeat(5,72px);padding:16px 30px 6px"><div></div><div></div>{head_row}</div>{rows}
</div>
<div style="position:absolute;left:72px;bottom:72px" class="bn-body m"><span style="font-size:26px">সবুজ = পরের রাউন্ডে · {d["venue"]}</span></div>"""
    return 1080, 1350, body, 1


# ---------------------------------------------------------------- DES-14 founding captain card 1080x1350
def captain(d):
    photo = (f'<img src="{d["photo"]}" style="width:100%;height:100%;object-fit:cover">' if d.get("photo")
             else f'<span class="en" style="font-size:180px;color:var(--ink)">{d["initials"]}</span>')
    body = atmosphere() + head('<span class="tag">ফাউন্ডিং ক্যাপ্টেন</span>') + f"""
<div style="position:absolute;left:50%;top:190px;transform:translateX(-50%);width:760px;height:1000px;border-radius:44px;
  background:linear-gradient(160deg,#123322,#0A1D12 55%,#0E2617);border:2px solid rgba(244,224,77,.55);
  box-shadow:0 0 0 10px rgba(244,224,77,.08),0 50px 120px rgba(0,0,0,.6);overflow:hidden;text-align:center">
  <div style="position:absolute;inset:0;background:repeating-linear-gradient(115deg,rgba(244,224,77,.06) 0 2px,transparent 2px 26px)"></div>
  <div class="mono y" style="position:relative;font-size:24px;letter-spacing:6px;margin-top:56px">SPORTZY · FOUNDING CAPTAIN · {d["number"]}</div>
  <div style="position:relative;margin:50px auto 0;width:400px;height:400px;border-radius:50%;overflow:hidden;display:grid;place-items:center;
    background:radial-gradient(circle at 35% 30%,#7CF0B0,#2FD67B 60%,#1A9C56);box-shadow:0 0 0 8px #0A1D12,0 0 0 12px var(--yellow)">{photo}</div>
  <div class="en" data-fit="680" style="position:relative;font-size:110px;margin:56px auto 0">{d["name"].upper()}</div>
  <div class="bn" style="position:relative;font-size:44px;color:var(--green);margin-top:12px">{d["team_bn"]}</div>
  <div class="bn-body m" style="position:relative;font-size:28px;margin-top:8px">{d["area_bn"]} · {d["since_bn"]}</div>
  <div style="position:absolute;left:0;right:0;bottom:56px;display:flex;justify-content:center;gap:12px">
    {''.join(f'<span class="badge" style="font-size:24px">{p}</span>' for p in d["perks_bn"])}
  </div>
</div>
<div style="position:absolute;left:0;right:0;bottom:56px;text-align:center"><span class="url">sportzy.live</span></div>"""
    return 1080, 1350, body, 1


# ---------------------------------------------------------------- DES-15 Ramadan night tournament (post 1080x1350, poster A3 @2x)
def ramadan(d):
    poster = d.get("format") == "a3"
    w, h = (1191, 1684) if poster else (1080, 1350)
    m = 90 if poster else 72
    lanterns = "".join(
        f'<div style="position:absolute;top:0;left:{x}%;width:2px;height:{ln}px;background:rgba(244,224,77,.35)"></div>'
        f'<div style="position:absolute;top:{ln}px;left:calc({x}% - 13px);width:28px;height:40px;border-radius:10px 10px 14px 14px;'
        f'background:radial-gradient(circle at 50% 60%,#fff6c4,#F4E04D 55%,#b89a1c);box-shadow:0 0 30px 10px rgba(244,224,77,.35)"></div>'
        for x, ln in [(44, 110), (56, 170), (68, 90)])
    body = atmosphere() + lanterns + f"""
<div style="position:absolute;right:{m + 10}px;top:{150 if poster else 130}px;width:170px;height:170px;border-radius:50%;box-shadow:-34px 18px 0 0 #F4E04D;filter:drop-shadow(0 0 30px rgba(244,224,77,.5));transform:rotate(-20deg)"></div>
<div style="position:absolute;left:{m}px;top:{m - 10}px">{brand()}</div>
<div style="position:absolute;left:{m}px;right:{m}px;top:{330 if poster else 300}px">
  <div class="bn-body y" style="font-size:32px">{d["greeting_bn"]}</div>
  <div class="en" style="font-size:{180 if poster else 160}px;margin-top:14px">RAMADAN</div>
  <div class="en g glow" style="font-size:{180 if poster else 160}px">NIGHTS</div>
  <div class="bn" style="font-size:{60 if poster else 54}px;margin-top:18px">{d["title_bn"]}</div>
</div>
<div class="card" style="position:absolute;left:{m}px;right:{m}px;top:{960 if poster else 820}px;display:grid;grid-template-columns:1fr 1fr">
  {''.join(f'<div style="padding:26px 30px;{bd}"><div class="bn-body m" style="font-size:24px">{a}</div><div class="{c}" style="font-size:34px;margin-top:4px">{b}</div></div>' for a, b, c, bd in [("সময়", d["time_bn"], "bn", "border-right:1.5px solid var(--line);border-bottom:1.5px solid var(--line)"), ("তারিখ", d["dates_bn"], "bn", "border-bottom:1.5px solid var(--line)"), ("ভেন্যু", d["venue"], "bn", "border-right:1.5px solid var(--line)"), ("এন্ট্রি ফি", d["fee"], "mono y", "")])}
</div>
{cta_block("টিম রেজিস্টার করো", left=m, bottom=m - 8)}"""
    return w, h, body, 2 if poster else 1


TEMPLATES = {
    "live_thumbnail": (live_thumbnail, "DES-06_live_thumbnail"),
    "turf_spotlight": (turf_spotlight, "DES-08_turf_spotlight"),
    "tournament": (tournament, "DES-09_tournament_announcement"),
    "fixtures": (fixtures, "DES-10_fixtures"),
    "standings": (standings, "DES-10_standings"),
    "open_slots": (open_slots, "DES-13_open_slots_story"),
    "captain": (captain, "DES-14_founding_captain"),
    "ramadan": (ramadan, "DES-15_ramadan_nights"),
}
