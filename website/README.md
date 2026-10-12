# Sportzy website

Static, SEO-ready marketing site for Sportzy: Scorezy and Streemzy (live, free beta), plus Visionzy and the Sportzy App (coming soon).

- `pages/` — page content (edit text here)
- `assets/` — styles, logos, favicons, Open Graph image
- `build.py` — wraps pages in the shared layout and writes the deployable site to `public/`
- `public/` — **upload/deploy this folder** (already built)
- `KEYWORDS.md` — which search keywords each page targets, and how to grow it

## Before going live

1. Open `build.py` and check `CONFIG`:
   - `SITE_URL` — the real domain of this website (used for canonical URLs, sitemap, social cards)
   - `SCOREZY_URL` / `STREEMZY_URL` — where the "Open Scorezy/Streemzy" buttons go
   - optional `GA4_ID` (Google Analytics) and `GSC_VERIFICATION` (Search Console)
2. Run `python3 build.py` (Python 3, no packages needed).
3. Deploy `public/` (details below).

## Deploying

`public/` is a complete static site (about 400 KB). `build.py` also writes the server settings for the common hosts into it: force HTTPS, redirect `www.sportzy.live` to `sportzy.live`, security headers, 7-day caching for `/assets/`, and `404.html` as the not-found page.

| Host | Steps | Config used |
|---|---|---|
| **Cloudflare Pages** (recommended, free) | Upload `public/` (or connect the repo with output directory `website/public`, no build command). Add custom domains `sportzy.live` and `www.sportzy.live`, then add a Redirect Rule for `www` → `https://sportzy.live`. | `_headers` |
| **Netlify** (free) | Drag `public/` onto Netlify Drop, or connect the repo with publish directory `website/public`. Add both domains; Netlify redirects `www` to the primary domain itself. | `_headers` |
| **Vercel** | Import the repo with root directory `website/public`, framework "Other", no build command. Add both domains. | `vercel.json` |
| **cPanel / shared hosting** | Upload the *contents* of `public/` (including the hidden `.htaccess`) into `public_html/`. Turn on free SSL (AutoSSL / Let's Encrypt) first. | `.htaccess` |

`.htaccess` has not been tested on a live Apache server. After uploading, open `http://www.sportzy.live/about/index.html` and check that it lands on `https://sportzy.live/about/`.

## Launch checklist

- [ ] `info@sportzy.live` receives mail (waitlist and contact buttons send there)
- [ ] `https://sportzy.live` loads with a padlock; `http://` and `www.` redirect to it
- [ ] `https://sportzy.live/robots.txt` and `/sitemap.xml` open
- [ ] A made-up address like `/nope` shows the Sportzy 404 page
- [ ] Share the home page link in WhatsApp/Facebook and check the preview image appears
- [ ] Google Search Console: verify `sportzy.live`, submit `/sitemap.xml`, request indexing for the home page
- [ ] Optional: add `GA4_ID` in `build.py`, rebuild and redeploy to track visitors
- [ ] Link to `https://sportzy.live` from streemzy.io and score.sportzy.live

## After launch

1. Link to the site from streemzy.io, Scorezy, your social profiles and LinkedIn. Backlinks from your own live products help Google find the site quickly.
2. Check the structured data with Google's Rich Results Test (FAQ, SoftwareApplication, Breadcrumb).
3. When Visionzy or the app launches, update its page in `pages/`, change the badge from "Coming soon" to "Live", and rebuild.

## Preview locally

    python3 build.py && python3 -m http.server -d public 8000
