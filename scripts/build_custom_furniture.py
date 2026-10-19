#!/usr/bin/env python3
"""
scripts/build_custom_furniture.py
Generates clean, stylized low-poly 3D models for furniture:
  1. assets/models/bookshelf.obj
  2. assets/models/coffee_table.obj
  3. assets/models/chair.obj
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_cleaning_tools import MeshBuilder, write_obj


def build_bookshelf():
    mb = MeshBuilder()
    # 1. Base plinth
    mb.add_box(0, 0.06, 0, 1.34, 0.12, 0.40)
    # 2. Top crown cornice
    mb.add_box(0, 2.16, 0, 1.36, 0.08, 0.42)
    # 3. Vertical side panels
    mb.add_box(-0.63, 1.11, 0, 0.06, 2.02, 0.38)
    mb.add_box(0.63, 1.11, 0, 0.06, 2.02, 0.38)
    # 4. Backboard panel
    mb.add_box(0, 1.11, -0.18, 1.22, 2.02, 0.02)
    # 5. 4 Shelves
    shelves_y = [0.14, 0.64, 1.14, 1.64]
    for sy in shelves_y:
        mb.add_box(0, sy, 0, 1.20, 0.04, 0.36)

    write_obj("assets/models/bookshelf.obj", mb.vertices, mb.faces)


def build_floor_lamp():
    mb = MeshBuilder()
    # 1. Heavy Weighted Circular Brass Base
    mb.add_frustum(0, 0.00, 0.05, 0, 0.24, 0.20, segments=12)
    mb.add_frustum(0, 0.05, 0.09, 0, 0.06, 0.035, segments=10) # Base collar
    # 2. Tall Slender Brass Pole
    mb.add_frustum(0, 0.09, 1.35, 0, 0.024, 0.022, segments=8)
    # 3. Shade Harp & Neck Ring
    mb.add_frustum(0, 1.35, 1.42, 0, 0.035, 0.045, segments=8)
    # 4. Flared Modern Drum Lampshade
    mb.add_frustum(0, 1.38, 1.76, 0, 0.32, 0.22, segments=12)
    write_obj("assets/models/floor_lamp.obj", mb.vertices, mb.faces)


def build_coffee_table():
    mb = MeshBuilder()
    # 1. Beveled main tabletop
    mb.add_box(0, 0.42, 0, 1.36, 0.045, 0.72)
    # 2. Apron frame rails beneath tabletop
    mb.add_box(0, 0.38, 0.31, 1.24, 0.04, 0.03)
    mb.add_box(0, 0.38, -0.31, 1.24, 0.04, 0.03)
    mb.add_box(-0.59, 0.38, 0, 0.03, 0.04, 0.60)
    mb.add_box(0.59, 0.38, 0, 0.03, 0.04, 0.60)

    # 3. 4 Tapered wooden legs with slight flare
    leg_coords = [
        (-0.58, 0.28), (0.58, 0.28),
        (-0.58, -0.28), (0.58, -0.28)
    ]
    for lx, lz in leg_coords:
        mb.add_frustum(lx, 0.00, 0.38, lz, 0.024, 0.036, segments=8)
        # Brass ferrule foot cap
        mb.add_frustum(lx, 0.00, 0.05, lz, 0.024, 0.026, segments=8)

    # 4. Lower slatted shelf for magazines
    mb.add_box(0, 0.14, 0, 1.08, 0.02, 0.52)
    for slat_x in [-0.40, -0.20, 0.0, 0.20, 0.40]:
        mb.add_box(slat_x, 0.155, 0, 0.08, 0.015, 0.50)

    write_obj("assets/models/coffee_table.obj", mb.vertices, mb.faces)


def build_chair():
    mb = MeshBuilder()
    # 1. Cushioned seat
    mb.add_box(0, 0.44, 0, 0.48, 0.05, 0.48)
    # Seat apron frame
    mb.add_box(0, 0.39, 0.20, 0.42, 0.04, 0.025)
    mb.add_box(0, 0.39, -0.20, 0.42, 0.04, 0.025)
    mb.add_box(-0.20, 0.39, 0, 0.025, 0.04, 0.38)
    mb.add_box(0.20, 0.39, 0, 0.025, 0.04, 0.38)

    # 2. 4 Tapered legs
    mb.add_frustum(-0.20, 0.00, 0.39, 0.20, 0.018, 0.026, segments=8)
    mb.add_frustum(0.20, 0.00, 0.39, 0.20, 0.018, 0.026, segments=8)
    mb.add_frustum(-0.20, 0.00, 0.39, -0.20, 0.018, 0.026, segments=8)
    mb.add_frustum(0.20, 0.00, 0.39, -0.20, 0.018, 0.026, segments=8)

    # Cross stretchers (leg braces)
    mb.add_box(0, 0.14, 0.20, 0.38, 0.02, 0.02)
    mb.add_box(0, 0.14, -0.20, 0.38, 0.02, 0.02)
    mb.add_box(-0.20, 0.14, 0, 0.02, 0.02, 0.38)
    mb.add_box(0.20, 0.14, 0, 0.02, 0.02, 0.38)

    # 3. Backrest uprights (extending up from rear legs)
    mb.add_box(-0.20, 0.68, -0.21, 0.035, 0.48, 0.035)
    mb.add_box(0.20, 0.68, -0.21, 0.035, 0.48, 0.035)

    # 4. Top curved back rail
    mb.add_box(0, 0.90, -0.21, 0.48, 0.065, 0.035)

    # 5. Middle cross rail & 3 vertical slats
    mb.add_box(0, 0.52, -0.21, 0.40, 0.03, 0.02)
    for sx in [-0.10, 0.0, 0.10]:
        mb.add_box(sx, 0.70, -0.21, 0.035, 0.32, 0.018)

    write_obj("assets/models/chair.obj", mb.vertices, mb.faces)


if __name__ == "__main__":
    build_bookshelf()
    build_floor_lamp()
    build_coffee_table()
    build_chair()
    print("[SUCCESS] All custom furniture models generated!")
