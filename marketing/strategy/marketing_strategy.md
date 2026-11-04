# Sportzy marketing strategy: launch to growth (16 Nov 2026 – 14 May 2027)

**Goal by 14 May 2027:** 30 active venues, 10 paid tournaments a month, and more than 35% repeat bookers.

**Approach:** win Dhaka through organisers and venues, not ads. Every tournament brings 8–16 teams into venues Sportzy has signed, and every broadcast advertises the next one. Paid ads speed up what already works; they don't replace field sales.

Owner: CMO (Persona A). Reviewed every Monday in the weekly report (`analytics/weekly_reports/TEMPLATE.md`).

---

## 1. Starting point (audit, 4 Nov 2026)

| Fact | Source |
|---|---|
| 10 of about 20 documented Dhaka turfs signed, with no ad spend | Pitch deck, founder-reported, Oct 2026 |
| 20 beta users on Scorezy and Streemzy; both live and free in beta | Pitch deck |
| Revenue to date: ৳0 | Pitch deck |
| sportzy.live didn't resolve on 3 Nov; production hosting, domains and the security review are open | Jira SPOR-14, 15, 16 |
| Pricing in the founder's pricing strategy: 8% booking commission, ৳300 per streamed game (+৳100 for a second platform), Club & League ৳3,600 a month for up to 12 games, 10% tournament entry-fee commission | Pitch deck business slide; SPOR-95 |
| Brand: Floodlight Night (Anton, Manrope, JetBrains Mono; green #2FD67B, floodlight yellow #F4E04D) | Homepage design canvas |

**What this changes:** 30 active venues is **more than Dhaka's ~20 documented turfs**. Reaching it means:

- activating the 10 already signed
- signing the other ~10 documented ones
- adding venues that aren't on the documented lists: box-cricket cages, futsal courts, badminton halls, school and club grounds that rent slots
- opening Chattogram from month 4

That is the single biggest risk to the target. See § 7.

## 2. KPI definitions (marketing reports only these as traction)

- **Active venue:** onboarded, with verified availability in Sportzy, and at least one *completed* booking through Sportzy in the reporting month. A signed venue with no completed booking is "onboarded", not active.
- **Paid tournament:** a tournament where the organiser *paid Sportzy* in the month for at least one of: game-day streams (৳300 a game), a Club & League plan (৳3,600 a month), or entry fees collected through Sportzy (10% commission). **FOUNDER APPROVAL NEEDED.**
- **Repeat booker rate:** unique customers with 2 or more completed bookings ÷ unique customers with 1 or more completed bookings, for customers whose *first* booking fell in the cohort month, measured over 60 days from their first booking. A customer is a Sportzy ID; if a team captain books, the captain is the customer.
- **Not traction:** followers, likes, registrations, enquiries, demos booked, venues "interested". They are tracked as funnel steps only.

## 3. Monthly targets (estimates, re-set after each month's actuals)

| Month | Active venues (end of month) | Paid tournaments in month | Repeat booker rate (cohort) | Completed bookings in month | What has to happen |
|---|---:|---:|---:|---:|---|
| Nov 2026 (pre-launch) | 0 (10 onboarded) | 0 | – | 0 | Go-live work; onboard the 10 signed venues; 15 organiser conversations |
| Dec 2026 (launch 12 Dec, if go-live ships) | 8 | 1 | – | 60 | First bookings at signed venues; one launch tournament |
| Jan 2027 | 14 | 3 | 20% (Dec cohort) | 180 | Winter cricket season; first corporate league pitches |
| Feb 2027 (Ramadan from about 8 Feb) | 18 | 5 | 25% | 260 | Ramadan night tournaments |
| Mar 2027 (Eid about 10 Mar) | 22 | 7 | 30% | 320 | Post-Eid leagues; Chattogram scouting |
| Apr 2027 | 26 | 9 | 33% | 420 | Pohela Boishakh cup; Chattogram venues live |
| 1–14 May 2027 | 30 | 10 (monthly run-rate) | 35% | 260 (two weeks) | Target date |

Ramadan and Eid dates are approximate and depend on the moon sighting, so confirm them in January.

**How marketing feeds each number:**

- **Active venues** come from field sales (Persona C), owner social proof (Persona D) and the venue referral (§ 6, loop 1).
- **Paid tournaments** come from the organiser funnel, plus corporate, university and Ramadan campaigns (Persona C with Persona B).
- **Repeat booking** comes from retention campaigns (§ 4, phase 6), recurring regulars at venues, and tournaments, which force repeat bookings.

## 4. The six phases

Each phase lists the campaign files that run it. Dates assume go-live ships by 11 Dec. **Launch-date slip rule:** if go-live slips, every row marked `[LAUNCH]` in `content/content_calendar.csv` moves by the same number of days, and pre-launch content extends with the "evergreen" rows.

| Phase | Dates | Objective | Exit gate (all must be true) | Campaign files |
|---|---|---|---|---|
| 1. Pre-launch / awareness | 16 Nov – 11 Dec | Brand known to owners and organisers; 10 signed venues onboarded; launch partners lined up | Go-live shipped (SPOR-14/15/16); 10 venues with verified availability; 3 organisers committed to a December or January event | `campaigns/pre_launch/*` |
| 2. Official launch | 12 Dec – 31 Dec | First completed bookings and the first paid tournament; social proof | 50 completed bookings; 1 paid tournament; 3 real testimonials recorded | `campaigns/launch/*` |
| 3. Venue acquisition | 16 Nov – 14 May (continuous, peaks Jan–Apr) | 30 active venues | 30 active | `campaigns/venue_acquisition/*` |
| 4. Player acquisition | 12 Dec onward | Bookings at active venues | 1,000 players with a completed booking by 14 May | `campaigns/player_acquisition/*` |
| 5. Tournament growth | 1 Jan onward (organiser outreach from 16 Nov) | 10 paid tournaments a month | 10 in one calendar month | `campaigns/tournament_acquisition/*` |
| 6. Retention and community | 15 Jan onward | Repeat booker rate above 35% | Two consecutive cohorts at 35%+ | `campaigns/retention/*` |

Phases 3–6 overlap by design. The weekly report shows which one is behind, and the time the founder and the sales lead spend moves to that phase.

## 5. Feature status (what marketing may promise)

Marketing promotes only **Built** features. **Gated** campaigns stay in the calendar but don't publish until product confirms the feature is live. The calendar's `Gate` column names the feature.

| Feature | Status | Source | May we advertise it? |
|---|---|---|---|
| Turf search by area, sport, time; venue pages; slot holds; checkout | Built (Jira Done) | SPOR-29, 83 | Yes, after go-live |
| bKash / Nagad / QR Pay BD payment, central collection | Built | SPOR-28, 89 | Yes |
| Cancellation and refunds under the 24-hour rule | Built | SPOR-31 | Yes, stating the rule exactly |
| Find a game, request to attend, Team A/B | Built | SPOR-40, 41 | Yes |
| Owner dashboard, earnings, walk-ins, discounts | Built | SPOR-85, 87, 88 | Yes (owner campaigns) |
| Tournaments: paid registration (QR Pay BD), fixtures, paid slots, standings | Built | SPOR-82, 95, 97, 98 | Yes |
| Scorezy scoring and Streemzy streaming (beta) | Live in beta, free | Pitch deck | Yes, labelled "beta" |
| Score overlay on the stream | In progress | SPOR-38 | **Gated:** overlay |
| Player and Organizer mobile apps | Planned | SPOR-110, 111 | Only "coming soon" teasers; no store links |
| Split payment per player | Not built (the design shows "split 10 ways" as information only) | — | **Gated:** split pay |
| Recurring weekly booking | Not built | — | **Gated:** recurring |
| Referral codes and credits | Not built | — | **Gated:** referral (run a manual version, § 6) |
| Highlights, player stats, leaderboards | Not built | — | **Gated:** stats |
| Multi-camera mixing, AI review (Visionzy) | Not built / R&D | SPOR-25, 12 | No |

## 6. Growth loops

Each loop shows how one customer brings the next, and what it needs from the product. Loops that work manually today start now; loops that need product work start at their gate.

| # | Loop | How one brings the next | Works today? | Product needed |
|---|---|---|---|---|
| 1 | **Venue → venue referral** | An active venue owner introduces a nearby owner; both get 1 month at 0% commission after the new venue's first 10 completed bookings | Manual: sales lead tracks it in the CRM sheet | Later: a referral code on owner signup |
| 2 | **Tournament → teams → players** | One tournament registers 8–16 captains. Each captain shares the registration link with 7–10 players, who create Sportzy IDs | Yes | — |
| 3 | **Match page → squad** | The booker shares the match page link on WhatsApp ("Bring your squad"); friends request spots and sign up | Yes (BookingConfirmation design) | — |
| 4 | **Open game → new player → new booker** | A player who joins via Find a game books their own slot next time | Yes | — |
| 5 | **Broadcast → viewers → bookers** | A streamed match on Facebook shows "Book this turf on Sportzy" in the post and pinned comment | Yes, with a manual caption; overlay gated | Overlay (SPOR-38) adds the on-screen call to action |
| 6 | **Organiser → organiser** | An organiser who ran a paid tournament refers another; the referrer gets 3 free streamed games (৳900 value) | Manual credit | Referral codes |
| 7 | **Highlights → shares** | A wicket or goal clip is posted with the venue, the teams tagged and a link | Manual edit by Persona G from stream recordings | Auto highlights (gated: stats) |
| 8 | **Venue-generated content** | Venues repost Sportzy's "Tonight at [venue]" story templates to their own pages | Yes (Canva templates) | — |
| 9 | **Community challenge** | A monthly "Floodlight League" for pickup teams: play 3 games booked through Sportzy in a month and enter a prize draw | Manual tracking | Later: team leaderboard |
| 10 | **Creator matches** | Local football or cricket creators stream their own games on Sportzy; followers book the same venue | Yes | — |

## 7. Main risks and what we do about them

| Risk | Early signal | Response |
|---|---|---|
| Go-live slips past 11 Dec | SPOR-14/15/16 open on 1 Dec | Apply the slip rule; keep pre-launch evergreen content running; owners and organisers keep onboarding |
| Venue supply caps out below 30 in Dhaka | Fewer than 20 active by the end of March | Widen to box-cricket cages, badminton halls and school grounds; open Chattogram in April (two-week field trip) |
| Owners keep peak hours off-platform | Bookings per venue below 10 a month | Sell off-peak demand, not peak demand; tournaments fill off-peak nights |
| Organisers won't pay | Fewer than 2 paid tournaments by the end of January | Lead with the 10% entry-fee collection, which costs organisers nothing up front; streams become an add-on |
| Repeat rate stalls around 20% | Jan and Feb cohorts | Prioritise the recurring-booking gate with product; run "same slot next week" reminders manually |
| Ad CAC too high | Cost per first booking above the stop rule in `budget_plan.md` | Move budget to organiser events and creators |

## 8. Team and cadence

The 10 personas are hats, not hires. See the RACI in `README.md`. Weekly rhythm:

- **Monday:** numbers review, using the weekly report.
- **Tuesday and Wednesday:** field sales days.
- **Thursday:** content shoot at a venue.
- **Friday and Saturday:** tournaments and match-day coverage.
- **Sunday:** plan next week and write captions.
