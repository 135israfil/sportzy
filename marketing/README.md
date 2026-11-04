# Sportzy marketing operation: start here

This folder is everything needed to run Sportzy's marketing from **Mon 16 Nov 2026 to Fri 14 May 2027**. The targets: **30 active venues, 10 paid tournaments a month, 35%+ repeat bookers** in Dhaka.

## How to use it each week

1. **Monday:** open `analytics/weekly_reports/TEMPLATE.md` and fill in last week's numbers. Look at the KPI that's furthest behind its line in `strategy/marketing_strategy.md` § 3.
2. Open `content/content_calendar.csv`, filtered to this week:
   - Each row says the platform, audience, campaign, the asset to make (Asset ID → `creative/`), the caption (Caption ID → `content/social_captions.md`) and the KPI.
   - Rows with a `Gate` value publish only when that feature is live (see `strategy/marketing_strategy.md` § 5).
3. **Field sales days:** use `sales/venue_outreach.md` and `sales/organizer_outreach.md`. Log every contact in the CRM sheet described in `analytics/kpi_dashboard_spec.md`.
4. **Video shoots:** pick the scripts due this week from `video/scripts/`.

## What's where

| Folder | What's in it |
|---|---|
| `strategy/` | Strategy and targets, positioning and messaging, personas, competitors, budget and paid ads |
| `campaigns/` | One file per campaign, grouped by phase, with the objective, audience, assets, schedule, KPI and the success/kill rule. `ads.md` in each folder has the paid creatives |
| `content/` | The 180-day calendar (CSV and summary), every caption in Bangla and English, and the copy banks |
| `creative/` | Brand guidelines, logo files, product screens, design briefs per format, image prompts, generated images and their index |
| `video/` | 14 production scripts, storyboards, voice-over text and editing guides, plus `renders/` (animated MP4 masters for 7 videos with no audio, made by `motion/`) |
| `sales/` | Venue and organiser outreach kits, partnership proposals, the player kit |
| `analytics/` | KPI definitions and dashboard spec, event tracking plan, weekly report template, `verify_plan.py` (run before each calendar edit is committed) |

## Who does what (RACI)

R = does it, A = accountable, C = consulted. For a 1–3 person team, one person wears several hats. Suggested split: **Founder** = CMO + B2B Sales; **Marketing exec** = Growth + Social + Copywriter + Performance + Analyst; **Freelance creative** = Creative Director + Designer + Video.

| Work | CMO (A) | Growth (B) | B2B Sales (C) | Social (D) | Creative Dir (E) | Designer (F) | Video (G) | Copy (H) | Performance (I) | Analyst (J) |
|---|---|---|---|---|---|---|---|---|---|---|
| Targets and weekly review | A | R | C | C | | | | | C | R |
| Venue acquisition | A | C | R | C | | C | | C | C | C |
| Tournament sales | A | C | R | C | | C | C | C | C | C |
| Content calendar and posting | C | C | | R/A | C | C | C | R | | C |
| Visual assets | C | | | C | A | R | | C | | |
| Videos | C | | | C | A | | R | R | | |
| Paid ads | A | C | | | C | C | C | C | R | C |
| Tracking and dashboard | C | R | | | | | | | C | R/A |

## FOUNDER APPROVAL NEEDED (decide before launch)

1. **Prices in public materials:** 8% booking commission; ৳300 per streamed game (+৳100 for a second platform); Club & League ৳3,600 a month for up to 12 games; 10% entry-fee commission. Taken from the pitch deck's pricing strategy.
2. **The "paid tournament" definition** in `strategy/marketing_strategy.md` § 2.
3. **Launch incentives (proposals):**
   - venues: 0% commission on their first 20 Sportzy bookings
   - organisers: first 3 streamed games free
   - players: none in cash, because launch offers train people to wait for discounts
4. **Budget scenario:** Bootstrap ৳40k a month recommended for December and January (`strategy/budget_plan.md`).
5. **Launch date:** Sat 12 Dec 2026, conditional on go-live (SPOR-14/15/16).
6. **Real venue names:** permission from each signed venue to name it in posts and ads. Until then, demo names only.
7. **Logo:** confirm the files in `creative/brand/` (taken from the pitch deck) and supply SVG and dark-on-light versions if they exist.

## Guardrails

- Nothing in this folder has been published, sent or paid for.
- No invented statistics, quotes or venue names in public content.
- Advertise only Built features; gated rows wait for their feature.
- Product screens in `creative/product_screens/` are design renders. Read its `INDEX.md` before using one.
