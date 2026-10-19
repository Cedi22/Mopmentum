#!/usr/bin/env python3
"""
scripts/build_textured_props.py
Builds fully UV-mapped 3D models for:
  1. assets/models/bookshelf.obj (Bookshelf with multi-tier shelves, cornice, and rows of colorful books)
  2. assets/models/muck_chest.obj (Rustic storage chest with oak planks, iron bands, studs, and brass lock)
All UV coordinates are accurately mapped to:
  - assets/textures/bookshelf_texture.png
  - assets/textures/chest_texture.png
"""

import math
import os


class UVMeshBuilder:
    def __init__(self):
        self.vertices = []      # (x, y, z)
        self.uvs = []           # (u, v)
        self.normals = []       # (nx, ny, nz)
        self.faces = []         # list of (v_idx, vt_idx, vn_idx)

    def add_vert(self, x, y, z):
        self.vertices.append((x, y, z))
        return len(self.vertices) - 1

    def add_uv(self, u, v):
        self.uvs.append((u, v))
        return len(self.uvs) - 1

    def add_normal(self, nx, ny, nz):
        self.normals.append((nx, ny, nz))
        return len(self.normals) - 1

    def add_quad(self, v_indices, uv_coords, normal):
        # v_indices: [v0, v1, v2, v3]
        # uv_coords: [(u0, v0), (u1, v1), (u2, v2), (u3, v3)]
        # normal: (nx, ny, nz)
        ni = self.add_normal(*normal)
        uv_indices = [self.add_uv(u, v) for u, v in uv_coords]
        face_pts = [
            (v_indices[0], uv_indices[0], ni),
            (v_indices[1], uv_indices[1], ni),
            (v_indices[2], uv_indices[2], ni),
            (v_indices[3], uv_indices[3], ni),
        ]
        self.faces.append(face_pts)

    def add_box_uv(self, cx, cy, cz, sx, sy, sz, uv_map, rx=0.0, ry=0.0, rz=0.0):
        """
        Adds a box with custom UV rectangles per face.
        uv_map: dict with keys 'front', 'back', 'left', 'right', 'top', 'bottom',
                each with (u0, v0, u1, v1)
        """
        hx, hy, hz = sx * 0.5, sy * 0.5, sz * 0.5
        local_verts = [
            (-hx, -hy, -hz), ( hx, -hy, -hz), ( hx,  hy, -hz), (-hx,  hy, -hz), # 0,1,2,3: back
            (-hx, -hy,  hz), ( hx, -hy,  hz), ( hx,  hy,  hz), (-hx,  hy,  hz), # 4,5,6,7: front
        ]
        base_v = len(self.vertices)
        for vx, vy, vz in local_verts:
            if rx != 0.0:
                c, s = math.cos(rx), math.sin(rx)
                vy, vz = vy * c - vz * s, vy * s + vz * c
            if ry != 0.0:
                c, s = math.cos(ry), math.sin(ry)
                vx, vz = vx * c + vz * s, -vx * s + vz * c
            if rz != 0.0:
                c, s = math.cos(rz), math.sin(rz)
                vx, vy = vx * c - vy * s, vx * s + vy * c
            self.add_vert(cx + vx, cy + vy, cz + vz)

        # 6 faces:
        # Front (+Z): vertices 4, 5, 6, 7
        fu0, fv0, fu1, fv1 = uv_map.get('front', (0,0,1,1))
        self.add_quad([base_v + 4, base_v + 5, base_v + 6, base_v + 7],
                      [(fu0, fv0), (fu1, fv0), (fu1, fv1), (fu0, fv1)],
                      (0, 0, 1))

        # Back (-Z): vertices 1, 0, 3, 2
        bu0, bv0, bu1, bv1 = uv_map.get('back', (0,0,1,1))
        self.add_quad([base_v + 1, base_v + 0, base_v + 3, base_v + 2],
                      [(bu0, bv0), (bu1, bv0), (bu1, bv1), (bu0, bv1)],
                      (0, 0, -1))

        # Left (-X): vertices 0, 4, 7, 3
        lu0, lv0, lu1, lv1 = uv_map.get('left', (0,0,1,1))
        self.add_quad([base_v + 0, base_v + 4, base_v + 7, base_v + 3],
                      [(lu0, lv0), (lu1, lv0), (lu1, lv1), (lu0, lv1)],
                      (-1, 0, 0))

        # Right (+X): vertices 5, 1, 2, 6
        ru0, rv0, ru1, rv1 = uv_map.get('right', (0,0,1,1))
        self.add_quad([base_v + 5, base_v + 1, base_v + 2, base_v + 6],
                      [(ru0, rv0), (ru1, rv0), (ru1, rv1), (ru0, rv1)],
                      (1, 0, 0))

        # Top (+Y): vertices 7, 6, 2, 3
        tu0, tv0, tu1, tv1 = uv_map.get('top', (0,0,1,1))
        self.add_quad([base_v + 7, base_v + 6, base_v + 2, base_v + 3],
                      [(tu0, tv0), (tu1, tv0), (tu1, tv1), (tu0, tv1)],
                      (0, 1, 0))

        # Bottom (-Y): vertices 0, 1, 5, 4
        du0, dv0, du1, dv1 = uv_map.get('bottom', (0,0,1,1))
        self.add_quad([base_v + 0, base_v + 1, base_v + 5, base_v + 4],
                      [(du0, dv0), (du1, dv0), (du1, dv1), (du0, dv1)],
                      (0, -1, 0))

    def write_obj(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write("# Mopmentum Procedurally Textured 3D Asset\n")
            f.write("mtllib material.mtl\n")
            f.write("o Object\n")
            for v in self.vertices:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            for vt in self.uvs:
                f.write(f"vt {vt[0]:.4f} {vt[1]:.4f}\n")
            for vn in self.normals:
                f.write(f"vn {vn[0]:.4f} {vn[1]:.4f} {vn[2]:.4f}\n")
            for face in self.faces:
                # 1-indexed v/vt/vn
                line = " ".join(f"{v+1}/{vt+1}/{vn+1}" for v, vt, vn in face)
                f.write(f"f {line}\n")
        print(f"[OK] Wrote UV-mapped OBJ: {filepath} ({len(self.vertices)} v, {len(self.faces)} f)")


def build_textured_bookshelf():
    builder = UVMeshBuilder()

    # Wood UV coordinates in bookshelf_texture.png: U: [0.02, 0.48], V: [0.02, 0.98]
    wood_uv = {
        'front': (0.02, 0.02, 0.48, 0.98),
        'back':  (0.02, 0.02, 0.48, 0.98),
        'left':  (0.05, 0.05, 0.45, 0.95),
        'right': (0.05, 0.05, 0.45, 0.95),
        'top':   (0.02, 0.20, 0.48, 0.50),
        'bottom':(0.02, 0.20, 0.48, 0.50),
    }

    # 1. Base plinth
    builder.add_box_uv(0, 0.06, 0, 1.34, 0.12, 0.40, wood_uv)
    # 2. Top crown cornice
    builder.add_box_uv(0, 2.16, 0, 1.36, 0.08, 0.42, wood_uv)
    # 3. Vertical side panels
    builder.add_box_uv(-0.63, 1.11, 0, 0.06, 2.02, 0.38, wood_uv)
    builder.add_box_uv(0.63, 1.11, 0, 0.06, 2.02, 0.38, wood_uv)
    # 4. Backboard panel
    builder.add_box_uv(0, 1.11, -0.18, 1.22, 2.02, 0.02, wood_uv)

    # 5. 4 Shelves: y = 0.14, 0.64, 1.14, 1.64
    shelves_y = [0.14, 0.64, 1.14, 1.64]
    for sy in shelves_y:
        builder.add_box_uv(0, sy, 0, 1.20, 0.04, 0.36, wood_uv)

    # 6. Procedural 3D Books with Colorful Spines & Parchment Paper
    # Book spine regions in texture:
    # 6 styles from U = 0.50 to 0.98, V = 0.02 to 0.84
    # Parchment pages: U = 0.55 to 0.95, V = 0.86 to 0.98
    pages_uv = (0.55, 0.86, 0.95, 0.98)

    def get_book_uv(style_idx):
        col_w = (0.98 - 0.50) / 6.0
        u0 = 0.50 + style_idx * col_w
        u1 = u0 + col_w
        return {
            'front':  (u0, 0.02, u1, 0.84),            # Spine facing out!
            'back':   pages_uv,                         # Paper edges against backboard
            'left':   (u0 + 0.01, 0.10, u0 + 0.04, 0.70), # Cover cloth side
            'right':  (u0 + 0.01, 0.10, u0 + 0.04, 0.70), # Cover cloth side
            'top':    pages_uv,                         # Top paper pages
            'bottom': pages_uv,                         # Bottom paper pages
        }

    # Shelf 1 (y = 0.64, top at y = 0.66): Dense colorful row of books
    shelf1_y = 0.66
    x_cursor = -0.54
    book_specs_1 = [
        # (width, height, depth, style, tilt_deg)
        (0.065, 0.28, 0.22, 0, 0.0),    # Crimson Gold
        (0.050, 0.25, 0.20, 1, 0.0),    # Sapphire Silver
        (0.075, 0.30, 0.24, 2, 0.0),    # Emerald Forest
        (0.055, 0.24, 0.19, 3, 0.0),    # Antique Leather
        (0.060, 0.27, 0.22, 4, 0.0),    # Terracotta
        (0.070, 0.29, 0.23, 5, 0.0),    # Midnight Violet
        (0.050, 0.23, 0.20, 0, 0.0),    # Crimson
        (0.080, 0.31, 0.24, 1, 0.0),    # Sapphire
        (0.060, 0.26, 0.21, 3, 0.0),    # Leather
        (0.065, 0.28, 0.22, 2, 0.0),    # Emerald
        (0.055, 0.24, 0.19, 4, 0.0),    # Terracotta
        (0.070, 0.29, 0.23, 5, 0.0),    # Violet
        (0.065, 0.26, 0.20, 0, -12.0),  # Leaning book!
    ]
    for w_b, h_b, d_b, s_b, tilt in book_specs_1:
        cx = x_cursor + w_b * 0.5
        cy = shelf1_y + h_b * 0.5
        cz = -0.06
        uvs = get_book_uv(s_b)
        builder.add_box_uv(cx, cy, cz, w_b, h_b, d_b, uvs, rz=math.radians(tilt))
        x_cursor += w_b + 0.006

    # Shelf 2 (y = 1.14, top at y = 1.16): Books on the left and right
    # (Leaving center-left around x = -0.35..0.15 open for vase / decorative items!)
    shelf2_y = 1.16
    x_cursor = 0.08
    book_specs_2 = [
        (0.070, 0.29, 0.23, 3, 0.0),    # Antique Leather
        (0.060, 0.26, 0.21, 2, 0.0),    # Emerald
        (0.055, 0.25, 0.20, 0, 0.0),    # Crimson
        (0.075, 0.31, 0.24, 4, 0.0),    # Terracotta
        (0.050, 0.22, 0.19, 5, 0.0),    # Violet
        (0.065, 0.27, 0.22, 1, 10.0),   # Leaning book
    ]
    for w_b, h_b, d_b, s_b, tilt in book_specs_2:
        cx = x_cursor + w_b * 0.5
        cy = shelf2_y + h_b * 0.5
        cz = -0.06
        uvs = get_book_uv(s_b)
        builder.add_box_uv(cx, cy, cz, w_b, h_b, d_b, uvs, rz=math.radians(tilt))
        x_cursor += w_b + 0.006

    # Shelf 3 (y = 1.64, top at y = 1.66): Upper row with various encyclopedias
    shelf3_y = 1.66
    x_cursor = -0.48
    book_specs_3 = [
        (0.080, 0.32, 0.24, 1, 0.0),
        (0.080, 0.32, 0.24, 1, 0.0),
        (0.080, 0.32, 0.24, 1, 0.0),
        (0.060, 0.27, 0.21, 0, 0.0),
        (0.060, 0.27, 0.21, 0, 0.0),
        (0.070, 0.29, 0.23, 2, 0.0),
        (0.055, 0.24, 0.19, 4, 0.0),
        (0.055, 0.24, 0.19, 5, 0.0),
    ]
    for w_b, h_b, d_b, s_b, tilt in book_specs_3:
        cx = x_cursor + w_b * 0.5
        cy = shelf3_y + h_b * 0.5
        cz = -0.06
        uvs = get_book_uv(s_b)
        builder.add_box_uv(cx, cy, cz, w_b, h_b, d_b, uvs, rz=math.radians(tilt))
        x_cursor += w_b + 0.008

    builder.write_obj("assets/models/bookshelf.obj")


def build_textured_chest():
    builder = UVMeshBuilder()

    # Chest texture atlas layout:
    # Wood planks: U: [0.02, 0.58], V: [0.02, 0.98]
    # Iron metal bands: U: [0.60, 0.82], V: [0.02, 0.98]
    # Brass latch & keyhole: U: [0.83, 0.98], V: [0.05, 0.48]
    # Corner brackets: U: [0.83, 0.98], V: [0.52, 0.98]

    # --- 1. CHEST BASE BOX ---
    # sx = 0.76, sy = 0.45, sz = 0.48, centered at y = 0.225
    base_uv = {
        'front': (0.02, 0.02, 0.58, 0.48),
        'back':  (0.02, 0.50, 0.58, 0.98),
        'left':  (0.05, 0.10, 0.45, 0.60),
        'right': (0.05, 0.10, 0.45, 0.60),
        'top':   (0.02, 0.10, 0.58, 0.50),
        'bottom':(0.02, 0.10, 0.58, 0.50),
    }
    builder.add_box_uv(0, 0.225, 0, 0.76, 0.45, 0.48, base_uv)

    # --- 2. IRON REINFORCEMENT STRAPS ON BASE ---
    iron_uv = {
        'front': (0.62, 0.02, 0.78, 0.48),
        'back':  (0.62, 0.50, 0.78, 0.98),
        'left':  (0.62, 0.10, 0.78, 0.60),
        'right': (0.62, 0.10, 0.78, 0.60),
        'top':   (0.62, 0.10, 0.78, 0.50),
        'bottom':(0.62, 0.10, 0.78, 0.50),
    }
    # Left strap and Right strap wrapping vertically around the base
    builder.add_box_uv(-0.24, 0.225, 0, 0.055, 0.455, 0.488, iron_uv)
    builder.add_box_uv(0.24, 0.225, 0, 0.055, 0.455, 0.488, iron_uv)

    # Horizontal bottom base trim band
    builder.add_box_uv(0, 0.03, 0, 0.768, 0.06, 0.488, iron_uv)

    # --- 3. BRASS KEYHOLE LATCH PLATE ON FRONT ---
    latch_uv = {
        'front': (0.83, 0.05, 0.98, 0.48), # Keyhole facing forward!
        'back':  (0.62, 0.10, 0.78, 0.30),
        'left':  (0.62, 0.10, 0.70, 0.30),
        'right': (0.62, 0.10, 0.70, 0.30),
        'top':   (0.83, 0.05, 0.98, 0.15),
        'bottom':(0.83, 0.35, 0.98, 0.48),
    }
    builder.add_box_uv(0, 0.34, 0.246, 0.11, 0.14, 0.015, latch_uv)

    # --- 4. CHEST LID (CURVED SEGMENTED VAULT) ---
    # Lid sits on top of base from y = 0.45 to y = 0.62
    # Composed of 5 faceted arched wooden planks
    lid_radius = 0.24
    lid_length = 0.768
    num_segments = 5
    d_theta = math.pi / num_segments
    lid_center_y = 0.45
    lid_center_z = 0.0

    for seg in range(num_segments):
        th0 = seg * d_theta
        th1 = (seg + 1) * d_theta
        # Normal & angle
        th_mid = (th0 + th1) * 0.5
        y_mid = lid_center_y + math.sin(th_mid) * (lid_radius * 0.5)
        z_mid = lid_center_z - math.cos(th_mid) * (lid_radius * 0.5)
        
        # Segment plank dimensions
        chord = 2.0 * lid_radius * math.sin(d_theta * 0.5)
        builder.add_box_uv(0, y_mid, z_mid,
                           lid_length, chord * 0.98, 0.035,
                           base_uv,
                           rx=-(math.pi * 0.5 - th_mid))

    # Lid iron straps on left and right
    for lx in [-0.24, 0.24]:
        for seg in range(num_segments):
            th_mid = (seg + 0.5) * d_theta
            y_mid = lid_center_y + math.sin(th_mid) * (lid_radius * 0.5)
            z_mid = lid_center_z - math.cos(th_mid) * (lid_radius * 0.5)
            chord = 2.0 * lid_radius * math.sin(d_theta * 0.5)
            builder.add_box_uv(lx, y_mid, z_mid,
                               0.058, chord * 1.02, 0.045,
                               iron_uv,
                               rx=-(math.pi * 0.5 - th_mid))

    # Lid front hasp hanging down over the keyhole
    builder.add_box_uv(0, 0.43, 0.252, 0.065, 0.08, 0.018, latch_uv)

    builder.write_obj("assets/models/muck_chest.obj")


if __name__ == "__main__":
    build_textured_bookshelf()
    build_textured_chest()
    print("[SUCCESS] All textured 3D models generated!")
