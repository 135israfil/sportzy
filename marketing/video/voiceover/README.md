# Voice-overs (ElevenLabs)

`make_voiceover.py` speaks each video's caption lines (`../renders/<name>_bn.srt`), each at its own cue. It mixes them under the picture at -16 LUFS and writes `../renders/voiced/<name>_vo.mp4`. The silent masters are left untouched.

## One-time setup (founder)

1. **API key:** open the cloud environment menu in the session's title bar and choose **Edit**. Under **Network secrets** (called **API credentials** in older versions), add `ELEVENLABS_API_KEY`. If there's no such section, add it as an environment variable. Never commit the key or paste it into chat.
2. **Network access:** in the same settings, add `api.elevenlabs.io` under **Allowed domains**, and leave **Allow package managers** ticked.
3. **Voice:** pick a voice in the ElevenLabs Voice Library that sounds natural in **Bangladeshi** Bangla (not Kolkata), then add its ID as `ELEVENLABS_VOICE_ID`. A warm, young male or female voice suits the player videos.
4. **New session:** start one so the settings take effect.

## Run

```bash
cd marketing/video/voiceover
python3 make_voiceover.py --check                     # character count + key and network check (free)
python3 make_voiceover.py VID-12_tonight_in_dhaka_9x16_sample   # try one video first and listen
python3 make_voiceover.py                             # all videos
python3 make_voiceover.py --lang en VID-03_how_to_book_9x16     # English version, if needed
```

The full Bangla set is about **1,200 characters**, a small fraction of a free ElevenLabs month. Clips are cached in `cache/`, so re-runs and re-mixes don't cost characters again.

The default model is `eleven_v3`, which handles Bengali. To change it, set `ELEVENLABS_MODEL`.

**Filled videos** (VID-09, VID-12, VID-13 from real data):

```bash
python3 make_voiceover.py --video ../out/VID-12_tonight_in_dhaka_9x16_2026-12-12.mp4 --srt ../renders/VID-12_tonight_in_dhaka_9x16_sample_bn.srt
```

Use the filled video's own lines if the data changed the captions.

## Quality checks before posting

- **Listen to every line.** Check that Bangla words and English brand words are pronounced correctly: Sportzy, bKash, Nagad, QR Pay BD, venue names. If a word is wrong, respell it in the caption text, for example "স্পোর্টজি", and re-run.
- **Fit:** a line is sped up by at most 1.2× to fit its slot. If the script warns about overlap, shorten that caption line.
- **Music:** add it underneath at about -24 LUFS so the voice stays clear.
- **Label it as AI:** where a platform requires it (Meta and TikTok do for realistic AI audio), mark the voice as AI-generated.
