#!/usr/bin/env python3
"""Generates img/tracker.svg (animated GitHub activity card) for the profile README.
Data source: public contribution calendar (no token required) + optional REST API for repos/followers."""
import os, re, json, math, datetime as dt, urllib.request, html

USER = os.environ.get("GH_USER", "Jaumns")
OUT = os.path.join(os.path.dirname(__file__), "..", "img", "tracker.svg")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def get(url, accept=None):
    h = {"User-Agent": "profile-tracker"}
    if accept: h["Accept"] = accept
    if TOKEN and "api.github.com" in url: h["Authorization"] = f"Bearer {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
        return r.read().decode()

def calendar():
    page = get(f"https://github.com/users/{USER}/contributions")
    dates = dict(re.findall(r'data-date="([\d-]+)" id="(contribution-day-component-\d+-\d+)"', page))
    dates = {v: k for k, v in dates.items()}                  # id -> date
    days = {}
    for m in re.finditer(r'for="(contribution-day-component-\d+-\d+)"[^>]*>\s*([^<]*?)\s*<', page):
        cid, txt = m.groups()
        if cid not in dates: continue
        n = re.match(r"(\d+) contribution", txt)
        days[dates[cid]] = int(n.group(1)) if n else 0
    return dict(sorted(days.items()))

def streaks(days):
    ds = [(dt.date.fromisoformat(d), n) for d, n in days.items()]
    best = (0, None, None); run = 0; start = None; prev = None
    for d, n in ds:
        if n > 0:
            if run == 0: start = d
            run += 1
            if run >= best[0]: best = (run, start, d)
        else: run = 0
    # current streak: walk back from the last day (today may still be 0)
    cur = 0; cs = ce = None; i = len(ds) - 1
    if i >= 0 and ds[i][1] == 0: i -= 1
    while i >= 0 and ds[i][1] > 0:
        cur += 1; cs = ds[i][0]; ce = ce or ds[i][0]; i -= 1
    return cur, cs, ce, best

def fmt(d): return d.strftime("%b ") + str(d.day) if d else "—"
def rng(a, b): return f"{fmt(a)} - {fmt(b)}" if a and b and a != b else fmt(a or b)

def profile():
    try:
        j = json.loads(get(f"https://api.github.com/users/{USER}"))
        return j["public_repos"], j["followers"], dt.datetime.fromisoformat(j["created_at"].replace("Z", "+00:00")).date()
    except Exception:
        return int(os.environ.get("FALLBACK_REPOS", 2)), int(os.environ.get("FALLBACK_FOLLOWERS", 1)), dt.date(2025, 11, 10)

def smooth(pts):
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d

def build():
    days = calendar()
    total = sum(days.values()); active = sum(1 for n in days.values() if n)
    cur, cs, ce, (lon, ls, le) = streaks(days)
    best_day = max(days.items(), key=lambda kv: kv[1]) if days else ("", 0)
    repos, followers, created = profile()
    first = next(iter(days), None)
    since = dt.date.fromisoformat(first) if first else created
    since = max(since, created) if created > since else since
    today = dt.date.fromisoformat(next(reversed(days)))
    # weekly series
    weeks = []; cur_w = 0; k = 0
    for i, (d, n) in enumerate(days.items()):
        cur_w += n; k += 1
        if k == 7: weeks.append((d, cur_w)); cur_w = 0; k = 0
    if k: weeks.append((next(reversed(days)), cur_w))
    vals = [math.sqrt(v) for _, v in weeks]; vmax = max(vals) or 1
    cx0, cx1, cy0, cy1 = 40, 790, 292, 218               # chart box (x left/right, y base/top)
    pts = [(cx0 + (cx1 - cx0) * i / (len(vals) - 1), cy0 - (cy0 - cy1) * v / vmax) for i, v in enumerate(vals)]
    line = smooth(pts); area = line + f" L{pts[-1][0]:.1f} {cy0} L{pts[0][0]:.1f} {cy0} Z"
    peak_i = max(range(len(weeks)), key=lambda i: weeks[i][1])
    months = []
    last_m = None
    for i, (d, _) in enumerate(weeks):
        m = dt.date.fromisoformat(d)
        if m.month != last_m and (not months or pts[i][0] - months[-1][0] > 50):
            months.append((pts[i][0], m.strftime("%b").upper())); 
        last_m = m.month
    joined_months = max(1, (today.year - created.year) * 12 + today.month - created.month)
    ring_pct = 100 if lon == 0 else min(100, round(cur / max(lon, cur, 1) * 100))
    E = html.escape
    rows = [("Total contributions", f"{total}"), ("Active days", f"{active}"),
            ("Best day", f"{best_day[1]}  ·  {fmt(dt.date.fromisoformat(best_day[0])) if best_day[0] else '—'}"),
            ("Public repositories", f"{repos}"), ("Followers", f"{followers}")]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="830" height="326" viewBox="0 0 830 326" font-family="'Segoe UI', system-ui, -apple-system, Helvetica, Arial, sans-serif" role="img" aria-label="GitHub activity of {USER}">
<style>
@keyframes up{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
@keyframes pop{{from{{opacity:0;transform:scale(.5)}}to{{opacity:1;transform:scale(1)}}}}
@keyframes ring{{from{{stroke-dashoffset:100}}to{{stroke-dashoffset:var(--to)}}}}
@keyframes draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
@keyframes fadein{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes flame{{0%,100%{{transform:scale(1) rotate(-2deg)}}50%{{transform:scale(1.14) rotate(3deg)}}}}
@keyframes beat{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
@keyframes ping{{0%{{r:4;opacity:.9}}100%{{r:15;opacity:0}}}}
@keyframes scan{{0%{{transform:translateX(0)}}100%{{transform:translateX(750px)}}}}
@keyframes glowring{{0%,100%{{filter:drop-shadow(0 0 0 #ff2e4d)}}50%{{filter:drop-shadow(0 0 6px #ff2e4d)}}}}
.u{{animation:up .7s ease both}} .p{{animation:pop .6s cubic-bezier(.2,1.4,.4,1) both;transform-box:fill-box;transform-origin:center}}
.r{{stroke-dasharray:100;animation:ring 1.6s cubic-bezier(.3,.7,.2,1) .4s both,glowring 3s ease-in-out 2s infinite}}
.d{{stroke-dasharray:1;animation:draw 2.4s ease-out .5s both}} .f{{animation:fadein 1.2s ease 1.6s both}}
.fl{{animation:flame 1.4s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 90%}}
.b{{animation:beat 1.4s ease-in-out infinite}} .pg{{animation:ping 2s ease-out 2.9s infinite}}
.sc{{animation:scan 6s linear 2.9s infinite}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}} .r{{stroke-dashoffset:var(--to)}} .d{{stroke-dashoffset:0}}}}
</style>
<defs>
<linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff2e4d" stop-opacity=".55"/><stop offset="1" stop-color="#ff2e4d" stop-opacity="0"/></linearGradient>
<linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="#ff2e4d"/><stop offset="1" stop-color="#ff9a8b"/></linearGradient>
<linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="#ff9a8b" stop-opacity="0"/><stop offset=".5" stop-color="#ff9a8b" stop-opacity=".35"/><stop offset="1" stop-color="#ff9a8b" stop-opacity="0"/></linearGradient>
<clipPath id="cc"><rect x="{cx0}" y="{cy1-12}" width="{cx1-cx0}" height="{cy0-cy1+14}"/></clipPath>
</defs>
<rect x=".5" y=".5" width="829" height="325" rx="10" fill="#0b0709" stroke="#2e1519"/>
<rect x="1" y="1" width="828" height="324" rx="10" fill="#ff2e4d" opacity=".03"/>
<g class="u" style="animation-delay:.05s">
<rect x="16" y="16" width="290" height="150" rx="9" fill="#150b0e" stroke="#2e1519"/>
<text x="32" y="42" font-size="14" font-weight="700" fill="#ff5366">{E(USER)} · GitHub activity</text>
<circle class="b" cx="290" cy="37" r="3.5" fill="#ff2e4d"/>
'''
    for i, (a, b) in enumerate(rows):
        y = 68 + i * 21
        svg += f'<g class="u" style="animation-delay:{.2+.08*i:.2f}s"><circle cx="35" cy="{y-4}" r="2.4" fill="#ff2e4d"/><text x="46" y="{y}" font-size="12" fill="#c9c3c6">{E(a)}</text><text x="290" y="{y}" text-anchor="end" font-size="12.5" font-weight="700" fill="#f5f2f3">{E(b)}</text></g>\n'
    svg += '</g>\n'
    # streak panel
    svg += f'''<g class="u" style="animation-delay:.15s"><rect x="316" y="16" width="498" height="150" rx="9" fill="#150b0e" stroke="#2e1519"/>
<line x1="482" y1="34" x2="482" y2="148" stroke="#2e1519"/><line x1="648" y1="34" x2="648" y2="148" stroke="#2e1519"/></g>
<g class="p" style="animation-delay:.35s"><text x="399" y="88" text-anchor="middle" font-size="32" font-weight="800" fill="#f5f2f3">{total}</text></g>
<g class="u" style="animation-delay:.45s"><text x="399" y="112" text-anchor="middle" font-size="12" fill="#ff9a8b">Total contributions</text>
<text x="399" y="132" text-anchor="middle" font-size="10" fill="#8f8793">{fmt(since)}, {since.year} - Present</text></g>
<g transform="translate(565,86)"><circle r="38" fill="none" stroke="#2e1519" stroke-width="5"/>
<circle class="r" style="--to:{100-ring_pct}" r="38" fill="none" stroke="#ff5366" stroke-width="5" stroke-linecap="round" pathLength="100" transform="rotate(-90)"/>
<g class="p" style="animation-delay:.9s"><text y="11" text-anchor="middle" font-size="32" font-weight="800" fill="#f5f2f3">{cur}</text></g>
<g class="fl" transform="translate(0,-38)"><path d="M0 -13 C5 -7 8 -3 8 2 A8 8 0 0 1 -8 2 C-8 -2 -5 -4 -4 -8 C-2 -6 -1 -5 0 -3 C1 -7 0 -10 0 -13 Z" fill="#ffd36a" stroke="#0b0709" stroke-width="3" paint-order="stroke"/></g></g>
<g class="u" style="animation-delay:.6s"><text x="565" y="146" text-anchor="middle" font-size="12" font-weight="700" fill="#f5f2f3">Current streak</text>
<text x="565" y="160" text-anchor="middle" font-size="10" fill="#8f8793">{E(rng(cs, ce) if cur else "—")}</text></g>
<g class="p" style="animation-delay:.75s"><text x="731" y="88" text-anchor="middle" font-size="32" font-weight="800" fill="#f5f2f3">{lon}</text></g>
<g class="u" style="animation-delay:.85s"><text x="731" y="112" text-anchor="middle" font-size="12" fill="#ff9a8b">Longest streak</text>
<text x="731" y="132" text-anchor="middle" font-size="10" fill="#8f8793">{E(rng(ls, le))}</text></g>
'''
    # chart
    svg += f'''<g class="u" style="animation-delay:.3s"><rect x="16" y="178" width="798" height="132" rx="9" fill="#150b0e" stroke="#2e1519"/>
<text x="32" y="202" font-size="12" font-weight="700" fill="#f5f2f3">Contributions · last 12 months</text>
<text x="798" y="202" text-anchor="end" font-size="10.5" fill="#8f8793">weekly activity · peak {weeks[peak_i][1]} in week ending {fmt(dt.date.fromisoformat(weeks[peak_i][0]))}</text></g>
<g stroke="#ff9a8b" stroke-opacity=".08"><path d="M{cx0} {cy0}H{cx1}M{cx0} {(cy0+cy1)/2:.0f}H{cx1}M{cx0} {cy1}H{cx1}"/></g>
<g clip-path="url(#cc)"><path class="f" d="{area}" fill="url(#a)"/>
<path class="d" d="{line}" pathLength="1" fill="none" stroke="url(#l)" stroke-width="2.2" stroke-linecap="round"/>
<rect class="sc" x="{cx0}" y="{cy1-12}" width="40" height="{cy0-cy1+14}" fill="url(#s)"/></g>
<g class="f"><circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="4" fill="#ffd36a"/><circle class="pg" cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="4" fill="none" stroke="#ffd36a" stroke-width="1.5"/></g>
<g font-size="9.5" fill="#8f8793" font-family="ui-monospace, SFMono-Regular, Consolas, monospace" letter-spacing=".8">'''
    for x, m in months: svg += f'<text x="{x:.0f}" y="305">{m}</text>'
    svg += '</g>\n</svg>'
    open(OUT, "w", encoding="utf-8").write(svg)
    print(f"total={total} active={active} cur={cur} ({rng(cs,ce)}) longest={lon} ({rng(ls,le)}) weeks={len(weeks)} repos={repos}")

if __name__ == "__main__":
    build()
