# Checks the marketing plan: asset and caption IDs exist, all 180 days covered,
# campaigns carry a KPI and feature-status tag, no gated feature promoted before its gate.
# Run: python3 marketing/analytics/verify_plan.py
import csv,re,glob,os,datetime as dt,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')); errs=[]
rows=list(csv.DictReader(open('content/content_calendar.csv')))
caps=open('content/social_captions.md').read()
assets=set()
for f in glob.glob('creative/design_briefs/DES-*.md'): assets.add(os.path.basename(f)[:-3])
for m in re.findall(r'## (IMG-\d+)',open('creative/image_prompts/image_prompts.md').read()): assets.add(m)
for f in glob.glob('video/scripts/*.md'):
    for m in re.findall(r'VID-\d+',open(f).read()[:300]): assets.add(m)
dates=set()
for r in rows:
    dates.add(r['Date'])
    for a in re.findall(r'(?:DES|IMG|VID)-\d+',r['Creative asset']):
        if a not in assets: errs.append(f"{r['Date']} missing asset {a}")
    for c in re.split(r'[,\s/]+',r['Caption ID']):
        if c and c not in caps: errs.append(f"{r['Date']} missing caption {c}")
d=dt.date(2026,11,16); end=dt.date(2027,5,14); n=0
while d<=end:
    n+=1
    if d.isoformat() not in dates: errs.append(f'no rows on {d}')
    d+=dt.timedelta(1)
print('days in range',n)
for f in glob.glob('campaigns/*/*.md'):
    if f.endswith('ads.md'): continue
    s=open(f).read()
    if 'KPI' not in s: errs.append(f'{f}: no KPI')
    if not re.search(r'Feature status|feature status',s): errs.append(f'{f}: no feature-status tag')
# gated features before gates: captions in calendar rows without Gate that mention gated terms
gated=re.compile(r'split pay|recurring|referral code|leaderboard|loyalty|overlay|app store|play store',re.I)
capblocks=dict(re.findall(r'(CAP-\d{3})(.*?)(?=CAP-\d{3}|\Z)',caps,re.S))
for r in rows:
    c=r['Caption ID']
    if c.startswith('CAP') and not r['Gate'] and c in capblocks:
        t=re.sub(r'do not show an overlay|slot overlay drawn in edit','',capblocks[c]); hits=gated.findall(t)
        if hits: errs.append(f"{r['Date']} {c} mentions gated {set(hits)} without gate")
print("rows",len(rows),"errors",len(errs)); print("\n".join(errs[:40])); sys.exit(1 if errs else 0)
