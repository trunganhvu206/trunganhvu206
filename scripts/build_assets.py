"""Render every SVG on the profile.

All copy lives in PROFILE below — edit it there, then run:

    python scripts/build_assets.py

Nothing else writes to assets/*.svg, so the files stay reproducible.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import theme as T
from theme import C, braille, card, chip, document, dot_text, esc, stars, w, window

ROOT = T.ROOT
OUT = os.path.join(ROOT, "assets")
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "art")
W = 900  # full-bleed asset width; GitHub scales it down to the column


# --------------------------------------------------------------- content
PROFILE = {
    "handle": "trunganhvu206",
    "name": "Trung Anh Vu ( Rosie Vu )",
    "role": "Data Science Student",
    "status": "Open to Internships",
    "email": "trunganhvu2611@gmail.com",
    "focus": "machine learning · statistics · reproducible analysis",
    "learning": "pandas · sql · scikit-learn",

    "about": [
        "Data science student learning to work with data end to end",
        "— cleaning and wrangling, exploratory analysis, modelling,",
        "then turning the results into something a non-technical",
        "reader can act on.",
        "",
        "Statistics-first: I would rather check an assumption and",
        "report uncertainty than hand over a single accuracy",
        "number. Every notebook runs top to bottom.",
    ],

    "stack": [
        ("languages", ["python", "r", "sql"]),
        ("data",      ["pandas", "numpy", "postgresql", "excel"]),
        ("ml",        ["scikit-learn", "pytorch", "statsmodels"]),
        ("viz",       ["matplotlib", "seaborn", "plotly", "power bi"]),
        ("tooling",   ["git", "jupyter", "vs code"]),
    ],

    "cards": [
        ("project log", "in progress", [
            "Write-ups land here as I finish them —",
            "question, data, method, results against",
            "an honest baseline, and how to rerun it.",
        ]),
        ("working toward", "planned", [
            "An end-to-end analysis on public data,",
            "a supervised model with a real baseline,",
            "a statistics write-up, a small dashboard.",
        ]),
    ],

    # one panel per row, so each can be wrapped in its own link in the README
    "contact": [
        ("email",    "trunganhvu2611@gmail.com"),
        ("linkedin", "linkedin.com/in/trunganhvu206"),
        ("github",   "github.com/trunganhvu206"),
        ("live",     "trunganhvu206.github.io/trunganhvu206"),
    ],

    "sections": [
        ("contact",  "00", "contact"),
        ("about",    "01", "about me"),
        ("projects", "02", "work in progress"),
        ("stack",    "03", "toolkit"),
        ("stats",    "04", "activity"),
    ],
}


def write(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("  %-26s %5.1f KB" % (name, len(svg.encode()) / 1024))


# -------------------------------------------------------------- terminal
def build_terminal():
    bar = 42
    p = PROFILE
    rows = [
        ("Role",     p["role"]),
        ("Status",   p["status"]),
        ("Focus",    p["focus"]),
        ("Learning", p["learning"]),
    ]
    head, alias = "Trung Anh Vu", "( Rosie Vu )"
    tx, pitch = 40, 5

    # the name, drawn as dot-matrix lettering
    name, name_w, name_h, base = dot_text(head, tx, bar + 32, pitch, 3.8, C["accent"])
    rule_y = bar + 32 + name_h + 16
    first = rule_y + 36
    H = first + (len(rows) - 1) * 30 + 32

    body = [f'<defs>{stars()}</defs>', window(W, H, "trung_anh_vu — neofetch", bar)]
    body.append(f'<rect x="1.2" y="{bar + 1}" width="{W - 2.4}" height="{H - bar - 2}" fill="url(#st)"/>')
    body.append(name)
    body.append(f'<text x="{tx + name_w + 22}" y="{bar + 32 + base * pitch}" class="s" '
                f'font-size="24">{esc(alias)}</text>')
    body.append(f'<path d="M{tx} {rule_y} H{W - tx}" stroke="{C["frame"]}" stroke-width="1.2"/>')

    y = first
    for key, value in rows:
        body.append(f'<text x="{tx}" y="{y}" class="t" font-size="22">{key.ljust(9)}: '
                    f'<tspan class="s">{esc(value)}</tspan></text>')
        y += 30

    chars = "".join(v for _, v in rows) + "".join(k for k, _ in rows) + alias + "trung_anh_vu — neofetch:"
    return document(W, H, "\n".join(body), chars,
                    f'{head} {alias} — {p["role"]}, {p["status"]}',
                    f'{p["role"]}. Focus: {p["focus"]}. Learning: {p["learning"]}. Contact: {p["email"]}.')


# --------------------------------------------------------------- section
def build_section(num, label):
    H = 54
    size = 26
    text = f'{num} — {label}'
    body = [
        f'<rect x="0" y="{H / 2 - 13}" width="5" height="26" fill="{C["accent"]}"/>',
        f'<text x="20" y="{H / 2 + 9}" class="a" font-size="{size}">{esc(num)} <tspan class="t">— {esc(label)}</tspan></text>',
        f'<path d="M{28 + w(text, size)} {H / 2} H{W}" stroke="{C["frame"]}" stroke-width="1.2" stroke-dasharray="3 4"/>',
    ]
    return document(W, H, "\n".join(body), text, f'Section {num}: {label}')


# ----------------------------------------------------------------- about
def build_about():
    lines = PROFILE["about"]
    H = 48 + len([l for l in lines]) * 30
    body = [card(0.6, 0.6, W - 1.2, H - 1.2)]
    y = 44
    for line in lines:
        if line:
            body.append(f'<text x="28" y="{y}" class="t" font-size="22">{esc(line)}</text>')
        y += 30
    body.append(f'<text x="28" y="{y - 2}" class="a" font-size="22">$ <tspan class="bl">_</tspan></text>')

    # dot-art sparkle on the right, vertically centred in the card
    pitch = 2.2
    art_w, art_h = 102 * pitch, 100 * pitch
    art, _, _ = braille(os.path.join(ART, "sparkle.txt"),
                        W - 40 - art_w, (H - art_h) / 2, pitch, 1.6, C["accent"], 0.85)
    body.append(art)
    return document(W, H + 6, "\n".join(body), "".join(lines) + "$_",
                    "About", " ".join(l for l in lines if l))


# ----------------------------------------------------------------- stack
def build_stack():
    groups = PROFILE["stack"]
    pad, label_w, row_h = 28, 118, 42
    H = 34 + len(groups) * row_h
    body = [card(0.6, 0.6, W - 1.2, H - 1.2)]
    y = 26
    for label, items in groups:
        body.append(f'<text x="{pad}" y="{y + 21}" class="a" font-size="22">{esc(label)}</text>')
        x = pad + label_w
        for item in items:
            svg, cw = chip(x, y, item)
            body.append(svg)
            x += cw + 8
        y += row_h
    chars = "".join(l for l, _ in groups) + "".join("".join(i) for _, i in groups)
    return document(W, H, "\n".join(body), chars, "Toolkit",
                    "; ".join(f'{l}: {", ".join(i)}' for l, i in groups))


# --------------------------------------------------------------- contact
def build_contact_row(label, value):
    """A slim About-style panel: `$ label   value   ->`.

    GitHub serves each SVG as an image, and an image can carry only one
    link, so every contact gets its own panel.
    """
    H, size = 54, 22
    y = H / 2 + 7
    body = [card(0.6, 0.6, W - 1.2, H - 1.2),
            f'<text x="28" y="{y}" class="a" font-size="{size}">$ {esc(label)}</text>',
            f'<text x="170" y="{y}" class="t" font-size="{size}">{esc(value)}</text>',
            f'<text x="{W - 28}" y="{y}" class="s" font-size="{size}" text-anchor="end">-&gt;</text>']
    return document(W, H, "\n".join(body), "$ " + label + value + "->",
                    f"{label}: {value}")


# ----------------------------------------------------------------- cards
def build_card(title, badge, lines):
    cw, H = 440, 186
    body = [card(0.6, 0.6, cw - 1.2, H - 1.2)]
    body.append(f'<rect x="0.6" y="0.6" width="{cw - 1.2}" height="38" rx="4" fill="{C["sub"]}"/>')
    body.append(f'<path d="M0.6 38.6 H{cw - 0.6}" stroke="{C["frame"]}" stroke-width="1.2"/>')
    body.append(f'<text x="20" y="27" class="t" font-size="23">{esc(title)}</text>')
    bw = w(badge, 18) + 18
    body.append(f'<rect x="{cw - bw - 16}" y="9" width="{bw}" height="22" rx="2" fill="{C["accent"]}"/>')
    body.append(f'<text x="{cw - bw - 7}" y="25" class="p" font-size="18">{esc(badge)}</text>')
    y = 70
    for line in lines:
        body.append(f'<text x="20" y="{y}" class="s" font-size="21">{esc(line)}</text>')
        y += 28
    return document(cw, H, "\n".join(body), title + badge + "".join(lines),
                    f'{title} — {badge}', " ".join(lines))


# ---------------------------------------------------------------- footer
def build_footer():
    H = 74
    left, right = "$ exit", "thanks for stopping by."
    body = [card(0.6, 0.6, W - 1.2, H - 1.2, C["bg"])]
    body.append(f'<text x="28" y="{H / 2 + 8}" class="a" font-size="24">{esc(left)}<tspan class="bl">_</tspan></text>')
    body.append(f'<text x="{W - 28}" y="{H / 2 + 8}" class="s" font-size="22" text-anchor="end">{esc(right)}</text>')
    return document(W, H, "\n".join(body), left + right + "_", "exit — thanks for stopping by")


def main():
    os.makedirs(OUT, exist_ok=True)
    print("building assets ->", OUT)
    write("terminal.svg", build_terminal())
    for key, num, label in PROFILE["sections"]:
        write(f"section-{key}.svg", build_section(num, label))
    for label, value in PROFILE["contact"]:
        write(f"contact-{label}.svg", build_contact_row(label, value))
    write("about.svg", build_about())
    write("stack.svg", build_stack())
    for (title, badge, lines), key in zip(PROFILE["cards"], ["log", "next"]):
        write(f"card-{key}.svg", build_card(title, badge, lines))
    write("footer.svg", build_footer())
    print("done.")


if __name__ == "__main__":
    main()
