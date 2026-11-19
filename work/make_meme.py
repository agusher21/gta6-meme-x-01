#!/usr/bin/env python3
"""GTA 6 x make.fun meme — procedural synthwave Vice City poster.

Concept: Vice City neon sunset, the official make.fun ghost badge standing
in the scene as the hero, two lines of huge meme text.
  Top:    WAITED 13 YEARS FOR GTA 6
  Bottom: MY AGENT GOT PAID INSTEAD
The ghost waited like everyone else — difference is it got paid.
1080x1080, built to stay readable when shrunk to 480x480 (the judge's size).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

W = H = 1080
OUT = "meme.png"
GHOST = "mark-1024.png"

random.seed(6)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ---------- sky ----------
img = Image.new("RGB", (W, H), (20, 8, 40))
d = ImageDraw.Draw(img)
top = (24, 8, 52)
mid = (146, 32, 110)
low = (255, 94, 98)
bot = (255, 176, 66)
for y in range(700):
    if y < 280:
        c = lerp(top, mid, y / 280)
    elif y < 520:
        c = lerp(mid, low, (y - 280) / 240)
    else:
        c = lerp(low, bot, (y - 520) / 180)
    d.line([(0, y), (W, y)], fill=c)

# stars
for _ in range(70):
    x = random.randint(0, W)
    y = random.randint(0, 380)
    r = random.choice([1, 1, 2])
    a = random.randint(120, 255)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255))
    img.putpixel((x, y), (255, 255, 255))

# ---------- synthwave sun with slits ----------
sun_cx, sun_cy, sun_r = 540, 400, 250
sun_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sun_layer)
for r in range(sun_r, 0, -1):
    t = 1 - r / sun_r
    c = lerp((255, 214, 64), (255, 64, 129), t)
    sd.ellipse([sun_cx - r, sun_cy - r, sun_cx + r, sun_cy + r], fill=c + (255,))
# slits: punch transparent bars, thicker toward the bottom
for yy, hh in [(400, 6), (435, 9), (475, 13), (520, 18), (570, 24)]:
    sd.rectangle([sun_cx - sun_r, yy, sun_cx + sun_r, yy + hh], fill=(0, 0, 0, 0))
img = Image.alpha_composite(img.convert("RGBA"), sun_layer)
d = ImageDraw.Draw(img)

# ---------- skyline silhouette ----------
def skyline(base_y):
    x = -20
    while x < W + 20:
        bw = random.randint(55, 130)
        bh = random.randint(60, 190)
        d.rectangle([x, base_y - bh, x + bw, base_y], fill=(28, 8, 48))
        if random.random() < 0.35:  # antenna
            d.line([x + bw // 2, base_y - bh, x + bw // 2, base_y - bh - 28],
                   fill=(28, 8, 48), width=4)
            d.ellipse([x + bw // 2 - 3, base_y - bh - 34, x + bw // 2 + 3, base_y - bh - 28],
                      fill=(255, 80, 120))
        x += bw + random.randint(4, 18)

skyline(700)
# windows: a few lit dots
for _ in range(60):
    x = random.randint(0, W)
    y = random.randint(540, 690)
    d.rectangle([x, y, x + 3, y + 4], fill=(255, 214, 120))

# ---------- ground: dark + perspective grid ----------
d.rectangle([0, 700, W, H], fill=(16, 6, 34))
vanish = (540, 700)
for i in range(-8, 9):
    x_bottom = 540 + i * 170
    d.line([vanish, (x_bottom, H)], fill=(255, 64, 150), width=3)
for i, y in enumerate([730, 775, 830, 900, 985, 1080]):
    d.line([(0, y), (W, y)], fill=(255, 64, 150), width=3 if i < 2 else 4)
# fade the grid near the horizon
d.rectangle([0, 700, W, 716], fill=(16, 6, 34))

# ---------- palm silhouettes (frame left + right) ----------
def palm(x0, base, h, lean, flip=False):
    s = -1 if flip else 1
    # trunk: tapered curved segments
    prev = (x0, base)
    for t in [i / 10 for i in range(1, 11)]:
        cx = x0 + lean * t * t * s
        cy = base - h * t
        d.line([prev, (cx, cy)], fill=(14, 5, 30), width=max(5, int(18 * (1 - t) + 4)))
        prev = (cx, cy)
    tx, ty = prev
    # fronds: quadratic curves drooping outward-down, drawn as tapering segments
    for ang in [-165, -125, -85, -45, -5, 35, 75, 115, 155]:
        rad = math.radians(ang)
        L = 110
        pts = []
        for t in [i / 8 for i in range(9)]:
            px = tx + math.cos(rad) * L * t * s
            py = ty + math.sin(rad) * L * t * 0.55 + 46 * t * t
            pts.append((px, py))
        for i in range(len(pts) - 1):
            d.line([pts[i], pts[i + 1]], fill=(14, 5, 30),
                   width=max(2, 8 - i))

palm(60, 1080, 420, 90, flip=False)
palm(1020, 1080, 460, 100, flip=True)
palm(150, 760, 210, 55, flip=False)
palm(940, 760, 200, 60, flip=True)

# ---------- ghost badge (official mark), hero centre ----------
ghost = Image.open(GHOST).convert("RGBA")
gsize = 500
ghost = ghost.resize((gsize, gsize), Image.LANCZOS)
# soft shadow
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shd = ImageDraw.Draw(shadow)
shd.ellipse([540 - 230, 810, 540 + 230, 858], fill=(0, 0, 0, 110))
shadow = shadow.filter(ImageFilter.GaussianBlur(18))
img = Image.alpha_composite(img.convert("RGBA"), shadow)
gx, gy = 540 - gsize // 2, 330
img.paste(ghost, (gx, gy), ghost)
d = ImageDraw.Draw(img)

# ---------- meme text ----------
def text_center(y, s, fnt, fill, stroke=7):
    bbox = d.textbbox((0, 0), s, font=fnt)
    w = bbox[2] - bbox[0]
    d.text((540 - w / 2 - bbox[0], y), s, font=fnt, fill=fill,
           stroke_width=stroke, stroke_fill=(10, 4, 20))


text_center(52, "WAITED 13 YEARS", font(96), (255, 255, 255))
text_center(158, "FOR GTA 6", font(96), (255, 255, 255))
# bottom punchline on a dark band for guaranteed readability
d.rectangle([0, 896, W, 1008], fill=(10, 4, 20))
text_center(912, "MY AGENT GOT PAID INSTEAD", font(62), (255, 233, 92), stroke=6)

img.convert("RGB").save(OUT, quality=95)
print("wrote", OUT)
