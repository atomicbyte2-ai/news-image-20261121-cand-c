#!/usr/bin/env python3
"""news-image-20261121-cand-c: "THE WORLD IN ONE IMAGE"

A cream broadsheet front page summing up Saturday 21 November 2026 in
38 stories, all first reported that day. Masthead + giant date + headline
strip + 6-number strip + region bar (counts sum to 38) + 4 big illustrated
leads in a row + 9 small illustrated cards + 25 numbered one-liners +
dotted world map + DATE CHECK box (20 Nov stories left out) + footer.

All text is exact programmatic text; all illustrations are flat vector-style
drawings made with PIL shapes. Deterministic: no network, no randomness,
no timestamps. Paths resolve from this file's own directory; output goes
to MAKEFUN_OUTPUT_DIR (default /output) and to entry.png beside this file.
"""
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

W = 1600
MARGIN = 30
CONTENT = W - 2 * MARGIN  # 1540

CREAM = (250, 244, 228)
PAPER = (253, 249, 238)
INK = (26, 26, 26)
RED = (178, 34, 34)
NAVY = (18, 48, 86)
TEAL = (14, 110, 110)
GOLD = (184, 134, 11)
RULE = (120, 110, 95)
LIGHT = (238, 230, 212)
BLUE = (38, 90, 160)
GREEN = (34, 120, 70)
ORANGE = (214, 96, 20)


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = lambda s: font(SERIF, s)
F_SANS = lambda s: font(SANS, s)
F_SANSB = lambda s: font(SANS_B, s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading, align="left"):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        if align == "center":
            lx = x + (max_w - draw.textlength(ln, font=fnt)) // 2
        else:
            lx = x
        draw.text((lx, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x, y, w, fill=INK, thickness=2):
    draw.rectangle([x, y, x + w, y + thickness - 1], fill=fill)
    return y + thickness


# ---------------------------------------------------------------- stories
# (num, region, place, source, headline, copy)
LEADS = [
    (1, "Global", "Antalya, Turkiye", "Guardian / AP",
     "COP31 RUNS INTO OVERTIME",
     "No deal yet as talks stretch past the deadline, with negotiators "
     "working through the night in Antalya."),
    (2, "Europe", "Kryvyi Rih, Ukraine", "AP",
     "RUSSIAN STRIKES KILL 12 IN KRYVYI RIH",
     "82 wounded as missiles hit the industrial city in the latest "
     "barrage on Ukraine."),
    (3, "Americas", "Washington", "Reports",
     "US CLEARS 900,000 AI CHIPS FOR CHINA",
     "Washington approves the export licences in one of the largest "
     "clearances of its kind."),
    (4, "Global", "Global", "AP",
     "BAYER'S $7.25B ROUNDUP DEAL APPROVED",
     "A court signs off on the settlement, closing years of claims "
     "over the weedkiller."),
]

CARDS = [
    (5, "Europe", "Eastern Poland", "Reports",
     "MISSILE LANDS IN POLAND",
     "A Russian missile came down in eastern Poland, Warsaw says."),
    (6, "Europe", "The Hague", "Reports",
     'CHINA CALLS GENOCIDE RULING "UNJUST"',
     "Beijing rejects the Myanmar ruling from the court in The Hague."),
    (7, "Americas", "California", "Reuters",
     "CALIFORNIA SUBPOENAS NVIDIA",
     "The state demands documents in a widening inquiry into the chipmaker."),
    (8, "Asia", "New Delhi", "PR",
     "INDIA LAUNCHES FIRST H3N1 VACCINE",
     "New Delhi rolls out its home-grown flu shot."),
    (9, "Asia", "New Delhi", "PR",
     "MODI OPENS SCO DIALOGUE FORUM",
     "The prime minister opens the security bloc's talks in New Delhi."),
    (10, "Americas", "Washington", "AP",
     "TRUMP: IRAN WANTS A DEAL",
     "The president says Tehran is ready to talk."),
    (11, "Europe", "Sumy", "Reports",
     "HIMARS WIPES OUT 20 COMMANDERS",
     "A strike on a gathering in Sumy kills senior Russian officers."),
    (12, "Europe", "London", "UK",
     "BRITAIN HITS MOSCOW WITH CYBERATTACKS",
     "London confirms offensive cyber operations against Moscow."),
    (13, "Asia", "Jakarta", "Ministry",
     "JAKARTA ASKS GOOGLE: WHY 19,000 ACCOUNTS GONE?",
     "The ministry demands an explanation for the vanished accounts."),
]

# (num, region, place, source, one-liner headline)
ONELINERS = [
    (14, "Asia", "Tokyo", "Asahi",
     "Takaichi gets a frosty APEC greeting as Beijing presses Tokyo on Taiwan"),
    (15, "Americas", "Los Angeles", "AP",
     "Jury convicts the man who started the deadly 2025 Palisades Fire"),
    (16, "Americas", "Washington", "AP",
     "AP fact-checks false claims at Trump's post-Asia news conference"),
    (17, "Americas", "Ottawa", "Forum",
     "World can no longer count on US leadership, security forum chief warns"),
    (18, "Africa", "Johannesburg", "Stats",
     "Murder rate falls, but homicides still average 60 a day"),
    (19, "Americas", "Southern Mexico", "Reports",
     "Caravan of about 500 migrants crosses into Mexico"),
    (20, "Africa", "West Kordofan", "Army",
     "Sudanese army says it cleared RSF strongholds in 10 areas of West Kordofan"),
    (21, "Europe", "Brussels", "Reports",
     "Rare EU-UK summit as Burnham seeks to mend Brexit's effects"),
    (22, "Asia", "Tokyo", "Reports",
     "China warns on climbing Mount Fuji; missing climber's family offers a reward"),
    (23, "Asia", "Kabul", "UN",
     "UN warns ISIS-K is gaining drones and its threat is rising"),
    (24, "Europe", "Berlin", "Reports",
     "Students march against rearmament and mandatory service"),
    (25, "Europe", "Berlin", "Reports",
     '"Coalition of the willing" meets on Ukraine with Zelenskyy in Berlin'),
    (26, "Global", "Pasadena", "Reports",
     "Voyager 1 is now one light-day from Earth"),
    (27, "Americas", "Brasilia", "Reports",
     "Brazil advances Indigenous land bill as leader meets Amazon chief Raoni"),
    (28, "Middle East", "Baghdad", "Reports",
     "Pipeline chief arrested over illicit oil trading accusations"),
    (29, "Middle East", "Strait of Hormuz", "IRGC",
     "Iran claims waters 500 km beyond the strait, IRGC chief says"),
    (30, "Asia", "Mumbai", "Reports",
     "IndusInd ends ex-CEO Kathpalia's job and seeks to recover his pay"),
    (31, "Americas", "Washington", "Report",
     "SpaceX floats NATO membership for Ukraine in a post"),
    (32, "Europe", "Podgorica", "Reports",
     "Montenegro rejects land concessions to Croatia in EU bid row"),
    (33, "Americas", "Washington", "Reports",
     "US engagement against Iran has cost $48.3B, Pentagon official says"),
    (34, "Oceania", "Melbourne", "Reports",
     "Australia v England open the T20 series at the MCG tonight"),
    (35, "Europe", "Kyiv", "Reports",
     "Russia strikes Kyiv again as Ukraine rations power"),
    (36, "Middle East", "Kharg Island", "Reports",
     "Iran crews a tanker convoy to test the US blockade"),
    (37, "Europe", "Warsaw", "Reports",
     "NATO's chief takes Poland's airspace case to Warsaw"),
    (38, "Americas", "Washington", "Reports",
     "Trump threatens a 'tremendous tax' on data centres abroad"),
]

NUMBERS = [
    ("12", "killed in Russian strikes on Kryvyi Rih"),
    ("82", "wounded in the same attacks"),
    ("900,000", "AI chips cleared for China"),
    ("$7.25B", "Bayer Roundup settlement approved"),
    ("20", "Russian commanders killed in HIMARS strike"),
    ("500", "migrants in caravan crossing into Mexico"),
]

LEFT_OUT = [
    "Kyiv bridges hit (20 Nov)",
    "KCI ruling on the Myanmar genocide case (20 Nov)",
    "Trump-Xi summit in Shenzhen (20 Nov)",
    "COP31 Friday closing session (20 Nov)",
    "Senate 62-33 permitting vote (20 Nov)",
    "UK-EU summit in Brussels (20 Nov)",
    "Anthropic's $81.3B IPO (19 Nov)",
    "Mexico Revolution Day parade (20 Nov)",
]

MAP_DOTS = [  # (story num, lon, lat)
    (1, 30.7, 36.9), (2, 33.4, 47.9), (3, -77.0, 38.9),
    (5, 19.4, 52.0), (7, -122.4, 37.8), (8, 77.2, 28.6),
    (11, 34.8, 50.9), (13, 106.8, -6.2), (34, 145.0, -37.8),
    (35, 30.5, 50.4), (36, 50.3, 29.2),
]

# Rough landmass boxes in (lon_min, lon_max, lat_min, lat_max)
LAND = [
    (-168, -55, 15, 72), (-105, -77, 8, 20), (-80, -35, -55, 10),
    (-10, 40, 36, 70), (-18, 50, -35, 35), (40, 180, 5, 75),
    (95, 140, -10, 28), (113, 155, -45, -10),
]


def region_counts():
    counts = {}
    for s in LEADS + CARDS + ONELINERS:
        counts[s[1]] = counts.get(s[1], 0) + 1
    return counts


# ---------------------------------------------------------------- illustrations
def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(176, 214, 226))
    d.ellipse([x + w - 110, y + 18, x + w - 30, y + 98], fill=(255, 214, 90))
    cx, cy, r = x + w // 2 - 20, y + h // 2 + 20, 95
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 120, 190))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(20, 80, 140), width=3)
    d.ellipse([cx - 38, cy - r, cx + 38, cy + r], outline=(120, 190, 230), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(120, 190, 230), width=2)
    d.ellipse([cx - 70, cy - 55, cx - 10, cy - 5], fill=(46, 140, 70))
    d.ellipse([cx + 5, cy + 25, cx + 75, cy + 80], fill=(46, 140, 70))
    d.rectangle([x + 18, y + h - 52, x + 118, y + h - 18], fill=RED)
    d.text((x + 28, y + h - 48), "COP31", font=font(SANS_B, 26), fill=(255, 255, 255))


def art_strikes(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 32, 48))
    for bx, bw, bh in [(20, 70, 120), (100, 55, 170), (165, 80, 100),
                        (255, 60, 150), (325, 45, 90)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(12, 12, 20))
        for wy in range(y + h - bh + 14, y + h - 8, 26):
            d.rectangle([x + bx + 10, wy, x + bx + 26, wy + 12],
                        fill=(255, 200, 90))
    cx, cy = x + w - 90, y + 80
    for r, c in [(70, (255, 120, 30)), (48, (255, 180, 60)), (26, (255, 230, 140))]:
        pts = []
        import math
        for i in range(16):
            ang = math.pi * i / 8
            rr = r if i % 2 == 0 else r * 0.55
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=c)
    d.ellipse([x + 30, y + 40, x + 90, y + 90], fill=(120, 120, 140))
    d.ellipse([x + 60, y + 25, x + 110, y + 65], fill=(150, 150, 165))


def art_chips(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 40, 70))
    for i in range(5):
        d.line([x + 20, y + 30 + i * 46, x + 90, y + 30 + i * 46],
               fill=(60, 160, 220), width=3)
        d.line([x + w - 90, y + 30 + i * 46, x + w - 20, y + 30 + i * 46],
               fill=(60, 160, 220), width=3)
    cx, cy = x + w // 2, y + h // 2
    s = 110
    for k in range(6):
        px = cx - s // 2 - 16 + k * 0  # pins left
        d.rectangle([cx - s // 2 - 18, cy - 80 + k * 32, cx - s // 2, cy - 66 + k * 32],
                    fill=(220, 180, 60))
        d.rectangle([cx + s // 2, cy - 80 + k * 32, cx + s // 2 + 18, cy - 66 + k * 32],
                    fill=(220, 180, 60))
    d.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                fill=(20, 90, 60), outline=(220, 180, 60), width=4)
    d.rectangle([cx - 38, cy - 38, cx + 38, cy + 38], fill=(30, 130, 85))
    d.text((cx - 24, cy - 22), "AI", font=font(SANS_B, 44), fill=(255, 255, 255))
    d.text((x + 20, y + h - 40), "900,000", font=font(SANS_B, 30), fill=(255, 255, 255))


def art_bayer(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 200))
    d.polygon([(x + 40, y + 60), (x + w // 2, y + 18), (x + w - 40, y + 60)],
              fill=(150, 110, 50))
    for i in range(4):
        bx = x + 70 + i * 80
        d.rectangle([bx, y + 70, bx + 26, y + h - 40], fill=(120, 88, 40))
    d.rectangle([x + 40, y + h - 40, x + w - 40, y + h - 22], fill=(150, 110, 50))
    d.ellipse([x + w - 120, y + 30, x + w - 40, y + 110], fill=GOLD)
    d.text((x + w - 104, y + 42), "$", font=font(SERIF, 56), fill=(255, 255, 255))


def mini_art(d, kind, x, y, w, h):
    if kind == "missile":
        d.rectangle([x, y, x + w, y + h], fill=(200, 210, 225))
        d.line([x + 70, y + h - 35, x + w - 110, y + 30], fill=(90, 95, 110),
               width=26)
        d.polygon([(x + w - 110, y + 30), (x + w - 55, y + 12), (x + w - 75, y + 62)],
                  fill=RED)
        d.polygon([(x + 70, y + h - 35), (x + 30, y + h - 12), (x + 52, y + h - 62)],
                  fill=ORANGE)
        d.ellipse([x + w - 165, y + 38, x + w - 135, y + 68], fill=(255, 255, 255))
        d.line([x + 40, y + 30, x + w - 40, y + 30], fill=(140, 150, 165), width=2)
        d.line([x + 40, y + h - 12, x + w - 40, y + h - 12], fill=(140, 150, 165),
               width=2)
    elif kind == "gavel":
        d.rectangle([x, y, x + w, y + h], fill=(225, 215, 195))
        d.line([x + w // 2 - 20, y + h - 14, x + w // 2 + 55, y + 42],
               fill=(90, 60, 30), width=16)
        d.rectangle([x + w // 2 - 10, y + 18, x + w // 2 + 130, y + 56],
                    fill=(120, 80, 40), outline=(80, 50, 20), width=3)
        d.rectangle([x + 40, y + h - 34, x + 180, y + h - 18],
                    fill=(150, 105, 55))
    elif kind == "subpoena":
        d.rectangle([x, y, x + w, y + h], fill=(210, 225, 235))
        d.rectangle([x + w // 2 - 55, y + 12, x + w // 2 + 55, y + h - 12],
                    fill=(255, 255, 255), outline=(60, 60, 60), width=2)
        for i in range(4):
            d.line([x + w // 2 - 40, y + 32 + i * 18, x + w // 2 + 40, y + 32 + i * 18],
                   fill=(100, 100, 100), width=3)
        d.ellipse([x + w // 2 + 18, y + h - 46, x + w // 2 + 52, y + h - 12],
                  fill=RED)
    elif kind == "vaccine":
        d.rectangle([x, y, x + w, y + h], fill=(205, 232, 215))
        d.rectangle([x + 60, y + 35, x + 110, y + h - 20], fill=(255, 255, 255),
                    outline=(60, 60, 60), width=2)
        d.rectangle([x + 60, y + 35, x + 110, y + 65], fill=(120, 190, 230))
        d.rectangle([x + 72, y + 20, x + 98, y + 35], fill=(90, 90, 90))
        d.line([x + 160, y + 25, x + w - 40, y + h - 25], fill=(180, 180, 180),
               width=8)
        d.polygon([(x + w - 40, y + h - 25), (x + w - 70, y + h - 40),
                   (x + w - 70, y + h - 12)], fill=(200, 60, 60))
    elif kind == "forum":
        d.rectangle([x, y, x + w, y + h], fill=(215, 228, 245))
        d.ellipse([x + 40, y + 22, x + 170, y + 82], fill=(255, 255, 255))
        d.polygon([(x + 60, y + 78), (x + 80, y + 105), (x + 95, y + 78)],
                  fill=(255, 255, 255))
        d.ellipse([x + w - 180, y + 45, x + w - 40, y + 105], fill=NAVY)
        d.polygon([(x + w - 90, y + 100), (x + w - 70, y + 118), (x + w - 55, y + 100)],
                  fill=NAVY)
        for i in range(3):
            d.line([x + 60, y + 38 + i * 14, x + 150, y + 38 + i * 14],
                   fill=(120, 120, 120), width=3)
    elif kind == "deal":
        d.rectangle([x, y, x + w, y + h], fill=(240, 228, 205))
        d.rectangle([x + 55, y + 18, x + w - 90, y + h - 18], fill=(255, 255, 255),
                    outline=(60, 60, 60), width=2)
        for i in range(3):
            d.line([x + 75, y + 38 + i * 20, x + w - 110, y + 38 + i * 20],
                   fill=(100, 100, 100), width=3)
        d.line([x + 75, y + h - 40, x + 150, y + h - 52], fill=RED, width=3)
        d.line([x + 150, y + h - 52, x + 170, y + h - 34], fill=RED, width=3)
        d.line([x + 170, y + h - 34, x + 205, y + h - 48], fill=RED, width=3)
        d.line([x + w - 70, y + 30, x + w - 30, y + h - 40], fill=(40, 40, 40),
               width=6)
    elif kind == "target":
        d.rectangle([x, y, x + w, y + h], fill=(235, 225, 215))
        cx, cy = x + w // 2, y + h // 2
        for r, c in [(52, RED), (38, (255, 255, 255)), (24, RED), (10, (255, 255, 255))]:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
        d.line([cx - 62, cy, cx + 62, cy], fill=INK, width=2)
        d.line([cx, cy - 62, cx, cy + 62], fill=INK, width=2)
    elif kind == "cyber":
        d.rectangle([x, y, x + w, y + h], fill=(18, 30, 55))
        d.polygon([(x + w // 2 + 15, y + 12), (x + w // 2 - 30, y + h // 2 + 5),
                   (x + w // 2 + 2, y + h // 2 + 5), (x + w // 2 - 15, y + h - 12),
                   (x + w // 2 + 32, y + h // 2 - 5), (x + w // 2, y + h // 2 - 5)],
                  fill=(255, 214, 60))
        for i, (bx, by) in enumerate([(30, 25), (55, 90), (w - 60, 30), (w - 45, 95)]):
            d.text((x + bx, y + by), "01", font=font(SANS_B, 18), fill=(90, 180, 220))
    elif kind == "search":
        d.rectangle([x, y, x + w, y + h], fill=(225, 235, 245))
        d.rectangle([x + 60, y + 20, x + 150, y + h - 20], fill=(40, 45, 60))
        d.rectangle([x + 70, y + 32, x + 140, y + h - 32], fill=(160, 205, 235))
        d.ellipse([x + w - 130, y + 25, x + w - 55, y + 100], outline=NAVY, width=8)
        d.line([x + w - 70, y + 92, x + w - 35, y + h - 15], fill=NAVY, width=8)
        d.text((x + w - 118, y + 48), "?", font=font(SANS_B, 40), fill=NAVY)


CARD_ART = ["missile", "gavel", "subpoena", "vaccine", "forum", "deal",
            "target", "cyber", "search"]


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, 4300), CREAM)
    d = ImageDraw.Draw(img)
    y = 36

    # Masthead
    d.text((MARGIN, y), "THE WORLD IN ONE IMAGE",
           font=font(SERIF, 88), fill=INK)
    y += 104
    d.text((MARGIN, y), "38 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED "
           "SATURDAY 21 NOVEMBER 2026",
           font=font(SANS_B, 27), fill=RED)
    y += 48
    y = hrule(d, MARGIN, y, CONTENT, INK, 4) + 10

    # Giant date
    d.text((MARGIN, y), "Saturday 21 November 2026",
           font=font(SERIF, 92), fill=NAVY)
    y += 118
    y = hrule(d, MARGIN, y, CONTENT, NAVY, 3) + 12

    # Headline strip
    strip = ("COP31 RUNS INTO OVERTIME   ·   A MISSILE LANDS IN POLAND   ·   "
             "900,000 AI CHIPS CLEARED FOR CHINA   ·   BAYER'S $7.25B DEAL APPROVED")
    y = text_block(d, MARGIN, y, strip, font(SANS_B, 27), INK, CONTENT, 36) + 6
    y = hrule(d, MARGIN, y, CONTENT, RULE, 2) + 14

    # 6-number strip
    d.text((MARGIN, y), "THE DAY IN NUMBERS", font=font(SANS_B, 26), fill=RED)
    y += 38
    col_w = CONTENT // 6
    top = y
    for i, (num, cap) in enumerate(NUMBERS):
        x = MARGIN + i * col_w
        d.text((x, y), num, font=font(SERIF, 58), fill=NAVY)
        text_block(d, x, y + 70, cap, font(SANS, 21), INK, col_w - 18, 26)
        if i:
            d.line([x - 8, y, x - 8, y + 118], fill=RULE, width=2)
    y = top + 132
    y = hrule(d, MARGIN, y, CONTENT, RULE, 2) + 14

    # Region bar
    counts = region_counts()
    order = ["Europe", "Asia", "Middle East", "Africa", "Americas",
             "Oceania", "Global"]
    total = sum(counts.values())
    assert total == 38, f"story total {total} != 38"
    parts = [f"{r.upper()} {counts[r]}" for r in order]
    bar = "   ·   ".join(parts) + f"   —   TOTAL {total}"
    d.text((MARGIN, y), "WHERE THE STORIES COME FROM",
           font=font(SANS_B, 26), fill=RED)
    y += 38
    y = text_block(d, MARGIN, y, bar, font(SANS_B, 27), INK, CONTENT, 36) + 8
    y = hrule(d, MARGIN, y, CONTENT, INK, 3) + 18

    # 4 big leads in a row
    d.text((MARGIN, y), "THE BIG STORIES", font=font(SANS_B, 26), fill=RED)
    y += 38
    lead_w = (CONTENT - 3 * 20) // 4
    lead_art = [art_cop31, art_strikes, art_chips, art_bayer]
    lead_top = y
    lead_h = 560
    for i, s in enumerate(LEADS):
        x = MARGIN + i * (lead_w + 20)
        num, region, place, source, head, copy = s
        d.rectangle([x, y, x + lead_w, y + lead_h], outline=RULE, width=2)
        lead_art[i](d, x + 2, y + 2, lead_w - 4, 250)
        d.rectangle([x, y + 252, x + lead_w, y + 254], fill=RULE)
        d.text((x + 14, y + 266), f"{num}. {region.upper()}",
               font=font(SANS_B, 22), fill=RED)
        yy = text_block(d, x + 14, y + 296, head, font(SERIF, 33), INK,
                        lead_w - 28, 38)
        yy = text_block(d, x + 14, yy + 6, copy, font(SANS, 23), INK,
                        lead_w - 28, 29)
        d.text((x + 14, y + lead_h - 36), f"{place}  ·  {source}",
               font=font(SANS_B, 20), fill=TEAL)
    y = lead_top + lead_h + 22

    # 9 small cards, 3 x 3
    d.text((MARGIN, y), "ALSO MAKING NEWS", font=font(SANS_B, 26), fill=RED)
    y += 38
    card_w = (CONTENT - 2 * 12) // 3
    card_h = 330
    for row in range(3):
        for col in range(3):
            i = row * 3 + col
            s = CARDS[i]
            x = MARGIN + col * (card_w + 12)
            yy = y + row * (card_h + 16)
            num, region, place, source, head, copy = s
            d.rectangle([x, yy, x + card_w, yy + card_h], outline=RULE, width=2)
            mini_art(d, CARD_ART[i], x + 2, yy + 2, card_w - 4, 118)
            d.rectangle([x, yy + 120, x + card_w, yy + 122], fill=RULE)
            d.text((x + 14, yy + 132), f"{num}. {region.upper()}",
                   font=font(SANS_B, 20), fill=RED)
            ty = text_block(d, x + 14, yy + 158, head, font(SERIF, 27), INK,
                            card_w - 28, 32)
            ty = text_block(d, x + 14, ty + 4, copy, font(SANS, 21), INK,
                            card_w - 28, 26)
            d.text((x + 14, yy + card_h - 32), f"{place}  ·  {source}",
                   font=font(SANS_B, 19), fill=TEAL)
    y += 3 * card_h + 2 * 16 + 22

    # 25 one-liners, two columns
    d.text((MARGIN, y), "ALSO ON SATURDAY 21 NOVEMBER — 25 MORE STORIES",
           font=font(SANS_B, 26), fill=RED)
    y += 40
    y = hrule(d, MARGIN, y, CONTENT, INK, 2) + 10
    col_w = (CONTENT - 30) // 2
    left = ONELINERS[:13]
    right = ONELINERS[13:]
    row_h = 80
    for ci, group in enumerate([left, right]):
        x = MARGIN + ci * (col_w + 30)
        for ri, s in enumerate(group):
            num, region, place, source, head = s
            yy = y + ri * row_h
            d.text((x, yy), f"{num}.", font=font(SANS_B, 24), fill=RED)
            lines = wrap(d, head, font(SANS, 23), col_w - 52)
            for li, ln in enumerate(lines):
                d.text((x + 52, yy + li * 27), ln, font=font(SANS, 23), fill=INK)
            d.text((x + 52, yy + len(lines) * 27 + 2), f"{place}  ·  {source}",
                   font=font(SANS, 19), fill=(90, 85, 75))
    y += len(left) * row_h + 16
    y = hrule(d, MARGIN, y, CONTENT, INK, 3) + 18

    # Map
    d.text((MARGIN, y), "WHERE IT HAPPENED", font=font(SANS_B, 26), fill=RED)
    y += 38
    map_x, map_y, map_w, map_h = MARGIN, y, CONTENT, 380
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                fill=(222, 234, 244), outline=RULE, width=2)

    def lonlat_to_xy(lon, lat):
        px = map_x + (lon + 180) / 360 * map_w
        py = map_y + (75 - lat) / 130 * map_h
        return px, py

    step = 17
    gx, gy = map_x + 8, map_y + 8
    while gy < map_y + map_h - 8:
        while gx < map_x + map_w - 8:
            lon = (gx - map_x) / map_w * 360 - 180
            lat = 75 - (gy - map_y) / map_h * 130
            if any(lo <= lon <= hi and la <= lat <= lb
                   for lo, hi, la, lb in LAND):
                d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(110, 130, 150))
            gx += step
        gx = map_x + 8
        gy += step
    dot_nudge = {2: (-17, 13), 11: (19, -9), 35: (0, 0)}
    for num, lon, lat in MAP_DOTS:
        px, py = lonlat_to_xy(lon, lat)
        dx, dy = dot_nudge.get(num, (0, 0))
        px, py = px + dx, py + dy
        d.ellipse([px - 14, py - 14, px + 14, py + 14], fill=RED,
                  outline=(255, 255, 255), width=2)
        t = str(num)
        tw = d.textlength(t, font=font(SANS_B, 18))
        d.text((px - tw / 2, py - 11), t, font=font(SANS_B, 18),
               fill=(255, 255, 255))
    d.text((map_x + 12, map_y + map_h - 30),
           "Dots: 1 Antalya  ·  2 Kryvyi Rih  ·  3 Washington  ·  5 Poland  ·  "
           "7 California  ·  8 New Delhi  ·  11 Sumy  ·  13 Jakarta  ·  "
           "34 Melbourne  ·  35 Kyiv  ·  36 Kharg",
           font=font(SANS, 18), fill=INK)
    y = map_y + map_h + 22

    # Date check
    d.text((MARGIN, y), "DATE CHECK — WHAT WE LEFT OUT",
           font=font(SANS_B, 26), fill=RED)
    y += 38
    box_top = y
    d.rectangle([MARGIN, y, MARGIN + CONTENT, y + 300], outline=RED, width=3)
    d.text((MARGIN + 18, y + 12),
           "These stories are from Friday 20 November or earlier, so they are "
           "NOT in today's 38:",
           font=font(SANS_B, 23), fill=INK)
    yy = y + 52
    half = (len(LEFT_OUT) + 1) // 2
    for ci, group in enumerate([LEFT_OUT[:half], LEFT_OUT[half:]]):
        x = MARGIN + 18 + ci * (CONTENT // 2)
        for item in group:
            d.text((x, yy), "×  " + item, font=font(SANS, 23), fill=INK)
            yy += 34
        yy = y + 52
    y = box_top + 300 + 22

    # Footer
    y = hrule(d, MARGIN, y, CONTENT, INK, 3) + 12
    y = text_block(d, MARGIN, y,
                   "Every story here happened, or was first reported, on "
                   "Saturday 21 November 2026  ·  Sources named beside each "
                   "story  ·  Drawn illustrations, not photographs",
                   font(SANS, 22), (80, 75, 65), CONTENT, 30) + 10

    img = img.crop((0, 0, W, y + 30))
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    local = HERE / "entry.png"
    img.save(local, "PNG", optimize=True)
    img.save(out_dir / "entry.png", "PNG", optimize=True)
    import hashlib
    digest = hashlib.sha256(local.read_bytes()).hexdigest()
    print(f"entry.png {img.size[0]}x{img.size[1]} sha256 {digest}")
    print(f"stories: {total}  regions: "
          + ", ".join(f"{r} {counts[r]}" for r in order))
    print(f"leads {len(LEADS)} cards {len(CARDS)} one-liners {len(ONELINERS)}")
    return local


if __name__ == "__main__":
    build()
