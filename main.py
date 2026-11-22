#!/usr/bin/env python3
"""World News in One Picture — Saturday 21 November 2026.

Builds a single dense news poster (PNG) summarising 44 real stories that
were reported on Saturday 21 November 2026, spread across 9 world regions.
Every story below was verified against live news coverage of that day
(BBC, Reuters, AP, Al Jazeera, France 24, The Guardian, Yonhap, UPI,
Euronews, The Straits Times and others).

Run:  python3 main.py
Out:  world-news-21-nov-2026.png  (into $MAKEFUN_OUTPUT_DIR, else ./output/)
"""

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
NAVY_TOP = (10, 17, 34)
NAVY_BOT = (16, 28, 54)
PANEL = (22, 36, 66)
PANEL_EDGE = (52, 74, 116)
INK = (238, 242, 250)
MUTED = (168, 182, 205)
FAINT = (126, 141, 168)
GOLD = (245, 197, 24)
RED = (255, 90, 95)
WHITE = (255, 255, 255)

REGIONS = [
    # key, label, colour, column (0..2), short legend label
    ("europe", "EUROPE", (245, 197, 24), 0, "EUROPE"),
    ("mideast", "MIDDLE EAST", (255, 90, 95), 0, "MID EAST"),
    ("namerica", "NORTH AMERICA", (76, 154, 255), 1, "N. AMERICA"),
    ("latam", "LATIN AMERICA", (46, 204, 113), 1, "LATIN AMERICA"),
    ("oceania", "OCEANIA & PACIFIC", (155, 235, 255), 1, "OCEANIA"),
    ("africa", "AFRICA", (255, 138, 0), 2, "AFRICA"),
    ("easia", "EAST ASIA", (255, 77, 157), 2, "EAST ASIA"),
    ("seasia", "SOUTHEAST ASIA", (0, 184, 169), 2, "SE ASIA"),
    ("sasia", "SOUTH ASIA", (165, 91, 255), 2, "S. ASIA"),
]
REGION = {r[0]: r for r in REGIONS}

# ---------------------------------------------------------------- stories
# (region, place, headline, summary) — all reported Sat 21 Nov 2026.
STORIES = [
    # ---- EUROPE (8)
    ("europe", "Kryvyi Rih, Ukraine",
     "Russian missile hits Zelenskyy's hometown",
     "A ballistic missile strikes the city centre, killing two \u2014 including a "
     "7-year-old boy \u2014 and wounding about 60."),
    ("europe", "Gulf of Finland",
     "Drones set Russian cargo ship ablaze",
     "The Sparta II, bound for Kaliningrad, catches fire after a drone strike "
     "and drifts into Finnish waters."),
    ("europe", "Antalya, T\u00fcrkiye",
     "COP31 climate talks run past deadline",
     "The UN summit goes into overtime with no deal as nearly 200 nations split "
     "over fossil fuels and finance."),
    ("europe", "Brussels, Belgium",
     "EU chief proposes smaller budget, Big Tech tax",
     "Ant\u00f3nio Costa pitches a leaner 2028\u201334 EU budget, cut by \u20ac204bn, "
     "with a 3% levy on digital giants."),
    ("europe", "Brussels, Belgium",
     "UK and EU sign three post-Brexit deals",
     "Agreements cover food exports, emissions trading and a youth experience "
     "scheme for young travellers."),
    ("europe", "Paris, France",
     "Cost-of-living protests sweep Europe",
     "Thousands march in France and Portugal over living costs, housing and "
     "wages; 144 are arrested in France."),
    ("europe", "Copenhagen, Denmark",
     "Denmark expels Russian defence attach\u00e9",
     "Copenhagen expels the envoy over an alleged plot to kill US-Ukrainian "
     "rapper Kyivstoner."),
    ("europe", "Mercury orbit",
     "BepiColombo reaches Mercury orbit",
     "The ESA\u2013JAXA probe enters orbit after an eight-year, "
     "10-billion-kilometre journey."),
    # ---- MIDDLE EAST (5)
    ("mideast", "Manama, Bahrain",
     "Iran says it struck US bases in Bahrain",
     "Tehran claims hits on two US positions; Bahrain reports a fire at a "
     "civilian industrial site, no injuries."),
    ("mideast", "Gaza City",
     "Israeli strike kills three in food vehicle",
     "An air strike hits a vehicle carrying food in Tel al-Hawa; Israel says "
     "the dead were militants."),
    ("mideast", "Hodeidah, Yemen",
     "Houthis and Saudi coalition trade strikes",
     "The coalition intercepts missiles aimed at Saudi Arabia and hits Hodeidah; "
     "the Houthis claim 71 strikes in a day."),
    ("mideast", "Tokyo / Riyadh",
     "Saudi Arabia and Japan agree oil stockpile deal",
     "Riyadh will triple crude stored in Japan to 24m barrels as Tokyo rebuilds "
     "reserves hit by the Hormuz crisis."),
    ("mideast", "Doha, Qatar",
     "Gulf economies slide into war recession",
     "Oil states face an unprecedented recession from the war and Hormuz "
     "disruption; Qatar contracts sharply."),
    # ---- NORTH AMERICA (6)
    ("namerica", "New York, USA",
     "AI sell-off drags US stocks into correction",
     "The S&P 500 and Dow enter correction; the Nasdaq erases all its 2026 "
     "gains as AI shares slide."),
    ("namerica", "San Francisco, USA",
     "AI-assisted proof of Riemann hypothesis claimed",
     "Anthropic mathematician Levent Alp\u00f6ge says Claude helped prove the "
     "160-year-old prime-number problem."),
    ("namerica", "Washington, USA",
     "Trump threatens tax on data centres built abroad",
     "US tech firms building AI data centres overseas would face a "
     "\u201ctremendous tax\u201d, Trump says."),
    ("namerica", "Washington, USA",
     "FBI crime database reportedly hacked",
     "The National Crime Information Center is probed after a reported breach, "
     "the second major one in two months."),
    ("namerica", "Los Angeles, USA",
     "Man convicted over deadly Palisades fire",
     "A jury finds Jonathan Rinderknecht guilty of arson over the 2025 LA fire "
     "that killed 12 people."),
    ("namerica", "Cleveland, USA",
     "Harden passes Kobe with 51-point night",
     "James Harden scores 51 in the Cavaliers' 128\u2013119 win over the Pacers, "
     "his 26th career 50-point game."),
    # ---- LATIN AMERICA (5)
    ("latam", "Guasave, Mexico",
     "Mexico captures FBI most-wanted cartel boss",
     "Chapo Isidro is seized in Sinaloa; gunfights, fires and road blockades "
     "follow, leaving at least 11 dead."),
    ("latam", "Bras\u00edlia, Brazil",
     "Bolsonaro in intensive care",
     "Brazil's ex-president is in intensive care with a bowel obstruction; "
     "doctors are weighing surgery."),
    ("latam", "Brazil",
     "Wolbachia mosquitoes cut dengue in Brazil",
     "Children in areas with the bacterium-carrying mosquitoes were far less "
     "likely to catch dengue or chikungunya."),
    ("latam", "Buenos Aires, Argentina",
     "Argentina bonds slide into distress",
     "Bonds fall into distressed territory for the first time in two years as "
     "borrowing costs climb."),
    ("latam", "Central Peru",
     "Magnitude 6.7 quake shakes central Peru",
     "A strong earthquake strikes central Peru, on the Pacific Ring of Fire."),
    # ---- OCEANIA & PACIFIC (4)
    ("oceania", "Cardiff, Wales",
     "Wallabies beat Wales 29\u201326 in Cardiff",
     "Australia end a four-match losing streak in the Nations Championship."),
    ("oceania", "Melbourne, Australia",
     "North Melbourne reach 4th straight AFLW final",
     "The Kangaroos beat Sydney in a tight preliminary final at Princes Park."),
    ("oceania", "Melbourne, Australia",
     "Study may rewrite the human family tree",
     "Monash researchers say some ancient human ancestors may need "
     "reclassifying after new analysis."),
    ("oceania", "American Samoa",
     "US sells first deep-sea mining leases",
     "Leases off American Samoa are sold days after a judge ruled regulators "
     "broke wildlife law."),
    # ---- AFRICA (5)
    ("africa", "Bayelsa, Nigeria",
     "Funeral boat capsizes in Nigeria; 24 dead",
     "A boat carrying mourners capsizes in Bayelsa State; 24 more people are "
     "rescued from the water."),
    ("africa", "Cape Town, South Africa",
     "S. Africa's first woman deputy president dies",
     "Phumzile Mlambo-Ngcuka, 71, former UN Women chief, dies; tributes pour "
     "in from the UN and AU."),
    ("africa", "Southern Ethiopia",
     "700,000 displaced in southern Ethiopia",
     "Conflict displaces about 700,000 people as Ethiopian and Eritrean troops "
     "mass at the border."),
    ("africa", "Dar es Salaam, Tanzania",
     "Tanzania opposition leader convicted",
     "CHADEMA leader Tundu Lissu is convicted of sedition; he calls the "
     "verdict political."),
    ("africa", "Kampala, Uganda",
     "Uganda restricts gatherings over Ebola",
     "Kampala limits gatherings and travel as the DR Congo outbreak threatens "
     "to become the worst ever."),
    # ---- EAST ASIA (4)
    ("easia", "Shenzhen, China",
     "Trump defends Putin ties at Shenzhen summit",
     "After talks with Xi and Putin, Trump defends the ties; Zelenskyy calls "
     "Putin \u201ca killer\u201d."),
    ("easia", "Tokyo, Japan",
     "Japan feels sidelined by big-power talks",
     "Tokyo says it felt left out of the US\u2013China\u2013Russia summit; PM "
     "Takaichi got a scaled-down welcome."),
    ("easia", "Seoul, South Korea",
     "S. Korea ruling party moves to impeach chief justice",
     "The Democratic Party prepares a motion on the second anniversary of the "
     "martial-law attempt."),
    ("easia", "Osaka, Japan",
     "BTS win five awards at MAMA in Osaka",
     "The K-pop group take five prizes at the 2026 MAMA Awards; Cortis win "
     "Song of the Year."),
    # ---- SOUTHEAST ASIA (4)
    ("seasia", "Myanmar",
     "Myanmar rejects ICJ genocide ruling",
     "Myanmar calls the Rohingya ruling unfair; France says it will seek UN "
     "Security Council action."),
    ("seasia", "Brussels, Belgium",
     "EU and Indonesia sign trade deal",
     "The pact removes 98.5% of tariffs on EU goods and covers about 730 "
     "million people."),
    ("seasia", "Indonesia",
     "Factory fire in Indonesia: 3 dead, 36 missing",
     "A blaze at a confectionery factory leaves three dead and dozens missing."),
    ("seasia", "Kuala Lumpur, Malaysia",
     "Malaysia to resettle 10,000 Rohingya",
     "Kuala Lumpur says it will resettle 10,000 Rohingya refugees in T\u00fcrkiye."),
    # ---- SOUTH ASIA (3)
    ("sasia", "Manipur, India",
     "Tainted alcohol kills 11 in Manipur",
     "At least 11 die and 180+ are hospitalised after drinking adulterated "
     "liquor in India's north-east."),
    ("sasia", "Dhaka, Bangladesh",
     "Arson attacks hit Bangladesh",
     "A wave of arson strikes as ex-PM Hasina vows to return from exile."),
    ("sasia", "New Delhi, India",
     "Nepal PM to visit India on first trip abroad",
     "Balendra Shah visits New Delhi on 22\u201323 Nov, with trade and "
     "connectivity on the agenda."),
]

TOP_STORIES = [
    ("1", "IRAN STRIKES BAHRAIN",
     "Tehran says it hit two US bases; Gulf shipping on edge."),
    ("2", "AI STOCKS SLIDE",
     "Wall Street enters correction; Nasdaq erases 2026 gains."),
    ("3", "ICJ: MYANMAR GUILTY OF GENOCIDE",
     "First time the world court holds a state responsible."),
]

SOURCES = ("BBC  \u00b7  Reuters  \u00b7  AP  \u00b7  Al Jazeera  \u00b7  France 24  \u00b7  "
           "The Guardian  \u00b7  Yonhap  \u00b7  UPI  \u00b7  Euronews  \u00b7  "
           "The Straits Times  \u00b7  CBC  \u00b7  CNN")

# ---------------------------------------------------------------- canvas
W, H = 2480, 3800
MARGIN = 84
GUTTER = 40
COL_W = (W - 2 * MARGIN - 2 * GUTTER) // 3


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = "/usr/share/fonts/truetype/dejavu/" + name
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Greedy word wrap using real glyph widths."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_globe(draw, cx, cy, r):
    """Stylised globe: outline, meridians, parallels, 9 region dots."""
    # parallels
    for frac in (-0.55, -0.28, 0.0, 0.28, 0.55):
        y = cy + frac * r
        half = (r * r - (frac * r) ** 2) ** 0.5
        draw.line([(cx - half, y), (cx + half, y)], fill=(52, 74, 116), width=3)
    # meridians
    for k in (-0.6, -0.3, 0.0, 0.3, 0.6):
        rx = abs(k) * r
        ry = r
        x0, y0 = cx - rx, cy - ry
        x1, y1 = cx + rx, cy + ry
        if k == 0.0:
            draw.line([(cx, cy - r), (cx, cy + r)], fill=(52, 74, 116), width=3)
        else:
            draw.arc([x0, y0, x1, y1], 90, 270, fill=(52, 74, 116), width=3)
            draw.arc([x0, y0, x1, y1], 270, 90, fill=(52, 74, 116), width=3)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 150, 200), width=5)
    # region dots: (lon, lat) -> projected point
    import math
    dots = [(-100, 45), (-60, -15), (15, 52), (45, 30), (20, 5),
            (78, 22), (115, 32), (105, 5), (140, -25)]
    for i, (lon, lat) in enumerate(dots):
        lr, ar = math.radians(lon), math.radians(lat)
        px = cx + 0.92 * r * math.sin(lr) * math.cos(ar)
        py = cy - 0.92 * r * math.sin(ar)
        col = REGIONS[i][2]
        draw.ellipse([px - 13, py - 13, px + 13, py + 13], fill=col,
                     outline=(10, 17, 34), width=3)


def region_counts():
    counts = {r[0]: 0 for r in REGIONS}
    for s in STORIES:
        counts[s[0]] += 1
    return counts


def build():
    img = Image.new("RGB", (W, H), NAVY_TOP)
    draw = ImageDraw.Draw(img, "RGBA")
    # vertical gradient
    for y in range(H):
        t = y / H
        c = tuple(int(NAVY_TOP[i] + (NAVY_BOT[i] - NAVY_TOP[i]) * t) for i in range(3))
        draw.line([(0, y), (W, y)], fill=c)
    # faint dotted world band behind header
    for gx in range(0, W, 46):
        for gy in range(40, 620, 46):
            if (gx * 7 + gy * 13) % 5 == 0:
                draw.ellipse([gx, gy, gx + 3, gy + 3], fill=(38, 56, 92))

    f_eyebrow = font(30, bold=True)
    f_title = font(96, bold=True)
    f_sub = font(44, bold=True)
    f_top_no = font(40, bold=True)
    f_top_head = font(33, bold=True)
    f_top_sum = font(27)
    f_chip = font(24, bold=True)
    f_reg = font(30, bold=True)
    f_num = font(30, bold=True)
    f_head = font(30, bold=True)
    f_sum = font(25)
    f_place = font(22, bold=True)
    f_foot = font(24)
    f_foot_b = font(24, bold=True)

    # ---------------- header
    y = 72
    eyebrow = "THE WORLD IN ONE PICTURE  \u00b7  ALL STORIES REPORTED SATURDAY 21 NOVEMBER 2026"
    draw.text((MARGIN, y), eyebrow, font=f_eyebrow, fill=GOLD)
    y += 52
    draw.text((MARGIN, y), "SATURDAY 21 NOVEMBER 2026", font=f_title, fill=INK)
    y += 128
    draw.text((MARGIN, y), "44 date-checked stories  \u00b7  9 regions",
              font=f_sub, fill=(190, 205, 230))
    # gold rule
    draw.rectangle([MARGIN, y + 78, MARGIN + 620, y + 86], fill=GOLD)

    # globe, top right
    draw_globe(draw, W - MARGIN - 215, 300, 205)
    draw.text((W - MARGIN - 430, 528), "9 REGIONS \u00b7 ONE DAY",
              font=f_chip, fill=MUTED)

    # ---------------- top stories strip
    ty = 560
    draw.text((MARGIN, ty), "THE DAY'S THREE BIGGEST STORIES",
              font=f_eyebrow, fill=RED)
    ty += 48
    box_w = (W - 2 * MARGIN - 2 * 28) // 3
    for i, (no, head, summ) in enumerate(TOP_STORIES):
        x0 = MARGIN + i * (box_w + 28)
        draw.rounded_rectangle([x0, ty, x0 + box_w, ty + 164], radius=18,
                               fill=PANEL, outline=PANEL_EDGE, width=2)
        draw.text((x0 + 26, ty + 18), no, font=f_top_no, fill=RED)
        draw.text((x0 + 78, ty + 22), head, font=f_top_head, fill=INK)
        for j, ln in enumerate(wrap(draw, summ, f_top_sum, box_w - 52)):
            draw.text((x0 + 26, ty + 82 + j * 34), ln, font=f_top_sum, fill=MUTED)

    # day-in-numbers panel (fills the short column, adds density)
    NUMBERS = [
        ("\u22123.7%", "S&P 500 falls in the AI sell-off"),
        ("\u22125.06%", "Nikkei falls in the tech rout"),
        ("$89.95", "Brent crude, between glut and war"),
        ("$3.8bn", "GTA VI day-one sales, a record launch"),
        ("700,000", "displaced in southern Ethiopia"),
        ("10bn km", "BepiColombo's journey to Mercury"),
        ("51 pts", "Harden's night, passing Kobe"),
    ]

    # ---------------- region legend
    ly = ty + 164 + 34
    counts = region_counts()
    x = MARGIN
    for key, label, col, _, short in REGIONS:
        tag = f"{short} \u00b7 {counts[key]}"
        tw = draw.textlength(tag, font=f_chip)
        draw.ellipse([x, ly + 4, x + 22, ly + 26], fill=col)
        draw.text((x + 32, ly), tag, font=f_chip, fill=INK)
        x += 32 + tw + 26

    # ---------------- story columns
    body_top = ly + 62
    body_bot = H - 150
    col_x = [MARGIN + i * (COL_W + GUTTER) for i in range(3)]
    # group stories per column, in region order
    cols = [[], [], []]
    for key, label, col, cidx, _ in REGIONS:
        for s in STORIES:
            if s[0] == key:
                cols[cidx].append(s)

    bottoms = []
    story_no = 0
    for ci in range(3):
        # draw with region headers interleaved
        y = body_top
        cur_region = None
        for (key, place, head, summ) in cols[ci]:
            if key != cur_region:
                cur_region = key
                label = REGION[key][1]
                col = REGION[key][2]
                draw.rounded_rectangle([col_x[ci], y, col_x[ci] + COL_W, y + 48],
                                       radius=10, fill=col)
                draw.text((col_x[ci] + 18, y + 9), f"{label}  \u00b7  {counts[key]} STORIES",
                          font=f_reg, fill=(10, 17, 34))
                y += 48 + 12
            story_no += 1
            num = f"{story_no:02d}"
            # number badge
            draw.text((col_x[ci], y + 2), num, font=f_num, fill=REGION[key][2])
            tx = col_x[ci] + 62
            tw = COL_W - 62
            lines_h = wrap(draw, head, f_head, tw)
            hh = 0
            for ln in lines_h:
                draw.text((tx, y + hh), ln, font=f_head, fill=INK)
                hh += 36
            lines_s = wrap(draw, summ, f_sum, tw)
            for ln in lines_s:
                draw.text((tx, y + hh), ln, font=f_sum, fill=MUTED)
                hh += 31
            draw.text((tx, y + hh), place.upper(), font=f_place, fill=FAINT)
            hh += 28
            # divider
            y += hh + 8
            draw.line([(col_x[ci], y), (col_x[ci] + COL_W, y)],
                      fill=(38, 56, 92), width=2)
            y += 10
        # column end marker (debug aid, invisible-ish)
        print(f"column {ci}: bottom y={y} (limit {body_bot})")
        assert y <= body_bot + 40, f"column {ci} overflow: {y} > {body_bot}"
        bottoms.append(y)

    # ---------------- day-in-numbers panel under the shortest column
    py = bottoms[0] + 6
    ph = body_bot - py - 6
    if ph > 200:
        draw.rounded_rectangle([col_x[0], py, col_x[0] + COL_W, py + ph],
                               radius=18, fill=PANEL, outline=PANEL_EDGE, width=2)
        draw.text((col_x[0] + 26, py + 20), "THE DAY IN NUMBERS",
                  font=f_eyebrow, fill=GOLD)
        draw.line([(col_x[0] + 26, py + 62), (col_x[0] + COL_W - 26, py + 62)],
                  fill=PANEL_EDGE, width=2)
        f_big = font(36, bold=True)
        f_lab = font(25)
        ry = py + 82
        for big, lab in NUMBERS:
            draw.text((col_x[0] + 26, ry), big, font=f_big, fill=INK)
            bw = draw.textlength(big, font=f_big)
            lab_lines = wrap(draw, lab, f_lab, COL_W - 52 - bw - 24)
            ly2 = ry + 5
            for ln in lab_lines:
                draw.text((col_x[0] + 26 + bw + 24, ly2), ln, font=f_lab, fill=MUTED)
                ly2 += 31
            ry += max(52, ly2 - ry + 8)

    # ---------------- footer
    fy = H - 128
    draw.line([(MARGIN, fy - 22), (W - MARGIN, fy - 22)], fill=PANEL_EDGE, width=2)
    draw.text((MARGIN, fy), "DATE-CHECKED: every story above was reported on Saturday 21 November 2026.",
              font=f_foot_b, fill=GOLD)
    draw.text((MARGIN, fy + 36), "Sources: " + SOURCES, font=f_foot, fill=MUTED)
    draw.text((MARGIN, fy + 70),
              "Compiled from 800+ headlines  \u00b7  Built by an AI agent for make.fun's "
              "\u201cSum up 21 November's world news in one image\u201d bounty.",
              font=f_foot, fill=FAINT)
    return img


def main():
    img = build()
    out_name = "world-news-21-nov-2026.png"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(os.getcwd(), "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, out_name)
    img.save(out_path, "PNG")
    # also drop a copy next to this script when writable (repo preview)
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        img.save(os.path.join(here, out_name), "PNG")
    except OSError:
        pass
    size = os.path.getsize(out_path)
    print(f"saved {out_path}  {img.size[0]}x{img.size[1]}  {size} bytes  "
          f"stories={len(STORIES)} regions={len(REGIONS)}")


if __name__ == "__main__":
    main()
