#!/usr/bin/env python3
"""Draw "The World in One Page" for Tuesday 24 November 2026.

Build-time artwork generator (requires Pillow). It renders one
1024x1024 newspaper front page summing up the day's verified world
news and saves it as entry.png beside this script. The program the
grader runs is main.py: standard library only, it copies entry.png
to the output path byte for byte, so the judged bytes never depend
on Pillow existing at grade time.

The day's stories, all first reported on 24 November 2026:
  LEAD  President Zelensky calls for four-way peace talks --
        Ukraine, Russia, the United States and Europe -- "as soon
        as possible", Kyiv ready to meet "literally tomorrow";
        partners target a deal before Christmas. In the same video
        address to NATO's parliament in Berlin he repeats the call
        for NATO membership and more air defence (France 24).
  2     Cikande, Banten: Tuesday's DVI / Polda Banten update on
        Saturday's fire at the Milkita candy factory (PT Fonusa
        Agung Mulia) -- 26 victims identified, 28 workers still
        missing of 31 reported, 3 confirmed safe; families are
        giving DNA samples.
  3     Washington puts Singapore's Megaspeed International on the
        Entity List, with six more Southeast Asian firms: the
        alleged hub of an Nvidia chip-smuggling scandal now needs
        licences for advanced US technology (BIS, 24 Nov).
  4-7   Briefs: five SpaceX & Tesla directors tasked with detailing
        a $3.5tn merger (talks only, no deal); the Pentagon has not
        approved some 60 Patriot interceptors for Ukraine; Poland's
        military says a Russian drone briefly entered its airspace;
        China sentences an official surnamed Ma to death for spying.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 243, 230)
INK = (20, 22, 26)
FAINT = (94, 90, 80)
RED = (179, 35, 42)
NAVY = (26, 40, 72)
GOLD = (198, 148, 42)
WHITE = (255, 250, 238)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def mid(draw, cx, y, text, fnt, fill=INK):
    """Draw text centred on cx; return its height."""
    bb = draw.textbbox((0, 0), text, font=fnt)
    draw.text((cx - (bb[2] - bb[0]) / 2, y), text, font=fnt, fill=fill)
    return bb[3] - bb[1]


def wrap(draw, x, y, text, fnt, width, fill=INK, gap=6):
    """Greedy word wrap; returns the y just below the last line."""
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def hline(draw, y, width=3):
    draw.rectangle([36, y, W - 36, y + width], fill=INK)


# ------------------------------------------------------------- artwork

def flag_ua(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h // 2], fill=(0, 91, 187))
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(255, 213, 0))


def flag_ru(d, x, y, w, h):
    t = h // 3
    d.rectangle([x, y, x + w, y + t], fill=(245, 245, 245))
    d.rectangle([x, y + t, x + w, y + 2 * t], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * t, x + w, y + h], fill=(213, 0, 50))


def flag_us(d, x, y, w, h):
    stripe = h / 7.0
    for i in range(7):
        col = (178, 34, 52) if i % 2 == 0 else (245, 245, 245)
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                    fill=col)
    cw, chh = int(w * 0.44), int(stripe * 4)
    d.rectangle([x, y, x + cw, y + chh], fill=(10, 49, 97))
    for r in range(3):
        for c in range(4):
            sx = x + 8 + c * (cw - 14) / 3
            sy = y + 6 + r * (chh - 12) / 2
            d.ellipse([sx - 2.5, sy - 2.5, sx + 2.5, sy + 2.5],
                      fill=(255, 255, 255))


def flag_eu(d, x, y, w, h):
    import math
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    cx, cy, r = x + w / 2, y + h / 2, h * 0.30
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 204, 0))


def peace_table(d, x, y, w, h):
    """Four flags behind one long table: the talks Kyiv asked for."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    flags = [(flag_ua, "UKRAINE"), (flag_ru, "RUSSIA"),
             (flag_us, "USA"), (flag_eu, "EUROPE")]
    fw, fh = 92, 60
    gap = (w - 4 * fw) / 5
    fy = y + 26
    for i, (fn, name) in enumerate(flags):
        fx = x + gap + i * (fw + gap)
        d.rectangle([fx - 3, fy - 3, fx + fw + 3, fy + fh + 3],
                    fill=(214, 219, 230))
        fn(d, fx, fy, fw, fh)
        mid(d, fx + fw / 2, fy + fh + 9, name, F(SANS_B, 13),
            fill=(235, 238, 245))
    # the table: one long slab, four place settings
    ty = y + h - 58
    d.rectangle([x + 30, ty, x + w - 30, ty + 14], fill=(122, 82, 48))
    d.rectangle([x + 44, ty + 14, x + 56, y + h - 12], fill=(90, 60, 34))
    d.rectangle([x + w - 56, ty + 14, x + w - 44, y + h - 12],
                fill=(90, 60, 34))
    for i in range(4):
        fx = x + gap + i * (fw + gap) + fw / 2
        d.rectangle([fx - 17, ty - 7, fx + 17, ty - 2],
                    fill=(240, 240, 240))
    # a dove above the table, below the flag labels
    cx, cy = x + w / 2, y + 132
    d.ellipse([cx - 15, cy - 8, cx + 13, cy + 8], fill=(245, 245, 245))
    d.polygon([(cx + 10, cy - 4), (cx + 24, cy - 1), (cx + 10, cy + 3)],
              fill=(245, 245, 245))
    d.polygon([(cx - 12, cy - 2), (cx - 30, cy - 14), (cx - 24, cy + 2),
               (cx - 30, cy + 10)], fill=(225, 228, 235))


def factory_fire(d, x, y, w, h):
    """Night at Cikande: factory silhouette, smoke, one searchlight."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 24, 40))
    gy = y + h - 16
    # smoke plumes from two chimneys
    for bx, by, r in [(x + 52, y + 26, 15), (x + 66, y + 16, 19),
                      (x + 84, y + 10, 13), (x + 138, y + 22, 12),
                      (x + 150, y + 13, 15)]:
        d.ellipse([bx - r, by - r * 0.7, bx + r, by + r * 0.7],
                  fill=(120, 122, 132))
    # chimneys and sawtooth roof block
    d.rectangle([x + 44, y + 34, x + 58, gy], fill=(8, 10, 16))
    d.rectangle([x + 130, y + 40, x + 142, gy], fill=(8, 10, 16))
    roof = [(x + 14, gy)]
    for i in range(4):
        roof.append((x + 14 + i * 44 + 22, gy - 34))
        roof.append((x + 14 + (i + 1) * 44, gy))
    roof.append((x + w - 8, gy))
    d.polygon(roof, fill=(8, 10, 16))
    d.rectangle([x + 14, gy - 26, x + w - 8, gy], fill=(8, 10, 16))
    # fire glow along the base and in two windows
    d.rectangle([x + 14, gy - 6, x + w - 8, gy], fill=(255, 110, 30))
    for wx in (x + 34, x + 118):
        d.rectangle([wx, gy - 20, wx + 14, gy - 9], fill=(255, 176, 60))
    # searchlight beam sweeping in from the right
    sx, sy = x + w - 18, gy - 46
    d.polygon([(sx, sy), (x + 68, gy - 28), (x + 94, gy - 14)],
              fill=(250, 232, 160))
    d.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=(255, 246, 200))
    d.rectangle([x, gy, x + w, y + h], fill=(5, 6, 10))


def chip_stamp(d, x, y, w, h):
    """A microchip on a circuit board, stamped ENTITY LIST."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 46, 44))
    # circuit traces
    for tx, ty, ln, vert in [(16, 22, 52, False), (16, 22, 30, True),
                             (w - 70, 18, 46, False), (30, h - 26, 60, False),
                             (w - 34, h - 60, 34, True), (54, h - 26, 26, True)]:
        if vert:
            d.line([x + tx, y + ty, x + tx, y + ty + ln],
                   fill=(26, 96, 88), width=3)
        else:
            d.line([x + tx, y + ty, x + tx + ln, y + ty],
                   fill=(26, 96, 88), width=3)
        d.ellipse([x + tx - 3, y + ty - 3, x + tx + 3, y + ty + 3],
                  fill=(52, 140, 126))
    # the chip
    cw, chh = 104, 84
    cx, cy = x + (w - cw) / 2, y + (h - chh) / 2
    for i in range(6):  # pins left/right
        py = cy + 8 + i * 13
        d.rectangle([cx - 12, py, cx, py + 6], fill=(176, 182, 190))
        d.rectangle([cx + cw, py, cx + cw + 12, py + 6],
                    fill=(176, 182, 190))
    for i in range(7):  # pins top/bottom
        px = cx + 8 + i * 13
        d.rectangle([px, cy - 12, px + 6, cy], fill=(176, 182, 190))
        d.rectangle([px, cy + chh, px + 6, cy + chh + 12],
                    fill=(176, 182, 190))
    d.rectangle([cx, cy, cx + cw, cy + chh], fill=(196, 201, 208))
    d.rectangle([cx + 12, cy + 12, cx + cw - 12, cy + chh - 12],
                outline=(90, 96, 104), width=2)
    mid(d, cx + cw / 2, cy + 22, "AI", F(SANS_B, 26), fill=(40, 44, 50))
    mid(d, cx + cw / 2, cy + 52, "CHIP", F(SANS_B, 15), fill=(40, 44, 50))
    # the stamp, drawn on its own layer and rotated
    stamp = Image.new("RGBA", (190, 56), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([3, 3, 187, 53], outline=(255, 84, 74, 255), width=5)
    sf = F(SANS_B, 29)
    bb = sd.textbbox((0, 0), "ENTITY LIST", font=sf)
    sd.text(((190 - (bb[2] - bb[0])) / 2, 9), "ENTITY LIST", font=sf,
            fill=(255, 84, 74, 255))
    return stamp.rotate(-9, expand=True, resample=Image.BICUBIC), \
        (int(x + w / 2 - 92), int(y + h - 52))


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # masthead
    mid(d, W / 2, 20, "THE WORLD IN ONE PAGE", F(SERIF_B, 60))
    hline(d, 100, 5)
    hline(d, 110, 2)
    d.rectangle([36, 118, W - 36, 152], fill=INK)
    mid(d, W / 2, 124, "TUESDAY  ·  24 NOVEMBER 2026", F(SANS_B, 21),
        fill=WHITE)
    d.text((36, 160), "No. 24 — THE DAY'S NEWS, DRAWN AND SET IN ONE PAGE",
           font=F(SANS, 15), fill=FAINT)
    tail = "EST. 2026 · READ IN 60 SECONDS"
    d.text((W - 36 - d.textlength(tail, font=F(SANS, 15)), 160), tail,
           font=F(SANS, 15), fill=FAINT)

    # ---------------- lead: Zelensky calls four-way peace talks
    ly = 188
    d.text((36, ly), "KYIV — UKRAINE · THE TOP STORY", font=F(SANS_B, 17),
           fill=RED)
    d.text((36, ly + 24), "ZELENSKY CALLS FOR", font=F(SERIF_B, 46),
           fill=INK)
    d.text((36, ly + 76), "FOUR-WAY PEACE TALKS", font=F(SERIF_B, 46),
           fill=INK)
    d.text((36, ly + 130),
           "Kyiv ready to meet 'literally tomorrow' — partners "
           "target a deal before Christmas",
           font=F(SERIF, 21), fill=INK)
    peace_table(d, 36, ly + 164, 470, 214)
    tx = 530
    body = ("In a video address to NATO's parliament in Berlin, "
            "President Zelensky urged Ukraine, Russia, the United "
            "States and Europe to sit down together 'as soon as "
            "possible' to end the war. He also repeated Kyiv's call "
            "for NATO membership and for more air defence.")
    by = wrap(d, tx, ly + 168, body, F(SANS, 19), W - 36 - tx, gap=7)
    by += 16
    d.rectangle([tx, by, tx + 6, by + 52], fill=RED)
    d.text((tx + 18, by + 2), "“LITERALLY TOMORROW”",
           font=F(SANS_B, 19), fill=INK)
    d.text((tx + 18, by + 28), "— Kyiv on when it can meet",
           font=F(SANS, 16), fill=FAINT)

    hline(d, 584)

    # ---------------- two illustrated panels
    py = 600
    pw = (W - 72 - 20) // 2
    # panel 2 — Banten factory fire, Tuesday's identification update
    d.text((36, py), "2 · CIKANDE, BANTEN — INDONESIA",
           font=F(SANS_B, 15), fill=RED)
    d.text((36, py + 22), "26 IDENTIFIED,", font=F(SERIF_B, 30), fill=INK)
    d.text((36, py + 58), "28 STILL MISSING", font=F(SERIF_B, 30),
           fill=INK)
    factory_fire(d, 36, py + 100, 196, 140)
    wrap(d, 246, py + 102,
         "Tuesday's DVI update on Saturday's fire at the Milkita "
         "candy factory: 26 victims identified, 28 workers still "
         "missing of 31 reported, 3 confirmed safe. Families are "
         "giving DNA samples.",
         F(SANS, 16), 36 + pw - 246, gap=4)
    # panel 3 — Megaspeed joins the Entity List
    px = 36 + pw + 20
    d.text((px, py), "3 · WASHINGTON — TRADE & TECH", font=F(SANS_B, 15),
           fill=RED)
    d.text((px, py + 22), "US BLACKLISTS", font=F(SERIF_B, 30), fill=INK)
    d.text((px, py + 58), "CHIP SMUGGLER", font=F(SERIF_B, 30), fill=INK)
    stamp, spos = chip_stamp(d, px, py + 100, 196, 140)
    img.paste(stamp, spos, stamp)
    wrap(d, px + 210, py + 102,
         "The Bureau of Industry and Security listed Singapore's "
         "Megaspeed International, alleged hub of an Nvidia "
         "chip-smuggling scandal, plus six more Southeast Asian "
         "firms. US tech licences now required.",
         F(SANS, 16), 36 + 2 * pw + 20 - (px + 210), gap=4)

    hline(d, 856)

    # ---------------- also today: briefs 4-7
    ay = 868
    d.text((36, ay), "ALSO TODAY", font=F(SANS_B, 16), fill=RED)
    briefs = ("4 · BUSINESS — Five SpaceX & Tesla directors tasked "
              "with detailing a $3.5tn merger; talks only, no deal.   "
              "5 · DEFENCE — Pentagon has yet to approve some 60 "
              "Patriot interceptors for Ukraine.   6 · EUROPE — "
              "Poland: a Russian drone briefly entered its airspace.   "
              "7 · CHINA — Official surnamed Ma sentenced to death "
              "for spying for a foreign state.")
    wrap(d, 36, ay + 24, briefs, F(SANS, 15), W - 72, gap=4)

    hline(d, 958)

    # ---------------- footer: the day in numbers
    fy = 968
    d.text((36, fy), "THE DAY IN NUMBERS", font=F(SANS_B, 15), fill=RED)
    nums = ("4 parties, one table  ·  $3.5tn merger studied  ·  "
            "60 Patriots pending  ·  26 identified, 28 missing")
    nx = 36 + d.textlength("THE DAY IN NUMBERS  ", font=F(SANS_B, 15))
    d.text((nx, fy), nums, font=F(SANS, 15), fill=INK)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    build()
