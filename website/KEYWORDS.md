# Sportzy keyword map

Each page targets one primary keyword (used in its title, description, H1 and opening paragraph) plus related secondary keywords used in headings, body text and FAQ answers. One page per primary keyword, so pages don't compete with each other.

| Page | Primary keyword | Secondary keywords | Search intent |
|---|---|---|---|
| `/` | free live sports streaming app | sports scoring app, live stream sports from phone, grassroots sports broadcasting | Brand + discovery |
| `/scorezy/` | live scoring app with scoreboard overlay | live score overlay for live stream, cricket scorecard overlay, sports graphics for live stream, lower thirds | Product |
| `/streemzy/` | stream to Facebook, YouTube & Instagram at the same time | multistreaming, simulcast, restream, RTMP streaming, live stream to multiple platforms | Product |
| `/visionzy/` | AI ball tracking | LBW review, AI cricket highlights, VAR for grassroots football, sports video analysis | Product (waitlist) |
| `/app/` | multi-camera sports streaming from phones | multi-camera live streaming app, use phones as cameras | Product (waitlist) |
| `/cricket-live-streaming/` | cricket live streaming app | live cricket scoreboard app, stream cricket from phone, local cricket tournament streaming | Use case |
| `/football-live-streaming/` | football live streaming app | stream football match from phone, grassroots football streaming, football score overlay | Use case |
| `/tournament-live-streaming/` | tournament live streaming | league live streaming, sponsor overlay live stream, stream sports tournament | Use case (organizers) |
| `/guides/` | sports live streaming guides | how to live stream sports | Hub |
| `/guides/how-to-live-stream-cricket-on-youtube/` | how to live stream cricket on YouTube | cricket YouTube live with scoreboard, cricket live stream from mobile | How-to |
| `/guides/how-to-add-scoreboard-to-facebook-live/` | how to add scoreboard to Facebook Live | Facebook Live score overlay, Facebook Live graphics without OBS | How-to |
| `/guides/stream-to-facebook-youtube-instagram-at-once/` | stream to Facebook and YouTube at the same time | multistream free, simulcast from phone, go live on multiple platforms | How-to |
| `/about/` | Sportzy | sports tech startup Bangladesh, grassroots sports broadcasting | Brand |

## Keeping it working

- The keywords above are chosen from how organizers search; they are **not** measured search volumes. About 4–8 weeks after launch, open Google Search Console → *Performance → Queries*, see which searches actually bring impressions, and adjust titles and copy toward them.
- Every new guide should target one new question people search for (for example "how to stream kabaddi live" or "best camera position for football streaming"). Add it in `build.py` and `pages/`, link it from `/guides/` and from at least one product page, then rebuild.
- Don't add a `<meta name="keywords">` tag. Google ignores it.
