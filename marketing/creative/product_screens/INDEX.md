# Product screens: what you may use, and where

These are rendered from the founder's **"Sportzy Homepage Redesign" design canvas** (Floodlight Night), the design system applied sitewide per SPOR-48 and SPOR-63. They are **design renders, not captures of the live site**. Once sportzy.live is live, replace each one with a real capture of the same page before paid ads run, and check that the live page matches.

**Changes made for marketing use** (render copies only; the canvas is untouched):

- QA test accounts were replaced with demo handles: `rafi_k`, `tanvir_10`, `sabbir_fc`, `nayeem.u`, `imran_k`, "Rafi Karim".
- Real Dhaka venue names were replaced with demo names: Turf Nation → Green Line Turf, JAFF Turf → Pitch 9 Arena, Greenfield Arena → Banani Sports Field, Dhupkhola Field → Wari Floodlit Field. A real venue's name appears only with its written OK.
- Placeholder rating and address text was filled with demo values.

The viewport files (`*-desktop.png` at 1440×900, `*-mobile.png` at 390×844 @3x) are the ones checked. The `*-full.png` files are full-page and **still contain design placeholders** ("[4.x]", "[৳ —]", "[venue number]"), so they're internal reference only.

| File | Shows | Marketing status | Why |
|---|---|---|---|
| main-desktop.png, main-mobile.png | Homepage hero: "Your next match is one tap away", area/when/sport search | **Approved** (Built: SPOR-29, 83) | Clean; mentions bKash/Nagad, which central collection still uses |
| discover-desktop.png, discover-mobile.png | Find a game: open games with spots left | **Approved** (Built: SPOR-40) | Clean |
| turfdetail-desktop.png, turfdetail-mobile.png | Venue page: gallery, verified badge, slot availability | **Approved, viewport crop only** | The full page shows the old "send money to the venue" step (superseded by SPOR-89), so never use the full page |
| matchroster-desktop.png, matchroster-mobile.png | Match page: roster and requests | **Approved** (Built: SPOR-40, 41) | Clean after the test names were swapped |
| managematch-desktop.png, managematch-mobile.png | Organiser manages the match: players, teams, crew | **Approved** (Built: SPOR-35, 41) | Clean |
| signup-desktop.png, signup-mobile.png | Sign up | **Approved** (Built: SPOR-79) | Clean |
| ownersignup-desktop.png, ownersignup-mobile.png | List your turf | **Approved for owner campaigns** (Built: SPOR-18, 74) | Clean |
| dashboard-desktop.png | Player dashboard | **Not approved** | Shows "The venue is checking your bKash/Nagad reference", an old flow |
| dashboard-mobile.png | Player dashboard, top | Approved for organic only | The top fold is clean; recheck once the live site exists |
| ownerdashboard-*.png | Owner dashboard with "payments to verify" | **Not approved** | Manual payment checks were replaced by central collection (SPOR-89). Re-capture from the live owner dashboard (SPOR-85) |

**Rules for using screens:**

1. Put screens in a phone or laptop frame. Never present them as a native app: the iOS and Android apps are planned (SPOR-110, 111), not built.
2. Show only features marked Built in `strategy/marketing_strategy.md` § Feature status.
3. Paid ads need live-site captures, so this folder is a placeholder until go-live.
