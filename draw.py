#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: a 1024x1024 newspaper front page
summarising Friday 20 November 2026 world news, drawn with Pillow shapes
only (no generated imagery, so no garbled text).

Layout: navy masthead, 2x3 panel grid, one-line footer.
Each panel: coloured tag bar, flat vector icon, bold headline, 1-line summary.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (245, 241, 232)      # paper
NAVY = (20, 33, 61)
GOLD = (242, 193, 78)
INK = (24, 24, 24)
GREY = (68, 68, 68)
CARD = (255, 255, 255)
BORDER = (216, 210, 196)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


# ---------------------------------------------------------------- icons
def icon_scales(d, cx, cy, col):
    # balance / scales of justice (kept narrow so it never reaches the text)
    d.line([(cx, cy - 52), (cx, cy + 52)], fill=col, width=6)
    d.line([(cx - 40, cy - 40), (cx + 40, cy - 40)], fill=col, width=6)
    d.line([(cx, cy - 52), (cx, cy - 62)], fill=col, width=6)
    d.ellipse([cx - 7, cy - 69, cx + 7, cy - 55], fill=col)
    for s in (-1, 1):
        x = cx + s * 40
        d.line([(x, cy - 40), (x - 18, cy + 8)], fill=col, width=4)
        d.line([(x, cy - 40), (x + 18, cy + 8)], fill=col, width=4)
        d.line([(x - 18, cy + 8), (x + 18, cy + 8)], fill=col, width=5)
        d.pieslice([x - 20, cy + 2, x + 20, cy + 34], 0, 180, fill=col)
    d.line([(cx - 28, cy + 52), (cx + 28, cy + 52)], fill=col, width=6)


def icon_bridge(d, cx, cy, col):
    # bridge over the Dnipro: deck, arch, supports, water
    d.line([(cx - 58, cy - 18), (cx + 58, cy - 18)], fill=col, width=7)
    d.arc([cx - 52, cy - 58, cx + 52, cy + 6], 180, 360, fill=col, width=6)
    for x in (-34, 0, 34):
        d.line([(cx + x, cy - 18), (cx + x, cy - 44)], fill=col, width=4)
    for i, y in enumerate((cy + 22, cy + 38, cy + 54)):
        d.arc([cx - 58 + i * 8, y - 12, cx + 58 - i * 8, y + 12],
              180, 360, fill=(70, 130, 180), width=5)


def icon_radar(d, cx, cy, col):
    # airspace radar: ring, sweep, three intruding objects
    d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], outline=col, width=5)
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], outline=col, width=3)
    d.line([(cx, cy), (cx + 40, cy - 34)], fill=col, width=5)
    for (x, y) in ((-28, -18), (18, 8), (-6, 30)):
        d.ellipse([cx + x - 7, cy + y - 7, cx + x + 7, cy + y + 7],
                  fill=(178, 34, 34))
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=col)


def icon_tower(d, cx, cy, col):
    # twisted skyscraper (PIF Tower): tapering tower, floor lines, damage
    d.polygon([(cx - 26, cy + 56), (cx - 14, cy - 58),
               (cx + 14, cy - 58), (cx + 26, cy + 56)], fill=col)
    for i in range(6):
        y = cy - 44 + i * 16
        d.line([(cx - 22 + i, y), (cx + 22 - i, y)], fill=(255, 255, 255), width=2)
    # damage: broken floors near the top
    for (x, y) in ((-8, -38), (6, -26), (-2, -14)):
        d.rectangle([cx + x - 6, cy + y - 4, cx + x + 6, cy + y + 4],
                    fill=(220, 60, 40))
    d.line([(cx - 34, cy + 56), (cx + 34, cy + 56)], fill=col, width=5)


def icon_waves(d, cx, cy, col):
    # flood waves over a rooftop
    d.polygon([(cx - 40, cy + 10), (cx, cy - 22), (cx + 40, cy + 10)],
              fill=(178, 34, 34))
    d.rectangle([cx - 40, cy + 10, cx + 40, cy + 26], fill=(178, 34, 34))
    for i, y in enumerate((cy + 34, cy + 48)):
        d.arc([cx - 56 + i * 6, y - 10, cx + 56 - i * 6, y + 12],
              180, 360, fill=(40, 110, 170), width=6)
    d.arc([cx - 44, cy + 52, cx + 44, cy + 74], 180, 360,
          fill=(40, 110, 170), width=6)


def icon_chart(d, cx, cy, col):
    # falling market chart
    d.line([(cx - 54, cy + 48), (cx + 54, cy + 48)], fill=col, width=5)
    d.line([(cx - 54, cy + 48), (cx - 54, cy - 52)], fill=col, width=5)
    pts = [(cx - 48, cy - 38), (cx - 24, cy - 22), (cx - 2, cy - 30),
           (cx + 20, cy + 6), (cx + 48, cy + 34)]
    d.line(pts, fill=(178, 34, 34), width=7, joint="curve")
    # arrowhead at the end
    d.polygon([(cx + 48, cy + 34), (cx + 30, cy + 26), (cx + 38, cy + 44)],
              fill=(178, 34, 34))
    for (x, h) in ((-40, 22), (-16, 34), (8, 18)):
        d.rectangle([cx + x - 7, cy + 48 - h, cx + x + 7, cy + 48],
                    fill=(150, 150, 150))


PANELS = [
    dict(tag="THE HAGUE  ·  WORLD COURT", color=(20, 50, 107),
         icon=icon_scales,
         headline="MYANMAR GUILTY OF GENOCIDE",
         summary="ICJ rules 9–6: the 2017 crackdown on the Rohingya was genocide — a first for a state."),
    dict(tag="KYIV  ·  UKRAINE", color=(156, 43, 43),
         icon=icon_bridge,
         headline="MISSILES HIT KYIV BRIDGES",
         summary="Overnight strikes damage 3 Dnipro bridges; 8 killed, 28 injured in 9 regions."),
    dict(tag="POLAND  ·  NATO", color=(146, 96, 0),
         icon=icon_radar,
         headline="RUSSIAN OBJECTS ENTER POLAND",
         summary="3 objects — likely 2 missiles and a drone — cross the airspace; Warsaw calls it provocation."),
    dict(tag="RIYADH  ·  MIDDLE EAST", color=(15, 118, 110),
         icon=icon_tower,
         headline="MISSILE HITS RIYADH'S TALLEST TOWER",
         summary="Houthi strike damages PIF Tower floors in the financial district; no injuries."),
    dict(tag="FLORIDA  ·  USA", color=(29, 78, 216),
         icon=icon_waves,
         headline="RECORD FLOOD ON SPACE COAST",
         summary="St. Johns River hits 18.66 ft, beating the 1953 record; 100+ people rescued."),
    dict(tag="MARKETS  ·  AI", color=(120, 20, 20),
         icon=icon_chart,
         headline="AI SELL-OFF DEEPENS",
         summary="Nikkei falls 4.8% on Friday; S&P 500 down ~2% as Anthropic debuts +17%."),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    f_date = font(FONT_B, 54)
    f_sub = font(FONT_B, 27)
    d.text((W // 2, 62), "FRIDAY 20 NOVEMBER 2026", font=f_date,
           fill=(255, 255, 255), anchor="mm")
    d.text((W // 2, 118), "WORLD NEWS IN ONE IMAGE", font=f_sub,
           fill=GOLD, anchor="mm")

    # ---- panels
    px, py = 16, 170
    pw, ph, gap = 488, 252, 16
    f_tag = font(FONT_B, 17)
    f_head = font(FONT_B, 25)
    f_sum = font(FONT_R, 18)
    for i, p in enumerate(PANELS):
        x = px + (i % 2) * (pw + gap)
        y = py + (i // 2) * (ph + gap)
        d.rectangle([x, y, x + pw, y + ph], fill=CARD, outline=BORDER, width=2)
        d.rectangle([x, y, x + pw, y + 36], fill=p["color"])
        d.text((x + 14, y + 18), p["tag"], font=f_tag,
               fill=(255, 255, 255), anchor="lm")
        # icon, left column
        p["icon"](d, x + 68, y + 148, p["color"])
        # headline + summary, right column
        tx = x + 140
        tw = pw - 140 - 16
        lines = wrap(d, p["headline"], f_head, tw)[:2]
        ly = y + 58
        for ln in lines:
            d.text((tx, ly), ln, font=f_head, fill=INK)
            ly += 31
        ly += 6
        for ln in wrap(d, p["summary"], f_sum, tw)[:3]:
            d.text((tx, ly), ln, font=f_sum, fill=GREY)
            ly += 24

    # ---- footer strip
    d.rectangle([0, 966, W, H], fill=NAVY)
    f_foot = font(FONT_B, 16)
    d.text((W // 2, 995),
           "ALSO: Youth protests in 25+ European countries  ·  German metalworkers' first 24-hour strike in 8 years",
           font=f_foot, fill=(255, 255, 255), anchor="mm")

    out = "/home/hatch/workspace/makefun/news-image-20261120/entry/entry.png"
    img.save(out, "PNG", optimize=True)
    print("saved", out)


if __name__ == "__main__":
    main()
