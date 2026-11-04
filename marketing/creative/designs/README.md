# Core designs (built in code)

These replace the Canva AI drafts, which the founder rejected as not professional enough for the Bangladesh market. They're built in HTML/CSS (`src/`) and rendered to PNG at exact platform sizes, using:

- the Floodlight Night tokens
- the pitch-deck logo
- the approved product screens

## Rebuild after a change

```bash
cd marketing/creative/designs/src && python3 build.py && node render.js
```

- Copy and layout live in `src/build.py`, and the shared style in `src/base.css`.
- To render a single design: `node render.js DES-04_launch_post`.
- The QR code needs `pip install qrcode`.

## Files

| File | Size | Uses | Status |
|---|---|---|---|
| DES-04_launch_post.png | 1080×1350 | Launch day only, after go-live | Draft, founder review |
| DES-05_facebook_cover.png | 1640×624 (key content in the centre 1000×400) | Page cover | Draft |
| DES-06_live_thumbnail_sample.png | 1280×720 | Per stream | **SAMPLE**: teams and score are invented |
| DES-07_venue_qr_poster_sample.png | A3 ratio, 2382×3368 | One per partner venue | **SAMPLE**: the QR points to sportzy.live; swap in each venue's page link |
| DES-08_turf_spotlight_sample.png | 1080×1350 | Turf of the week | **SAMPLE**: venue, hours and price must come from the real venue, with written consent |
| DES-09_tournament_announcement_sample.png | 1080×1350 | Per tournament | **SAMPLE**: name, dates, venue, fee and spots come from the organiser |
| DES-11_owner_one_pager.png | A4 ratio, 2480×3508 | Field sales leave-behind | Draft; **8% pending founder approval**; add the real WhatsApp number |
| DES-12_organiser_card.png | 1080×1350 | Organiser outreach | Draft |
| DES-13_open_slots_story_sample.png | 1080×1920 (content inside the story safe zone) | Daily story | **SAMPLE**: fill from real open slots that day |
| DES-17_ad_tonight.png | 1080×1080 | Meta C2 "tonight" angle | Draft; no spend without budget approval |

## Rules

- Anything marked **SAMPLE** must have its data replaced with real, consented data before it's published.
- Venue names in the samples are placeholders. They match the product-screen renders and don't imply any partnership.
- Product screens appear only inside phone frames, and only screens marked approved in `../product_screens/INDEX.md` are used.
- The owner-signup screen was taken out of use on 4 Nov. Its copy still describes the old pay-the-venue-directly flow.
- Type:
  - **Anek Bangla 800** for Bangla display headlines (proposed addition to the brand, founder to confirm)
  - **Hind Siliguri** for Bangla body text
  - **Anton** for English display
  - **JetBrains Mono** for times and prices
