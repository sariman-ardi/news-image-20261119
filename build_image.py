#!/usr/bin/env python3
"""Draw entry.png: one image summing up Thursday 19 November 2026's world news.

A clean newspaper-style infographic, 1024x1024, drawn entirely with Pillow:
a dated masthead, then six cards, one per story, each with a short headline,
a one-sentence summary and a small icon drawn from shapes. No photographs,
no downloaded artwork. Running this script twice writes byte-identical PNGs.
"""

import hashlib
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

# --- palette -------------------------------------------------------------
NAVY = (13, 32, 56)
NAVY_LIGHT = (24, 48, 78)
GOLD = (201, 162, 39)
CREAM = (247, 244, 236)
CARD = (255, 255, 255)
INK = (18, 22, 30)
GREY = (96, 104, 116)
LINE = (214, 210, 198)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# --- the six stories of 19 November 2026 --------------------------------
STORIES = [
    {
        "accent": (176, 32, 48),
        "icon": "gamepad",
        "title": "GTA VI LAUNCHES WORLDWIDE",
        "summary": "After 13 years, the game opens at midnight from New Zealand — ~17m pre-orders, $1.65bn+, Metacritic 99.",
        "source": "REUTERS",
    },
    {
        "accent": (24, 90, 160),
        "icon": "flags",
        "title": "TRUMP, XI & PUTIN MEET IN SHENZHEN",
        "summary": "First-ever trilateral summit on the sidelines of APEC: nuclear weapons, Ukraine and Iran on the agenda.",
        "source": "YONHAP / REUTERS",
    },
    {
        "accent": (18, 110, 88),
        "icon": "scales",
        "title": "WORLD COURT RULES ON ROHINGYA",
        "summary": "The ICJ delivers its verdict today at 10:00 CET in Gambia v. Myanmar — a possible first genocide ruling.",
        "source": "ICJ / REUTERS",
    },
    {
        "accent": (196, 96, 16),
        "icon": "bridge",
        "title": "CRIMEA BRIDGE HIT A THIRD TIME",
        "summary": "A strike just after midnight halts traffic; part of the roadway already collapsed earlier this week.",
        "source": "BBC / REUTERS",
    },
    {
        "accent": (52, 110, 180),
        "icon": "cyclone",
        "title": "CYCLONE AKVAN NEARS INDIA",
        "summary": "The storm is set to make landfall between Machilipatnam and Puri on India's east coast.",
        "source": "THE HINDU / IMD",
    },
    {
        "accent": (104, 58, 150),
        "icon": "chart",
        "title": "ANTHROPIC DEBUTS ON NASDAQ",
        "summary": "Shares trade today as ANT — an $81bn IPO at $83 a share, valuing the firm near $1.5tn, the biggest ever.",
        "source": "REUTERS",
    },
]


# --- small icons, drawn from shapes --------------------------------------
def draw_icon(draw, kind, cx, cy, r, color):
    """Draw a simple pictogram centred on (cx, cy) inside radius r."""
    if kind == "gamepad":
        draw.rounded_rectangle([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
                               radius=r * 0.35, fill=color)
        draw.ellipse([cx - r * 0.62, cy - r * 0.28, cx - r * 0.30, cy + r * 0.04],
                     fill=(255, 255, 255))
        draw.ellipse([cx + r * 0.30, cy - r * 0.28, cx + r * 0.62, cy + r * 0.04],
                     fill=(255, 255, 255))
        draw.line([cx - r * 0.28, cy + r * 0.28, cx + r * 0.28, cy + r * 0.28],
                  fill=(255, 255, 255), width=4)
    elif kind == "flags":
        for i, c in enumerate([(176, 32, 48), (24, 90, 160), (201, 162, 39)]):
            x = cx - r + i * r
            draw.line([x, cy - r, x, cy + r], fill=INK, width=4)
            draw.polygon([(x, cy - r), (x + r * 0.85, cy - r * 0.55),
                          (x, cy - r * 0.1)], fill=c)
    elif kind == "scales":
        draw.line([cx, cy - r, cx, cy + r * 0.8], fill=color, width=5)
        draw.line([cx - r * 0.9, cy - r * 0.45, cx + r * 0.9, cy - r * 0.45],
                  fill=color, width=5)
        for s in (-1, 1):
            px = cx + s * r * 0.9
            draw.line([px, cy - r * 0.45, px, cy + r * 0.15], fill=color, width=3)
            draw.polygon([(px - r * 0.45, cy + r * 0.15), (px + r * 0.45, cy + r * 0.15),
                          (px, cy + r * 0.7)], fill=color)
        draw.ellipse([cx - 6, cy - r - 6, cx + 6, cy - r + 6], fill=color)
    elif kind == "bridge":
        draw.arc([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], 180, 360,
                 fill=color, width=6)
        draw.line([cx - r, cy + r * 0.5, cx + r, cy + r * 0.5], fill=color, width=6)
        for x in (cx - r * 0.55, cx - r * 0.18, cx + r * 0.18, cx + r * 0.55):
            draw.line([x, cy - r * 0.15, x, cy + r * 0.5], fill=color, width=3)
        # the break: a small burst above the middle of the deck
        for ang in (0, 45, 90, 135, 180, 225, 270, 315):
            import math
            a = math.radians(ang)
            x1 = cx + int(7 * math.cos(a))
            y1 = cy - r * 0.55 + int(7 * math.sin(a))
            x2 = cx + int(15 * math.cos(a))
            y2 = cy - r * 0.55 + int(15 * math.sin(a))
            draw.line([x1, y1, x2, y2], fill=(196, 96, 16), width=3)
    elif kind == "cyclone":
        for i, rr in enumerate((r, r * 0.68, r * 0.38)):
            start = 20 + i * 120
            draw.arc([cx - rr, cy - rr, cx + rr, cy + rr], start, start + 230,
                     fill=color, width=6)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=color)
    elif kind == "chart":
        pts = [(cx - r, cy + r * 0.55), (cx - r * 0.4, cy + r * 0.1),
               (cx + r * 0.1, cy + r * 0.3), (cx + r * 0.7, cy - r * 0.6)]
        draw.line(pts, fill=color, width=6, joint="curve")
        # arrowhead at the end
        ex, ey = pts[-1]
        draw.polygon([(ex, ey), (ex - 16, ey + 2), (ex - 2, ey + 16)], fill=color)
        draw.line([cx - r, cy + r * 0.8, cx + r, cy + r * 0.8], fill=GREY, width=3)


# --- the picture -----------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 178], fill=NAVY)
    d.rectangle([0, 178, W, 184], fill=GOLD)
    f_date = font(FONT_BOLD, 46)
    d.text((32, 26), "THURSDAY 19 NOVEMBER 2026", font=f_date, fill=(255, 255, 255))
    f_sub = font(FONT_REG, 26)
    d.text((34, 102), "The world in one image  ·  six stories from around the globe",
           font=f_sub, fill=(196, 205, 220))
    # small gold globe mark at the right of the masthead
    gx, gy, gr = 952, 92, 46
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=GOLD, width=4)
    d.ellipse([gx - gr * 0.45, gy - gr, gx + gr * 0.45, gy + gr], outline=GOLD, width=3)
    d.line([gx - gr, gy, gx + gr, gy], fill=GOLD, width=3)

    # cards: 2 columns x 3 rows
    f_title = font(FONT_BOLD, 29)
    f_body = font(FONT_REG, 22)
    f_tag = font(FONT_BOLD, 18)
    margin, gap = 16, 16
    cw = (W - 2 * margin - gap) // 2
    ch = 246
    top0 = 196
    for idx, story in enumerate(STORIES):
        col = idx % 2
        row = idx // 2
        x0 = margin + col * (cw + gap)
        y0 = top0 + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        accent = story["accent"]

        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=CARD,
                            outline=LINE, width=2)
        d.rounded_rectangle([x0, y0, x1, y0 + 10], radius=5, fill=accent)
        d.rectangle([x0, y0 + 5, x1, y0 + 10], fill=accent)

        # icon badge, top right
        icx, icy, ir = x1 - 52, y0 + 52, 30
        d.ellipse([icx - ir, icy - ir, icx + ir, icy + ir], fill=accent)
        draw_icon(d, story["icon"], icx, icy, 19, (255, 255, 255))

        # headline (up to two lines) and summary
        text_w = cw - 2 * 24 - 78
        title_lines = wrap_text(d, story["title"], f_title, text_w)[:2]
        ty = y0 + 22
        for line in title_lines:
            d.text((x0 + 24, ty), line, font=f_title, fill=INK)
            ty += 36
        body_lines = wrap_text(d, story["summary"], f_body, cw - 2 * 24)[:3]
        by = y0 + 102
        for line in body_lines:
            d.text((x0 + 24, by), line, font=f_body, fill=(52, 58, 70))
            by += 28
        d.text((x0 + 24, y1 - 30), story["source"], font=f_tag, fill=accent)

    # footer
    f_foot = font(FONT_REG, 19)
    d.text((32, 974), "Sources: Reuters · Yonhap · BBC · The Hindu · IMD · ICJ",
           font=f_foot, fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    data = open(OUT, "rb").read()
    print("wrote", OUT, len(data), "bytes",
          "sha256", hashlib.sha256(data).hexdigest()[:16])


if __name__ == "__main__":
    build()
