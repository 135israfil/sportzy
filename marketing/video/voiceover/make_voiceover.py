"""Generate Bangla (or English) voice-overs with ElevenLabs and mix them into the rendered videos.

The timed voice-over script is each video's caption file (renders/<name>_<lang>.srt): every caption
line is spoken, starting at its caption time, sped up slightly (max 1.2x) if it would overrun its slot.

  python3 make_voiceover.py --check                 # lines, character count (ElevenLabs bills per character), API reachability
  python3 make_voiceover.py                         # all videos in ../renders -> ../renders/voiced/<name>_vo.mp4
  python3 make_voiceover.py VID-03_how_to_book_9x16 # one video
  python3 make_voiceover.py --lang en ...           # English voice-over from the _en.srt files
  python3 make_voiceover.py --video path/to/out.mp4 --srt path/to/out_bn.srt   # a filled video from ../out/

Environment:
  ELEVENLABS_API_KEY   required (store it as an environment secret, never in the repo)
  ELEVENLABS_VOICE_ID  voice to use (pick one in the ElevenLabs Voice Library that sounds natural in Bangladeshi Bangla)
  ELEVENLABS_MODEL     default eleven_v3 (Bengali-capable); eleven_multilingual_v2 / eleven_flash_v2_5 also work for English
  ELEVENLABS_AUTH      leave unset to send the key as xi-api-key; set to "proxy" if an environment Network secret
                       already injects an xi-api-key header (ElevenLabs rejects two auth headers, and Bearer auth)
Generated clips are cached in voiceover/cache/ by text+voice+model, so re-runs don't cost characters again.
"""
import argparse, hashlib, json, os, pathlib, re, subprocess, sys, urllib.error, urllib.request

HERE = pathlib.Path(__file__).parent
RENDERS = HERE.parent / "renders"
OUT = RENDERS / "voiced"
CACHE = HERE / "cache"
API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128"
MAX_SPEEDUP = 1.2


def parse_srt(path):
    lines = []
    for block in re.split(r"\n\s*\n", pathlib.Path(path).read_text(encoding="utf-8").strip()):
        rows = block.strip().splitlines()
        if len(rows) < 3:
            continue
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", rows[1])
        if not m:
            continue
        g = list(map(int, m.groups()))
        t0 = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        t1 = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        text = " ".join(rows[2:]).strip()
        if text:
            lines.append((t0, t1, text))
    return lines


def duration(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).decode().strip())


def headers(key, extra=None):
    h = dict(extra or {})
    if os.environ.get("ELEVENLABS_AUTH") != "proxy":
        h["xi-api-key"] = key
    return h


def tts(text, voice, model, key):
    CACHE.mkdir(exist_ok=True)
    f = CACHE / (hashlib.sha1(f"{model}|{voice}|{text}".encode()).hexdigest()[:16] + ".mp3")
    if f.exists():
        return f
    body = json.dumps({"text": text, "model_id": model, "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}).encode()
    req = urllib.request.Request(API.format(voice=voice), data=body, method="POST",
                                 headers=headers(key, {"Content-Type": "application/json", "Accept": "audio/mpeg"}))
    with urllib.request.urlopen(req, timeout=120) as r:
        f.write_bytes(r.read())
    return f


def mix(video, clips, out):
    """clips: [(start_s, slot_s, mp3)] -> video with the voice track (loudness-normalised to -16 LUFS)."""
    vdur = duration(video)
    inputs, filters, labels = ["-i", str(video)], [], []
    for i, (t0, slot, mp3) in enumerate(clips, 1):
        inputs += ["-i", str(mp3)]
        d = duration(mp3)
        speed = min(MAX_SPEEDUP, max(1.0, d / max(slot, .3)))
        if d / speed > slot + .05:
            print(f"   ! line at {t0:.1f}s is {d:.1f}s for a {slot:.1f}s slot even at {MAX_SPEEDUP}x; it will overlap the next line. Shorten the text.")
        filters.append(f"[{i}:a]atempo={speed:.3f},adelay={int(t0 * 1000)}:all=1[a{i}]")
        labels.append(f"[a{i}]")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,apad,atrim=0:{vdur:.3f},loudnorm=I=-16:TP=-1.5:LRA=11[vo]")
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters), "-map", "0:v", "-map", "[vo]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart", str(out)], check=True)


def jobs(args):
    if args.video:
        return [(pathlib.Path(args.video), pathlib.Path(args.srt))]
    names = args.names or sorted(p.stem for p in RENDERS.glob("*.mp4"))
    return [(RENDERS / f"{n}.mp4", RENDERS / f"{n}_{args.lang}.srt") for n in names]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--lang", default="bn", choices=["bn", "en"])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--video"); ap.add_argument("--srt")
    args = ap.parse_args()
    key, voice = os.environ.get("ELEVENLABS_API_KEY"), os.environ.get("ELEVENLABS_VOICE_ID")
    model = os.environ.get("ELEVENLABS_MODEL", "eleven_v3")
    total = 0
    work = []
    for video, srt in jobs(args):
        if not video.exists() or not srt.exists():
            print(f"skip {video.name}: missing video or {srt.name}"); continue
        lines = parse_srt(srt)
        if not lines:
            print(f"skip {video.name}: no {args.lang} lines (e.g. a music-only bumper)"); continue
        chars = sum(len(t) for _, _, t in lines); total += chars
        work.append((video, lines))
        print(f"{video.name}: {len(lines)} lines, {chars} characters")
    print(f"TOTAL {total} characters ({args.lang}, model {model}). Cached lines are not billed again.")
    proxy = os.environ.get("ELEVENLABS_AUTH") == "proxy"
    if args.check:
        if not key and not proxy:
            print("ELEVENLABS_API_KEY is not set."); sys.exit(1)
        if not voice:
            print("ELEVENLABS_VOICE_ID is not set."); sys.exit(1)
        try:
            with urllib.request.urlopen(urllib.request.Request(f"https://api.elevenlabs.io/v1/voices/{voice}", headers=headers(key)), timeout=15) as r:
                v = json.loads(r.read())
            langs = [l.get("language") + (f"/{l['accent']}" if l.get("accent") else "") for l in v.get("verified_languages") or []]
            print(f"ElevenLabs OK. Voice: {v.get('name')} | labels: {v.get('labels')} | verified languages: {langs or 'n/a'}")
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:300]
            print(f"ElevenLabs refused the request ({e.code}): {detail}")
            if "Received both headers" in detail:
                print("-> An environment Network secret is also injecting an Authorization header. Remove it, or set ELEVENLABS_AUTH=proxy if it injects xi-api-key.")
            elif "authorization header was invalid" in detail:
                print("-> The injected Authorization (Bearer) header is not accepted by ElevenLabs: it needs xi-api-key. Remove the Network secret and keep ELEVENLABS_API_KEY as an environment variable.")
            sys.exit(1)
        except Exception as e:
            print(f"ElevenLabs API not reachable: {e}"); sys.exit(1)
        return
    if (not key and not proxy) or not voice:
        sys.exit("Set ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID first (see README.md).")
    for video, lines in work:
        print(f"-> {video.name}")
        clips = []
        for i, (t0, t1, text) in enumerate(lines):
            nxt = lines[i + 1][0] if i + 1 < len(lines) else duration(video)
            clips.append((t0 + .15, min(t1, nxt) - t0 - .25, tts(text, voice, model, key)))
        out = (OUT if not args.video else video.parent) / f"{video.stem}_vo{'' if args.lang == 'bn' else '_en'}.mp4"
        mix(video, clips, out)
        print(f"   wrote {out.relative_to(HERE.parents[1]) if HERE.parents[1] in out.parents else out}")


if __name__ == "__main__":
    main()
