#!/usr/bin/env python3
"""Draw 'The World in One Image - 20 November 2026'.

A newspaper-style infographic summarising seven verified news stories
from Friday 20 November 2026. Stdlib + Pillow only. Fully deterministic:
no timestamps, no randomness, no network. Running it twice produces a
byte-identical PNG.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

W, H = 1024, 1024

NAVY = (10, 17, 40)
PANEL = (22, 33, 66)
PANEL_EDGE = (58, 74, 120)
HERO_BG = (34, 22, 74)
GOLD = (245, 184, 29)
GOLD_DIM = (232, 169, 12)
WHITE = (255, 255, 255)
MIST = (196, 205, 224)
FAINT = (148, 160, 186)
ORANGE = (255, 122, 26)
RED = (235, 64, 52)
GREEN = (74, 222, 128)
CYAN = (56, 189, 248)
VIOLET = (167, 139, 250)
SKY = (125, 211, 252)

MARGIN = 26


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap using real glyph widths."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, xy, text, font, fill, max_width, line_gap=6):
    x, y = xy
    lines = wrap_text(draw, text, font, max_width)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y


def rounded_panel(draw, box, fill, outline, radius=14, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- icons
def icon_scales(draw, cx, cy, s, color):
    """Balanced scales of justice, abstract."""
    draw.line([(cx, cy - s), (cx, cy + s)], fill=color, width=4)
    draw.line([(cx - s, cy - s + 6), (cx + s, cy - s + 6)], fill=color, width=4)
    draw.line([(cx - s, cy - s + 6), (cx - s, cy + 2)], fill=color, width=3)
    draw.line([(cx + s, cy - s + 6), (cx + s, cy + 2)], fill=color, width=3)
    draw.arc([cx - s - 4, cy - 4, cx - s + 16, cy + 16], 0, 180, fill=color, width=3)
    draw.arc([cx + s - 16, cy - 4, cx + s + 4, cy + 16], 0, 180, fill=color, width=3)
    draw.line([(cx - 12, cy + s), (cx + 12, cy + s)], fill=color, width=4)


def icon_cyclone(draw, cx, cy, s, color):
    for i, r in enumerate((s, int(s * 0.72), int(s * 0.45))):
        start = 200 + i * 55
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, start + 250,
                 fill=color, width=5)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=color)


def icon_globe(draw, cx, cy, s, color):
    draw.ellipse([cx - s, cy - s, cx + s, cy + s], outline=color, width=4)
    draw.ellipse([cx - int(s * 0.45), cy - s, cx + int(s * 0.45), cy + s],
                 outline=color, width=3)
    draw.line([(cx - s, cy), (cx + s, cy)], fill=color, width=3)
    draw.arc([cx - s, cy - int(s * 0.55), cx + s, cy + int(s * 0.55)],
             200, 340, fill=color, width=3)
    draw.arc([cx - s, cy - int(s * 0.55), cx + s, cy + int(s * 0.55)],
             20, 160, fill=color, width=3)


def icon_rocket(draw, cx, cy, s, color):
    draw.polygon([(cx, cy - s), (cx + int(s * 0.45), cy - 4),
                  (cx, cy + int(s * 0.4)), (cx - int(s * 0.45), cy - 4)],
                 fill=color)
    draw.ellipse([cx - 7, cy - 14, cx + 7, cy], fill=WHITE)
    draw.polygon([(cx - int(s * 0.45), cy + 2), (cx - int(s * 0.7), cy + s),
                  (cx - int(s * 0.2), cy + int(s * 0.55))], fill=ORANGE)
    draw.polygon([(cx + int(s * 0.45), cy + 2), (cx + int(s * 0.7), cy + s),
                  (cx + int(s * 0.2), cy + int(s * 0.55))], fill=ORANGE)
    draw.polygon([(cx - 6, cy + int(s * 0.4)), (cx + 6, cy + int(s * 0.4)),
                  (cx, cy + s + 8)], fill=GOLD)


def icon_dove(draw, cx, cy, s, color):
    draw.ellipse([cx - int(s * 0.9), cy - int(s * 0.35),
                  cx + int(s * 0.9), cy + int(s * 0.35)], fill=color)
    draw.ellipse([cx + int(s * 0.45), cy - int(s * 0.75),
                  cx + int(s * 1.05), cy - int(s * 0.1)], fill=color)
    draw.polygon([(cx + int(s * 0.95), cy - int(s * 0.6)),
                  (cx + int(s * 1.35), cy - int(s * 0.75)),
                  (cx + int(s * 0.95), cy - int(s * 0.35))], fill=GOLD)
    draw.polygon([(cx - int(s * 0.85), cy - int(s * 0.1)),
                  (cx - int(s * 1.3), cy - int(s * 0.45)),
                  (cx - int(s * 1.25), cy + int(s * 0.25))], fill=color)
    draw.ellipse([cx + int(s * 0.72), cy - int(s * 0.55),
                  cx + int(s * 0.82), cy - int(s * 0.45)], fill=NAVY)
    # olive branch
    draw.line([(cx - int(s * 0.6), cy + int(s * 0.75)),
               (cx + int(s * 0.5), cy + int(s * 0.6))], fill=GREEN, width=3)
    for t in (-0.5, -0.1, 0.3):
        lx = cx + int(s * t)
        draw.ellipse([lx - 5, cy + int(s * 0.55), lx + 5, cy + int(s * 0.7)],
                     fill=GREEN)


def icon_controller(draw, cx, cy, s, color):
    draw.rounded_rectangle([cx - s, cy - int(s * 0.55), cx + s, cy + int(s * 0.55)],
                           radius=16, outline=color, width=4)
    draw.line([(cx - int(s * 0.62), cy), (cx - int(s * 0.32), cy)],
              fill=color, width=4)
    draw.line([(cx - int(s * 0.47), cy - int(s * 0.15)),
               (cx - int(s * 0.47), cy + int(s * 0.15))], fill=color, width=4)
    for dx, dy in ((0.42, -0.18), (0.62, 0.02), (0.42, 0.2), (0.62, 0.4)):
        draw.ellipse([cx + int(s * dx) - 4, cy + int(s * dy) - 4,
                      cx + int(s * dx) + 4, cy + int(s * dy) + 4], fill=GOLD)
    draw.ellipse([cx - 4, cy + int(s * 0.22) - 4, cx + 4, cy + int(s * 0.22) + 4],
                 outline=color, width=3)


def hero_sun_skyline(draw, x0, y0, x1, y1):
    """Gold sun over a dark skyline, right side of the hero panel."""
    cx, cy = (x0 + x1) // 2 + 20, (y0 + y1) // 2 - 6
    r = 78
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ORANGE)
    draw.ellipse([cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16],
                 fill=GOLD)
    base = y1 - 8
    towers = [(x0 + 8, 96), (x0 + 62, 128), (x0 + 122, 82),
              (x0 + 182, 118), (x0 + 236, 96)]
    for tx, th in towers:
        draw.rectangle([tx, base - th, tx + 46, base], fill=NAVY)
    draw.rectangle([x0, base, x1, base + 8], fill=NAVY)


# ---------------------------------------------------------------- build
def build_image():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    f_date = load_font(FONT_BOLD, 46)
    f_tag = load_font(FONT_BOLD, 27)
    f_day = load_font(FONT_BOLD, 21)
    f_kicker = load_font(FONT_BOLD, 19)
    f_hero_head = load_font(FONT_BOLD, 44)
    f_hero_sub = load_font(FONT_REG, 22)
    f_head = load_font(FONT_BOLD, 22)
    f_sub = load_font(FONT_REG, 17)
    f_foot = load_font(FONT_BOLD, 22)
    f_foot2 = load_font(FONT_REG, 19)

    # ---- header ------------------------------------------------------
    draw.text((MARGIN, 30), "20 NOVEMBER 2026", font=f_date, fill=WHITE)
    draw.text((MARGIN, 88), "THE WORLD IN ONE IMAGE", font=f_tag, fill=GOLD)
    draw.text((MARGIN, 122), "FRIDAY", font=f_day, fill=MIST)

    rx = 782
    draw.rectangle([rx, 34, rx + 216, 40], fill=GOLD)
    draw.text((rx, 50), "SEVEN STORIES", font=f_tag, fill=WHITE)
    draw.text((rx, 86), "ONE DAY", font=f_day, fill=MIST)

    # ---- hero panel --------------------------------------------------
    hx0, hy0, hx1, hy1 = MARGIN, 158, W - MARGIN, 392
    rounded_panel(draw, (hx0, hy0, hx1, hy1), HERO_BG, (92, 66, 160))
    draw.text((hx0 + 24, hy0 + 18), "MIDDLE EAST  \u00b7  WASHINGTON",
              font=f_kicker, fill=ORANGE)
    draw_wrapped(draw, (hx0 + 24, hy0 + 50),
                 "TRUMP: NO IRAN DECISION UNTIL 2027",
                 f_hero_head, WHITE, 640, line_gap=4)
    draw_wrapped(draw, (hx0 + 24, hy0 + 162),
                 "US president says \u201cwe\u2019ll see what happens after "
                 "January 1\u201d \u2014 no rush on new strikes.",
                 f_hero_sub, MIST, 640, line_gap=4)
    hero_sun_skyline(draw, hx1 - 300, hy0 + 14, hx1 - 16, hy1 - 14)

    # ---- six story panels --------------------------------------------
    stories = [
        dict(kicker="WORLD COURT", accent=GOLD,
             head="MYANMAR GUILTY OF GENOCIDE",
             sub="ICJ: Myanmar guilty of genocide against the Rohingya "
                 "in 2017; reparations ordered.",
             icon=icon_scales, icon_color=GOLD),
        dict(kicker="WEATHER  \u00b7  INDIA", accent=CYAN,
             head="CYCLONE AKVAN NEARS ODISHA",
             sub="Landfall due at noon near Gopalpur; 50,000+ evacuated; "
                 "red alert in Odisha.",
             icon=icon_cyclone, icon_color=CYAN),
        dict(kicker="DIPLOMACY  \u00b7  CHINA", accent=RED,
             head="TRUMP, XI AND PUTIN MEET IN CHINA",
             sub="First-ever three-way summit in Shenzhen at APEC; "
                 "nuclear risks and energy on the table.",
             icon=icon_globe, icon_color=SKY),
        dict(kicker="SPACE", accent=VIOLET,
             head="VOYAGER 1 PASSES A LIGHT-DAY",
             sub="NASA confirms the farthest human-made object hits a new "
                 "milestone, 48 years on.",
             icon=icon_rocket, icon_color=WHITE),
        dict(kicker="EUROPE  \u00b7  UKRAINE", accent=GREEN,
             head="EUROPE READY FOR RUSSIA TALKS",
             sub="European leaders say they are ready to negotiate an end "
                 "to the war, as diplomacy stirs.",
             icon=icon_dove, icon_color=WHITE),
        dict(kicker="CULTURE  \u00b7  BUSINESS", accent=GOLD,
             head="GTA 6 SALES PASS $1.8 BILLION",
             sub="Rockstar\u2019s blockbuster overtakes the global run of "
                 "\u201cThe Odyssey\u201d within days of launch.",
             icon=icon_controller, icon_color=GREEN),
    ]

    grid_y = [410, 660]
    grid_h = 238
    col_w = 310
    gap = 19
    for idx, story in enumerate(stories):
        row, col = divmod(idx, 3)
        x0 = MARGIN + col * (col_w + gap)
        y0 = grid_y[row]
        x1, y1 = x0 + col_w, y0 + grid_h
        rounded_panel(draw, (x0, y0, x1, y1), PANEL, PANEL_EDGE)
        draw.rectangle([x0 + 16, y0 + 14, x1 - 16, y0 + 19], fill=story["accent"])
        draw.text((x0 + 16, y0 + 30), story["kicker"],
                  font=f_kicker, fill=story["accent"])
        story["icon"](draw, x1 - 48, y0 + 80, 24, story["icon_color"])
        draw_wrapped(draw, (x0 + 16, y0 + 112), story["head"],
                     f_head, WHITE, col_w - 32, line_gap=3)
        # sub sits below the headline block
        head_lines = wrap_text(draw, story["head"], f_head, col_w - 32)
        sub_y = y0 + 112 + len(head_lines) * (f_head.size + 3) + 8
        draw_wrapped(draw, (x0 + 16, sub_y), story["sub"],
                     f_sub, MIST, col_w - 32, line_gap=2)

    # ---- footer ------------------------------------------------------
    fy = 916
    draw.line([(MARGIN, fy), (W - MARGIN, fy)], fill=PANEL_EDGE, width=2)
    draw.text((MARGIN, fy + 16), "All events of Friday 20 November 2026",
              font=f_foot, fill=WHITE)
    draw.text((MARGIN, fy + 48), "One day, seven stories \u2014 as reported.",
              font=f_foot2, fill=FAINT)

    img.save(OUT_PATH, format="PNG", optimize=True)
    print("wrote", OUT_PATH, img.size)


if __name__ == "__main__":
    build_image()
