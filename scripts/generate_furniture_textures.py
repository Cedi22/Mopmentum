#!/usr/bin/env python3
"""
scripts/generate_furniture_textures.py
Generates high-resolution, copyright-free, procedurally-crafted textures for:
  1. assets/textures/bookshelf_texture.png (Polished mahogany wood grain + 6 ornate book bindings + paper edges)
  2. assets/textures/chest_texture.png (Rustic oak planks + iron bands with rivets + brass keyhole latch)
All generated assets are original and released under CC0 / Public Domain.
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter


def clamp(val, low, high):
    return max(low, min(val, high))


def make_bookshelf_master_texture(filepath):
    w, h = 1024, 1024
    img = Image.new("RGBA", (w, h), (35, 20, 12, 255))
    draw = ImageDraw.Draw(img)

    # =========================================================================
    # 1. LEFT HALF (0..511): WARM MAHOGANY / DARK WALNUT WOOD GRAIN
    # =========================================================================
    wood_w = 512
    for x in range(wood_w):
        # Base rich mahogany stain: reddish-brown
        base_r = 115
        base_g = 62
        base_b = 32
        for y in range(h):
            # Procedural organic grain lines
            grain1 = math.sin(x * 0.12 + y * 0.02) * 16.0
            grain2 = math.sin(x * 0.03 + y * 0.08) * 12.0
            fine_fibers = math.sin(x * 1.8 + y * 0.05) * 6.0
            knot = math.exp(-((x - 220)**2 + (y - 340)**2) / 6000.0) * -35.0
            knot2 = math.exp(-((x - 140)**2 + (y - 780)**2) / 4500.0) * -30.0

            val = grain1 + grain2 + fine_fibers + knot + knot2
            r = int(clamp(base_r + val, 45, 210))
            g = int(clamp(base_g + val * 0.65, 25, 140))
            b = int(clamp(base_b + val * 0.40, 15, 95))
            img.putpixel((x, y), (r, g, b, 255))

    # Add subtle vertical plank seams and highlight bevels
    for px in [128, 256, 384, 508]:
        draw.line([(px, 0), (px, h)], fill=(40, 20, 10, 255), width=3)
        draw.line([(px + 2, 0), (px + 2, h)], fill=(160, 95, 55, 180), width=1)

    # =========================================================================
    # 2. RIGHT HALF (512..1023, 0..860): 6 DISTINCT COLORFUL BOOK BINDINGS
    # =========================================================================
    book_styles = [
        # (name, base_rgb, accent_rgb, motif)
        ("Crimson Gold", (150, 25, 30), (245, 205, 75), "gold_bands"),
        ("Royal Sapphire", (25, 55, 135), (230, 235, 245), "silver_filigree"),
        ("Emerald Forest", (20, 95, 50), (235, 195, 60), "gold_geo"),
        ("Antique Leather", (105, 55, 25), (210, 165, 80), "ribbed_spine"),
        ("Golden Terracotta", (175, 75, 35), (250, 225, 110), "gold_classic"),
        ("Midnight Violet", (65, 25, 95), (240, 210, 85), "gold_stars")
    ]

    col_w = int((1024 - 512) / len(book_styles)) # ~85 px each
    for i, (name, base_c, accent_c, motif) in enumerate(book_styles):
        bx0 = 512 + i * col_w
        bx1 = bx0 + col_w
        # Book spine height
        by0 = 0
        by1 = 860

        # Background gradient for spine curvature (dark edges, lighter center)
        for x in range(bx0, bx1):
            t = (x - bx0) / float(col_w)
            curve = math.sin(t * math.pi)
            shade = 0.65 + curve * 0.45
            r = int(clamp(base_c[0] * shade, 0, 255))
            g = int(clamp(base_c[1] * shade, 0, 255))
            b = int(clamp(base_c[2] * shade, 0, 255))
            draw.line([(x, by0), (x, by1)], fill=(r, g, b, 255))

        # Spine spine groove lines (embossed indents on left and right)
        draw.line([(bx0 + 4, by0), (bx0 + 4, by1)], fill=(15, 15, 15, 200), width=2)
        draw.line([(bx1 - 5, by0), (bx1 - 5, by1)], fill=(15, 15, 15, 200), width=2)

        # Ornaments / gold leaf foil patterns
        cx = (bx0 + bx1) // 2
        
        # Top and bottom decorative bands
        for band_y in [by0 + 35, by0 + 75, by1 - 75, by1 - 35]:
            draw.line([(bx0 + 8, band_y), (bx1 - 8, band_y)], fill=accent_c, width=3)
            draw.line([(bx0 + 12, band_y + 6), (bx1 - 12, band_y + 6)], fill=accent_c, width=1)

        # Middle raised ribs / title box
        title_y0 = by0 + 180
        title_y1 = by0 + 320
        draw.rectangle((bx0 + 10, title_y0, bx1 - 10, title_y1), outline=accent_c, width=2)
        draw.rectangle((bx0 + 14, title_y0 + 4, bx1 - 14, title_y1 - 4), outline=accent_c, width=1)
        
        # Horizontal title lines
        for ty in range(title_y0 + 25, title_y1 - 20, 22):
            draw.line([(bx0 + 20, ty), (bx1 - 20, ty)], fill=accent_c, width=3)

        # Lower emblem / medallion
        med_cy = by0 + 520
        draw.ellipse((cx - 18, med_cy - 24, cx + 18, med_cy + 24), outline=accent_c, width=2)
        draw.line([(cx - 14, med_cy), (cx + 14, med_cy)], fill=accent_c, width=2)
        draw.line([(cx, med_cy - 18), (cx, med_cy + 18)], fill=accent_c, width=2)

        # Additional ribs
        for ry in [by0 + 130, by0 + 370, by0 + 640, by0 + 730]:
            draw.line([(bx0 + 6, ry), (bx1 - 6, ry)], fill=(20, 20, 20, 220), width=4)
            draw.line([(bx0 + 6, ry + 1), (bx1 - 6, ry + 1)], fill=accent_c, width=2)

    # =========================================================================
    # 3. BOTTOM RIGHT (512..1023, 860..1023): PARCHMENT PAPER PAGES
    # =========================================================================
    for py in range(860, 1024):
        t = (py - 860) / 164.0
        r = int(240 - t * 25)
        g = int(230 - t * 30)
        b = int(210 - t * 40)
        draw.line([(512, py), (1024, py)], fill=(r, g, b, 255))
        # Page line fibers
        if py % 4 == 0:
            draw.line([(512, py), (1024, py)], fill=(190, 175, 145, 120))

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath, "PNG")
    print(f"[OK] Generated Master Bookshelf Texture: {filepath}")


def make_chest_master_texture(filepath):
    w, h = 1024, 1024
    img = Image.new("RGBA", (w, h), (40, 25, 15, 255))
    draw = ImageDraw.Draw(img)

    # =========================================================================
    # 1. LEFT HALF (0..600): RUSTIC OAK WOOD PLANKS
    # =========================================================================
    wood_w = 600
    for x in range(wood_w):
        base_r = 130
        base_g = 82
        base_b = 42
        for y in range(h):
            grain = math.sin(x * 0.05 + y * 0.18) * 14.0 + math.sin(x * 0.25) * 6.0
            r = int(clamp(base_r + grain + (x % 3), 50, 220))
            g = int(clamp(base_g + grain * 0.75 + (y % 2), 30, 155))
            b = int(clamp(base_b + grain * 0.45, 15, 95))
            img.putpixel((x, y), (r, g, b, 255))

    # Horizontal wood planks with dark grooved gaps
    plank_h = 128
    for py in range(0, h, plank_h):
        draw.line([(0, py), (wood_w, py)], fill=(20, 12, 6, 255), width=4)
        draw.line([(0, py + 3), (wood_w, py + 3)], fill=(175, 115, 65, 180), width=1)
        # Nail pegs on plank edges
        for nx in [45, 180, 320, 460, 560]:
            draw.ellipse((nx - 4, py + 18 - 4, nx + 4, py + 18 + 4), fill=(35, 30, 28, 255))
            draw.ellipse((nx - 2, py + 18 - 2, nx + 2, py + 18 + 2), fill=(75, 70, 68, 255))

    # =========================================================================
    # 2. IRON METAL BANDS WITH STUDS (600..840)
    # =========================================================================
    for x in range(600, 840):
        t = (x - 600) / 240.0
        # Dark wrought iron gradient with metallic center highlight
        metal_shade = 45 + int(math.sin(t * math.pi) * 45)
        for y in range(h):
            noise = (x * 7 + y * 13) % 9 - 4
            r = clamp(metal_shade + noise, 25, 120)
            g = clamp(metal_shade + noise + 2, 25, 125)
            b = clamp(metal_shade + noise + 5, 30, 135)
            img.putpixel((x, y), (r, g, b, 255))

    # Beveled iron border edges
    draw.line([(602, 0), (602, h)], fill=(15, 15, 18, 255), width=3)
    draw.line([(837, 0), (837, h)], fill=(15, 15, 18, 255), width=3)
    draw.line([(605, 0), (605, h)], fill=(120, 125, 135, 180), width=1)

    # Rivets / Studs along iron bands
    for ry in range(40, h, 80):
        for rx in [640, 720, 800]:
            # Outer dark ring shadow
            draw.ellipse((rx - 10, ry - 10, rx + 10, ry + 10), fill=(18, 18, 20, 255))
            # Raised metallic bolt head
            draw.ellipse((rx - 8, ry - 8, rx + 7, ry + 7), fill=(85, 90, 100, 255))
            # Glint
            draw.ellipse((rx - 4, ry - 4, rx, ry), fill=(195, 205, 220, 240))

    # =========================================================================
    # 3. ANTIQUE BRASS LATCH & LOCK PLATE (840..1024, 0..512)
    # =========================================================================
    lx0, ly0 = 840, 0
    lx1, ly1 = 1024, 512
    # Brass gradient
    for y in range(ly0, ly1):
        for x in range(lx0, lx1):
            t = (x - lx0) / 184.0
            r = int(clamp(195 + t * 45 - (y % 4), 110, 250))
            g = int(clamp(155 + t * 35 - (y % 4), 90, 210))
            b = int(clamp(45 + t * 20, 20, 85))
            img.putpixel((x, y), (r, g, b, 255))

    # Lock plate border
    draw.rectangle((lx0 + 16, ly0 + 16, lx1 - 16, ly1 - 16), outline=(80, 55, 15), width=5)
    draw.rectangle((lx0 + 22, ly0 + 22, lx1 - 22, ly1 - 22), outline=(245, 215, 95), width=2)

    # Keyhole
    cx, cy = (lx0 + lx1) // 2, (ly0 + ly1) // 2
    # Keyhole circular top
    draw.ellipse((cx - 20, cy - 35, cx + 20, cy + 5), fill=(20, 15, 10, 255))
    # Keyhole triangular slit
    draw.polygon([(cx - 12, cy), (cx + 12, cy), (cx + 18, cy + 45), (cx - 18, cy + 45)], fill=(20, 15, 10, 255))
    # Keyhole brass rim highlight
    draw.ellipse((cx - 22, cy - 37, cx + 22, cy + 7), outline=(255, 235, 140, 200), width=2)

    # Screws on 4 corners of lock plate
    for sx, sy in [(lx0 + 36, ly0 + 36), (lx1 - 36, ly0 + 36), (lx0 + 36, ly1 - 36), (lx1 - 36, ly1 - 36)]:
        draw.ellipse((sx - 8, sy - 8, sx + 8, sy + 8), fill=(40, 30, 10))
        draw.ellipse((sx - 6, sy - 6, sx + 5, sy + 5), fill=(160, 130, 45))
        draw.line([(sx - 5, sy - 2), (sx + 5, sy + 2)], fill=(40, 30, 10), width=2)

    # =========================================================================
    # 4. LOWER RIGHT (840..1024, 512..1024): REINFORCED CORNER BRACKETS
    # =========================================================================
    for y in range(512, 1024):
        for x in range(840, 1024):
            img.putpixel((x, y), (55, 58, 65, 255))
    draw.rectangle((845, 517, 1019, 1019), outline=(25, 25, 30), width=6)
    draw.rectangle((852, 524, 1012, 1012), outline=(135, 140, 150), width=2)
    # Studs on corner bracket
    for bx, by in [(880, 560), (980, 560), (880, 970), (980, 970), (930, 765)]:
        draw.ellipse((bx - 12, by - 12, bx + 12, by + 12), fill=(15, 15, 18))
        draw.ellipse((bx - 9, by - 9, bx + 8, by + 8), fill=(95, 100, 110))
        draw.ellipse((bx - 4, by - 4, bx, by), fill=(210, 215, 230))

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath, "PNG")
    print(f"[OK] Generated Master Wooden Chest Texture: {filepath}")


if __name__ == "__main__":
    make_bookshelf_master_texture("assets/textures/bookshelf_texture.png")
    make_chest_master_texture("assets/textures/chest_texture.png")
    print("[SUCCESS] All furniture textures generated successfully!")
