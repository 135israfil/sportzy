# VID-12: Weekly promo: "Tonight in Dhaka"

| | |
|---|---|
| **Objective** | Fill tonight's or the weekend's open slots |
| **Audience** | Players |
| **Duration** | 15 s |
| **Formats** | 9:16 |
| **Hook (first 3 s)** | A clock hits 7:00 PM; slot cards flip in. |
| **CTA** | Book now |
| **Production status** | Template rendered (no audio): `renders/VID-12_tonight_in_dhaka_9x16_sample.mp4`. Make it weekly with `python3 motion/build_videos.py fill VID-12 <open_slots.json>`. |

## Scenes

| Time | Visual | Camera | Voice-over (BN) | Voice-over (EN) | On-screen text | Music / sound |
|---|---|---|---|---|---|---|
| 0–3 s | Clock 7:00 PM; "TONIGHT IN DHAKA" | Graphic | আজ রাতে ঢাকায়। | Tonight in Dhaka. | TONIGHT IN DHAKA | Tick |
| 3–12 s | 3–4 real open slots flip in (area, time, price) over turf b-roll | Graphic over b-roll | [Area] রাত [time], [Area] রাত [time]। | [Area] at [time], [Area] at [time]. | [AREA] · [TIME] · ৳[PRICE] | UI flips |
| 12–15 s | "Book now", sportzy.live | Graphic | এখনই বুক করো। | Book now. | BOOK NOW | Hit |

## Editing instructions

- Cut on the beat; first frame must be the hook (no logo intro).
- Burn in Bangla subtitles (Hind Siliguri 600, white with a 60% black box) and keep an English subtitle file.
- Colour: lift greens, warm the highlights, keep the floodlight glow; follow `../editing_guides/editing_guide.md`.
- End card: logo + CTA, 2 s, inside the safe zones.

## Notes

Made weekly from a Canva or CapCut template in 20 minutes. Slot data must be real on the day of posting.
