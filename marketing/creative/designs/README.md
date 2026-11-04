# Sportzy designs (built in code)

Floodlight Night designs, built in HTML/CSS and rendered to PNG at exact platform sizes. They use:

- the brand tokens
- the pitch-deck logo
- the approved product screens

These replaced the Canva AI drafts on 4 Nov 2026, and the founder approved the look.

## How to make this week's posts (no coding)

1. **Copy a data file** from `data/`, for example `data/open_slots.json` → `my_slots.json`.
2. **Fill in real values:** venues, times and prices that are actually open, and real tournament details. Every value is plain text, and the `_note` in each file explains the rules. Add `"_label": "2026-12-12"` (any date or word) to name the output file.
3. **Run one command** from `marketing/creative/designs/src/`:

   ```bash
   python3 build.py fill open_slots ../my_slots.json
   ```

4. **Collect the file** from `designs/out/`, for example `DES-13_open_slots_story_2026-12-12.png`. The `out/` folder isn't committed.

Long names shrink automatically to fit.

**Templates:**

| Template | Data file | What you get |
|---|---|---|
| `open_slots` | `open_slots.json` | Story 1080×1920 with up to 5 open slots tonight |
| `tournament` | `tournament.json` | Tournament announcement, 1080×1350 |
| `fixtures` | `fixtures.json` | Round fixtures, 1080×1350 (up to 6) |
| `standings` | `fixtures.json` | Table, 1080×1350 (up to 8 teams); the top `qualify` rows are highlighted |
| `turf_spotlight` | `turf_spotlight.json` | Turf of the week, 1080×1350 (venue consent needed) |
| `live_thumbnail` | `live_thumbnail.json` | YouTube / live thumbnail, 1280×720 |
| `captain` | `captain.json` | Founding Captain card, 1080×1350 (written consent needed for name and photo) |
| `ramadan` | `ramadan.json` | Ramadan Nights post 1080×1350, or `"format": "a3"` for the print poster |

**Rebuild everything** (samples and fixed designs) after editing code:

```bash
python3 build.py && node render.js
```

The code is split across:

- `src/kit.py`: shared pieces
- `src/templates.py`: data-driven templates
- `src/build.py`: fixed designs and the command line
- `src/base.css`: the style

The QR code needs `pip install qrcode`.

## Files

**Status key:**

- **SAMPLE:** made-up data. Never publish as-is. Make a real version with `fill`.
- **Draft:** final copy, waiting for founder review.
- **Gated:** only usable after the condition shown.

| File(s) | Size | Brief and use | Status |
|---|---|---|---|
| DES-01_brand_carousel_01–06 | 1080×1350 ×6 | Brand intro: BOOK · PLAY · SCORE · STREAM · SHARE, then launch (CAP-002, CAP-058) | Draft. Slides 3–4 mark Scorezy/Streemzy as BETA; slide 4's scoreboard card is illustrative |
| DES-02_seven_stages_01–07 | 1080×1350 ×7 | "7 stages of booking a turf" meme carousel (CAP-005) | Draft. Chats are redrawn, with no real names or numbers |
| DES-03_countdown_story_7…1, DES-03_countdown_feed | 1080×1920 ×7, 1080×1080 | Launch countdown (CAP-013, STY-CD) | Gated by go-live. The date is set in one place in `build.py` (`LAUNCH_DATE_*`) for the `[LAUNCH]` slip rule |
| DES-04_launch_post | 1080×1350 | Launch day | Gated by go-live |
| DES-05_facebook_cover | 1640×624 (key content in the centre 1000×400) | Page cover | Draft |
| DES-06_live_thumbnail_sample | 1280×720 | Per stream | SAMPLE |
| DES-07_venue_qr_poster_sample | A3 ratio, 2382×3368 | One per partner venue | SAMPLE: the QR points to sportzy.live; use each venue's page link |
| DES-08_turf_spotlight_sample | 1080×1350 | Turf of the week | SAMPLE |
| DES-09_tournament_announcement_sample | 1080×1350 | Per tournament | SAMPLE |
| DES-10_fixtures_sample, DES-10_standings_sample | 1080×1350 | Sunday fixtures and standings (STY-SUN) | SAMPLE |
| DES-11_owner_one_pager | A4 ratio, 2480×3508 | Field sales leave-behind | Draft; 8% pending founder approval; add the real WhatsApp number |
| DES-12_organiser_card | 1080×1350 | Organiser outreach | Draft |
| DES-13_open_slots_story_sample | 1080×1920 | Daily story | SAMPLE |
| DES-14_founding_captain_sample | 1080×1350 | Founding Captain announcement (6 captions) | SAMPLE: perks must match the approved offer |
| DES-15_ramadan_nights_sample, DES-15_ramadan_nights_poster_sample | 1080×1350, A3 2382×3368 | Ramadan night tournaments (CAP-037, CAP-050) | SAMPLE: Ramadan 2027 is about 8 Feb – 9 Mar; confirm the dates |
| DES-16_corporate_league_linkedin, DES-16_corporate_league_feed | 1200×627, 1080×1350 | Corporate league (CAP-029, CAP-057, SALES-C) | Draft. No prices shown until the founder sets them |
| DES-17_ad_tonight | 1080×1080 | Meta C2 "tonight" angle | Draft; no spend without budget approval |

DES-18 (referral card) isn't built on purpose. It waits until referrals ship.

## Rules

- **Venue names in samples** are placeholders that match the product-screen renders. They don't imply any partnership.
- **Product screens** appear only inside phone frames, and only screens marked approved in `../product_screens/INDEX.md` are used.
- **The owner-signup screen** is excluded. Its copy describes the old pay-the-venue-directly flow.
- **Type:**
  - **Anek Bangla 800:** Bangla display (proposed, founder to confirm)
  - **Hind Siliguri:** Bangla body
  - **Anton:** English display
  - **Manrope:** English body
  - **JetBrains Mono:** times, prices and scores
