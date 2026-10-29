#!/usr/bin/env python3
"""Generate the connected VCF depot content paths (PGG-563), in bc style.

    python3 generate.py            # supervisor-content-paths.svg and .png
    python3 generate.py --no-png

Two bands. Top: the connected Software Depot and what it feeds. Bottom: the admin host (bastion), its PAIS
acquisition sources and the optional Harbor. One customer proxy serves both, and every source card names
who requests it.

Layout rule: rows are aligned so every arrow is one straight segment, or one bus, in its own lane, and no
two arrows cross. Each lane is a y in ROW; change it and the cards and arrows on it move together.
"""
import subprocess
import sys
from pathlib import Path

import bcstyle as b

out = Path(__file__).resolve().parent
k = b.K
W, H = 2400, 1680
TEAL, PURPLE, GREY = k["teal"], k["purple"], k["slate"]

COL = {"src": (40, 400), "proxy": (500, 240), "svc": (800, 540), "dist": (1400, 440), "fleet": (1900, 460)}
TOP0, TOP1 = 196, 1000          # top band: connected
BOT0, BOT1 = 1040, 1500         # bottom band: admin host
ROW = {"bm": 330, "out": 560, "sup": 600, "ovf": 680, "vkr": 740, "vks_oci": 820, "oci": 860, "cli": 900,
       "svcs": 960, "vmdt": 1160, "amt": 1300, "busB": 1300}


def cx(col, inset=16):
    x, w = COL[col]
    return x + inset, w - 2 * inset


def line(pts, color, sw=3, dash=None, head=True):
    """A straight or orthogonal connector; arrowhead at the last point."""
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    s = f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"{da}/>'
    if head:
        (xa, ya), (xb, yb) = pts[-2], pts[-1]
        ux, uy = (xb > xa) - (xb < xa), (yb > ya) - (yb < ya)
        s += (f'<path d="M{xb} {yb} L{xb - ux * 14 - uy * 7} {yb - uy * 14 + ux * 7} '
              f'L{xb - ux * 14 + uy * 7} {yb - uy * 14 - ux * 7} z" fill="{color}"/>')
    return s


def tag(x, y, words, color=GREY):
    """A small right-aligned chip on a source card: who requests this source."""
    w = 16 + 7.4 * len(words)
    return b.rect(x - w, y - 11, w, 22, 11, "#fff", color, 1.3) + b.t(x - w / 2, y + 5, words, 12.5, color, 700, "middle")


def source(x, y, w, h, title, sub, who, dash=False):
    s = b.rect(x, y, w, h, 12, "#fff", GREY if dash else k["navy"], 1.6, "7 5" if dash else None)
    s += b.icon("cloud", x + 28, y + h / 2, 16, GREY if dash else k["navy"])
    s += b.t(x + 54, y + h / 2 - 4, title, 17, k["ink"], 700)
    s += b.t(x + 54, y + h / 2 + 16, sub, 13.5, GREY)
    return s + tag(x + w - 10, y + 2, who)


def legend(y):
    items = [(GREY, None, "Request, from its initiator"), (TEAL, None, "Binaries and OVF content"),
             (PURPLE, None, "OCI artifacts"), (PURPLE, "10 7", "Optional path"), (GREY, "7 5", "Manual, separate")]
    s, x = "", 40
    for color, dash, words in items:
        s += line([(x, y), (x + 44, y)], color, 3, dash)
        s += b.t(x + 56, y + 6, words, 16, GREY)
        x += 56 + 8.2 * len(words) + 40
    return s


def band_label(y, words):
    return b.t(40, y, words.upper(), 14, GREY, 700, ls=1.6)


def build():
    s = b.header("VCF 9.1.x  ·  Connected Software Depot", "Broadcom software paths across the VCF fleet",
                 "The Software Depot fetches through the customer proxy and feeds VCF. The admin host fetches PAIS "
                 "content separately and mirrors it to an optional Harbor.")
    s += legend(150)

    # ── panels ──
    sx0, sw0 = COL["src"]
    s += b.panel(sx0, TOP0, sw0, TOP1 - TOP0, "VCF online sources", "Requested by the Software Depot, and by VMDT",
                 k["slate"], k["design"], "srcA")
    s += b.panel(sx0, BOT0, sw0, BOT1 - BOT0, "PAIS acquisition sources", "PAIF 9.1 pp. 108–111 · representative",
                 k["slate"], k["design"], "srcB")
    s += b.panel(COL["proxy"][0], TOP0, COL["proxy"][1], BOT1 - TOP0, "Customer proxy", "Outbound access",
                 k["navy"], k["cyan"], "proxy")
    s += b.panel(COL["svc"][0], TOP0, COL["svc"][1], TOP1 - TOP0, "VCF Services",
                 "Software Depot and lifecycle · fleet-level", k["purple"], k["navy"], "svc")
    s += b.panel(COL["svc"][0], BOT0, COL["svc"][1], BOT1 - BOT0, "Admin host (bastion)",
                 "Manual workflows; its own proxy settings", k["navy"], k["cyan"], "admin")
    s += b.panel(COL["dist"][0], TOP0, COL["dist"][1], TOP1 - TOP0, "Distribution", "Content paths",
                 k["navy"], k["cyan"], "dist")
    s += b.panel(COL["dist"][0], BOT0, COL["dist"][1], BOT1 - BOT0, "Customer registry", "Optional",
                 k["purple"], k["navy"], "creg")
    s += b.panel(COL["fleet"][0], TOP0, COL["fleet"][1], BOT1 - TOP0, "VCF fleet and region",
                 "Management and workload consumers", k["purple"], k["navy"], "fleet")

    # ── sources ──
    x, w = cx("src")
    ysA = []
    for i, (title, sub) in enumerate([("dl.broadcom.com", "VCF binaries"),
                                      ("eapi.broadcom.com", "Authorization and services"),
                                      ("vvs.broadcom.com", "VCF download host"),
                                      ("vsanhealth.vmware.com", "VCF download host"),
                                      ("projects.packages.broadcom.com", "Supervisor and VCF service artifacts"),
                                      ("vcf.packages.broadcom.com", "VCF 9.1.1 and later")]):
        y = 280 + i * 114
        s += source(x, y, w, 84, title, sub, "Software Depot")
        ysA.append(y + 42)
    ysB = []
    for i, (title, sub, who, dash) in enumerate([
            ("pais-docker.packages.broadcom.com", "PAIS AMT and PAIS packages", "PAIS AMT", False),
            ("packages.broadcom.com", "Inference engines", "PAIS AMT", False),
            ("helm.ngc.nvidia.com/nvidia", "NVIDIA GPU Operator chart", "PAIS AMT", False),
            ("nvcr.io", "NVIDIA images", "PAIS AMT", False),
            ("archive.ubuntu.com", "Ubuntu mirror: a separate repository", "admin, by hand", True)]):
        y = 1116 + i * 76
        s += source(x, y, w, 64, title, sub, who, dash)
        ysB.append(y + 32)

    # ── proxy: one service, two clients ──
    px, pw = cx("proxy")
    # one proxy, two clients: a tall service with its text at the top
    s += b.rect(px, 500, pw, 840, 12, "#fff", k["navy"], 1.8)
    s += b.icon("proxy", px + 30, 540, 18)
    s += b.t(px + 58, 546, "Proxy service", 18, k["ink"], 700)
    for i, words in enumerate(("Authenticated; site trust", "", "Depot: set per VCF", "services runtime", "",
                               "Admin host: set per", "tool (VMDT, AMT)")):
        s += b.t(px + 20, 600 + i * 20 if i < 2 else (640 + i * 20 if i < 5 else 1010 + i * 20), words, 14.5, GREY)
    bus = 470
    s += line([(bus, ysA[0]), (bus, ysA[-1])], GREY, 2.6, head=False)
    for y in ysA:
        s += line([(bus, y), (x + w, y)], GREY, 2.6)
    s += line([(px, ROW["out"]), (bus, ROW["out"])], GREY, 2.6, head=False)
    s += line([(bus, ysB[0]), (bus, ysB[-2])], GREY, 2.6, head=False)
    for y in ysB[:-1]:
        s += line([(bus, y), (x + w, y)], GREY, 2.6)
    s += line([(bus, ysB[-2]), (bus, ysB[-1]), (x + w, ysB[-1])], GREY, 2.6, dash="7 5")
    s += line([(px, ROW["busB"]), (bus, ROW["busB"])], GREY, 2.6, head=False)

    # ── VCF Services: Binary Management on top; one Software Depot that holds binaries and OVFs and exposes an
    #    OCI registry interface (Peter: not two separate stores) ──
    sx, sw_ = cx("svc", 20)
    s += b.card(sx, ROW["bm"] - 50, sw_, 100, "vcfops", "Binary Management",
                ("VCF Operations manages lifecycle software",))
    dy0, dy1 = 440, 980
    s += b.rect(sx, dy0, sw_, dy1 - dy0, 14, "#fff", k["navy"], 2)
    s += b.icon("box", sx + 32, dy0 + 44, 20)
    s += b.t(sx + 64, dy0 + 40, "Software Depot", 22, k["ink"], 700)
    s += b.t(sx + 64, dy0 + 66, "Holds binaries and OVFs; exposes an OCI registry interface", 15, GREY)
    ix, iw = sx + 20, sw_ - 40
    s += b.card(ix, ROW["ovf"] - 70, iw, 140, "box", "Holds: binaries and OVFs",
                ("Install, upgrade and patch binaries", "Supervisor and VKr OVF templates"))
    s += b.card(ix, ROW["oci"] - 50, iw, 100, "registry", "Exposes: OCI registry interface", ("Serves registry content to Harbor",),
                border=PURPLE, ic=PURPLE)
    s += line([(sx, ROW["out"]), (px + pw, ROW["out"])], GREY, 2.6)
    bmx = sx + sw_ / 2
    s += line([(bmx, dy0), (bmx, ROW["bm"] + 50)], TEAL)

    # ── distribution ──
    dx, dw = cx("dist")
    s += b.card(dx, ROW["sup"] - 40, dw, ROW["vkr"] - ROW["sup"] + 80, "library", "vCenter content library",
                ("Subscribed to the depot", "Supervisor and VKr OVFs"))
    s += b.card(dx, ROW["vks_oci"] - 20, dw, ROW["svcs"] - ROW["vks_oci"] + 40, "registry", "Regional Harbor",
                ("Project vcf proxies the", "depot OCI registry"), border=PURPLE, ic=PURPLE)
    s += line([(ix + iw, ROW["ovf"]), (dx, ROW["ovf"])], TEAL)
    s += line([(ix + iw, ROW["oci"]), (dx, ROW["oci"])], PURPLE)

    # ── fleet and region ──
    fx, fw = cx("fleet")
    s += b.card(fx, ROW["bm"] - 50, fw, 100, "cluster", "SDDC Manager, VCF lifecycle",
                ("Install, upgrade and patch", "binaries for VCF instances"))
    s += b.card(fx, ROW["sup"] - 40, fw, 80, "k8s", "Supervisor", ("Control plane image: OVF",), ic=PURPLE)
    s += b.card(fx, ROW["vkr"] - 40, fw, ROW["vks_oci"] - ROW["vkr"] + 80, "k8s", "VKS clusters",
                ("VKr OVF and OCI add-ons",), ic=PURPLE)
    s += b.card(fx, ROW["cli"] - 26, fw, 52, "plugin", "VCF CLI plug-ins", ("OCI packages",), border=PURPLE, ic=PURPLE)
    s += b.card(fx, ROW["svcs"] - 26, fw, 52, "app", "Supervisor Services", ("OCI packages and images",),
                border=PURPLE, ic=PURPLE)
    s += b.card(fx, ROW["amt"] - 50, fw, 100, "app", "PAIS (a Supervisor Service)",
                ("Installed from the optional Harbor (1)", "with the AMT-generated YAML"), border=PURPLE, ic=PURPLE)
    s += line([(sx + sw_, ROW["bm"]), (fx, ROW["bm"])], TEAL)
    s += line([(dx + dw, ROW["sup"]), (fx, ROW["sup"])], TEAL)
    s += line([(dx + dw, ROW["vkr"]), (fx, ROW["vkr"])], TEAL)
    s += line([(dx + dw, ROW["vks_oci"]), (fx, ROW["vks_oci"])], PURPLE)
    s += line([(dx + dw, ROW["cli"]), (fx, ROW["cli"])], PURPLE)
    s += line([(dx + dw, ROW["svcs"]), (fx, ROW["svcs"])], PURPLE)

    # ── admin host: VMDT and PAIS AMT ──
    s += b.card(sx, ROW["vmdt"] - 50, sw_, 100, "download", "VMDT / VCF Download Tool",
                ("Downloads VCF depot content", "and uploads artifacts when required"))
    s += b.card(sx, ROW["amt"] - 50, sw_, 100, "upload", "VCF commands: PAIS AMT",
                ("Pulls PAIS and third-party artifacts", "and pushes them to a Harbor project"),
                border=PURPLE, ic=PURPLE)
    s += line([(sx, ROW["vmdt"]), (px + pw, ROW["vmdt"])], GREY, 2.6)
    s += line([(sx, ROW["amt"]), (px + pw, ROW["amt"])], GREY, 2.6)
    upx = sx + sw_ - 70
    s += line([(upx, ROW["vmdt"] - 50), (upx, dy1)], TEAL)
    # optional Harbor, level with AMT, so the push and the pull are one straight line
    s += b.card(dx, ROW["amt"] - 50, dw, 100, "registry", "Optional Harbor",
                ("Alternative registry path;", "site-specific content and trust"), border=PURPLE, ic=PURPLE)
    s += f'<circle cx="{dx + dw - 24}" cy="{ROW["amt"] - 50}" r="15" fill="white" stroke="{PURPLE}" stroke-width="2"/>'
    s += b.t(dx + dw - 24, ROW["amt"] - 44, "1", 15, PURPLE, 700, "middle")
    s += line([(sx + sw_, ROW["amt"]), (dx, ROW["amt"])], PURPLE)
    s += line([(dx + dw, ROW["amt"]), (fx, ROW["amt"])], PURPLE, dash="10 7")

    # ── notes ──
    s += b.t(40, 1550, "1  PAIS mirrored to an optional Harbor requires the external PAIS YAML definition; AMT generates "
                       "the installation and service configuration YAML files.", 16, k["ink"], 700)
    s += b.t(40, 1580, "Sources are representative, not a complete network allowlist. Management arrows do not prove an "
                       "instance-level staging sequence.", 15, GREY)
    s += b.t(40, 1610, "Sources: VCF 9.1.x pp. 2442–2443, 3973–3979, 4498–4503, 6866–6868, 7008–7017; "
                       "Private AI Foundation 9.1 pp. 99–113 (PAIS acquisition pp. 108–111).", 15, GREY)
    s += b.t(40, 1636, "Connected mode above; the admin host's VMDT uploads and PAIS AMT mirroring are separate "
                       "workflows with distinct purposes.", 15, GREY)
    return b.svg(W, H, s)


def main():
    svg = out / "supervisor-content-paths.svg"
    svg.write_text(build(), encoding="utf-8")
    if "--no-png" not in sys.argv:
        subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new",
                        "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{H}", "--force-device-scale-factor=2",
                        f"--screenshot={out / 'supervisor-content-paths.png'}", svg.as_uri()],
                       check=True, capture_output=True, timeout=90)
    print(svg)


if __name__ == "__main__":
    main()
