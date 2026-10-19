"""Render the contribution calendar in the profile's own theme.

Third-party calendar images can't be restyled (their empty days stay
white), so this reads GitHub's public contributions page — the same data
as the graph on a profile, no token needed — and draws the year itself.

    python scripts/contributions.py [username]

Runs daily via .github/workflows/contributions.yml, which commits the
refreshed assets/contributions.svg when the data has changed.
"""

import datetime as dt
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import theme as T
from theme import C, document, esc, stars

USER = sys.argv[1] if len(sys.argv) > 1 else "trunganhvu206"
OUT = os.path.join(T.ROOT, "assets", "contributions.svg")

W = 900
LEFT, RIGHT = 46, 24          # room for weekday labels / right margin
TOP = 84                      # title + month labels above the grid
PITCH, CELL = 15.6, 12.4      # 53 weeks across 830px
# level 0..4: empty days stay quiet, busy days go bright
RAMP = ["#232323", "#4A4A4A", "#7A7A7A", "#B4B4B4", C["text"]]


def fetch(user):
    req = urllib.request.Request(f"https://github.com/users/{user}/contributions",
                                 headers={"User-Agent": "profile-assets"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse(html):
    """[(date, weekday_row, week_col, level, count)] for every day shown."""
    counts = {}
    for cell_id, text in re.findall(r'<tool-tip[^>]*for="(contribution-day-component-\d+-\d+)"[^>]*>([^<]*)', html):
        m = re.match(r"\s*(\d+)\s+contribution", text)
        counts[cell_id] = int(m.group(1)) if m else 0

    days = []
    for tag in re.findall(r"<td[^>]*data-date=[^>]*>", html):
        date = re.search(r'data-date="([\d-]+)"', tag)
        cid = re.search(r'id="(contribution-day-component-(\d+)-(\d+))"', tag)
        level = re.search(r'data-level="(\d)"', tag)
        if not (date and cid and level):
            continue
        days.append((dt.date.fromisoformat(date.group(1)), int(cid.group(2)),
                     int(cid.group(3)), int(level.group(1)), counts.get(cid.group(1), 0)))
    if len(days) < 300:
        raise SystemExit(f"only parsed {len(days)} days — GitHub's markup may have changed")
    return days


def render(days):
    weeks = max(d[2] for d in days) + 1
    total = sum(d[4] for d in days)
    H = TOP + 7 * PITCH + 52

    body = [f'<rect x="0.6" y="0.6" width="{W - 1.2}" height="{H - 1.2}" rx="{T.RADIUS}" '
            f'fill="{C["panel"]}" stroke="{C["frame"]}" stroke-width="1.2"/>',
            f'<defs>{stars()}</defs><rect x="0.6" y="0.6" width="{W - 1.2}" height="{H - 1.2}" '
            f'rx="{T.RADIUS}" fill="url(#st)"/>']

    title = f"{total:,} contributions in the last year"
    body.append(f'<text x="{LEFT}" y="36" class="t" font-size="24">{esc(title)}</text>')

    # month labels at the first column each month appears in
    first_in_col = {}
    for date, _, col, _, _ in days:
        if col not in first_in_col or date < first_in_col[col]:
            first_in_col[col] = date
    starts, last_month = [], None
    for col in sorted(first_in_col):
        if first_in_col[col].month != last_month:
            starts.append(col)
            last_month = first_in_col[col].month
    # like GitHub: a sliver of a month at the left edge yields to the next label
    if len(starts) > 1 and starts[1] - starts[0] < 3:
        starts.pop(0)
    for col in starts:
        body.append(f'<text x="{LEFT + col * PITCH}" y="{TOP - 12}" class="s" font-size="19">'
                    f'{first_in_col[col].strftime("%b")}</text>')

    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        body.append(f'<text x="{LEFT - 8}" y="{TOP + row * PITCH + CELL - 1.5}" class="s" '
                    f'font-size="18" text-anchor="end">{name}</text>')

    for date, row, col, level, count in days:
        tip = f"{count} contribution{'s' if count != 1 else ''} on {date:%b %d, %Y}"
        body.append(f'<rect x="{LEFT + col * PITCH:.1f}" y="{TOP + row * PITCH:.1f}" width="{CELL}" '
                    f'height="{CELL}" rx="2" fill="{RAMP[level]}"><title>{tip}</title></rect>')

    # legend, bottom right
    ly = TOP + 7 * PITCH + 18
    lx = W - RIGHT - 5 * PITCH - 52
    body.append(f'<text x="{lx - 8}" y="{ly + CELL - 1.5}" class="s" font-size="18" text-anchor="end">less</text>')
    for i, shade in enumerate(RAMP):
        body.append(f'<rect x="{lx + i * PITCH:.1f}" y="{ly}" width="{CELL}" height="{CELL}" rx="2" fill="{shade}"/>')
    body.append(f'<text x="{lx + 5 * PITCH + 6}" y="{ly + CELL - 1.5}" class="s" font-size="18">more</text>')

    chars = title + "JanFebMarAprMayJunJulAugSepOctNovDec" + "MonWedFri" + "lessmore"
    return document(W, H, "\n".join(body), chars,
                    f"{USER}: {title}",
                    f"Contribution calendar for {USER}, {days[0][0]} to {days[-1][0]}.")


def main():
    days = parse(fetch(USER))
    svg = render(sorted(days))
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"wrote {OUT} — {len(days)} days, {sum(d[4] for d in days)} contributions")


if __name__ == "__main__":
    main()
