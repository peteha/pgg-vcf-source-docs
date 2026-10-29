"""bc style: the company-deck look (VMware26-light) for VCF Source figures.

Ported from pgg-platformcon `deck/lead-in/brand.py` (jazzy, PGG-682, branch jazzy/pgg-682 at 4b2373c):
Arial, white cards with a gradient header band and a navy outline, white line icons in navy circles,
chevron connectors and a gradient platform bar. Only the primitives are ported; no content is.

Added here, for PGG-696: the validation treatment. Every object and connection carries a state, and the
state is drawn by outline AND a badge with words, never by colour alone:

    doc    documented: a cited product document says it            solid outline, no badge
    lab    measured: documented, and seen working in a reference build   solid outline + green tick
    open   unvalidated: a research question, not a claim           dashed amber outline + "? Qn" badge
    unsup  not supported, or documented as not working             dotted red outline + "x Qn" badge

Broadcom product marks are internal brand assets. They are read in place at build time, only with
--marks, and only into out/ (gitignored). The committed renders use the line icons below.
"""
from __future__ import annotations

import base64
import html
import pathlib

K = {"fw": "#CC092F", "ts": "#61A60E", "navy": "#005B84", "cyan": "#009ECC", "teal": "#007B8C", "teal2": "#0098C7",
     "purple": "#6C4B94", "ink": "#1B1D36", "slate": "#52616D", "tint": "#EAF6FB", "line": "#C9DCE8", "design": "#8A99A6",
     "white": "#FFFFFF",
     # validation states (local to PGG-696; contrast on white: open 5.6, unsup 5.8, lab 5.2)
     "open": "#A35200", "open-t": "#FFF4E5", "unsup": "#CC092F", "unsup-t": "#FDECEF", "lab": "#3E7B0A"}
FONT = "Arial, Helvetica, sans-serif"
MONO = "Menlo, Consolas, 'DejaVu Sans Mono', monospace"

BC = pathlib.Path.home() / "Github/tools/diagrammer/archive/icons/src/broadcom/vcf-division-products"
MARKS = {"vcf": "cloud-foundation", "vcfa": "cloud-foundation-automation", "vcfops": "cloud-foundation-operations",
         "vsphere": "vsphere", "vsan": "vsan", "nsx": "nsx", "pais": "private-ai-services"}
USE_MARKS = False  # set by the generator's --marks

e = html.escape


def t(x, y, s, size=16, fill=K["ink"], weight=400, anchor="start", ls=0, op=1, family=FONT, halo=False):
    sp = f' letter-spacing="{ls}"' if ls else ""
    o = f' opacity="{op}"' if op != 1 else ""
    h = ' stroke="#fff" stroke-width="5" stroke-linejoin="round" paint-order="stroke"' if halo else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{sp}{o}{h}>{e(s)}</text>')


def rect(x, y, w, h, r=12, fill="none", stroke="none", sw=1.5, dash=None, extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}"{d}{extra}/>')


# White line drawings on a 24-unit grid. git/app/network/db/shield/cloud/users from brand.py; the rest are new here.
ICONS = {
    "cloud": '<path d="M7 18h10.5a4 4 0 0 0 .5-8 6 6 0 0 0-11.4 1.6A3.3 3.3 0 0 0 7 18z"/>',
    "network": '<circle cx="12" cy="5" r="2.2"/><circle cx="5" cy="18" r="2.2"/><circle cx="19" cy="18" r="2.2"/>'
               '<path d="M12 7.2v4.3M12 11.5L6.3 16.2M12 11.5l5.7 4.7"/>',
    "db": '<ellipse cx="12" cy="5.5" rx="7" ry="2.6"/><path d="M5 5.5v13c0 1.4 3.1 2.6 7 2.6s7-1.2 7-2.6v-13"/>'
          '<path d="M5 12c0 1.4 3.1 2.6 7 2.6s7-1.2 7-2.6"/>',
    "shield": '<path d="M12 3l7 3v5.5c0 4.5-3 8-7 9.5-4-1.5-7-5-7-9.5V6z"/><path d="M8.8 12.2l2.2 2.2 4.2-4.4"/>',
    "users": '<circle cx="9" cy="8" r="3"/><path d="M3.5 19.5c0-3.2 2.5-5.6 5.5-5.6s5.5 2.4 5.5 5.6"/>'
             '<circle cx="16.5" cy="9" r="2.4"/><path d="M15.6 13.9c2.8.3 4.9 2.6 4.9 5.6"/>',
    "app": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
    "download": '<path d="M12 3v12M7 10l5 5 5-5"/><path d="M4 17v3h16v-3"/>',
    "upload": '<path d="M12 15V3M7 8l5-5 5 5"/><path d="M4 17v3h16v-3"/>',
    "server": '<rect x="4" y="4" width="16" height="7" rx="1.5"/><rect x="4" y="13" width="16" height="7" rx="1.5"/>'
              '<path d="M7.5 7.5h4M7.5 16.5h4"/><circle cx="16" cy="7.5" r=".8"/><circle cx="16" cy="16.5" r=".8"/>',
    "laptop": '<rect x="5" y="5" width="14" height="10" rx="1.5"/><path d="M3 19h18l-2-4H5z"/>',
    "media": '<rect x="6" y="3" width="12" height="18" rx="2"/><path d="M9 7h6M9 10h6"/><circle cx="12" cy="16" r="1.6"/>',
    "proxy": '<path d="M3 12h5M16 12h5"/><rect x="8" y="7" width="8" height="10" rx="2"/><path d="M10.5 10.5h3M10.5 13.5h3"/>',
    "registry": '<rect x="4" y="4" width="7" height="7" rx="1"/><rect x="13" y="4" width="7" height="7" rx="1"/>'
                '<rect x="4" y="13" width="7" height="7" rx="1"/><rect x="13" y="13" width="7" height="7" rx="1"/>',
    "library": '<path d="M5 4h3v16H5zM10 4h3v16h-3z"/><path d="M15.2 4.6l2.9-.8 3.6 15.4-2.9.8z"/>',
    "box": '<path d="M12 3l8 4v10l-8 4-8-4V7z"/><path d="M4 7l8 4 8-4M12 11v10"/>',
    "k8s": '<path d="M12 3l7.8 3.8 1.9 8.4-5.4 6.8H7.7l-5.4-6.8 1.9-8.4z"/><circle cx="12" cy="12" r="2.6"/>'
           '<path d="M12 6.2v3.2M12 14.6v3.2M6.6 10.3l3 .9M14.4 12.8l3 .9M8.6 16.6l1.8-2.5M13.6 9.9l1.8-2.5"/>',
    "cluster": '<rect x="3" y="4" width="8" height="7" rx="1.2"/><rect x="13" y="4" width="8" height="7" rx="1.2"/>'
               '<rect x="3" y="13" width="8" height="7" rx="1.2"/><rect x="13" y="13" width="8" height="7" rx="1.2"/>',
    "ops": '<path d="M4 17a8 8 0 1 1 16 0"/><path d="M12 17l4-5"/><circle cx="12" cy="17" r="1.2"/>',
    "key": '<circle cx="8" cy="12" r="4"/><path d="M12 12h9M17.5 12v3.5M20.5 12v2.5"/>',
    "doc": '<path d="M6 3h9l4 4v14H6z"/><path d="M14.5 3v4.5H19M9 12h7M9 15.5h7"/>',
    "fleet": '<circle cx="6" cy="7" r="2.5"/><circle cx="18" cy="7" r="2.5"/><circle cx="12" cy="18" r="2.5"/>'
             '<path d="M8.2 8.3l2.6 7.3M15.8 8.3l-2.6 7.3M8.5 7h7"/>',
    "plugin": '<path d="M9 3v5M15 3v5"/><rect x="6" y="8" width="12" height="7" rx="2"/><path d="M12 15v6"/>',
}


def _mark_data(key):
    p = BC / f"{MARKS[key]}.svg"
    return "data:image/svg+xml;base64," + base64.b64encode(p.read_bytes()).decode()


def icon(name, cx, cy, r=19, fill=K["navy"]):
    """A line icon in a filled circle; with --marks, a VCF product's own mark on white instead."""
    if USE_MARKS and name in MARKS and (BC / f"{MARKS[name]}.svg").exists():
        d = r * 1.25
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{fill}" stroke-width="2"/>'
                f'<image href="{_mark_data(name)}" x="{cx - d / 2}" y="{cy - d / 2}" width="{d}" height="{d}"/>')
    glyph = ICONS.get(name) or ICONS[{"vcf": "cloud", "vcfa": "app", "vcfops": "ops", "vsphere": "cluster",
                                       "vsan": "db", "nsx": "network", "pais": "app"}[name]]
    s = r * 1.15 / 24
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            f'<g transform="translate({cx - 12 * s:.2f},{cy - 12 * s:.2f}) scale({s:.3f})" fill="none" stroke="#fff" '
            f'stroke-width="{1.9 / s * .9:.2f}" stroke-linecap="round" stroke-linejoin="round">{glyph}</g>')


def chevrons(x, y, color=K["navy"]):
    return "".join(f'<path d="M{x + i * 8} {y - 7} L{x + 6 + i * 8} {y} L{x + i * 8} {y + 7}" fill="none" stroke="{color}" '
                   f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity="{.55 + .45 * i}"/>' for i in range(2))


# ── validation state ──
STATE = {"doc": (None, None, None), "lab": (None, None, None),
         "open": (K["open"], "7 5", K["open-t"]), "unsup": (K["unsup"], "2 5", K["unsup-t"])}


def outline(state, normal):
    """Stroke colour and dash for an object in this state."""
    c, d, _ = STATE[state]
    return (c or normal), d


def badge(state, qid, x, y, anchor="end"):
    """The words that make the state readable without colour: "? Q4" or "x Q9"; a tick for measured."""
    if state == "lab":
        return (f'<circle cx="{x}" cy="{y}" r="11" fill="#fff"/><circle cx="{x}" cy="{y}" r="9" fill="{K["lab"]}"/>'
                f'<path d="M{x - 4.2} {y + .2} L{x - 1.2} {y + 3.3} L{x + 4.4} {y - 3.1}" fill="none" stroke="#fff" '
                f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    if state not in ("open", "unsup"):
        return ""
    c, _, tint = STATE[state]
    label = ("? " if state == "open" else "✕ ") + qid
    w = 14 + 9.2 * len(label)
    x0 = x - w if anchor == "end" else (x - w / 2 if anchor == "middle" else x)
    return (rect(x0, y - 13, w, 26, 13, tint, c, 1.6)
            + t(x0 + w / 2, y + 5.5, label, 15, c, 700, "middle", family=FONT))


def card(x, y, w, h, m, title, subs=(), state="doc", qid="", border=K["navy"], sw=1.8, fill="#fff", ic=None):
    """Icon on the left, a bold title and up to three quiet lines beside it; badge on the top-right corner."""
    stroke, dash = outline(state, border)
    s = rect(x, y, w, h, 12, fill, stroke, sw, dash)
    if m:
        s += icon(m, x + 30, y + h / 2, 18, ic or K["navy"])
    tx = x + (58 if m else 18)
    ty = y + h / 2 + 6 - 9.5 * len(subs)
    s += t(tx, ty, title, 18, K["ink"], 700)
    s += "".join(t(tx, ty + 21 + i * 18, sub, 14.5, K["slate"]) for i, sub in enumerate(subs))
    return s + badge(state, qid, x + w - 10, y, "end")


def panel(x, y, w, h, title, sub, c1, c2, gid, head=64):
    """A container with a gradient header band, as the company deck's step cards."""
    s = (f'<defs><linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
         f'<clipPath id="{gid}-c"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18"/></clipPath></defs>')
    s += rect(x, y, w, h, 18, "url(#body)", c1, 2)
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{head}" fill="url(#{gid})" clip-path="url(#{gid}-c)"/>'
    s += rect(x, y, w, h, 18, "none", c1, 2)
    s += t(x + 22, y + head / 2 + 2, title, 22, "#fff", 700)
    return s + (t(x + 22, y + head / 2 + 22, sub, 14, "#fff", 400, op=.9) if sub else "")


def zone(x, y, w, h, label, color=K["slate"], dash="6 5", fill="none"):
    """A plain boundary (a site, a network edge): outline and an uppercase caption, no header band."""
    return rect(x, y, w, h, 14, fill, color, 1.6, dash) + t(x + 16, y + 24, label.upper(), 13, color, 700, ls=1.2)


def arrow(pts, color=K["navy"], sw=2.4, state="doc", head=True, r=10, label=None, lpos=None, qid=""):
    """An orthogonal connector through pts, corners rounded, arrowhead where it lands. The state sets dash and colour;
    an open or unsupported connector also carries its badge at lpos (default: the middle of its longest leg)."""
    # a connector keeps its path colour when open (dash + badge carry the state); unsupported turns red
    c, dash = outline(state, color) if state == "unsup" else (color, STATE[state][1])
    d = f"M{pts[0][0]} {pts[0][1]}"
    for (x0, y0), (x1, y1), (x2, y2) in zip(pts, pts[1:], pts[2:]):
        k = min(r, abs(x1 - x0) / 2 + abs(y1 - y0) / 2, abs(x2 - x1) / 2 + abs(y2 - y1) / 2)
        sx, sy = (x1 > x0) - (x1 < x0), (y1 > y0) - (y1 < y0)
        tx, ty = (x2 > x1) - (x2 < x1), (y2 > y1) - (y2 < y1)
        d += f" L{x1 - sx * k} {y1 - sy * k} Q{x1} {y1} {x1 + tx * k} {y1 + ty * k}"
    d += f" L{pts[-1][0]} {pts[-1][1]}"
    da = f' stroke-dasharray="{dash}"' if dash else ""
    s = f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{da}/>'
    if head:  # inline head, so any colour works
        (xa, ya), (xb, yb) = pts[-2], pts[-1]
        ux, uy = (xb > xa) - (xb < xa), (yb > ya) - (yb < ya)
        px, py = -uy, ux
        s += (f'<path d="M{xb} {yb} L{xb - ux * 12 + px * 6} {yb - uy * 12 + py * 6} '
              f'L{xb - ux * 12 - px * 6} {yb - uy * 12 - py * 6} z" fill="{c}"/>')
    if lpos is None:
        legs = sorted(zip(pts, pts[1:]), key=lambda p: -(abs(p[1][0] - p[0][0]) + abs(p[1][1] - p[0][1])))
        (a, b) = legs[0]
        lpos = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    if label:
        s += t(lpos[0], lpos[1] - 10, label, 14, c, 700, "middle", halo=True)
    if state in ("open", "unsup"):
        s += badge(state, qid, lpos[0], lpos[1] + (12 if label else 0), "middle")
    return s


def media(pts, color=K["slate"]):
    """Carried by hand: a row of dots, no network connection."""
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round" stroke-dasharray="1 8"/>'


def chip(x, y, label, color=K["navy"], fill=None, size=14):
    """A small pill naming a content class that rides on a flow."""
    w = 18 + size * .56 * len(label)
    return rect(x, y - 13, w, 26, 13, fill or "#fff", color, 1.4) + t(x + w / 2, y + 5, label, size, color, 700, "middle"), w


def header(kicker, title, sub=None):
    s = t(40, 44, kicker.upper(), 15, K["slate"], 700, ls=1.6)
    s += t(40, 82, title, 30, K["ink"], 700)
    return s + (t(40, 110, sub, 17, K["slate"]) if sub else "")


def legend(y, used, x=40):
    """One row: only the encodings this figure uses."""
    items = {
        "doc": lambda x_: rect(x_, y - 10, 30, 20, 6, "#fff", K["navy"], 1.8),
        "lab": lambda x_: rect(x_, y - 10, 30, 20, 6, "#fff", K["navy"], 1.8) + badge("lab", "", x_ + 30, y - 10),
        "open": lambda x_: rect(x_, y - 10, 30, 20, 6, "#fff", K["open"], 1.8, "7 5"),
        "unsup": lambda x_: rect(x_, y - 10, 30, 20, 6, "#fff", K["unsup"], 1.8, "2 5"),
        "flow": lambda x_: arrow([(x_, y), (x_ + 34, y)], K["navy"]),
        "depot": lambda x_: arrow([(x_, y), (x_ + 34, y)], K["teal"]),
        "oci": lambda x_: arrow([(x_, y), (x_ + 34, y)], K["purple"]),
        "media": lambda x_: media([(x_, y), (x_ + 34, y)]),
    }
    words = {"doc": "Documented (cited)", "lab": "Documented and measured in a reference build",
             "open": "Unvalidated: a research question (? Qn)", "unsup": "Not supported (✕ Qn)",
             "flow": "Software moves", "depot": "Depot path (bundles, metadata)", "oci": "Registry path (OCI artifacts)",
             "media": "Carried by hand (approved media)"}
    s, xx = "", x
    for k in used:
        s += items[k](xx)
        s += t(xx + 44, y + 5, words[k], 14.5, K["slate"])
        xx += 44 + 7.4 * len(words[k]) + 30
    return s


def svg(w, h, body):
    defs = (f'<defs><linearGradient id="body" x1="0" x2="1"><stop offset="0" stop-color="#fff"/>'
            f'<stop offset="1" stop-color="{K["tint"]}"/></linearGradient>'
            f'<linearGradient id="vcf" x1="0" x2="1"><stop offset="0" stop-color="{K["purple"]}"/>'
            f'<stop offset=".55" stop-color="{K["navy"]}"/><stop offset="1" stop-color="{K["cyan"]}"/></linearGradient></defs>')
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">{defs}<rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>\n')
