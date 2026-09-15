# Sportzy

A sports-tech platform turning any smartphone into a broadcast setup — live scoring graphics, multi-platform streaming, and AI-powered sports analysis, built as three connected products for grassroots leagues that professional broadcast tech has always priced out.

**Status:** active startup I founded and run. Source is private; this repo documents the product and the engineering behind it. See [`docs/product-overview.html`](docs/product-overview.html) for the full product one-pager.

## Why I built this

Roughly four million organized amateur matches are played every year, and almost none of them are broadcast — not because nobody would watch, but because a broadcast truck, a production crew, and a rack of switchers cost tens of thousands of dollars, which no club, school, or grassroots league has. Meanwhile the phones already in everyone's pockets are more capable than a lot of that gear. Sportzy is built on that gap: professional-grade sports broadcasting and analysis, running on hardware organizers already own.

## The three products

- **Scorezy** (*Scoring App*) — the broadcast-graphics engine: live scoreboards, team lineups, lower thirds, tournament branding overlays, and cricket-specific scorecards, rendered in real time onto a raw camera feed. Market-ready.
- **Streemzy** (*Stream Cloud*) — the delivery layer: multi-platform simulcast (Facebook, YouTube, Instagram at once), multi-location streaming from a single match, RTMP ingest from any camera, remote commentator dial-in. Market-ready.
- **Visionzy** (*Ai vision*) — AI-powered computer vision on top of the broadcast: ball and player tracking for LBW review, VAR-style replay, auto-generated highlights, offside and tactical analysis. In R&D.

The central Sportzy app connects and manages all three from one Android/iOS app, and its most distinctive engineering piece is turning several phones on the sideline into synchronized multi-angle camera feeds over a local network — no dedicated broadcast hardware, run by one organizer or a small volunteer team.

## Engineering work behind the product

- **Brand and product design** — full logo and visual identity across all three products, taken through many rounds of feedback to a professional standard
- **Streaming infrastructure debugging** — investigated Facebook's Graph API live-streaming behavior and traced an OAuth privacy-ceiling issue that was silently affecting profile-level stream visibility
- **SEO and growth engineering** on streemzy.io — programmatic blog content generation, Rank Math configuration fixes, and Google Search Console sitemap resubmission to recover indexing
- **Fundraising materials** — built a 19-slide investor pitch deck for a pre-seed raise, with a fundraising strategy targeting foreign/diaspora angel investors structured through a Singapore holding company

## Stack

Multistreaming and RTMP ingest infrastructure, Figma-to-HTML landing page pipelines for the earlier product iteration, AI/computer-vision R&D for ball tracking. (Full technical stack for the current build is kept private alongside the source.)

## What I'd do differently

The Facebook Graph API OAuth issue is the clearest lesson here: a third-party platform's privacy defaults can silently cap a core feature's reach in a way that looks like a bug in your own code until you trace it all the way to the platform's own settings. I'd budget time to audit every third-party integration's default visibility/privacy behavior earlier in a product's life, rather than discovering it once real users are affected.
