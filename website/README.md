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
3. Deploy `public/` to any static host (Netlify, Cloudflare Pages, Vercel, GitHub Pages, cPanel). Serve it from the domain root, because links start with `/`. Set `404.html` as the not-found page if your host asks for one.

## After launch

1. In Google Search Console, verify the domain and submit `https://YOUR-DOMAIN/sitemap.xml`.
2. Link to the site from streemzy.io, Scorezy, your social profiles and LinkedIn. Backlinks from your own live products help Google find the site quickly.
3. Check the structured data with Google's Rich Results Test (FAQ, SoftwareApplication, Breadcrumb).
4. When Visionzy or the app launches, update its page in `pages/`, change the badge from "Coming soon" to "Live", and rebuild.

## Preview locally

    python3 build.py && python3 -m http.server -d public 8000
