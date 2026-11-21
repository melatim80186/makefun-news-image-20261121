#!/usr/bin/env python3
"""news-image-20261121 v2 — draws the entry image from scratch with PIL.

Layout (1024x1024, flat-vector broadsheet, top-10 recipe):
giant date masthead, 6-number stat strip, region tabs summing to 35,
3 hero + 10 secondary pictured stories (13 flat-vector illustrations),
numbered-pin world map, numbered ALSO list to 35, DATE CHECK box,
verification key + sources footer. Deterministic: no randomness, no
network, no timestamps. Writes entry.png to MAKEFUN_OUTPUT_DIR.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 242, 228)      # cream paper
PAPER = (255, 253, 246)   # panel white
INK = (25, 25, 25)
RED = (179, 39, 30)
NAVY = (23, 55, 94)
TEAL = (14, 107, 107)
GOLD = (196, 154, 27)
GREY = (90, 86, 76)
LINE = (216, 207, 184)
MAPLAND = (232, 222, 190)
MAPLINE = (170, 158, 122)

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
if not os.path.exists(SANSB):
    SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(size, bold=False):
    return ImageFont.truetype(SANSB if bold else SANS, size)


def wrap(d, text, font, maxw):
    """Greedy word wrap to a list of lines fitting maxw pixels."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(d, y, text, font, fill=INK, x0=0, x1=W):
    d.text(((x0 + x1 - d.textlength(text, font=font)) / 2, y), text,
           font=font, fill=fill)


def chip(d, x, y, text, fill=RED, fg=(255, 255, 255), font=None):
    font = font or F(11, True)
    w = int(d.textlength(text, font=font)) + 12
    d.rounded_rectangle([x, y, x + w, y + 19], radius=4, fill=fill)
    d.text((x + 6, y + 3), text, font=font, fill=fg)
    return w


# ---- story data: every figure verified against reporting on 21 Nov 2026 ----
# (n, region, headline, body, badge, source, icon)
HEROES = [
    (1, "GLOBAL", "CLIMATE TALKS RUN INTO OVERTIME",
     "No deal in Antalya as the draft drops all fossil-fuel words; a third text is due Saturday.",
     "0 DEAL", "AP · AFP", "cop"),
    (2, "MIDDLE EAST", "THREE MISSILES SHOT DOWN OVER RIYADH",
     "Saudi defences down 3 Houthi missiles fired at the capital before dawn.",
     "3 DOWN", "Reuters", "riyadh"),
    (3, "AMERICAS", "M6.7 QUAKE SHAKES PERU — NO DEAD",
     "Tremor near Junin is felt in Lima; no casualties or serious damage reported.",
     "M6.7", "USGS · AFP", "quake"),
]
SECONDARY = [
    (4, "EUROPE", "DOUBLE-TAP STRIKE KILLS 2, HURTS 42",
     "Boy, 7, and a paramedic die; 42 hurt.",
     "42 HURT", "Kyiv Independent", "blast"),
    (5, "GLOBAL", "BEPICOLOMBO REACHES MERCURY",
     "Probe fires thrusters at 19:24 CET.",
     "19:24 CET", "ESA", "mercury"),
    (6, "EUROPE", "DENMARK EXPELS RUSSIAN ATTACHE",
     "Diplomat out in 7 days over plot claim.",
     "7 DAYS", "Al Jazeera", "door"),
    (7, "ASIA", "JET LANDS SAFE — ALL 146 ABOARD OK",
     "767 diverts to Davao; all 146 safe.",
     "146 SAFE", "AP · CAAP", "plane"),
    (8, "ASIA", "RAHUL 136 PUTS INDIA ON TOP",
     "India 486/4, lead 118; Rahul's 13th ton.",
     "136", "ESPNcricinfo", "cricket"),
    (9, "EUROPE", "RUTTE DUE IN WARSAW",
     "NATO chief to meet Tusk in Warsaw.",
     "SAT VISIT", "AP", "nato"),
    (10, "GLOBAL", "BITCOIN SLIDES BELOW $59,000",
     "Sat low $55,130; liquidations near $2bn.",
     "$55,130", "Reuters", "bitcoin"),
    (11, "AMERICAS", "ANTONELLI FASTEST; VERSTAPPEN ON POLE",
     "Rookie tops qualifying; P1 to Verstappen.",
     "P1 VER", "Formula 1", "race"),
    (12, "GLOBAL", "CANCER PILL: TUMOURS GONE IN 1 IN 12",
     "Daraxonrasib + chemo clears tumours.",
     "1 IN 12", "Telegraph", "pill"),
    (13, "EUROPE", "ZELENSKY: PUTIN IS A \u2018KILLER\u2019",
     "Rebukes Trump for calling Putin \u2018friend\u2019.",
     "CNN", "CNN", "mic"),
]
# (n, text, source, confirmed?) — one line each, 14..35
ALSO = [
    (14, "Houthi drone bound for south Saudi Arabia destroyed", "Al Jazeera", True),
    (15, "Riyadh on third night of alerts; 8 warnings in 24 hours", "Al Jazeera", True),
    (16, "COP31 loss-and-damage fund to triple — but no sum set", "AP", True),
    (17, "Panama vows to block a weak COP31 text", "AP", True),
    (18, "Israeli strikes kill Palestinians in Gaza", "AP", True),
    (19, "Spain heads to 29 Nov vote as conservatives gain", "Reuters", True),
    (20, "Nepal PM Balendra Shah makes first visit to India", "BBC", True),
    (21, "ANC fights to hold South Africa's big cities", "BBC", True),
    (22, "US declassifies more UFO footage from Middle East", "BBC", True),
    (23, "NFL suspends Puka Nacua amid lawsuit", "AP", True),
    (24, "South Korea court clears ex-PM over martial law", "Wire", False),
    (25, "Trump hails $22bn in Southeast Asia deals", "Reuters", True),
    (26, "1 in 4 of world's youth live in conflict zones", "Aid groups", False),
    (27, "Italian court orders child's return to Ukraine", "Wire", False),
    (28, "Russian missiles and drones hit Ivano-Frankivsk", "Reuters", True),
    (29, "US floated giving part of Guyana to Venezuela", "Wire", False),
    (30, "Prabowo and Xi discuss South China Sea ties", "Wire", False),
    (31, "Trump vows to punish firms building AI hubs abroad", "Reuters", True),
    (32, "Myanmar and China reject ICJ genocide ruling", "Reuters", True),
    (33, "Bangladesh seeks compensation after Rohingya ruling", "Wire", False),
    (34, "Rohingya survivors welcome Hague verdict", "BBC", True),
    (35, "Ferraris out in Q2 at Vegas: Leclerc 11th, Hamilton 12th", "F1", True),
]
REGIONS = [("EUROPE", 7), ("ASIA", 9), ("AMERICAS", 7),
           ("MIDDLE EAST", 4), ("GLOBAL", 7), ("AFRICA", 1)]
STATS = [
    ("0", "CLIMATE DEAL AGREED AT COP31"),
    ("3", "HOUTHI MISSILES SHOT DOWN OVER RIYADH"),
    ("6.7", "PERU QUAKE — MAGNITUDE, NO DEAD"),
    ("146", "SAFE AFTER DAVAO EMERGENCY LANDING"),
    ("$55,130", "BITCOIN'S SATURDAY LOW"),
    ("136", "RAHUL'S RUNS IN WELLINGTON"),
]


# ---- flat-vector illustrations (all drawn in code, no photos) ----
def draw_icon(d, kind, x, y, w, h):
    """Draw a simple flat illustration for `kind` inside box (x,y,w,h)."""
    cx, cy = x + w // 2, y + h // 2
    if kind == "cop":  # climate talks: sun + flags + empty chair
        d.ellipse([cx - 26, cy - 30, cx + 26, cy + 22], fill=(255, 214, 90),
                  outline=(200, 150, 20), width=2)
        d.ellipse([cx - 12, cy - 16, cx + 12, cy + 8], fill=(255, 236, 160))
        for i, c in enumerate([(46, 134, 193), (39, 174, 96), (192, 57, 43)]):
            fx = x + 18 + i * 26
            d.line([fx, cy + 8, fx, cy + 34], fill=INK, width=3)
            d.polygon([(fx, cy + 8), (fx + 18, cy + 13), (fx, cy + 18)], fill=c)
        d.rectangle([x + 8, cy + 34, x + w - 8, cy + 38], fill=INK)
    elif kind == "riyadh":  # night skyline + interceptor trails
        d.rectangle([x, y, x + w, y + h], fill=NAVY)
        for sx, sy in [(x + 14, y + 12), (x + 40, y + 8), (x + 66, y + 16),
                       (x + 88, y + 10)]:
            d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
        for bx, bh in [(x + 10, 46), (x + 34, 62), (x + 62, 52), (x + 86, 40)]:
            d.rectangle([bx, y + h - bh, bx + 18, y + h], fill=(52, 84, 122))
            for wy in range(y + h - bh + 6, y + h - 4, 10):
                d.rectangle([bx + 4, wy, bx + 8, wy + 4], fill=(255, 214, 90))
                d.rectangle([bx + 11, wy, bx + 15, wy + 4], fill=(255, 214, 90))
        d.line([x + 8, y + 14, cx + 6, cy - 6], fill=(255, 214, 90), width=3)
        d.line([cx + 6, cy - 6, x + w - 10, y + 30], fill=(255, 214, 90), width=3)
        d.ellipse([cx - 2, cy - 12, cx + 14, cy + 4], fill=(255, 120, 60))
    elif kind == "quake":  # mountains + seismograph zigzag
        d.polygon([(x + 4, y + h), (x + w // 3, y + 14), (x + w // 2 + 8, y + h)],
                  fill=(120, 110, 140))
        d.polygon([(x + w // 3, y + h), (x + 2 * w // 3, y + 6),
                   (x + w - 4, y + h)], fill=(90, 80, 115))
        d.polygon([(x + 2 * w // 3 - 8, y + 22), (x + 2 * w // 3 + 8, y + 22),
                   (x + 2 * w // 3, y + 34)], fill=(255, 255, 255))
        pts = [(x + 6, cy + 18), (x + 22, cy + 18), (x + 30, cy + 2),
               (x + 38, cy + 32), (x + 46, cy + 8), (x + 54, cy + 26),
               (x + 62, cy + 18), (x + w - 6, cy + 18)]
        d.line(pts, fill=RED, width=3, joint="curve")
        d.line([x + 4, y + h - 6, x + w - 4, y + h - 6], fill=INK, width=2)
    elif kind == "blast":  # explosion starburst over buildings
        for j, bh in enumerate((16, 22, 14)):
            bx = x + 2 + j * 11
            d.rectangle([bx, y + h - bh, bx + 9, y + h - 2], fill=(90, 90, 100))
            d.rectangle([bx + 2, y + h - bh + 3, bx + 4, y + h - bh + 5],
                        fill=(255, 214, 90))
        for ang in range(0, 360, 45):
            import math as _m
            a = _m.radians(ang)
            d.line([cx + int(7 * _m.cos(a)), y + 12 + int(7 * _m.sin(a)),
                    cx + int(13 * _m.cos(a)), y + 12 + int(13 * _m.sin(a))],
                   fill=(255, 140, 40), width=3)
        d.ellipse([cx - 8, y + 4, cx + 8, y + 20], fill=(255, 200, 60))
    elif kind == "mercury":  # grey planet + probe
        r = min(w, h) // 2 - 3
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 160, 150),
                  outline=(120, 112, 102), width=2)
        for ox, oy, rr in [(-6, -5, 3), (5, 3, 4), (-1, 7, 2), (7, -7, 2)]:
            d.ellipse([cx + ox - rr, cy + oy - rr, cx + ox + rr, cy + oy + rr],
                      fill=(140, 132, 122))
        d.rectangle([x + w - 12, y + 2, x + w - 4, y + 9], fill=NAVY)
        d.line([x + w - 8, y + 9, cx + r - 2, cy - r + 2], fill=RED, width=2)
    elif kind == "door":  # door + exit arrow
        d.rectangle([cx - 12, y + 4, cx + 12, y + h - 4], fill=(192, 57, 43))
        d.rectangle([cx - 12, cy - 2, cx + 12, cy + 2], fill=(255, 255, 255))
        d.rectangle([cx - 2, y + 4, cx + 2, y + h - 4], fill=(255, 255, 255))
        d.ellipse([cx + 6, cy + 4, cx + 10, cy + 8], fill=GOLD)
        d.line([cx + 14, cy + 6, x + w - 4, cy + 6], fill=INK, width=2)
        d.polygon([(x + w - 4, cy + 2), (x + w - 4, cy + 10), (x + w - 1, cy + 6)],
                  fill=INK)
    elif kind == "plane":  # jet + runway + green check
        d.polygon([(x + 8, cy), (x + w - 22, cy - 10), (x + w - 8, cy - 4),
                   (x + w - 22, cy + 4), (x + 30, cy + 8)], fill=NAVY)
        d.polygon([(cx - 6, cy - 4), (cx + 8, cy - 16), (cx + 16, cy - 4)],
                  fill=NAVY)
        d.line([x + 6, y + h - 8, x + w - 6, y + h - 8], fill=INK, width=3)
        for gx in range(x + 14, x + w - 10, 16):
            d.line([gx, y + h - 8, gx + 8, y + h - 8], fill=(255, 255, 255), width=2)
        d.ellipse([x + w - 26, y + h - 26, x + w - 6, y + h - 6],
                  fill=(39, 174, 96))
        d.line([x + w - 21, y + h - 16, x + w - 17, y + h - 11,
                x + w - 10, y + h - 20], fill=(255, 255, 255), width=3)
    elif kind == "cricket":  # bat + ball + stumps
        d.line([cx - 10, cy + 16, cx + 10, cy - 12], fill=(150, 110, 60), width=8)
        d.rectangle([cx + 8, cy - 18, cx + 15, cy - 10], fill=(150, 110, 60))
        d.ellipse([x + 2, cy - 6, x + 14, cy + 6], fill=RED)
        for sx in (x + w - 26, x + w - 20, x + w - 14):
            d.line([sx, cy + 8, sx, cy + 28], fill=GOLD, width=3)
        d.rectangle([x + w - 28, cy + 4, x + w - 12, cy + 8], fill=GOLD)
    elif kind == "nato":  # compass star + dome
        import math as _m
        for k in range(4):
            a = _m.radians(90 * k)
            d.polygon([(cx, cy),
                       (cx + int(5 * _m.cos(a - 0.35)), cy - int(5 * _m.sin(a - 0.35))),
                       (cx + int(13 * _m.cos(a)), cy - int(13 * _m.sin(a))),
                       (cx + int(5 * _m.cos(a + 0.35)), cy - int(5 * _m.sin(a + 0.35)))],
                      fill=NAVY)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))
        d.arc([x + 4, cy + 6, x + w - 4, cy + 20], 180, 360, fill=GREY, width=2)
        d.line([x + 4, cy + 13, x + w - 4, cy + 13], fill=GREY, width=2)
    elif kind == "bitcoin":  # coin with B
        r = min(w, h) // 2 - 3
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(247, 147, 26),
                  outline=(200, 110, 10), width=2)
        d.text((cx - 8, cy - 13), "B", font=F(24, True), fill=(255, 255, 255))
        d.line([x + 4, cy + r - 2, cx - 6, cy + 8], fill=RED, width=2)
        d.line([cx - 6, cy + 8, cx + 2, cy + 14], fill=RED, width=2)
        d.line([cx + 2, cy + 14, x + w - 4, cy + 2], fill=RED, width=2)
    elif kind == "race":  # chequered flag + car
        for r in range(3):
            for c in range(3):
                if (r + c) % 2 == 0:
                    d.rectangle([x + 4 + c * 8, y + 6 + r * 8,
                                 x + 12 + c * 8, y + 14 + r * 8], fill=INK)
        d.line([x + 30, y + 6, x + 30, y + 34], fill=INK, width=2)
        d.rounded_rectangle([x + 8, cy + 2, x + w - 8, cy + 16], radius=5, fill=RED)
        d.rounded_rectangle([cx - 8, cy - 8, cx + 12, cy + 4], radius=4, fill=NAVY)
        for wx in (x + 10, x + w - 20):
            d.ellipse([wx, cy + 12, wx + 10, cy + 22], fill=INK)
    elif kind == "pill":  # capsule + cross
        d.rounded_rectangle([x + 10, cy - 10, x + w - 26, cy + 10], radius=10,
                            fill=(255, 255, 255), outline=TEAL, width=2)
        d.rectangle([cx - 4, cy - 10, cx + 4, cy + 10], fill=TEAL)
        d.ellipse([x + w - 26, cy - 12, x + w - 6, cy + 8], fill=TEAL)
        d.rectangle([x + w - 19, cy - 7, x + w - 13, cy + 3], fill=(255, 255, 255))
        d.rectangle([x + w - 22, cy - 4, x + w - 10, cy], fill=(255, 255, 255))
    elif kind == "mic":  # microphone + flag bars
        d.rounded_rectangle([cx - 8, cy - 14, cx + 8, cy + 6], radius=7, fill=INK)
        d.arc([cx - 12, cy - 2, cx + 12, cy + 16], 0, 180, fill=INK, width=3)
        d.line([cx, cy + 16, cx, cy + 24], fill=INK, width=3)
        d.rectangle([x + 6, y + 6, x + 22, y + 16], fill=(0, 91, 187))
        d.rectangle([x + 6, y + 16, x + 22, y + 26], fill=(255, 213, 0))


# ---- layout ----
def draw_page():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 7], fill=RED)
    d.rectangle([0, H - 7, W, H], fill=RED)

    # masthead
    center(d, 16, "THE WORLD IN ONE DAY", F(19, True), fill=RED)
    center(d, 38, "SATURDAY 21 NOVEMBER 2026", F(54, True))
    d.line([20, 100, W - 20, 100], fill=INK, width=2)
    center(d, 106, "35 STORIES  ·  6 REGIONS  ·  EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
           F(15, True))

    # stat strip
    y0, y1, gap = 130, 184, 8
    bw = (W - 40 - 5 * gap) // 6
    for i, (num, label) in enumerate(STATS):
        x0 = 20 + i * (bw + gap)
        d.rounded_rectangle([x0, y0, x0 + bw, y1], radius=6, fill=PAPER,
                            outline=LINE, width=1)
        center(d, y0 + 4, num, F(26, True), fill=RED, x0=x0, x1=x0 + bw)
        for j, ln in enumerate(wrap(d, label, F(10, True), bw - 10)):
            center(d, y0 + 32 + j * 11, ln, F(10, True), x0=x0, x1=x0 + bw)

    # region tabs (must sum to 35)
    ty = 192
    total = sum(c for _, c in REGIONS)
    assert total == 35, total
    x = 20
    for name, c in REGIONS:
        t = "%s %d" % (name, c)
        w = int(d.textlength(t, font=F(13, True))) + 18
        d.rounded_rectangle([x, ty, x + w, ty + 24], radius=5, fill=NAVY)
        d.text((x + 9, ty + 5), t, font=F(13, True), fill=(255, 255, 255))
        x += w + 6
    d.text((x + 4, ty + 5), "TOTAL = 35", font=F(13, True), fill=INK)

    # heroes: 3 panels
    hy, hh = 226, 168
    hw = (W - 40 - 2 * 10) // 3
    for i, (n, reg, head, body, badge, src, icon) in enumerate(HEROES):
        x0 = 20 + i * (hw + 10)
        d.rounded_rectangle([x0, hy, x0 + hw, hy + hh], radius=6, fill=PAPER,
                            outline=LINE, width=1)
        d.rectangle([x0, hy, x0 + hw, hy + 76], fill=(238, 232, 214))
        draw_icon(d, icon, x0 + hw // 2 - 52, hy + 6, 104, 64)
        d.text((x0 + 8, hy + 80), "%d · %s" % (n, reg), font=F(10, True), fill=RED)
        yy = hy + 94
        for ln in wrap(d, head, F(15, True), hw - 16)[:2]:
            d.text((x0 + 8, yy), ln, font=F(15, True), fill=INK)
            yy += 17
        for ln in wrap(d, body, F(11), hw - 16):
            if yy + 13 > hy + hh - 26:
                break
            d.text((x0 + 8, yy), ln, font=F(11), fill=GREY)
            yy += 13
        bw2 = chip(d, x0 + 8, hy + hh - 24, badge)
        d.text((x0 + 8 + bw2 + 6, hy + hh - 21), "● " + src, font=F(10),
               fill=GREY)

    # secondary: 10 panels, 5 x 2
    sy, sh = 404, 84
    sw = (W - 40 - 4 * 8) // 5
    for i, (n, reg, head, body, badge, src, icon) in enumerate(SECONDARY):
        r, c = divmod(i, 5)
        x0 = 20 + c * (sw + 8)
        y0 = sy + r * (sh + 8)
        d.rounded_rectangle([x0, y0, x0 + sw, y0 + sh], radius=5, fill=PAPER,
                            outline=LINE, width=1)
        draw_icon(d, icon, x0 + 4, y0 + 4, 38, 38)
        d.text((x0 + 46, y0 + 4), "%d · %s" % (n, reg), font=F(9, True), fill=RED)
        yy = y0 + 16
        for ln in wrap(d, head, F(11, True), sw - 50)[:2]:
            d.text((x0 + 46, yy), ln, font=F(11, True), fill=INK)
            yy += 12
        for ln in wrap(d, body, F(9), sw - 10)[:1]:
            d.text((x0 + 6, y0 + 46, ), ln, font=F(9), fill=GREY)
        bw2 = chip(d, x0 + 6, y0 + sh - 22, badge, font=F(10, True))
        d.text((x0 + 6 + bw2 + 5, y0 + sh - 19), "● " + src, font=F(9), fill=GREY)

    # world map with numbered pins 1-13
    my = 586
    d.text((20, my), "WHERE IT HAPPENED — PINS 1–13", font=F(14, True), fill=INK)
    d.text((W - 20 - d.textlength("5 MERCURY · 10 BITCOIN — OFF MAP", font=F(11)),
            my + 2), "5 MERCURY · 10 BITCOIN — OFF MAP", font=F(11), fill=GREY)
    mx0, my0, mx1, my1 = 20, my + 22, W - 20, my + 132
    d.rounded_rectangle([mx0, my0, mx1, my1], radius=6, fill=(233, 240, 244),
                        outline=LINE, width=1)
    NA = [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
          (-80, 73), (-70, 62), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
          (-80, 32), (-81, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
          (-125, 40), (-125, 48), (-140, 60), (-155, 58), (-165, 60)]
    SA = [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-40, -10), (-35, -20),
          (-48, -28), (-58, -35), (-65, -45), (-70, -55), (-73, -40),
          (-73, -20), (-80, -5)]
    EU = [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
          (18, 56), (21, 55), (24, 59), (30, 60), (30, 70), (40, 68), (45, 68),
          (40, 60), (35, 55), (30, 50), (28, 45), (23, 40), (19, 42), (12, 44),
          (8, 44), (3, 43), (-2, 37)]
    AF = [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
          (43, 12), (48, 11), (51, 10), (40, 0), (35, -18), (32, -29), (25, -34),
          (19, -35), (15, -27), (12, -18), (9, 0), (9, 4), (-8, 5), (-13, 8)]
    AS = [(30, 70), (45, 68), (60, 69), (75, 72), (90, 75), (110, 76), (130, 72),
          (160, 70), (180, 66), (170, 60), (162, 55), (158, 50), (142, 45),
          (140, 40), (130, 35), (127, 35), (122, 30), (120, 25), (110, 20),
          (105, 10), (100, 8), (98, 12), (95, 16), (92, 22), (88, 22), (85, 19),
          (80, 13), (77, 8), (75, 12), (72, 20), (68, 23), (62, 25), (57, 26),
          (52, 28), (48, 30), (44, 29), (40, 32), (36, 36), (35, 36), (30, 36)]
    AU = [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
          (140, -38), (145, -38), (150, -37), (153, -27), (146, -19), (142, -11),
          (136, -12), (132, -11), (126, -14), (122, -17), (118, -20)]

    def proj(lon, lat):
        x = mx0 + (lon + 170) / 360.0 * (mx1 - mx0)
        y = my0 + (75 - lat) / 130.0 * (my1 - my0)
        return (x, y)

    for poly in (NA, SA, EU, AF, AS, AU):
        d.polygon([proj(lo, la) for lo, la in poly], fill=MAPLAND,
                  outline=MAPLINE)
    PINS = {1: (30.7, 36.9), 2: (46.7, 24.7), 3: (-75.9, -10.9),
            4: (33.4, 47.9), 6: (12.6, 55.7), 7: (125.6, 7.1),
            8: (174.8, -41.3), 9: (21.0, 52.2), 11: (-115.1, 36.2),
            12: (2.2, 41.4), 13: (30.5, 50.5)}
    # small display offsets so the Europe cluster stays readable
    OFF = {1: (0, 10), 4: (-13, 9), 6: (-10, -9), 9: (1, -11),
           12: (-15, 5), 13: (13, 7)}
    for n, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        dx, dy = OFF.get(n, (0, 0))
        px, py = px + dx, py + dy
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(n)
        d.text((px - d.textlength(t, font=F(10, True)) / 2, py - 7), t,
               font=F(10, True), fill=(255, 255, 255))

    # ALSO list 14-35, two columns
    ay = my + 140
    d.text((20, ay), "ALSO ON SATURDAY 21 NOVEMBER — 22 MORE STORIES",
           font=F(14, True), fill=INK)
    d.line([20, ay + 20, W - 20, ay + 20], fill=INK, width=1)
    colw = (W - 40 - 24) // 2
    for i, (n, text, src, conf) in enumerate(ALSO):
        col, row = divmod(i, 11)
        x0 = 20 + col * (colw + 24)
        y = ay + 26 + row * 14
        mark = "●" if conf else "○"
        line = "%d. %s [%s]" % (n, text, src)
        # shrink only if needed; lines are written to fit one row
        fnt = F(11)
        while d.textlength(mark + " " + line, font=fnt) > colw and fnt.size > 9:
            fnt = F(fnt.size - 1)
        d.text((x0, y), mark + " " + line, font=fnt, fill=INK)

    # DATE CHECK box
    dy = ay + 26 + 11 * 14 + 8
    d.rounded_rectangle([20, dy, W - 20, dy + 62], radius=6,
                        outline=RED, width=2, fill=(255, 240, 238))
    d.text((28, dy + 5), "DATE CHECK — WHAT WE LEFT OUT (NOT SATURDAY'S NEWS)",
           font=F(12, True), fill=RED)
    dc = ("FRI 20 NOV: Wall Street correction (S&P + Dow, Nasdaq −5.28%) · Russian "
          "missiles land in Poland · Kyiv bridges hit · UK–EU deal signed · Cyclone "
          "Akvan landfall · GTA VI $3.79bn sales · Gen Z strike, 25 countries · FBI "
          "crime-database breach · Rikers plan · Bolsonaro in hospital · EU €1bn "
          "Ukraine aid · Palisades verdict.  THU 19 NOV: ICJ Myanmar genocide ruling "
          "· Shenzhen Trump–Xi–Putin summit · Anthropic IPO.  WED 18 NOV: Van Gogh "
          "$190.4m auction record.")
    yy = dy + 22
    for ln in wrap(d, dc, F(10), W - 56):
        d.text((28, yy), ln, font=F(10), fill=INK)
        yy += 12

    # footer
    fy = dy + 68
    center(d, fy, "KEY:  ● CONFIRMED = 2+ outlets  ·  ○ REPORTED = one outlet  ·  "
                  "◆ OFFICIAL = on the record",
           F(10, True))
    center(d, fy + 14, "Sources named beside each story. Original drawings, not "
                       "photographs. — THE WORLD, SATURDAY 21 NOVEMBER 2026",
           F(10), fill=GREY)
    return img


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    img = draw_page()
    path = os.path.join(outdir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    print("wrote", path, img.size, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
