# Tracking plan

**Status:** a specification for the product team. Marketing doesn't change product code (see the guardrails in `README.md`). Each event below needs a product ticket. Until an event is live, the metric comes from the admin export (see `kpi_dashboard_spec.md`).

**Consent:** load the Meta Pixel and GA4 only after the visitor accepts analytics cookies (SPOR-105). Before consent, nothing fires. Send server-side conversions (Meta Conversions API) only for completed bookings and signups, hashed, and only where the privacy policy allows it. **Founder and engineering to confirm.**

## 1. Events

| Event | When it fires | Key properties | GA4 | Meta | Used for |
|---|---|---|---|---|---|
| `page_view` | Every page | `page_type` (home, search, venue, match, tournament, owner_signup, dashboard), `lang` (bn/en) | auto | PageView | Traffic |
| `search_performed` | Search submitted | `area`, `sport`, `date`, `time_band` (morning / afternoon / evening / night), `results_count` | custom | Search | Player funnel |
| `venue_viewed` | Venue page opens | `venue_id`, `area`, `sport` | `view_item` | ViewContent | Player funnel, retargeting C6 |
| `booking_hold_started` | Slot held (timer starts) | `venue_id`, `slot_start`, `price_bdt`, `is_offpeak`, `discount_applied` | `add_to_cart` | AddToCart | Hold → paid |
| `booking_payment_started` | The payment method is chosen | `method` (bkash / nagad / qrpay_bd) | `begin_checkout` | InitiateCheckout | Funnel drop-off |
| `booking_completed` | Payment confirmed by the gateway | `booking_id`, `venue_id`, `value`, `currency`=BDT, `is_first_booking`, `method`, `is_offpeak` | `purchase` | Purchase | North Star, C2/C3/C6/C7 optimisation |
| `booking_hold_expired` | The hold timer runs out without payment | `venue_id`, `price_bdt` | custom | — | Hold expiry rate |
| `booking_refunded` | Refund issued | `booking_id`, `reason` | `refund` | — | Quality |
| `spot_request_sent` | A player requests to join an open match (request-to-attend) | `match_id`, `venue_id` | custom | — | Find a game |
| `spot_request_accepted` | The host accepts | `match_id` | custom | — | Find a game |
| `owner_signup_started` | The first step of owner signup opens | `source` | `generate_lead` (step 1) | Lead (optional) | C1 |
| `owner_signup_submitted` | Owner signup is submitted | `venue_type`, `area`, `courts` | `sign_up` | CompleteRegistration | C1 |
| `organiser_lead` | The organiser landing page form is submitted, or the organiser access request is sent (SPOR-100) | `org_type` (club / company / university / academy / community), `sport` | `generate_lead` | Lead | C4, C5 |
| `tournament_created` | Draft saved | `tournament_id`, `sport`, `fee_bdt`, `max_teams` | custom | — | Tournament funnel |
| `tournament_published` | Registration opens | `tournament_id` | custom | — | Tournament funnel |
| `team_registration_paid` | A team's entry fee is paid | `tournament_id`, `value` | custom | Purchase (`content_type`=tournament) | Tournament funnel, C6 |
| `stream_started` | A Streemzy stream starts, from the Streemzy logs | `tournament_id` (if any), `platforms` | — | — | Paid tournaments |
| `share_clicked` | A share button is tapped on a match or tournament page | `object_type`, `channel` (whatsapp / facebook / copy) | `share` | — | Growth loops |
| `lang_switched` | Bangla / English toggle | `to` | custom | — | Copy language decisions |

**Rules:**

- No personal data goes in event properties: no names, phones or emails. Use IDs only.
- Server-side and admin numbers win over client-side events when they disagree.
- Exclude `qa_*` and staff accounts with the `is_internal` user property.

## 2. UTM rules

Every link Sportzy shares outside the site carries UTMs. Use lowercase, with hyphens, no spaces.

| Parameter | Values |
|---|---|
| `utm_source` | `facebook`, `instagram`, `tiktok`, `youtube`, `google`, `whatsapp`, `messenger`, `email`, `poster_qr`, `standee_qr`, `partner` |
| `utm_medium` | `paid_social`, `organic_social`, `cpc`, `broadcast` (opted-in WhatsApp list), `dm`, `qr`, `referral`, `email` |
| `utm_campaign` | The campaign file name: for example `launch-announcement`, `c2-football`, `ramadan-night-tournaments`, `venue-acquisition` |
| `utm_content` | The Caption ID or ad angle: for example `cap-041`, `c2-tonight`, `des-07-mirpur` |
| `utm_term` | Google keyword only |

**Examples:**

- `https://sportzy.live/?utm_source=facebook&utm_medium=paid_social&utm_campaign=c2-football&utm_content=c2-tonight`
- `https://sportzy.live/play/owner/signup/?utm_source=standee_qr&utm_medium=qr&utm_campaign=venue-acquisition&utm_content=des-07-[venue-slug]`

Keep the link builder as a tab in the KPI sheet (columns: base URL, source, medium, campaign, content, final URL). Shorten links only with a Sportzy-controlled domain once one exists.

## 3. Meta setup

- **Pixel events:** PageView, Search, ViewContent, AddToCart, InitiateCheckout, Purchase, Lead, CompleteRegistration (see § 1).
- **Custom audiences:**
  - venue page viewers (14 d)
  - hold started but not purchased (7 d)
  - owner signup started but not submitted (14 d)
  - tournament page viewers (14 d)
  - customers with 1 completed booking, 5–25 days ago (C7; via a hashed customer list only with consent)
- **Optimisation:** C1 → CompleteRegistration; C2/C3 → Purchase once there are 50 or more a week, otherwise optimise for AddToCart; C4/C5 → Lead.

## 4. QA before any paid campaign starts

- [ ] Cookie banner blocks Pixel and GA4 until consent (check in a fresh browser)
- [ ] A test booking fires `booking_completed` once, with the right value in BDT, and is excluded as internal
- [ ] UTMs survive the redirect to the venue page and the payment return
- [ ] Meta Events Manager and GA4 DebugView both show the events
- [ ] Owner signup and organiser lead events fire on submit, not on page load
