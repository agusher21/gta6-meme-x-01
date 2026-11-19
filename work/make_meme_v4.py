#!/usr/bin/env python3
"""Meme v4 — 'MISSION PASSED' concept (unique, colourful, GTA 6 theme).
Vice City sunset scene, official make.fun ghost badge centre,
GTA-style MISSION PASSED headline, reward lines in a bottom band.
Square 1080x1080 (judge sees it at 480x480).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, math

W = H = 1080
random.seed(6)
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# ---------- sky gradient: indigo -> purple -> magenta -> orange -> gold
stops = [(0, (26, 11, 46)), (0.30, (88, 28, 135)), (0.52, (199, 44, 120)),
         (0.72, (255, 110, 80)), (0.88, (255, 183, 110)), (1.0, (255, 214, 140))]
def grad(y):
    t = y / H
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]; t1, c1 = stops[i + 1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0)
            return tuple(int(c0[k] + (c1[k] - c0[k]) * f) for k in range(3))
    return stops[-1][1]

for y in range(H):
    d.line([(0, y), (W, y)], fill=grad(y))

# ---------- sun (striped synthwave sun) centred (540, 380), r 150
sun_cx, sun_cy, sun_r = 540, 380, 150
sun = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sun)
for r in range(sun_r, 0, -1):
    f = r / sun_r
    col = (255, int(190 + 65 * f), int(90 + 100 * f), 255)
    sd.ellipse([sun_cx - r, sun_cy - r, sun_cx + r, sun_cy + r], fill=col)
# horizontal slits, thicker toward the bottom of the sun
for i, (sy, th) in enumerate([(400, 4), (425, 6), (452, 8), (480, 10), (508, 12)]):
    sd.rectangle([sun_cx - sun_r - 5, sy, sun_cx + sun_r + 5, sy + th],
                 fill=(26, 11, 46, 255))
img = Image.alpha_composite(img.convert("RGBA"), sun)
d = ImageDraw.Draw(img)

# ---------- stars in the upper sky
for _ in range(70):
    x = random.randint(0, W); y = random.randint(0, 260)
    r = random.choice([1, 1, 2])
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 200))

# ---------- skyline silhouette (horizon ~y 640), neon windows
HORIZON = 640
buildings = []
x = -20
while x < W + 20:
    bw = random.randint(60, 130)
    bh = random.randint(90, 260)
    buildings.append((x, HORIZON - bh, x + bw, HORIZON))
    x += bw + random.randint(4, 18)
for (x0, y0, x1, y1) in buildings:
    d.rectangle([x0, y0, x1, y1], fill=(24, 8, 44, 255))
    # neon windows
    for wy in range(y0 + 14, y1 - 12, 22):
        for wx in range(x0 + 10, x1 - 10, 20):
            if random.random() < 0.4:
                col = random.choice([(255, 80, 180), (80, 230, 255),
                                     (255, 220, 90), (255, 255, 255)])
                d.rectangle([wx, wy, wx + 8, wy + 12], fill=col + (255,))

# ---------- ocean with sun reflection (y 640-1080)
for y in range(HORIZON, H):
    f = (y - HORIZON) / (H - HORIZON)
    base = (int(40 + 60 * f), int(16 + 30 * f), int(70 + 40 * f))
    d.line([(0, y), (W, y)], fill=base + (255,))
for _ in range(260):
    y = random.randint(HORIZON + 8, H - 10)
    spread = 40 + (y - HORIZON) * 0.55
    x = int(540 + random.gauss(0, spread))
    ln = random.randint(14, 60)
    col = random.choice([(255, 170, 90), (255, 120, 140), (255, 210, 130)])
    d.line([(x, y), (x + ln, y)], fill=col + (200,), width=3)

# ---------- palm silhouettes (left + right)
def palm(cx, base_y, s, lean):
    pts = []
    top_x, top_y = cx + lean, base_y - int(300 * s)
    d.line([(cx, base_y), (top_x, top_y)], fill=(18, 6, 34, 255), width=int(16 * s))
    for k in range(7):
        ang = math.radians(-160 + k * 32)
        L = int(150 * s * random.uniform(0.85, 1.1))
        ex = top_x + int(math.cos(ang) * L)
        ey = top_y + int(math.sin(ang) * L * 0.45) + int(46 * s)
        # curved frond: two segments
        mx = top_x + int(math.cos(ang) * L * 0.55)
        my = top_y + int(math.sin(ang) * L * 0.55 * 0.45) + int(10 * s)
        d.line([(top_x, top_y), (mx, my), (ex, ey)], fill=(18, 6, 34, 255),
               width=int(11 * s))
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(18, 6, 34, 255))
    d.ellipse([top_x - 12, top_y - 12, top_x + 12, top_y + 12], fill=(18, 6, 34, 255))

palm(60, 700, 1.15, 50)
palm(1030, 720, 1.25, -60)
palm(200, 760, 0.8, 30)
palm(900, 770, 0.85, -35)

# ---------- ghost badge (official mark) centre, with glow + shadow
mark = Image.open("mark-1024.png").convert("RGBA")
GS = 380
ghost = mark.resize((GS, GS), Image.LANCZOS)
gx, gy = (W - GS) // 2, 520
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([gx - 30, gy - 30, gx + GS + 30, gy + GS + 30], fill=(255, 60, 160, 90))
glow = glow.filter(ImageFilter.GaussianBlur(35))
img = Image.alpha_composite(img, glow)
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd2 = ImageDraw.Draw(sh)
sd2.ellipse([gx + 40, gy + GS - 22, gx + GS - 40, gy + GS + 18], fill=(0, 0, 0, 130))
sh = sh.filter(ImageFilter.GaussianBlur(12))
img = Image.alpha_composite(img, sh)
img.paste(ghost, (gx, gy), ghost)
d = ImageDraw.Draw(img)

# ---------- bottom band (translucent) + reward lines
band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(band)
bd.rectangle([0, 936, W, H], fill=(8, 2, 18, 185))
img = Image.alpha_composite(img, band)
d = ImageDraw.Draw(img)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def text_center(y, s, size, fill, stroke=8, stroke_fill=(8, 2, 18)):
    f = ImageFont.truetype(FONT, size)
    bbox = d.textbbox((0, 0), s, font=f)
    w = bbox[2] - bbox[0]
    d.text((W // 2 - w / 2 - bbox[0], y), s, font=f, fill=fill,
           stroke_width=stroke, stroke_fill=stroke_fill)

text_center(52, "MISSION PASSED", 108, (255, 255, 255), stroke=10)
text_center(948, "WAITED 13 YEARS FOR GTA 6", 44, (255, 255, 255), stroke=6)
text_center(1002, "+$100  MY AGENT GOT PAID INSTEAD", 44, (255, 217, 77), stroke=6)

img.convert("RGB").save("meme.png", quality=95)
img.convert("RGB").resize((480, 480), Image.LANCZOS).save("meme-480.png")
print("saved meme.png + meme-480.png")
