# Video renders (motion-graphics masters)

These are rendered from code in `../motion/` with the Floodlight Night design system and the approved product screens. Every file is H.264 MP4 at 30 fps.

**There is no audio in any of them.** No music or voice-over has been produced yet. The `.srt` files hold the Bangla and English lines from each script.

| ID | File | Length | Format | Gate | Status |
|---|---|---|---|---|---|
| VID-01 | VID-01_brand_intro_animated_9x16.mp4 | 30 s | 1080×1920 | Pre-launch | Draft (animated cut; the filmed version still needs a shoot) |
| VID-01 | VID-01_brand_intro_animated_1x1.mp4 | 30 s | 1080×1080 | Pre-launch | Draft |
| VID-01 | VID-01_brand_intro_animated_15s_9x16.mp4 | 15 s | 1080×1920 | Pre-launch | Draft |
| VID-02 | VID-02_launch_announcement_9x16.mp4 | 20 s | 1080×1920 | **Go-live** | Draft |
| VID-02 | VID-02_launch_announcement_1x1.mp4 | 20 s | 1080×1080 | **Go-live** | Draft |
| VID-02 | VID-02_launch_teaser_10s_9x16.mp4 | 10 s | 1080×1920 | Pre-launch | Draft |
| VID-03 | VID-03_how_to_book_9x16.mp4 | 45 s | 1080×1920 | **Go-live** | Draft |
| VID-05 | VID-05_organiser_tournaments_9x16.mp4 | 45 s | 1080×1920 | Organiser access live | Draft (team counts are SAMPLE) |
| VID-06 | VID-06_find_a_game_9x16.mp4 | 25 s | 1080×1920 | **Go-live** | Draft |
| VID-09 | VID-09_tournament_promo_9x16_sample.mp4, `_1x1_sample.mp4` | 15 s | 9:16, 1:1 | Per tournament | **SAMPLE**: re-render with real data |
| VID-12 | VID-12_tonight_in_dhaka_9x16_sample.mp4 | 15 s | 1080×1920 | Go-live | **SAMPLE**: re-render weekly with real slots |
| VID-13 | VID-13_match_of_the_week_bumper_9x16_sample.mp4 | 5 s | 1080×1920 | Per match | **SAMPLE** bumper to put before real footage |

Each video also has a `<name>_poster.png` (a cover frame) and `<name>_bn.srt` / `_en.srt` caption files.

**Not rendered, because they need real footage or approved screen captures:**

- VID-04 and VID-14: owner dashboard
- VID-07: stream demo
- VID-08: testimonials
- VID-10: Turf Talk
- VID-11: founder story
- VID-13: the full match edit

The scripts in `../scripts/` say what each one needs.

## Before posting

1. **Add music** in CapCut, or from the Meta Sound Collection / TikTok commercial library. Only use tracks licensed for business use. Keep it under the on-screen beats: hooks land at 0–3 s.
2. **Optional voice-over:** record the lines in `../voiceovers/VID-xx_vo.md`.
3. **Captions:** keep or upload the `.srt` files. The key text is already burned into the picture.
4. **Data:** files marked SAMPLE contain made-up teams, venues, slots and prices. Re-render them from real data first.
5. **Gates and claims:** respect the launch gate, and don't post anything that shows a feature before it's live.

## Re-rendering and making real versions

All commands run from `marketing/video/motion/`.

**Rebuild and render everything:**

```bash
python3 build_videos.py && node render_videos.js
```

**Render a single video:**

```bash
node render_videos.js VID-12_tonight_in_dhaka_9x16_sample
```

**Make this week's real version** of VID-12. It uses the same JSON as the static design. Copy `creative/designs/data/open_slots.json`, fill in real slots, then run:

```bash
python3 build_videos.py fill VID-12 ../my_slots.json
```

The output goes to `video/out/`. VID-09 and VID-13 work the same way, using `tournament.json` and `live_thumbnail.json`.

**Check a layout without a full render:**

```bash
node preview.js <name> out.png 1.5 6 12
```

**Change the launch date** in one place: `LAUNCH_DATE_*` in `creative/designs/src/kit.py`. Then rebuild the designs and the videos.
