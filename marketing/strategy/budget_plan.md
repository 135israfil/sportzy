# Budget and paid advertising plan (BDT)

**Rule zero:** no money is spent until the founder approves a scenario and go-live has shipped. Nothing in this file is a forecast. Every cost and conversion figure is a **planning assumption to test**, marked (A). The weeks 1–4 experiments in § 5 replace these assumptions with real numbers.

## 1. Three scenarios (monthly, from launch in December)

| Line | Bootstrap | Growth | Aggressive |
|---|---:|---:|---:|
| Meta ads (Facebook and Instagram) | ৳20,000 | ৳70,000 | ৳1,60,000 |
| TikTok ads (test) | ৳0 | ৳10,000 | ৳40,000 |
| YouTube ads (test, the launch film) | ৳0 | ৳5,000 | ৳25,000 |
| Google Search ads | ৳3,000 | ৳10,000 | ৳25,000 |
| Creators and influencers (cash or kind) | ৳5,000 | ৳20,000 | ৳60,000 |
| Venue and organiser incentives (commission holidays, free streams), **pending approval** | ৳5,000 | ৳15,000 | ৳40,000 |
| Production (freelance editor, shoots, printing posters and standees) | ৳7,000 | ৳20,000 | ৳50,000 |
| **Total a month** | **৳40,000** | **৳1,50,000** | **৳4,00,000** |
| People assumed | Founder + 1 part-time content person | Founder + marketing exec + freelance editor | + field sales hire + full-time video |
| Expected activity | 3 feed posts a week, daily stories, 2 field-sales days a week, 1 tournament a week covered | 4–5 posts a week, 3 field days, 2 tournaments a week covered, 2 creator collabs a month | Daily posts, 5 field days, Chattogram team from month 4, 4 creator collabs a month |
| Acquisition assumption (A) | Mostly organic and field sales. Ads only retarget site visitors and promote tournaments. | Ads drive about 30% of first bookings (A) | Ads drive about 50% of first bookings (A); needs CAC proof first |
| Expected results by 14 May (A) | 20–24 active venues, 6–8 paid tournaments a month, repeat rate about 30% | The plan's targets: 30 venues, 10 paid tournaments a month, 35%+ | The targets reached 4–6 weeks earlier, if supply keeps up |
| Main risk | Too slow to reach 30 venues | Spending ahead of the venue supply | Paying for demand that venues can't serve; burn |

**Recommendation:** start on **Bootstrap for December and January**. Move to **Growth** only once two things are true: cost per first completed booking is under the stop rule (§ 4), and at least 14 venues are active. Aggressive makes sense only with external funding and proven CAC.

## 2. Campaign structure (Meta)

| Campaign (objective) | Ad sets (audience hypotheses) | Creative (see `campaigns/*/ads.md`) | Landing page | Conversion event |
|---|---|---|---|---|
| **C1 Venue owners** (leads) | Interests: business owners, sports facility, "turf" page admins; Dhaka; 25–55. Plus a custom audience from venue page visitors. | 3 angles: empty hours, cash control, weekly payout | `/play/owner/signup/` (List your turf) | `owner_signup_started`, `owner_signup_submitted` |
| **C2 Football players** (sales) | Dhaka 17–34; interests football, futsal, Premier League; radius 5 km around active venues | 3 angles: tonight's slots, one link for the squad, floodlights | Homepage search, pre-filled with area and "Tonight" | `booking_completed` (Purchase) |
| **C3 Cricket players** (sales) | Dhaka 17–40; interests cricket, BPL, box cricket | 3 angles: box cricket nights, T10 with friends, live scoreboard | Homepage search with Cricket | `booking_completed` |
| **C4 Organisers** (leads) | Admins of sports pages and groups (proxy: interest in event planning plus sports); people engaged with tournament posts | 3 angles: money collected, fixtures done, stream the final | Tournament organiser landing page (§ 3) | `organiser_lead`, `tournament_created`, `tournament_published` |
| **C5 University communities** (traffic, then leads) | 18–24, education interests, key universities' areas (Bashundhara, Dhanmondi, Mohakhali) | Campus league, student squads | University league page | `organiser_lead` |
| **C6 Retargeting** (sales) | Site visitors 14 days without a booking; owner signup started but not finished; tournament page viewers | "Slot still open", "Finish listing your turf", "Registration closes Friday" | The exact page they left | `booking_completed`, `owner_signup_submitted`, `team_registration_paid` |
| **C7 Repeat booking** (sales) | Customers with 1 completed booking, 5–25 days ago | "Same time next week?", "Your turf has 9 PM free Thursday" | Venue page of their last booking | `booking_completed` (repeat) |

- **TikTok:** C2 and C3 test only, with Spark Ads boosting the best organic reels.
- **YouTube:** the 30-second launch film and the venue tour, targeting Dhaka 18–34 sports viewers.
- **Google Search (exact and phrase match):** "turf booking dhaka", "futsal turf near me", "box cricket dhaka", "turf bashundhara", "football turf mirpur", plus Bangla queries such as "টার্ফ বুকিং". Negatives: "artificial grass price", "turf grass seller".

## 3. Landing page recommendations (product team)

| Page | Exists? | Needs |
|---|---|---|
| Homepage search | Yes (design) | UTM-preserving deep links: `?area=&sport=&when=tonight` |
| Venue page | Yes | A "Tonight" filter; venue-specific ad links |
| List your turf | Yes | A lead form that also works without a full signup (name, turf, phone) |
| Tournament organiser landing page | **No** | Build it: what it does, pricing (once approved), a 3-step "how it works", a demo booking form |
| University and corporate league page | **No** | Can be a section of the organiser page at first |

## 4. Stop and scale rules (set the numbers after the experiments)

- **Stop rule (A):** pause an ad set if cost per completed first booking exceeds **৳250**, or cost per owner lead exceeds **৳600**, after ৳3,000 spent. Revise both after week 4 of real data.
- **Scale rule:** raise spend 20% a week on any ad set that beats the target cost two weeks in a row and has venue capacity behind it.
- **Payback check:** first-booking CAC should pay back within 3 bookings at 8% commission (about ৳120 a booking on a ৳1,500 slot (A)). If it can't, the money goes to field sales and organisers instead.

## 5. Experiments that replace the assumptions (weeks 1–4 after launch)

| # | Question | Test | Budget | Decision |
|---|---|---|---:|---|
| E1 | What does a Dhaka player cost to reach and click? | C2 with 3 creatives × 2 audiences, ৳500 a day for 7 days | ৳3,500 | Real CPM, CTR and CPC replace the assumptions |
| E2 | Bangla or English copy? | Same creative, BN vs EN caption | ৳2,000 | Default language per segment |
| E3 | "Tonight" urgency vs "one link for your squad" | Two angles on C2 | ৳2,000 | Winning angle for January |
| E4 | Owner leads from ads vs field visits | C1 at ৳300 a day for 10 days vs 10 field visits | ৳3,000 | Where the sales lead spends time |
| E5 | Do organisers respond to ads? | C4 lead form, 14 days | ৳4,000 | Keep or drop C4 |
