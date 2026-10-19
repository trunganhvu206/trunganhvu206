"""Render every SVG on the profile.

Layout follows an avionics-display convention: a banner headline flanked by
asterisks, a rule, then rows of LABEL + value aligned in columns. All copy
lives in PROFILE below — edit it there, then run:

    python scripts/build_assets.py

Nothing else writes to assets/*.svg, so the files stay reproducible.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import theme as T
from theme import C, banner, card, cols, document, esc, line, rule, stars, w, window

ROOT = T.ROOT
OUT = os.path.join(ROOT, "assets")

W = 900      # full-bleed asset width; GitHub scales it to the column
SIZE = 26    # body type
PAD = 28
LEAD = 34    # line height
NCOL = cols(W, SIZE, PAD)


# --------------------------------------------------------------- content
PROFILE = {
    "handle": "trunganhvu206",
    "email": "trunganhvu2611@gmail.com",

    "id": [
        ("NAME",     "Trung Anh Vu ( Rosie Vu )"),
        ("ROLE",     "Data Science Student"),
        ("STATUS",   "Open to Internships"),
        ("FOCUS",    "machine learning / statistics"),
        ("LEARNING", "pandas / sql / scikit-learn"),
        ("EMAIL",    "trunganhvu2611@gmail.com"),
    ],

    "about": [
        "Data science student learning to work with data end to end — cleaning",
        "and wrangling, exploratory analysis, modelling, then turning the",
        "results into something a non-technical reader can act on.",
        "",
        "Statistics-first: I would rather check an assumption and report",
        "uncertainty than hand over a single accuracy number. Every notebook",
        "runs top to bottom.",
    ],

    "work": [
        ("PROJECT LOG",         "write-ups land here as I finish them"),
        ("END-TO-END ANALYSIS", "public data, raw csv to a conclusion"),
        ("SUPERVISED MODEL",    "measured against an honest baseline"),
        ("STATISTICS WRITE-UP", "assumptions, effect size, decision"),
        ("DASHBOARD",           "the same findings, for a non-technical reader"),
    ],

    "stack": [
        ("LANGUAGES", "python / r / sql"),
        ("DATA",      "pandas / numpy / postgresql / excel"),
        ("ML",        "scikit-learn / pytorch / statsmodels"),
        ("VIZ",       "matplotlib / seaborn / plotly / power bi"),
        ("TOOLING",   "git / jupyter / vs code"),
    ],

    "links": [
        ("github",    "GitHub",       True),
        ("live",      "Live Profile", True),
        ("email",     "Email",        True),
        ("projects",  "Project Log",  True),
        ("notebooks", "Notebooks",    True),
        ("linkedin",  "LinkedIn",     False),
    ],
}


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("  %-22s %5.1f KB" % (name, len(svg.encode()) / 1024))


def rows(pairs, gap=2):
    """LABEL padded to one column, value in the next."""
    width = max(len(k) for k, _ in pairs) + gap
    return [k.ljust(width) + v for k, v in pairs]


def block(num, label, body_lines):
    """A section: banner headline, rule, then the body lines."""
    lines = [banner(f"{num}  {label}", NCOL), rule(NCOL)] + body_lines
    height = PAD * 2 + len(lines) * LEAD - (LEAD - SIZE)

    body = [f'<rect width="{W}" height="{height}" fill="{C["backdrop"]}"/>',
            f'<rect x="0.6" y="0.6" width="{W - 1.2}" height="{height - 1.2}" fill="none" '
            f'stroke="{C["frame"]}" stroke-width="1.2"/>']
    y = PAD + SIZE
    for i, text in enumerate(lines):
        cls = "a" if i == 0 else ("s" if i == 1 else "t")
        if text:
            body.append(line(PAD, y, text, SIZE, cls))
        y += LEAD

    return document(W, height, "\n".join(body), "".join(lines),
                    f"{num} — {label}", " ".join(l for l in body_lines if l))


# -------------------------------------------------------------- terminal
def build_terminal():
    bar_h = 42
    id_rows = rows(PROFILE["id"], gap=3)
    head = f'{PROFILE["handle"]}@github'
    H = 334

    body = [f'<defs>{stars()}</defs>', window(W, H, "trung_anh_vu.exe", bar_h)]
    body.append(f'<rect x="1.2" y="{bar_h + 1}" width="{W - 2.4}" height="{H - bar_h - 2}" fill="url(#st)"/>')

    bx, by = 40, bar_h + 34
    body.append(card(bx, by, 150, 150, C["bg"]))
    body.append(f'<rect x="{bx + 18}" y="{by + 18}" width="114" height="114" rx="3" fill="none" stroke="{C["frame"]}"/>')
    body.append(f'<text x="{bx + 75}" y="{by + 97}" class="a" font-size="62" text-anchor="middle" letter-spacing="2">TA</text>')

    tx, ty, size = 224, bar_h + 52, 24
    body.append(line(tx, ty, head, size, "a"))
    body.append(line(tx, ty + 26, rule(cols(W - tx - PAD, size)), size, "s"))
    y = ty + 60
    for text in id_rows:
        body.append(line(tx, y, text, size))
        y += 30

    chars = "".join(id_rows) + head + "TA" + "trung_anh_vu.exe-"
    return document(W, H, "\n".join(body), chars,
                    "Trung Anh Vu (Rosie Vu) — data science student, open to internships",
                    "; ".join(f"{k}: {v}" for k, v in PROFILE["id"]))


# ------------------------------------------------------------------ link
def build_link(label, live):
    H, size = 40, 21
    width = int(w(label, size) + 44)
    body = [f'<rect x="0.6" y="0.6" width="{width - 1.2}" height="{H - 1.2}" rx="3" '
            f'fill="{C["accent"] if live else C["bg"]}" '
            f'stroke="{C["accent"] if live else C["frame"]}" stroke-width="1.2"/>',
            f'<text x="{width / 2}" y="{H / 2 + 8}" class="{"p" if live else "s"}" font-size="{size}" '
            f'text-anchor="middle">{esc(label)}</text>']
    return document(width, H, "\n".join(body), label, label)


# ---------------------------------------------------------------- footer
def build_footer():
    H, size = 70, 24
    left, right = "$ exit", "thanks for stopping by."
    body = [f'<rect width="{W}" height="{H}" fill="{C["backdrop"]}"/>',
            f'<rect x="0.6" y="0.6" width="{W - 1.2}" height="{H - 1.2}" fill="none" stroke="{C["frame"]}" stroke-width="1.2"/>',
            line(PAD, 30, rule(cols(W, size, PAD)), size, "s"),
            f'<text x="{PAD}" y="58" class="a" font-size="{size}">{esc(left)}<tspan class="bl">_</tspan></text>',
            f'<text x="{W - PAD}" y="58" class="s" font-size="{size}" text-anchor="end">{esc(right)}</text>']
    return document(W, H, "\n".join(body), left + right + "_-", "exit — thanks for stopping by")


def main():
    os.makedirs(OUT, exist_ok=True)
    print("building assets ->", OUT)
    write("terminal.svg", build_terminal())

    write("sec-about.svg", block("01", "ABOUT", PROFILE["about"]))
    write("sec-work.svg", block("02", "WORK IN PROGRESS", rows(PROFILE["work"])))
    write("sec-stack.svg", block("03", "TOOLKIT", rows(PROFILE["stack"])))
    write("sec-activity.svg", block("04", "ACTIVITY", []))

    for key, label, live in PROFILE["links"]:
        write(f"link-{key}.svg", build_link(label if live else f"{label} — soon", live))
    write("footer.svg", build_footer())
    print("done.")


if __name__ == "__main__":
    main()
