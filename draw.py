#!/usr/bin/env python3
"""Draw THE WORLD TODAY — Monday 23 November 2026 (heroes-scene, news-23 b140).
1024x1024 front page: masthead, number strip, region bar, 3 BIG hero scenes,
10 cards, map + ALSO, DATE CHECK, footer. Drawn illustrations, not photos.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (247, 243, 232)
INK = (20, 20, 20)
RED = (178, 34, 34)
NAVY = (16, 42, 90)
GOLD = (176, 141, 26)
GREEN = (27, 94, 60)
GREY = (90, 90, 90)
LIGHT = (232, 226, 210)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_one_line(draw, text, fnt_path, size, max_w):
    """Shrink font until text fits one line; return (font, text)."""
    s = size
    while s > 9:
        f = font(fnt_path, s)
        if draw.textlength(text, font=f) <= max_w:
            return f, text
        s -= 1
    return font(fnt_path, 9), text


def chip(draw, x, y, text, fill):
    f = font(SANS_B, 10)
    w = draw.textlength(text, font=f) + 10
    draw.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    draw.text((x + 5, y + 2), text, font=f, fill=(255, 255, 255))
    return w


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
MX = 10  # margin
CW = W - 2 * MX  # 1004 content width

# ---------- masthead ----------
d.text((MX, 8), "THE WORLD TODAY", font=font(SERIF, 46), fill=INK)
f_date = font(SANS_B, 15)
d.text((W - MX - d.textlength("MONDAY 23 NOVEMBER 2026", font=f_date), 26),
       "MONDAY 23 NOVEMBER 2026", font=f_date, fill=GOLD)
d.line([(MX, 62), (W - MX, 62)], fill=INK, width=2)

# ---------- kicker ----------
d.rectangle([MX, 66, W - MX, 88], fill=RED)
d.text((MX + 8, 71), "AI rout hits Asia   ·   UN chief urges AI rules   ·   US lead over China at record low   ·   Anthropic IPO $107.3B",
       font=font(SANS_B, 14), fill=(255, 255, 255))

# ---------- number strip: 2 rows x 5 ----------
nums = [("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"),
        ("11,762", "EBOLA CASES, DRC"), ("10T won", "SEOUL STABILISATION FUND"),
        ("2%", "BILLIONAIRE TAX IN PARIS"),
        ("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"),
        ("12,000", "CLEARED IN MANCHESTER"), ("264 kg", "EXPLOSIVES SEIZED"),
        ("$107.3B", "ANTHROPIC IPO")]
col_w = CW // 5
for i, (val, lab) in enumerate(nums):
    cx = MX + (i % 5) * col_w
    cy = 94 + (i // 5) * 34
    d.text((cx + 4, cy), val, font=font(SANS_B, 21), fill=INK)
    f_lab = font(SANS_B, 9)
    d.text((cx + 4, cy + 23), lab, font=f_lab, fill=GREY)
    if i % 5:
        d.line([(cx, cy + 2), (cx, cy + 30)], fill=(200, 192, 170), width=1)

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", (0, 90, 160), 226), ("AMERICAS 8", RED, 259),
           ("MIDDLE EAST 6", (128, 0, 128), 194), ("EUROPE 5", (0, 128, 128), 162),
           ("AFRICA 3", (34, 139, 34), 97), ("WORLD 2", (120, 120, 120), 66)]
rx = MX
for name, col, w in regions:
    d.rectangle([rx, 166, rx + w, 186], fill=col)
    f_r = font(SANS_B, 11)
    tw = d.textlength(name, font=f_r)
    d.text((rx + (w - tw) / 2, 171), name, font=f_r, fill=(255, 255, 255))
    rx += w

# ---------- THE DAY IN UTC ----------
d.text((MX, 190), "THE DAY IN UTC   ~00:00 Kospi dives   ~05:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
       font=font(SANS, 10), fill=GREY)
d.text((W - MX - d.textlength("~ APPROX", font=font(SANS, 10)), 190), "~ APPROX",
       font=font(SANS, 10), fill=GREY)

# ---------- hero scenes (3 big) ----------
HY, HH = 206, 252          # hero block top / height
SW = 328                    # scene width
gap = 10
heroes = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE", "REPORTED"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS", "REPORTED"),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", "REPORTED"),
]
for i, (head, body, src, ch) in enumerate(heroes):
    x0 = MX + i * (SW + gap)
    x1 = x0 + SW
    # --- scene illustration (140px) ---
    sy0, sy1 = HY, HY + 140
    if i == 0:  # Kospi skyline + falling chart
        d.rectangle([x0, sy0, x1, sy1], fill=(10, 24, 56))
        import random
        rnd = random.Random(7)
        bx = x0 + 8
        while bx < x1 - 30:
            bw, bh = rnd.randint(26, 44), rnd.randint(40, 64)
            d.rectangle([bx, sy1 - 22 - bh, bx + bw, sy1 - 22], fill=(24, 48, 96))
            for wy in range(sy1 - 22 - bh + 6, sy1 - 26, 12):
                for wx in range(bx + 4, bx + bw - 4, 9):
                    if rnd.random() < 0.55:
                        d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
            bx += bw + 6
        pts = [(x0 + 14, sy0 + 62), (x0 + 70, sy0 + 48), (x0 + 120, sy0 + 66),
               (x0 + 180, sy0 + 58), (x0 + 240, sy0 + 86), (x0 + 300, sy0 + 108)]
        d.line(pts, fill=(255, 140, 40), width=3)
        for p in pts:
            d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=(255, 255, 255))
        d.text((x0 + 10, sy0 + 6), "-3.3%", font=font(SANS_B, 34), fill=(255, 255, 255))
        d.rectangle([x0, sy1 - 22, x1, sy1], fill=(0, 0, 0))
        d.text((x0 + 8, sy1 - 19), "KOSPI 4,708.54 · -161 PTS", font=font(SANS_B, 11), fill=(255, 214, 90))
    elif i == 1:  # Guterres globe
        d.rectangle([x0, sy0, x1, sy1], fill=(16, 84, 48))
        cxg, cyg, r = x1 - 62, sy0 + 66, 46
        d.ellipse([cxg - r, cyg - r, cxg + r, cyg + r], fill=(190, 235, 200))
        for k in range(-2, 3):
            d.ellipse([cxg - r + abs(k) * 12, cyg - r, cxg + r - abs(k) * 12, cyg + r],
                      outline=(120, 190, 140), width=1)
        d.line([(cxg - r, cyg), (cxg + r, cyg)], fill=(120, 190, 140), width=1)
        d.text((x0 + 10, sy0 + 8), "150", font=font(SANS_B, 40), fill=(255, 214, 90))
        d.text((x0 + 10, sy0 + 52), "DELEGATES", font=font(SANS_B, 17), fill=(255, 214, 90))
        d.text((x0 + 10, sy0 + 72), "BACK A RISK", font=font(SANS_B, 17), fill=(255, 214, 90))
        d.text((x0 + 10, sy0 + 92), "FRAMEWORK", font=font(SANS_B, 17), fill=(255, 214, 90))
        d.rectangle([x0, sy1 - 22, x1, sy1], fill=(0, 0, 0))
        d.text((x0 + 8, sy1 - 19), "BRIDGETOWN SUMMIT, BARBADOS", font=font(SANS_B, 11), fill=(255, 214, 90))
    else:  # Power Index bars
        d.rectangle([x0, sy0, x1, sy1], fill=(250, 246, 236))
        d.rectangle([x0, sy0, x1, sy1], outline=(200, 192, 170), width=1)
        d.text((x0 + 10, sy0 + 6), "NARROWEST SINCE 2018", font=font(SANS_B, 12), fill=INK)
        f_gap = font(SANS_B, 12)
        d.text((x1 - 10 - d.textlength("GAP 5.3", font=f_gap), sy0 + 6), "GAP 5.3",
               font=f_gap, fill=RED)
        bars = [("78.9", "US", NAVY, 250), ("73.6", "CHINA", RED, 232),
                ("40.5", "INDIA", (176, 141, 26), 128)]
        by = sy0 + 34
        for val, name, col, bw in bars:
            d.text((x0 + 10, by), val, font=font(SANS_B, 13), fill=INK)
            d.rectangle([x0 + 62, by + 2, x0 + 62 + bw, by + 16], fill=col)
            f_n = font(SANS_B, 11)
            tw = d.textlength(name, font=f_n)
            d.text((x0 + 62 + bw - tw - 6, by + 3), name, font=f_n,
                   fill=(255, 255, 255) if col != (176, 141, 26) else INK)
            by += 26
        d.rectangle([x0, sy1 - 22, x1, sy1], fill=(0, 0, 0))
        d.text((x0 + 8, sy1 - 19), "ASIA POWER INDEX 2026 · LOWY INSTITUTE",
               font=font(SANS_B, 11), fill=(255, 214, 90))
    # --- headline / body / source+chip (below scene) ---
    ty = HY + 148
    f_head, _ = fit_one_line(d, head, SANS_B, 16, SW)
    d.text((x0, ty), head, font=f_head, fill=INK)
    blines = wrap(d, body, font(SANS, 12), SW)
    for j, ln in enumerate(blines[:2]):
        d.text((x0, ty + 22 + j * 15), ln, font=font(SANS, 12), fill=(40, 40, 40))
    sy = HY + 148 + 22 + 30
    d.text((x0, sy + 2), src, font=font(SANS, 10), fill=GREY)
    chip(d, x0 + 150, sy, ch, (16, 90, 160))

# ---------- MORE OF THE DAY bar ----------
d.rectangle([MX, 462, W - MX, 482], fill=INK)
d.text((MX + 8, 467), "MORE OF THE DAY  —  10 STORIES", font=font(SANS_B, 13), fill=(255, 255, 255))

# ---------- 10 cards: 5 cols x 2 rows ----------
cards = [
    ("1", "AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", "REPORTED"),
    ("2", "AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("3", "WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("4", "MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("5", "SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.", "AP", "REPORTED"),
    ("6", "SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("7", "LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("8", "TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("9", "EUROPE", "POLAND: 3 MISSILES CROSSED", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("10", "SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
cw = CW // 5
for i, (num, cat, head, body, src, ch) in enumerate(cards):
    cx = MX + (i % 5) * cw
    cy = 488 + (i // 5) * 58
    f_num = font(SANS_B, 12)
    d.text((cx + 4, cy), num, font=f_num, fill=RED)
    nw = d.textlength(num, font=f_num)
    d.text((cx + 8 + nw, cy + 1), cat, font=font(SANS_B, 10), fill=RED)
    f_ch, _ = fit_one_line(d, head, SANS_B, 12, cw - 8)
    d.text((cx + 4, cy + 16), head, font=f_ch, fill=INK)
    d.text((cx + 4, cy + 31), body, font=font(SANS, 10), fill=(60, 60, 60))
    # source + chip on one row at card bottom, chip right-aligned inside column
    d.text((cx + 4, cy + 44), src, font=font(SANS, 9), fill=GREY)
    chw = d.textlength(ch, font=font(SANS_B, 10)) + 10
    chip(d, cx + cw - 8 - chw, cy + 43, ch, (16, 90, 160) if ch == "REPORTED" else RED)

# ---------- WHERE IT HAPPENED bar ----------
d.rectangle([MX, 606, W - MX, 626], fill=INK)
d.text((MX + 8, 611), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=(255, 255, 255))

# ---------- map (left) ----------
map_x0, map_y0, map_x1, map_y1 = MX, 632, 430, 800
d.rectangle([map_x0, map_y0, map_x1, map_y1], fill=(238, 240, 228))
# simplified blobs: Americas, Europe/Africa, Asia
d.ellipse([map_x0 + 18, map_y0 + 12, map_x0 + 128, map_y0 + 118], fill=(196, 222, 178))
d.ellipse([map_x0 + 150, map_y0 + 8, map_x0 + 262, map_y0 + 92], fill=(196, 222, 178))
d.ellipse([map_x0 + 268, map_y0 + 22, map_x0 + 402, map_y0 + 128], fill=(196, 222, 178))
pins = [(66, 730, "2"), (56, 690, "5"), (96, 660, "4"), (200, 668, "7"),
        (232, 648, "8"), (248, 690, "10"), (262, 664, "9"), (292, 700, "6"),
        (330, 668, "11"), (352, 706, "12"), (244, 712, "13"), (368, 668, "3"),
        (392, 690, "1")]
for px, py, n in pins:
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=2)
    f_p = font(SANS_B, 9)
    tw = d.textlength(n, font=f_p)
    d.text((px - tw / 2, py - 5), n, font=f_p, fill=(255, 255, 255))
d.text((map_x0 + 4, map_y1 - 34), "Pins 1–13:  1 Seoul · 2 Bridgetown · 3 Beijing · 4 Washington · 5 New York · 6 Kyiv · 7 Paris",
       font=font(SANS, 9), fill=GREY)
d.text((map_x0 + 4, map_y1 - 22), "8 London · 9 Warsaw · 10 Manchester · 11 Beirut · 12 Gaza · 13 Khartoum",
       font=font(SANS, 9), fill=GREY)

# ---------- ALSO (right) ----------
d.text((440, 632), "ALSO ON MONDAY", font=font(SANS_B, 14), fill=INK)
also = [
    ("14. Paris: 100+ back 2% billionaire tax", False),
    ("15. Manchester: 12,000 cleared", False),
    ("16. Zelenskyy: 165 missiles in a week", False),
    ("17. COP31: Antalya pact rejected", False),
    ("18. Israel unity talks resume", False),
    ("19. Gaza: two killed in Israeli strike", False),
    ("20. West Bank settler attacks", False),
    ("21. Iran war: no deal in sight", False),
    ("22. Lebanon seizes 264 kg explosives", False),
    ("23. Bahrain: strike hits plant, 2 hurt", False),
    ("24. Benghazi: UN demands probe", True),
    ("25. Sudan: air defences down drones", True),
    ("26. DRC: fighting traps Ebola teams", False),
    ("27. Bangladesh: Hasina jailed if she returns", False),
    ("28. Seoul minister quits over AI exam row", False),
    ("29. SK Telecom -7.3% as hype cools", False),
    ("30. China eases margin rules", False),
    ("31. Seoul readies 10T-won fund", False),
]
f_also = font(SANS, 12)
for j, (txt, claim) in enumerate(also):
    ax = 440 + (j // 9) * 292
    ay = 654 + (j % 9) * 16
    d.text((ax, ay), txt, font=f_also, fill=INK)
    if claim:
        d.text((ax + d.textlength(txt, font=f_also) + 4, ay), "[CLAIM]",
               font=font(SANS_B, 10), fill=RED)

# ---------- DATE CHECK ----------
d.rectangle([MX, 808, W - MX, 884], outline=RED, width=2)
d.text((MX + 8, 814), "DATE CHECK  —  READ 23 NOV 2026, 23:59 UTC  ·  STORIES DATED 23 NOV ONLY",
       font=font(SANS_B, 12), fill=RED)
d.text((MX + 8, 834), "LEFT OUT — NOT 23 NOV:  Dems reach 258 (22 Nov)  ·  Sparta II fire (22 Nov)  ·  El Chapo Isidro captured (22 Nov)",
       font=font(SANS, 11), fill=INK)
d.text((MX + 8, 850), "EU–Indonesia pact (21 Nov)  ·  Nigeria boat (21 Nov)  ·  ICJ Myanmar ruling (19 Nov)",
       font=font(SANS, 11), fill=INK)
d.text((MX + 8, 868), "NOT YET —  Dymer search continues (14 missing)  ·  4 House races uncalled  ·  COP32 venue not set  ·  WHO evacuating trapped Ebola staff",
       font=font(SANS, 11), fill=INK)

# ---------- footer ----------
d.text((MX, 892), "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · ESPN · Lowy Institute (Asia Power Index 2026).",
       font=font(SANS, 10), fill=GREY)
d.text((MX, 906), "CHIPS: REPORTED = confirmed by wires · CLAIM = one side's claim, independently unconfirmed · ONGOING = still developing.",
       font=font(SANS, 10), fill=GREY)
d.text((MX, 920), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=font(SANS, 10), fill=GREY)
d.line([(MX, 940), (W - MX, 940)], fill=GOLD, width=2)
f_foot = font(SANS_B, 12)
ft = "THE WORLD TODAY  ·  Monday 23 November 2026  ·  31 stories  ·  6 regions"
d.text(((W - d.textlength(ft, font=f_foot)) / 2, 948), ft, font=f_foot, fill=GOLD)
d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=3)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
