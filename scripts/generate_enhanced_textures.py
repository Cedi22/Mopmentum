#!/usr/bin/env python3
"""
scripts/generate_enhanced_textures.py
Generates high-resolution transparent textures for dirt, grime, mud, liquids,
and clean tool badge icons in assets/textures/.
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter

SIZE = 512
CENTER = SIZE // 2

def make_mud_texture(filepath):
    random.seed(42)
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Base organic mud puddle
    for _ in range(25):
        ang = random.uniform(0, math.tau)
        dist = random.uniform(0, 110)
        rx = random.randint(55, 120)
        ry = random.randint(45, 110)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        shade = random.randint(50, 75)
        draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(shade, int(shade * 0.65), int(shade * 0.35), 235))

    # Darker wet inner mud core
    for _ in range(16):
        ang = random.uniform(0, math.tau)
        dist = random.uniform(0, 60)
        r = random.randint(35, 75)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(38, 22, 12, 245))

    # Wet gloss / sheen highlights
    for _ in range(10):
        ang = random.uniform(0, math.tau)
        dist = random.uniform(10, 50)
        r = random.randint(12, 28)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        draw.ellipse((cx - r, cy - r * 0.6, cx + r, cy + r * 0.6), fill=(110, 75, 45, 180))

    # Satellite splatter droplets
    for _ in range(50):
        ang = random.uniform(0, math.tau)
        dist = random.uniform(120, 235)
        r = random.randint(4, 18)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(48, 28, 14, 230))

    img = img.filter(ImageFilter.GaussianBlur(1.2))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"[OK] Wrote mud texture: {filepath}")


def make_liquid_texture(filepath):
    random.seed(99)
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer liquid tension ring (coffee / soda / juice puddle)
    for i in range(72):
        ang = (math.tau * i) / 72.0
        jitter = random.uniform(-12, 12)
        rad = 170 + math.sin(ang * 6) * 22 + jitter
        cx = int(CENTER + math.cos(ang) * rad * 0.45)
        cy = int(CENTER + math.sin(ang) * rad * 0.45)
        r = int(rad * 0.6)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(70, 35, 15, 180))

    # Smooth translucent body
    for _ in range(12):
        ang = random.uniform(0, math.tau)
        dist = random.uniform(0, 50)
        r = random.randint(90, 140)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(120, 60, 25, 160))

    # Specular glossy reflections
    draw.arc((CENTER - 110, CENTER - 90, CENTER + 90, CENTER + 100), 200, 310, fill=(255, 235, 200, 190), width=6)
    draw.arc((CENTER - 70, CENTER - 60, CENTER + 60, CENTER + 70), 210, 290, fill=(255, 245, 220, 160), width=4)

    # Stray drops
    for _ in range(30):
        ang = random.uniform(0, math.tau)
        dist = random.uniform(140, 230)
        r = random.randint(4, 15)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(95, 45, 20, 210))

    img = img.filter(ImageFilter.GaussianBlur(1.0))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"[OK] Wrote liquid texture: {filepath}")


def make_grime_stain_texture(filepath):
    random.seed(123)
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Stubborn kitchen grease & wine grime crust
    for _ in range(35):
        ang = random.uniform(0, math.tau)
        dist = random.uniform(0, 120)
        rx = random.randint(40, 100)
        ry = random.randint(30, 85)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        # Deep magenta/grease crust
        draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(80, 20, 35, 210))

    for _ in range(20):
        ang = random.uniform(0, math.tau)
        dist = random.uniform(0, 60)
        r = random.randint(30, 70)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(50, 12, 22, 235))

    # Oily greasy film sheen
    for _ in range(15):
        ang = random.uniform(0, math.tau)
        dist = random.uniform(10, 80)
        r = random.randint(20, 45)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(140, 85, 40, 95))

    img = img.filter(ImageFilter.GaussianBlur(1.5))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"[OK] Wrote grime stain texture: {filepath}")


def make_dust_cluster_texture(filepath):
    random.seed(333)
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Soft fluffy dust bunny base
    for _ in range(40):
        ang = random.uniform(0, math.tau)
        dist = random.uniform(0, 130)
        r = random.randint(45, 95)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        grey = random.randint(130, 175)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(grey, grey, grey + 5, 120))

    # Dense dust core
    for _ in range(25):
        ang = random.uniform(0, math.tau)
        dist = random.uniform(0, 70)
        r = random.randint(30, 65)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        grey = random.randint(95, 135)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(grey, grey, grey + 8, 175))

    # Wispy lint fiber streaks
    for _ in range(45):
        ang = random.uniform(0, math.tau)
        dist = random.uniform(40, 180)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        ex = cx + random.randint(-40, 40)
        ey = cy + random.randint(-40, 40)
        draw.line((cx, cy, ex, ey), fill=(185, 185, 190, 160), width=random.randint(1, 3))

    img = img.filter(ImageFilter.GaussianBlur(2.0))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"[OK] Wrote dust cluster texture: {filepath}")


def make_tool_badge(filepath, tool_name, bg_color, symbol_char):
    # Circular 256x256 UI badge
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    c = size // 2

    # Drop shadow
    draw.ellipse((c - 105, c - 95, c + 105, c + 115), fill=(0, 0, 0, 80))

    # Outer metallic rim
    draw.ellipse((c - 110, c - 110, c + 110, c + 110), fill=(245, 245, 250, 255))
    draw.ellipse((c - 102, c - 102, c + 102, c + 102), fill=(30, 32, 40, 255))

    # Colored inner field
    draw.ellipse((c - 94, c - 94, c + 94, c + 94), fill=bg_color)

    # Gloss shine arc
    draw.arc((c - 84, c - 84, c + 84, c + 84), 210, 330, fill=(255, 255, 255, 160), width=6)

    # Tool specific graphic icon
    if tool_name == "mop":
        # Draw stylized mop: handle line and mop head yarn
        draw.line((c + 35, c - 60, c - 15, c + 20), fill=(210, 180, 140, 255), width=10) # handle
        draw.line((c + 30, c - 65, c + 40, c - 55), fill=(230, 80, 40, 255), width=12)  # grip
        draw.rectangle((c - 40, c + 18, c + 10, c + 32), fill=(70, 70, 85, 255))         # clamp
        # Yarn strands
        for sx in range(c - 45, c + 15, 6):
            draw.line((sx, c + 32, sx - 8, c + 70), fill=(240, 240, 250, 255), width=4)
    elif tool_name == "broom":
        # Draw stylized broom: handle and straw bristles
        draw.line((c + 35, c - 60, c - 10, c + 15), fill=(180, 130, 80, 255), width=10)
        draw.polygon([(c - 15, c + 15), (c - 5, c + 15), (c + 25, c + 70), (c - 55, c + 70)], fill=(225, 195, 80, 255))
        draw.line((c - 30, c + 35, c + 10, c + 35), fill=(180, 40, 30, 255), width=5) # twine band
    elif tool_name == "sponge":
        # Draw bubbly yellow rectangular sponge with rounded corners
        draw.rounded_rectangle((c - 55, c - 35, c + 55, c + 35), radius=15, fill=(250, 215, 50, 255), outline=(220, 180, 30, 255), width=4)
        # Sponge holes
        holes = [(-30, -12, 8), (15, -15, 10), (-10, 10, 9), (32, 12, 7), (-35, 15, 6), (5, -5, 5)]
        for hx, hy, hr in holes:
            draw.ellipse((c + hx - hr, c + hy - hr, c + hx + hr, c + hy + hr), fill=(205, 170, 25, 255))
    elif tool_name == "spray":
        # Draw spray bottle
        draw.rounded_rectangle((c - 35, c - 10, c + 35, c + 65), radius=10, fill=(60, 160, 240, 255)) # bottle body
        draw.rectangle((c - 18, c - 30, c + 18, c - 10), fill=(230, 235, 245, 255)) # bottle neck
        # Trigger head
        draw.polygon([(c - 20, c - 50), (c + 30, c - 50), (c + 20, c - 30), (c - 20, c - 30)], fill=(230, 235, 245, 255))
        draw.rectangle((c - 35, c - 46, c - 18, c - 34), fill=(240, 70, 60, 255)) # nozzle tip
        draw.line((c - 15, c - 30, c - 22, c - 12), fill=(200, 205, 215, 255), width=6) # trigger lever

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"[OK] Wrote badge: {filepath}")


def make_table_coffee_ring_texture(filepath):
    random.seed(777)
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Thick, unmistakable dried coffee mug rings & sticky syrup spill
    ring_cx, ring_cy = CENTER - 25, CENTER - 15
    r = 95
    # Inner dark sticky coffee puddle wash
    for _ in range(18):
        ang = random.uniform(0, math.tau)
        dist = random.uniform(0, 65)
        rx = random.randint(30, 65)
        ry = random.randint(25, 55)
        cx = int(ring_cx + math.cos(ang) * dist)
        cy = int(ring_cy + math.sin(ang) * dist)
        draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(55, 24, 8, 175))

    # Darkest coffee core
    draw.ellipse((ring_cx - 45, ring_cy - 40, ring_cx + 45, ring_cy + 40), fill=(40, 16, 5, 230))

    # Primary thick capillary mug ring (bold, dark brown)
    for i in range(160):
        ang0 = (math.tau * i) / 160.0
        ang1 = (math.tau * (i + 1)) / 160.0
        jitter = random.uniform(-4, 4)
        w = random.randint(14, 24)
        draw.line([
            (ring_cx + math.cos(ang0) * (r + jitter), ring_cy + math.sin(ang0) * (r + jitter)),
            (ring_cx + math.cos(ang1) * (r + jitter), ring_cy + math.sin(ang1) * (r + jitter))
        ], fill=(32, 12, 4, 245), width=w)

    # Second overlapping mug ring
    r2_cx, r2_cy = CENTER + 55, CENTER + 35
    r2 = 80
    for _ in range(12):
        rx = random.randint(25, 50)
        draw.ellipse((r2_cx - rx, r2_cy - rx, r2_cx + rx, r2_cy + rx), fill=(50, 20, 6, 160))
    for i in range(120):
        ang0 = (math.tau * i) / 120.0
        ang1 = (math.tau * (i + 1)) / 120.0
        jitter = random.uniform(-3, 3)
        w = random.randint(12, 20)
        draw.line([
            (r2_cx + math.cos(ang0) * (r2 + jitter), r2_cy + math.sin(ang0) * (r2 + jitter)),
            (r2_cx + math.cos(ang1) * (r2 + jitter), r2_cy + math.sin(ang1) * (r2 + jitter))
        ], fill=(36, 15, 5, 240), width=w)

    # Dripping splatter droplets & sticky syrup streaks
    for _ in range(45):
        ang = random.uniform(0, math.tau)
        dist = random.uniform(60, 210)
        dr = random.randint(6, 18)
        dx = int(ring_cx + math.cos(ang) * dist)
        dy = int(ring_cy + math.sin(ang) * dist)
        draw.ellipse((dx - dr, dy - dr, dx + dr, dy + dr), fill=(42, 16, 5, 235))

    # Glossy dried coffee highlights
    draw.arc((ring_cx - 65, ring_cy - 65, ring_cx + 45, ring_cy + 45), 210, 310, fill=(185, 125, 75, 170), width=4)

    img = img.filter(ImageFilter.GaussianBlur(0.8))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"[OK] Wrote bold table coffee ring texture: {filepath}")


if __name__ == "__main__":
    out_dir = "assets/textures"
    make_mud_texture(f"{out_dir}/dirt_mud_splat.png")
    make_liquid_texture(f"{out_dir}/dirt_coffee_spill.png")
    make_grime_stain_texture(f"{out_dir}/dirt_stain_grime.png")
    make_table_coffee_ring_texture(f"{out_dir}/dirt_table_grime.png")
    make_dust_cluster_texture(f"{out_dir}/dirt_dust_cluster.png")
    
    # Tool badges
    make_tool_badge(f"{out_dir}/badge_mop.png", "mop", (35, 115, 235, 240), "M")
    make_tool_badge(f"{out_dir}/badge_broom.png", "broom", (210, 130, 40, 240), "B")
    make_tool_badge(f"{out_dir}/badge_sponge.png", "sponge", (230, 185, 30, 240), "S")
    make_tool_badge(f"{out_dir}/badge_spray.png", "spray", (40, 195, 175, 240), "P")
    print("All textures and badges generated successfully!")
