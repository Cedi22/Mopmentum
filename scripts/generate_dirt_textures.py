#!/usr/bin/env python3
"""
scripts/generate_dirt_textures.py
Generates 512x512 transparent cartoon PNG decals in assets/textures/:
  1. assets/textures/dirt_mud_splat.png
  2. assets/textures/dirt_coffee_spill.png
  3. assets/textures/dirt_soap_suds.png
  4. assets/textures/dirt_dust_cluster.png
Requires: pip install Pillow
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter

SIZE = 512
CENTER = SIZE // 2

def make_mud_splat(filepath):
    rng = random.Random(101)
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Organic main mud puddle lobes
    for _ in range(18):
        ang = rng.uniform(0, math.tau)
        dist = rng.uniform(0, 95)
        rx = rng.randint(45, 95)
        ry = rng.randint(40, 90)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(76, 46, 22, 255))

    # Darker inner wet mud core
    for _ in range(10):
        ang = rng.uniform(0, math.tau)
        dist = rng.uniform(0, 55)
        r = rng.randint(30, 65)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(54, 32, 14, 255))

    # Radial satellite splatter droplets
    for _ in range(42):
        ang = rng.uniform(0, math.tau)
        dist = rng.uniform(115, 225)
        r = rng.randint(6, 24)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(68, 40, 18, 255))

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"[OK] Wrote {filepath}")


def make_coffee_spill(filepath):
    rng = random.Random(202)
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer dark dry coffee ring
    for i in range(60):
        ang = (math.tau * i) / 60.0
        jitter = rng.uniform(-14, 14)
        rad = 155 + math.sin(ang * 5) * 18 + jitter
        cx = int(CENTER + math.cos(ang) * rad * 0.4)
        cy = int(CENTER + math.sin(ang) * rad * 0.4)
        r = int(rad * 0.65)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(58, 30, 12, 220))

    # Lighter translucent amber coffee interior
    draw.ellipse((CENTER - 135, CENTER - 125, CENTER + 140, CENTER + 130), fill=(115, 68, 32, 155))

    # Side cup splash droplets
    for _ in range(25):
        ang = rng.uniform(-0.8, 1.4)
        dist = rng.uniform(155, 235)
        r = rng.randint(5, 18)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(72, 38, 16, 215))

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"[OK] Wrote {filepath}")


def make_soap_suds(filepath):
    rng = random.Random(303)
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Translucent foam bed
    for _ in range(20):
        ang = rng.uniform(0, math.tau)
        dist = rng.uniform(0, 110)
        r = rng.randint(45, 90)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(225, 248, 255, 140))

    # Individual cartoon bubbles with iridescent cyan/pink rims and specular dots
    for _ in range(65):
        ang = rng.uniform(0, math.tau)
        dist = rng.uniform(0, 195)
        r = rng.randint(10, 42)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)

        rim_col = (160, 235, 255, 235) if rng.random() > 0.35 else (255, 205, 245, 235)
        draw.ellipse(
            (cx - r, cy - r, cx + r, cy + r),
            fill=(240, 252, 255, 165),
            outline=rim_col,
            width=3
        )
        # Specular highlight dot
        hr = max(2, r // 4)
        hx, hy = cx - r // 3, cy - r // 3
        draw.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=(255, 255, 255, 250))

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"[OK] Wrote {filepath}")


def make_dust_cluster(filepath):
    rng = random.Random(404)
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Soft gray dust bunnies
    for _ in range(35):
        ang = rng.uniform(0, math.tau)
        dist = rng.uniform(0, 150)
        r = rng.randint(25, 65)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        gray = rng.randint(135, 175)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(gray, gray, gray - 5, 95))

    img = img.filter(ImageFilter.GaussianBlur(radius=6))
    draw = ImageDraw.Draw(img)

    # Tangled hair/lint strands and coarse dust specks
    for _ in range(28):
        pts = []
        x = CENTER + rng.randint(-140, 140)
        y = CENTER + rng.randint(-140, 140)
        for _ in range(5):
            pts.append((x, y))
            x += rng.randint(-28, 28)
            y += rng.randint(-28, 28)
        draw.line(pts, fill=(95, 92, 88, 210), width=3, joint="curve")

    for _ in range(80):
        ang = rng.uniform(0, math.tau)
        dist = rng.uniform(0, 190)
        r = rng.randint(3, 8)
        cx = int(CENTER + math.cos(ang) * dist)
        cy = int(CENTER + math.sin(ang) * dist)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(110, 108, 102, 220))

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"[OK] Wrote {filepath}")


if __name__ == "__main__":
    make_mud_splat("assets/textures/dirt_mud_splat.png")
    make_coffee_spill("assets/textures/dirt_coffee_spill.png")
    make_soap_suds("assets/textures/dirt_soap_suds.png")
    make_dust_cluster("assets/textures/dirt_dust_cluster.png")