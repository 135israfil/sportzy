# KPI dashboard spec

**Owner:** Analyst (Persona J). **Reviewed by:** CMO and the founder in the Monday review (`weekly_reports/TEMPLATE.md`).

**Build:** one Google Sheet with five tabs: North Star, Venues, Tournaments, Players, Marketing. Fill it from the Sportzy admin exports, Meta Ads Manager, GA4 and the CRM tab. A Looker Studio view can come later, once the events in `tracking_plan.md` are live.

**Rule:** the dashboard shows only measured numbers. Targets sit in their own column, labelled "target (estimate)". Never fill a cell with a guess.

## 1. North Star targets

All three are estimates set in `strategy/marketing_strategy.md` § 2. The founder can change them.

| KPI | Definition | Formula | Source | Monthly target (estimate) |
|---|---|---|---|---|
| **Active venues** | An onboarded venue with verified availability and at least 1 **completed** Sportzy booking in the calendar month | `COUNT(DISTINCT venue_id WHERE booking.status = completed AND booking.source = sportzy AND month = M)` | Admin bookings export | Dec 8 · Jan 14 · Feb 18 · Mar 22 · Apr 26 · May 30 |
| **Paid tournaments** | A tournament whose organiser paid Sportzy for at least one of: streams, a Club & League plan, or the 10% entry-fee commission. *Definition pending founder approval.* | `COUNT(DISTINCT tournament_id WHERE sportzy_revenue > 0 AND first_match_date in M)` | Admin tournaments + payments export | Dec 1 · Jan 3 · Feb 5 · Mar 7 · Apr 9 · May 10 |
| **Repeat booker rate** | Of the customers whose first completed booking was in month M, the share who complete a second booking within 60 days | `customers with ≥2 completed bookings within 60 days of first ÷ customers with first completed booking in M` | Admin bookings export (customer_id, completed_at) | Jan 20% · Feb 25% · Mar 30% · Apr 33% · May 35% |

**Notes:**

- A booking counts once its slot has been played and its status is completed. Cancelled or refunded bookings don't count.
- Repeat rate is a cohort metric, so month M can only be reported 60 days after it ends. Also report a **provisional 30-day rate** every week as an early signal, labelled "provisional".
- Tournament bookings made by an organiser count for venue activity. They do **not** count for repeat booker rate, which counts players and captains only.

## 2. Venue funnel (tab: Venues)

| Metric | Formula | Source |
|---|---|---|
| Listed | Rows in CRM with stage ≥ 1 | CRM tab |
| Contacted | Stage ≥ 2 | CRM tab |
| Demo done | Stage ≥ 3 | CRM tab |
| Signed | Stage ≥ 4 | CRM tab |
| Onboarded | Stage ≥ 5 (checklist complete, `sales/venue_outreach.md` § 7) | CRM tab |
| Active (month) | See § 1 | Admin export |
| Contact → signed rate | Signed ÷ Contacted | CRM |
| Signed → active (30 days) | Venues active within 30 days of signing ÷ Signed | CRM + admin |
| Bookings per active venue | Completed Sportzy bookings ÷ Active venues | Admin |
| Off-peak share | Bookings in slots marked off-peak ÷ all completed bookings | Admin |
| Venue GMV | Sum of completed Sportzy booking value | Admin |
| Commission revenue | GMV × 8% (pending approval), minus any launch-offer waivers | Admin |
| Payout on time | Weekly payouts paid by the due day ÷ payouts due | Finance |
| Churned venues | Active last month but not this month | Admin |

### CRM sheet spec (tab: CRM)

One row per venue:

`venue_id, venue_name, area, city, venue_type (turf / futsal / box cricket / badminton / other), sports, courts, owner_name, owner_phone, source (FB DM / WhatsApp / referral / ad / walk-in), sales_owner, stage (1–6), stage_date, next_action, next_action_date, objection, incentive_offered (needs approval), consent_marketing (yes / no / not asked), first_booking_date, notes`

Rules:

- Personal phone numbers live only in this sheet, and only the sales team can see it.
- Never copy the CRM into public files or the repo.

## 3. Tournament funnel (tab: Tournaments)

| Metric | Formula | Source |
|---|---|---|
| Organiser leads | `organiser_lead` events + CRM rows (organiser) | GA4 + CRM |
| Organiser access approved | SPOR-100 approvals | Admin |
| Tournaments created | `tournament_created` | Admin |
| Tournaments published | `tournament_published` | Admin |
| Teams registered (paid) | `team_registration_paid` | Admin |
| Fill rate | Paid teams ÷ max teams | Admin |
| Entry fees collected (GMV) | Sum of paid entry fees | Admin |
| Streams run | `stream_started`, from Streemzy | Streemzy |
| Paid tournaments | See § 1 | Admin + payments |
| Revenue per paid tournament | Sportzy revenue (commission + streams + plans) ÷ paid tournaments | Payments |
| Repeat organisers | Organisers with ≥2 tournaments in 90 days ÷ organisers with ≥1 | Admin |
| Refund rate | Refunded registrations ÷ paid registrations | Admin |

## 4. Player funnel (tab: Players)

| Metric | Formula | Source |
|---|---|---|
| Site sessions (Dhaka) | GA4 sessions, city = Dhaka | GA4 |
| Search to venue view | `venue_viewed` ÷ `search_performed` | GA4 |
| Hold started | `booking_hold_started` | GA4 / admin |
| Hold → paid | `booking_completed` ÷ `booking_hold_started` | Admin |
| Hold expiry rate | Expired holds ÷ holds started | Admin |
| First bookings | Customers whose first completed booking is in the period | Admin |
| Repeat booker rate | See § 1 | Admin |
| Bookings per booker (60 d) | Completed bookings ÷ unique bookers | Admin |
| Spot requests (Find a game) | `spot_request_sent`, and the accepted share | Admin |
| Payment method mix | bKash / Nagad / QR Pay BD share | Payments |
| WhatsApp opt-ins | Rows in the opt-in list (consent recorded) | Opt-in sheet |

## 5. Marketing performance (tab: Marketing)

| Metric | Formula | Source |
|---|---|---|
| Spend by campaign (C1–C7) | Ads Manager, BDT | Meta, TikTok, Google |
| CPM, CTR, CPC | Platform-reported | Ads platforms |
| Cost per owner lead | Spend (C1) ÷ `owner_signup_submitted` attributed to C1 | Ads + GA4 |
| Cost per first booking | Spend (C2, C3, C6) ÷ first completed bookings with that `utm_campaign` | Ads + admin |
| Cost per organiser lead | Spend (C4, C5) ÷ `organiser_lead` | Ads + GA4 |
| Organic reach and 3-s views | Per post, joined to the Caption ID | Meta Business Suite, TikTok |
| Saves, shares, comments | Per post | Platforms |
| Posts published vs planned | Published rows ÷ calendar rows for the week | Calendar CSV |
| Bookings by source | `booking_completed` split by `utm_source` / `utm_medium` (or "direct / unknown") | GA4 + admin |

**Attribution:**

- Use last non-direct click with a 7-day click window. Always also show the share of "direct / unknown" bookings.
- Never report platform-modelled conversions as Sportzy bookings. Use completed bookings from the admin export.

**Stop and scale rules** (copied from `strategy/budget_plan.md` § 4; assumptions until experiments E1–E5 finish):

- **Stop:** after ৳3,000 spent, pause an ad set if cost per completed first booking is above ৳250, or cost per owner lead is above ৳600.
- **Scale:** raise budget by up to 20% a week while cost stays under 70% of the stop rule for 7 days.

## 6. Layout

Top row, as four tiles: Active venues, Paid tournaments (month to date), Provisional 30-day repeat rate, Spend vs plan. Each tile shows the measured value, the target (estimate) and the change from last week.

Below the tiles, one weekly line chart per funnel, then the campaign table sorted by spend.

## 7. Data quality checks (every Monday)

- [ ] Admin export row count matches the admin dashboard's booking total for the week
- [ ] Test bookings (QA accounts, `qa_*` names) are excluded
- [ ] Every paid booking has a `utm_*` value or is marked "direct / unknown"
- [ ] Ad spend in the sheet matches Ads Manager billing
- [ ] No personal data (names, phones) in the Marketing tab
