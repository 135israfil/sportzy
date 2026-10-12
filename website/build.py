#!/usr/bin/env python3
"""Build the static Sportzy marketing site.

Reads page bodies from pages/, wraps them in the shared layout (head + SEO
tags + header + footer), and writes a deploy-ready site to public/.

    python3 build.py

Everything you may need to change before going live is in CONFIG below.
No third-party packages required.
"""
import json
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"
ASSETS = ROOT / "assets"
OUT = ROOT / "public"

CONFIG = {
    # Final public domain of this website, no trailing slash. Used for
    # canonical URLs, sitemap.xml, Open Graph and structured data.
    "SITE_URL": "https://sportzy.live",
    # Where the "Open Scorezy" / "Open Streemzy" buttons send people.
    "SCOREZY_URL": "https://score.sportzy.live",
    "STREEMZY_URL": "https://streemzy.io",
    "CONTACT_EMAIL": "info@sportzy.live",
    "FOUNDER": "Israfil Islam",
    "FOUNDER_LINKEDIN": "https://www.linkedin.com/in/israfil-islam",
    # Optional: Google Analytics 4 measurement ID (e.g. "G-XXXXXXX"). Empty = no analytics.
    "GA4_ID": "",
    # Optional: Google Search Console HTML-tag verification token. Empty = omitted.
    "GSC_VERIFICATION": "",
}

# path -> page metadata. "path" is the public URL path (folder style, clean URLs).
SITE_PAGES = [
    {
        "src": "index.html", "path": "/", "nav": "home", "priority": "1.0",
        "title": "Sportzy — Free Live Sports Streaming & Scoring App",
        "description": "Sportzy is a free live sports streaming and scoring app. Add live scoreboards with Scorezy and stream to Facebook, YouTube & Instagram at once with Streemzy.",
        "schema": ["software_suite", "faq"],
    },
    {
        "src": "scorezy.html", "path": "/scorezy/", "nav": "scorezy", "priority": "0.9",
        "title": "Scorezy — Free Live Scoring & Scoreboard Overlay App",
        "description": "Scorezy is a free live scoring app with a scoreboard overlay for live streams: cricket scorecards, team lineups, lower thirds and sponsor graphics in real time.",
        "crumb": "Scorezy", "schema": ["app_scorezy", "faq"],
    },
    {
        "src": "streemzy.html", "path": "/streemzy/", "nav": "streemzy", "priority": "0.9",
        "title": "Streemzy — Stream to Facebook, YouTube & Instagram at Once",
        "description": "Multistream one live match to Facebook, YouTube and Instagram at the same time. RTMP from any camera or phone, remote commentary, cloud recording. Free beta.",
        "crumb": "Streemzy", "schema": ["app_streemzy", "faq"],
    },
    {
        "src": "visionzy.html", "path": "/visionzy/", "nav": "visionzy", "priority": "0.7",
        "title": "Visionzy — AI Ball Tracking, LBW Review & Highlights",
        "description": "AI ball tracking, LBW and VAR-style review, instant replay and automatic highlights for grassroots sports broadcasts. Coming soon — join the waitlist.",
        "crumb": "Visionzy", "schema": [],
    },
    {
        "src": "app.html", "path": "/app/", "nav": "app", "priority": "0.7",
        "title": "Sportzy App — Multi-Camera Sports Streaming From Phones",
        "description": "The Sportzy app brings multi-camera sports streaming to phones: link several phones as synchronized camera angles and run everything from one app. Coming soon.",
        "crumb": "Sportzy App", "schema": [],
    },
    {
        "src": "cricket.html", "path": "/cricket-live-streaming/", "nav": "", "priority": "0.8",
        "title": "Cricket Live Streaming App With Live Scoreboard — Free | Sportzy",
        "description": "Sportzy is a free cricket live streaming app with a live scoreboard. Stream local matches from your phone to Facebook, YouTube and Instagram at once.",
        "crumb": "Cricket live streaming", "schema": ["faq"],
    },
    {
        "src": "football.html", "path": "/football-live-streaming/", "nav": "", "priority": "0.8",
        "title": "Football Live Streaming App for Local Matches — Free | Sportzy",
        "description": "Free football live streaming app for local matches: live score graphics, team lineups and multistreaming to Facebook, YouTube and Instagram from one phone.",
        "crumb": "Football live streaming", "schema": ["faq"],
    },
    {
        "src": "tournament.html", "path": "/tournament-live-streaming/", "nav": "", "priority": "0.8",
        "title": "Tournament Live Streaming With Live Scores — Free | Sportzy",
        "description": "Tournament live streaming for leagues and cups: branded live scores, sponsor overlays and streaming to Facebook, YouTube & Instagram at once. Free beta.",
        "crumb": "Tournament live streaming", "schema": ["faq"],
    },
    {
        "src": "guides.html", "path": "/guides/", "nav": "guides", "priority": "0.7",
        "title": "Sports Live Streaming Guides & How-Tos | Sportzy",
        "description": "Sports live streaming guides: how to live stream cricket and football from a phone, add a scoreboard to Facebook Live and multistream to YouTube for free.",
        "crumb": "Guides", "schema": [],
    },
    {
        "src": "guide-cricket-youtube.html", "path": "/guides/how-to-live-stream-cricket-on-youtube/", "nav": "guides", "priority": "0.7",
        "h1": "How to live stream a cricket match on YouTube (with a live scoreboard)",
        "title": "How to Live Stream Cricket on YouTube With a Scoreboard",
        "description": "How to live stream cricket on YouTube from your phone: setup, camera angle, live scorecard overlay and simulcasting to Facebook. Free step-by-step guide.",
        "crumb": "Live stream cricket on YouTube", "parent": ("Guides", "/guides/"),
        "published": "2026-10-12", "schema": ["article", "faq"],
    },
    {
        "src": "guide-facebook-scoreboard.html", "path": "/guides/how-to-add-scoreboard-to-facebook-live/", "nav": "guides", "priority": "0.7",
        "h1": "How to add a live scoreboard to Facebook Live",
        "title": "How to Add a Live Scoreboard to Facebook Live (Free)",
        "description": "How to add a scoreboard to Facebook Live: show real-time scores, cricket scorecards, lineups and sponsor logos on your sports stream without OBS or a PC.",
        "crumb": "Scoreboard on Facebook Live", "parent": ("Guides", "/guides/"),
        "published": "2026-10-12", "schema": ["article", "faq"],
    },
    {
        "src": "guide-multistream.html", "path": "/guides/stream-to-facebook-youtube-instagram-at-once/", "nav": "guides", "priority": "0.7",
        "h1": "How to stream to Facebook, YouTube and Instagram at the same time",
        "title": "Stream to Facebook, YouTube & Instagram at the Same Time",
        "description": "How multistreaming works and how to go live on Facebook, YouTube and Instagram simultaneously from one phone or camera — free with Streemzy.",
        "crumb": "Multistream to Facebook, YouTube & Instagram", "parent": ("Guides", "/guides/"),
        "published": "2026-10-12", "schema": ["article", "faq"],
    },
    {
        "src": "about.html", "path": "/about/", "nav": "about", "priority": "0.6",
        "title": "About Sportzy — Democratizing Sports Broadcasting",
        "description": "Sportzy is building the operating system for grassroots sports broadcasting — starting in Bangladesh, growing across South Asia, the Middle East and Africa.",
        "crumb": "About", "schema": [],
    },
    {
        "src": "404.html", "path": "/404.html", "nav": "", "noindex": True,
        "title": "Page not found | Sportzy",
        "description": "This page doesn't exist. Head back to Sportzy to start broadcasting your matches for free.",
        "schema": [],
    },
]

NAV = [
    ("scorezy", "/scorezy/", "Scorezy"),
    ("streemzy", "/streemzy/", "Streemzy"),
    ("visionzy", "/visionzy/", "Visionzy"),
    ("app", "/app/", "Sportzy App"),
    ("guides", "/guides/", "Guides"),
    ("about", "/about/", "About"),
]

ICONS = {
    "scoreboard": '<rect x="3" y="4" width="18" height="16" rx="2"/><line x1="12" y1="4" x2="12" y2="20"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "stream": '<rect x="2" y="3" width="20" height="7" rx="1.5"/><rect x="2" y="14" width="20" height="7" rx="1.5"/><circle cx="6" cy="6.5" r=".8"/><circle cx="6" cy="17.5" r=".8"/>',
    "ai": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><line x1="12" y1="3" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="21"/><line x1="3" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="21" y2="12"/>',
    "phone": '<rect x="7" y="2" width="10" height="20" rx="2"/><line x1="11" y1="18" x2="13" y2="18"/>',
    "money": '<circle cx="12" cy="12" r="9"/><path d="M15 9.5c-.5-1-1.6-1.5-3-1.5-1.7 0-3 .8-3 2s1.3 1.7 3 2 3 .8 3 2-1.3 2-3 2c-1.4 0-2.5-.5-3-1.5"/><line x1="12" y1="6" x2="12" y2="18"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.5-3.5 3.2-5.5 6.5-5.5s6 2 6.5 5.5"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14.8c2 .7 3.3 2.5 3.5 5.2"/>',
    "layers": '<path d="M12 3 2 8l10 5 10-5-10-5z"/><path d="m2 13 10 5 10-5"/>',
    "replay": '<path d="M3 12a9 9 0 1 0 3-6.7"/><polyline points="3 3 3 9 9 9"/><polygon points="10 9 15 12 10 15 10 9"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><line x1="3" y1="12" x2="21" y2="12"/><path d="M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0"/><line x1="12" y1="18" x2="12" y2="21"/>',
    "cloud": '<path d="M7 18a4.5 4.5 0 0 1-.5-9 6 6 0 0 1 11.5 2 3.5 3.5 0 0 1 0 7z"/>',
    "camera": '<path d="M3 8a2 2 0 0 1 2-2h2l1.5-2h7L17 6h2a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><circle cx="12" cy="13" r="3.5"/>',
    "trophy": '<path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4"/><line x1="12" y1="13" x2="12" y2="17"/><line x1="8" y1="20" x2="16" y2="20"/>',
    "palette": '<circle cx="12" cy="12" r="9"/><circle cx="8" cy="10" r="1"/><circle cx="12" cy="7.5" r="1"/><circle cx="16" cy="10" r="1"/><path d="M12 21a2 2 0 0 1 0-4h2a3 3 0 0 0 3-3"/>',
    "bolt": '<polygon points="13 2 4 14 12 14 11 22 20 10 12 10 13 2"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
}


def icon(name):
    return f'<span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS[name]}</svg></span>'


def abs_url(path):
    return CONFIG["SITE_URL"] + path


# ---------------------------------------------------------------- schema ---

def org_schema():
    return {
        "@type": "Organization",
        "@id": abs_url("/#org"),
        "name": "Sportzy",
        "url": abs_url("/"),
        "logo": abs_url("/assets/icon-512.png"),
        "email": CONFIG["CONTACT_EMAIL"],
        "founder": {"@type": "Person", "name": CONFIG["FOUNDER"], "sameAs": CONFIG["FOUNDER_LINKEDIN"]},
        "foundingLocation": {"@type": "Place", "name": "Bangladesh"},
        "sameAs": [CONFIG["STREEMZY_URL"], CONFIG["SCOREZY_URL"]],
    }


def free_offer():
    return {"@type": "Offer", "price": "0", "priceCurrency": "USD", "description": "Free beta for everyone"}


def app_schema(name, url, category, desc, features):
    return {
        "@type": "SoftwareApplication",
        "name": name,
        "url": url,
        "applicationCategory": category,
        "operatingSystem": "Web, Android, iOS",
        "description": desc,
        "featureList": features,
        "offers": free_offer(),
        "publisher": {"@id": abs_url("/#org")},
    }


SCOREZY_APP = lambda: app_schema(
    "Scorezy", CONFIG["SCOREZY_URL"], "MultimediaApplication",
    "Live scoring and broadcast-graphics engine for live sports streams.",
    ["Live scoreboards", "Cricket scorecards", "Team lineups", "Lower thirds",
     "Tournament branding overlays", "Sponsor graphics", "Match statistics overlays"])

STREEMZY_APP = lambda: app_schema(
    "Streemzy", CONFIG["STREEMZY_URL"], "MultimediaApplication",
    "Multi-platform live streaming to Facebook, YouTube and Instagram at once.",
    ["Multistream to Facebook, YouTube and Instagram", "RTMP ingest from any camera",
     "Multi-location streaming", "Remote commentator dial-in", "Cloud recording and VOD"])


def faq_schema(body):
    items = re.findall(r"<details>\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>\s*</details>", body, re.S)
    strip = lambda s: re.sub(r"<[^>]+>", "", s).strip()
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": strip(q),
             "acceptedAnswer": {"@type": "Answer", "text": strip(a)}}
            for q, a in items
        ],
    }


def build_schema(page, body):
    graph = [org_schema(), {
        "@type": "WebSite", "@id": abs_url("/#website"), "name": "Sportzy",
        "url": abs_url("/"), "publisher": {"@id": abs_url("/#org")}, "inLanguage": "en",
    }, {
        "@type": "WebPage", "@id": abs_url(page["path"]), "url": abs_url(page["path"]),
        "name": page["title"], "description": page["description"],
        "isPartOf": {"@id": abs_url("/#website")}, "inLanguage": "en",
    }]
    if page.get("crumb"):
        trail = [("Home", "/")] + ([page["parent"]] if page.get("parent") else []) + [(page["crumb"], page["path"])]
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": n, "item": abs_url(u)}
                for i, (n, u) in enumerate(trail, 1)
            ],
        })
    for kind in page["schema"]:
        if kind == "faq":
            graph.append(faq_schema(body))
        elif kind == "article":
            graph.append({
                "@type": "Article",
                "headline": page["h1"],
                "description": page["description"],
                "image": abs_url("/assets/og-image.png"),
                "datePublished": page["published"],
                "dateModified": page.get("modified", page["published"]),
                "author": {"@type": "Organization", "name": "Sportzy", "url": abs_url("/")},
                "publisher": {"@id": abs_url("/#org")},
                "mainEntityOfPage": {"@id": abs_url(page["path"])},
                "inLanguage": "en",
            })
        elif kind == "app_scorezy":
            graph.append(SCOREZY_APP())
        elif kind == "app_streemzy":
            graph.append(STREEMZY_APP())
        elif kind == "software_suite":
            graph += [SCOREZY_APP(), STREEMZY_APP()]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- layout ---

def head(page, body):
    canonical = abs_url(page["path"])
    og_img = abs_url("/assets/og-image.png")
    robots = "noindex, follow" if page.get("noindex") else "index, follow, max-image-preview:large"
    extra = ""
    if CONFIG["GSC_VERIFICATION"]:
        extra += f'<meta name="google-site-verification" content="{CONFIG["GSC_VERIFICATION"]}">\n'
    if CONFIG["GA4_ID"]:
        gid = CONFIG["GA4_ID"]
        extra += (f'<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>\n'
                  f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}"
                  f"gtag('js',new Date());gtag('config','{gid}');</script>\n")
    canonical_tag = "" if page.get("noindex") else f'<link rel="canonical" href="{canonical}">\n'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page["title"]}</title>
<meta name="description" content="{page["description"]}">
<meta name="robots" content="{robots}">
{canonical_tag}<meta name="theme-color" content="#0A0E0C">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Sportzy">
<meta property="og:title" content="{page["title"]}">
<meta property="og:description" content="{page["description"]}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Sportzy — Every match deserves a broadcast.">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{page["title"]}">
<meta name="twitter:description" content="{page["description"]}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="48x48" href="/assets/favicon-48.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/styles.css">
{extra}<script type="application/ld+json">
{build_schema(page, body)}
</script>
</head>"""


def header(page):
    links = []
    for key, href, label in NAV:
        cur = ' aria-current="page"' if page["nav"] == key else ""
        links.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    links.append('<li><a class="btn btn-primary btn-sm" href="/#get-started">Start free</a></li>')
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<div class="beta-bar"><strong>Free beta is open.</strong> Scorezy &amp; Streemzy are live — free for everyone.</div>
<header class="site-header">
  <nav class="wrap nav" aria-label="Main">
    <a class="logo" href="/" aria-label="Sportzy home"><img src="/assets/sportzy-wordmark-64.png" alt="Sportzy" width="231" height="64"></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="Open menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>
    </button>
    <ul class="nav-links" id="nav-links">
      {chr(10).join("      " + l if i else l for i, l in enumerate(links))}
    </ul>
  </nav>
</header>
"""


def crumbs(page):
    if not page.get("crumb"):
        return ""
    parent = f'<li><a href="{page["parent"][1]}">{page["parent"][0]}</a></li>' if page.get("parent") else ""
    return f"""<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>{parent}<li aria-current="page">{page["crumb"]}</li></ol></nav>"""


def footer():
    year = date.today().year
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a href="/" aria-label="Sportzy home"><img src="/assets/sportzy-wordmark-64.png" alt="Sportzy" width="173" height="48" style="height:48px;width:auto"></a>
        <p class="about">Professional sports broadcasting on the phones organizers already own. Built for grassroots leagues, clubs, schools and academies.</p>
      </div>
      <div>
        <h2>Products</h2>
        <ul>
          <li><a href="/scorezy/">Scorezy — live scoring</a></li>
          <li><a href="/streemzy/">Streemzy — multistreaming</a></li>
          <li><a href="/visionzy/">Visionzy — AI vision</a></li>
          <li><a href="/app/">Sportzy App</a></li>
        </ul>
      </div>
      <div>
        <h2>Use cases</h2>
        <ul>
          <li><a href="/cricket-live-streaming/">Cricket live streaming</a></li>
          <li><a href="/football-live-streaming/">Football live streaming</a></li>
          <li><a href="/tournament-live-streaming/">Tournament live streaming</a></li>
          <li><a href="/guides/">Streaming guides</a></li>
        </ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="/about/">About Sportzy</a></li>
          <li><a href="/#faq">FAQ</a></li>
          <li><a href="mailto:{CONFIG["CONTACT_EMAIL"]}">Contact</a></li>
          <li><a href="{CONFIG["FOUNDER_LINKEDIN"]}" rel="noopener" target="_blank">LinkedIn</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>© {year} Sportzy. All rights reserved.</span>
      <span>Made in Bangladesh for every match, everywhere.</span>
    </div>
  </div>
</footer>
<script>
(function () {{
  var b = document.querySelector('.nav-toggle'), l = document.getElementById('nav-links');
  if (!b || !l) return;
  b.addEventListener('click', function () {{
    var open = l.classList.toggle('open');
    b.setAttribute('aria-expanded', open);
    b.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }});
}})();
</script>
</body>
</html>
"""


def render_body(page):
    body = (PAGES / page["src"]).read_text(encoding="utf-8")
    body = body.replace("{{crumbs}}", crumbs(page))
    body = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: icon(m.group(1)), body)
    for k, v in CONFIG.items():
        body = body.replace("{{" + k + "}}", v)
    leftover = re.findall(r"\{\{[^}]+\}\}", body)
    if leftover:
        raise SystemExit(f"{page['src']}: unresolved placeholders {leftover}")
    return body


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ASSETS, OUT / "assets")
    shutil.copy(ASSETS / "favicon.ico", OUT / "favicon.ico")

    for page in SITE_PAGES:
        body = render_body(page)
        html = head(page, body) + "\n" + header(page) + '<main id="main">\n' + \
            body + "</main>\n" + footer()
        target = OUT / page["path"].lstrip("/")
        if page["path"].endswith("/"):
            target = target / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")

    today = date.today().isoformat()
    urls = "\n".join(
        f"  <url><loc>{abs_url(p['path'])}</loc><lastmod>{today}</lastmod><priority>{p['priority']}</priority></url>"
        for p in SITE_PAGES if not p.get("noindex"))
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8")
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {abs_url('/sitemap.xml')}\n", encoding="utf-8")
    (OUT / "site.webmanifest").write_text(json.dumps({
        "name": "Sportzy", "short_name": "Sportzy",
        "description": "Free live sports scoring and multi-platform streaming for grassroots matches.",
        "start_url": "/", "display": "standalone",
        "background_color": "#0A0E0C", "theme_color": "#0A0E0C",
        "icons": [
            {"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, indent=2), encoding="utf-8")
    print(f"Built {len(SITE_PAGES)} pages into {OUT.relative_to(ROOT)}/ for {CONFIG['SITE_URL']}")


if __name__ == "__main__":
    build()
