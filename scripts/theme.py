"""Shared look for every generated SVG on the profile.

One palette, one font, one set of borders and radii, so the assets read as
a single system. Edit a colour here and every card changes on the next
`python scripts/build_assets.py`.
"""

import base64
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONT_PATH = os.path.join(ROOT, "assets", "fonts", "VT323-Regular.ttf")

# ---------------------------------------------------------------- palette
C = {
    "bg":       "#101010",  # page / recessed areas
    "panel":    "#171717",  # card surfaces
    "sub":      "#1F1F1F",  # header strips
    "backdrop": "#0A0A0A",  # the black behind everything
    "accent":   "#E6E6E6",  # buttons, numbers, the name
    "frame":    "#3A3A3A",  # every border
    "text":     "#EDEDED",  # primary ink
    "soft":     "#9A9A9A",  # secondary ink
}

RADIUS = 4
# VT323 is monospaced: every glyph advances 0.4em, which makes layout exact.
ADV = 0.4


def w(text, size):
    """Rendered width of `text` at `size` px."""
    return len(text) * ADV * size


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def font_face(chars):
    """@font-face carrying only the glyphs `chars` needs, as a data URI.

    GitHub serves these SVGs as images, and an image may not fetch an
    external font — so the font has to travel inside the file. Subsetting
    keeps that cost to a few KB per asset instead of 150.
    """
    from fontTools import subset
    from fontTools.ttLib import TTFont

    font = TTFont(FONT_PATH)
    opts = subset.Options()
    opts.layout_features = []          # no shaping needed for latin monospace
    opts.hinting = False               # rendered at fixed sizes
    opts.notdef_outline = False
    opts.desubroutinize = True
    opts.drop_tables += ["GSUB", "GPOS", "FFTM", "DSIG", "LTSH", "VDMX", "hdmx"]
    opts.name_IDs = []
    opts.glyph_names = False
    subsetter = subset.Subsetter(options=opts)
    subsetter.populate(text="".join(sorted(set(chars))) + " ")
    subsetter.subset(font)

    buf = io.BytesIO()
    font.save(buf)
    font.close()
    b64 = base64.b64encode(buf.getvalue()).decode()
    return ("@font-face{font-family:'VT323';font-style:normal;font-weight:400;"
            "src:url(data:font/ttf;base64,%s) format('truetype')}" % b64)


def document(width, height, body, chars, title, desc=""):
    """Wrap `body` in an SVG that carries its own font and base styles."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>{f'''
<desc>{esc(desc)}</desc>''' if desc else ''}
<defs><style>
{font_face(chars)}
text{{font-family:'VT323','Courier New',monospace;font-weight:400}}
.t{{fill:{C['text']}}} .s{{fill:{C['soft']}}} .a{{fill:{C['accent']}}} .p{{fill:{C['panel']}}}
@keyframes bl{{0%,49%{{opacity:1}}50%,100%{{opacity:.15}}}}
.bl{{animation:bl 1.2s steps(1) infinite}}
</style></defs>
{body}
</svg>
"""


def card(x, y, width, height, fill=None, radius=RADIUS):
    """A panel with the house border."""
    return (f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" '
            f'fill="{fill or C["panel"]}" stroke="{C["frame"]}" stroke-width="1.2"/>')


def window(width, height, title, titlebar=42):
    """Window chrome: a tab with the filename, and three dots."""
    tab_w = w(title, 22) + 54
    return f"""<rect x="0.6" y="0.6" width="{width - 1.2}" height="{height - 1.2}" rx="{RADIUS}" fill="{C['panel']}" stroke="{C['frame']}" stroke-width="1.2"/>
<path d="M0.6 {titlebar} V{RADIUS} a{RADIUS} {RADIUS} 0 0 1 {RADIUS} -{RADIUS} H{width - RADIUS - 0.6} a{RADIUS} {RADIUS} 0 0 1 {RADIUS} {RADIUS} v{titlebar - RADIUS} z" fill="{C['sub']}"/>
<path d="M0.6 {titlebar} H{width - 0.6}" stroke="{C['frame']}" stroke-width="1.2"/>
<rect x="14" y="7" width="{tab_w}" height="{titlebar - 7}" rx="3" fill="{C['panel']}" stroke="{C['frame']}" stroke-width="1"/>
<text x="32" y="{titlebar - 13}" class="t" font-size="22">{esc(title)}</text>
<circle cx="{width - 76}" cy="{titlebar / 2}" r="7" fill="{C['panel']}" stroke="{C['frame']}"/>
<circle cx="{width - 52}" cy="{titlebar / 2}" r="7" fill="{C['frame']}"/>
<circle cx="{width - 28}" cy="{titlebar / 2}" r="7" fill="{C['accent']}"/>"""


def chip(x, y, label, size=20, pad=11, height=30):
    """A bordered tag. Returns (svg, width) so callers can flow them."""
    width = w(label, size) + pad * 2
    svg = (f'<rect x="{x:.1f}" y="{y}" width="{width:.1f}" height="{height}" rx="2" '
           f'fill="{C["bg"]}" stroke="{C["frame"]}" stroke-width="1"/>'
           f'<text x="{x + pad:.1f}" y="{y + height - 9}" class="s" font-size="{size}">{esc(label)}</text>')
    return svg, width


def stars(seed_id="st"):
    """The sparkle tile, for assets that want the backdrop showing through."""
    pts = [(28, 34, 1.0), (118, 20, 0.6), (196, 58, 0.85), (74, 86, 0.7),
           (164, 124, 0.75), (30, 142, 0.9), (210, 150, 0.55), (108, 160, 0.65)]
    marks = "".join(
        f'<g transform="translate({x},{y}) scale({s})"><path d="M0 -6 C0.8 -1.6 1.6 -0.8 6 0 '
        f'C1.6 0.8 0.8 1.6 0 6 C-0.8 1.6 -1.6 0.8 -6 0 C-1.6 -0.8 -0.8 -1.6 0 -6 Z"/></g>'
        for x, y, s in pts)
    return (f'<pattern id="{seed_id}" width="230" height="190" patternUnits="userSpaceOnUse">'
            f'<g stroke="{C["accent"]}" fill="none" stroke-width="1.1" opacity="0.35">{marks}</g>'
            f'</pattern>')
