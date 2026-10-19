#!/usr/bin/env python3
"""
scripts/generate_asset_textures.py
Generates rich, vibrant textures for:
  1. assets/textures/painting_landscape.png (Scenic mountain sunset canvas)
  2. assets/textures/painting_retro_milk.png (Pop-art stylized Dani milk canvas)
  3. assets/textures/tv_screen_retro.png (Retro CRT SMPTE color bars with scanlines)
  4. assets/textures/bookshelf_texture.png (Wood grain + colorful book bindings)
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont


def make_landscape_painting(filepath):
    w, h = 512, 384
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 1. Sunset Sky Gradient (Rich orange, pink, violet, deep indigo)
    for y in range(h):
        t = y / float(h)
        if t < 0.35:
            # Deep purple to warm coral
            f = t / 0.35
            r = int(55 + f * 190)
            g = int(35 + f * 90)
            b = int(95 + f * 20)
        elif t < 0.65:
            # Coral to golden sunset yellow
            f = (t - 0.35) / 0.30
            r = int(245 + f * 10)
            g = int(125 + f * 95)
            b = int(115 - f * 85)
        else:
            # Golden horizon glow
            f = (t - 0.65) / 0.35
            r = int(255 - f * 25)
            g = int(220 - f * 50)
            b = int(30 + f * 40)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Glowing Sun on horizon
    sun_cx, sun_cy = w // 2, int(h * 0.58)
    for r in range(48, 0, -2):
        alpha = int(255 - (r / 48.0) * 120)
        draw.ellipse((sun_cx - r, sun_cy - r, sun_cx + r, sun_cy + r), fill=(255, 245, 180))

    # 2. Distant Low-Poly Mountain Range (Deep violet silhouettes)
    mtn_pts1 = [(0, h * 0.65)]
    peaks1 = [
        (0, 0.65), (70, 0.44), (130, 0.52), (190, 0.38), (260, 0.50),
        (330, 0.36), (410, 0.48), (470, 0.42), (w, 0.62), (w, h), (0, h)
    ]
    poly1 = [(int(p[0]), int(p[1] * h)) for p in peaks1]
    draw.polygon(poly1, fill=(75, 45, 95))

    # 3. Near Mountain Ridge (Darker indigo/slate)
    peaks2 = [
        (0, 0.72), (90, 0.58), (170, 0.66), (240, 0.52), (320, 0.64),
        (400, 0.54), (460, 0.62), (w, 0.70), (w, h), (0, h)
    ]
    poly2 = [(int(p[0]), int(p[1] * h)) for p in peaks2]
    draw.polygon(poly2, fill=(42, 28, 62))

    # 4. Mirror Lake / Water (Lower quarter)
    water_y = int(h * 0.72)
    for y in range(water_y, h):
        t = (y - water_y) / float(h - water_y)
        r = int(45 + t * 20)
        g = int(55 + t * 45)
        b = int(95 + t * 50)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Water reflections & ripples
    for y in range(water_y + 4, h, 6):
        width_jitter = random.randint(30, 160)
        cx = sun_cx + random.randint(-20, 20)
        draw.line([(cx - width_jitter, y), (cx + width_jitter, y)], fill=(240, 180, 100), width=2)

    # 5. Pine Tree Silhouettes on Forefront Shore
    for tx in [25, 45, 75, 120, 380, 420, 455, 485]:
        th = random.randint(45, 80)
        by = int(h * 0.88 + random.randint(-8, 8))
        # Pine layers
        draw.polygon([(tx, by - th), (tx - 14, by - th // 2), (tx + 14, by - th // 2)], fill=(22, 18, 32))
        draw.polygon([(tx, by - th * 2 // 3), (tx - 18, by - th // 4), (tx + 18, by - th // 4)], fill=(22, 18, 32))
        draw.polygon([(tx, by - th // 3), (tx - 22, by), (tx + 22, by)], fill=(18, 14, 26))

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"[OK] Wrote landscape painting: {filepath}")


def make_milk_painting(filepath):
    w, h = 512, 384
    img = Image.new("RGB", (w, h), (40, 150, 230)) # Vibrant Dani Cyan background
    draw = ImageDraw.Draw(img)

    # 1. Retro Starburst Sunray Background
    cx, cy = w // 2, h // 2
    num_rays = 20
    for i in range(num_rays):
        if i % 2 == 0:
            ang1 = (2.0 * math.pi * i) / num_rays
            ang2 = (2.0 * math.pi * (i + 1)) / num_rays
            rad = 450
            p1 = (cx, cy)
            p2 = (int(cx + math.cos(ang1) * rad), int(cy + math.sin(ang1) * rad))
            p3 = (int(cx + math.cos(ang2) * rad), int(cy + math.sin(ang2) * rad))
            draw.polygon([p1, p2, p3], fill=(70, 180, 245))

    # Vignette border
    draw.rectangle((0, 0, w - 1, h - 1), outline=(25, 110, 180), width=6)

    # 2. Stylized Milk Carton (Chunky cartoon style)
    # Carton Body
    carton_x, carton_y = cx - 65, cy - 80
    cw, ch = 130, 160
    # Shadow
    draw.ellipse((cx - 85, carton_y + ch - 10, cx + 85, carton_y + ch + 35), fill=(25, 95, 160))
    # Main White Body
    draw.rectangle((carton_x, carton_y, carton_x + cw, carton_y + ch), fill=(245, 245, 250), outline=(30, 40, 50), width=5)
    # Blue lower band
    draw.rectangle((carton_x, carton_y + ch - 50, carton_x + cw, carton_y + ch), fill=(35, 120, 220), outline=(30, 40, 50), width=4)
    # Gabled carton top
    roof_pts = [
        (carton_x, carton_y),
        (carton_x + cw // 2, carton_y - 45),
        (carton_x + cw, carton_y)
    ]
    draw.polygon(roof_pts, fill=(235, 235, 242), outline=(30, 40, 50), width=5)
    # Carton fin spout
    fin_pts = [
        (carton_x + cw // 2 - 25, carton_y - 45),
        (carton_x + cw // 2 - 25, carton_y - 65),
        (carton_x + cw // 2 + 25, carton_y - 65),
        (carton_x + cw // 2 + 25, carton_y - 45)
    ]
    draw.polygon(fin_pts, fill=(215, 215, 225), outline=(30, 40, 50), width=4)

    # Cartoon "MILK" text on carton
    draw.rectangle((carton_x + 15, carton_y + 35, carton_x + cw - 15, carton_y + 80), fill=(225, 45, 45))
    # Milk droplets & splash stars
    for dx, dy in [(-90, -40), (100, -30), (-80, 60), (95, 70), (0, -110)]:
        draw.ellipse((cx + dx - 8, cy + dy - 8, cx + dx + 8, cy + dy + 8), fill=(255, 255, 255), outline=(30, 40, 50), width=2)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"[OK] Wrote milk painting: {filepath}")


def make_tv_screen(filepath):
    w, h = 512, 384
    img = Image.new("RGB", (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. SMPTE Standard Color Bars
    # Top 70% of screen: 7 vertical bars (White, Yellow, Cyan, Green, Magenta, Red, Blue)
    colors = [
        (205, 205, 205), # White
        (205, 205, 30),  # Yellow
        (30, 205, 205),  # Cyan
        (30, 205, 30),   # Green
        (205, 30, 205),  # Magenta
        (205, 30, 30),   # Red
        (30, 30, 205)    # Blue
    ]
    bar_w = w / float(len(colors))
    top_h = int(h * 0.70)
    for i, c in enumerate(colors):
        x0 = int(i * bar_w)
        x1 = int((i + 1) * bar_w)
        draw.rectangle((x0, 0, x1, top_h), fill=c)

    # Middle 10%: cast bars (Blue, Black, Magenta, Black, Cyan, Black, White)
    mid_colors = [
        (30, 30, 205), (15, 15, 15), (205, 30, 205),
        (15, 15, 15), (30, 205, 205), (15, 15, 15), (205, 205, 205)
    ]
    mid_h = int(h * 0.80)
    for i, c in enumerate(mid_colors):
        x0 = int(i * bar_w)
        x1 = int((i + 1) * bar_w)
        draw.rectangle((x0, top_h, x1, mid_h), fill=c)

    # Bottom 20%: Pluge pulse / black blocks
    draw.rectangle((0, mid_h, int(w * 0.18), h), fill=(10, 40, 75))
    draw.rectangle((int(w * 0.18), mid_h, int(w * 0.36), h), fill=(245, 245, 245))
    draw.rectangle((int(w * 0.36), mid_h, int(w * 0.54), h), fill=(45, 15, 65))
    draw.rectangle((int(w * 0.54), mid_h, w, h), fill=(18, 18, 18))

    # 2. Glowing "NO SIGNAL" / MOPMENTUM TV Broadcast Banner
    draw.rectangle((w // 2 - 130, top_h // 2 - 25, w // 2 + 130, top_h // 2 + 25), fill=(10, 10, 15), outline=(255, 255, 255), width=3)
    # Inner accent border
    draw.rectangle((w // 2 - 124, top_h // 2 - 20, w // 2 + 124, top_h // 2 + 20), outline=(240, 200, 30), width=2)

    # 3. CRT Phosphor Scanlines
    for y in range(0, h, 3):
        draw.line([(0, y), (w, y)], fill=(0, 0, 0))

    # Curved CRT Glass Bezel Vignette
    draw.rectangle((0, 0, w, h), outline=(10, 10, 12), width=10)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"[OK] Wrote retro TV screen: {filepath}")


def make_bookshelf_wood_texture(filepath):
    # Rich warm wood texture with subtle grain and golden highlights
    w, h = 512, 512
    img = Image.new("RGB", (w, h), (115, 70, 38))
    draw = ImageDraw.Draw(img)

    for y in range(h):
        grain = math.sin(y * 0.18) * 12 + math.sin(y * 0.05) * 8
        r = int(clamp(115 + grain + random.randint(-3, 3), 0, 255))
        g = int(clamp(70 + grain * 0.7 + random.randint(-2, 2), 0, 255))
        b = int(clamp(38 + grain * 0.4 + random.randint(-2, 2), 0, 255))
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Add dark wood planks & joins
    for py in [128, 256, 384]:
        draw.line([(0, py), (w, py)], fill=(65, 38, 20), width=3)
        draw.line([(0, py + 1), (w, py + 1)], fill=(145, 95, 55), width=1)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"[OK] Wrote wood texture: {filepath}")


def clamp(val, low, high):
    return max(low, min(val, high))


if __name__ == "__main__":
    out_dir = "assets/textures"
    make_landscape_painting(f"{out_dir}/painting_landscape.png")
    make_milk_painting(f"{out_dir}/painting_retro_milk.png")
    make_tv_screen(f"{out_dir}/tv_screen_retro.png")
    make_bookshelf_wood_texture(f"{out_dir}/wood_warm_grain.png")
    print("[SUCCESS] All asset textures generated successfully!")
