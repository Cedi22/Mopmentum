#!/usr/bin/env python3
"""
scripts/build_cleaning_tools.py
Generates low-poly Wavefront .obj meshes for the 4 core cleaning tools in Mopmentum:
  1. assets/models/tool_mop.obj
  2. assets/models/tool_sponge.obj
  3. assets/models/tool_broom.obj
  4. assets/models/tool_spray.obj
"""

import math
import os

def write_obj(filepath, vertices, faces):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write("# Mopmentum Asset\n")
        for v in vertices:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
        for face in faces:
            v0, v1, v2 = vertices[face[0]], vertices[face[1]], vertices[face[2]]
            e1 = (v1[0]-v0[0], v1[1]-v0[1], v1[2]-v0[2])
            e2 = (v2[0]-v0[0], v2[1]-v0[1], v2[2]-v0[2])
            nx = e1[1]*e2[2] - e1[2]*e2[1]
            ny = e1[2]*e2[0] - e1[0]*e2[2]
            nz = e1[0]*e2[1] - e1[1]*e2[0]
            l = math.sqrt(nx*nx + ny*ny + nz*nz) or 1.0
            f.write(f"vn {nx/l:.4f} {ny/l:.4f} {nz/l:.4f}\n")
        for i, face in enumerate(faces):
            idx_str = " ".join(f"{idx+1}//{i+1}" for idx in face)
            f.write(f"f {idx_str}\n")
    print(f"[OK] Wrote {filepath} ({len(vertices)} verts, {len(faces)} faces)")


class MeshBuilder:
    def __init__(self):
        self.vertices = []
        self.faces = []

    def add_vert(self, x, y, z):
        self.vertices.append((x, y, z))
        return len(self.vertices) - 1

    def add_face(self, *indices):
        self.faces.append(list(indices))

    def add_box(self, cx, cy, cz, sx, sy, sz, rx=0.0, ry=0.0, rz=0.0):
        hx, hy, hz = sx * 0.5, sy * 0.5, sz * 0.5
        local_verts = [
            (-hx, -hy, -hz), ( hx, -hy, -hz), ( hx,  hy, -hz), (-hx,  hy, -hz),
            (-hx, -hy,  hz), ( hx, -hy,  hz), ( hx,  hy,  hz), (-hx,  hy,  hz),
        ]
        base = len(self.vertices)
        for vx, vy, vz in local_verts:
            # Rotate X, Y, Z
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

        quads = [
            (0, 3, 2, 1), (4, 5, 6, 7),
            (0, 1, 5, 4), (2, 3, 7, 6),
            (0, 4, 7, 3), (1, 2, 6, 5)
        ]
        for q in quads:
            self.add_face(base + q[0], base + q[1], base + q[2], base + q[3])

    def add_frustum(self, cx, y0, y1, cz, r0, r1, segments=8, z_scale=1.0, tilt_x=0.0):
        base_bot = len(self.vertices)
        for i in range(segments):
            ang = (2.0 * math.pi * i) / segments
            x = cx + math.cos(ang) * r0
            z = cz + math.sin(ang) * r0 * z_scale
            self.add_vert(x, y0, z)

        base_top = len(self.vertices)
        for i in range(segments):
            ang = (2.0 * math.pi * i) / segments
            x = cx + math.cos(ang) * r1 + tilt_x
            z = cz + math.sin(ang) * r1 * z_scale
            self.add_vert(x, y1, z)

        # Side quads
        for i in range(segments):
            ni = (i + 1) % segments
            self.add_face(base_bot + i, base_bot + ni, base_top + ni, base_top + i)

        # Bottom & Top caps
        c_bot = self.add_vert(cx, y0, cz)
        c_top = self.add_vert(cx + tilt_x, y1, cz)
        for i in range(segments):
            ni = (i + 1) % segments
            self.add_face(c_bot, base_bot + ni, base_bot + i)
            self.add_face(c_top, base_top + i, base_top + ni)


def build_mop():
    mb = MeshBuilder()
    # 1. Telescoping Handle & Plastic Grip
    mb.add_frustum(0, -0.55, 0.25, 0, 0.016, 0.016, segments=8)
    mb.add_frustum(0, 0.25, 0.65, 0, 0.020, 0.020, segments=8)  # Upper sleeve
    mb.add_frustum(0, 0.65, 0.85, 0, 0.024, 0.022, segments=8)  # Ribbed plastic grip
    mb.add_frustum(0, 0.85, 0.89, 0, 0.028, 0.015, segments=8)  # End cap

    # 2. Screw Clamp Collar & Bracket
    mb.add_frustum(0, -0.63, -0.53, 0, 0.032, 0.024, segments=8)
    mb.add_box(0, -0.66, 0, 0.18, 0.06, 0.07)

    # 3. Multi-strand Tassel Mop Head (14 splayed strands)
    num_strands = 14
    for i in range(num_strands):
        ang = (2.0 * math.pi * i) / num_strands
        ring_r = 0.05 if i % 2 == 0 else 0.03
        sx = math.cos(ang) * ring_r
        sz = math.sin(ang) * ring_r * 0.65
        spread_x = math.cos(ang) * 0.09
        mb.add_frustum(
            cx=sx, y0=-0.95, y1=-0.67, cz=sz,
            r0=0.026, r1=0.018, segments=6,
            tilt_x=-spread_x * 0.5
        )
    write_obj("assets/models/tool_mop.obj", mb.vertices, mb.faces)


def build_sponge():
    mb = MeshBuilder()
    # 1. Yellow Porous Cellulose Base (with side wave grooves)
    mb.add_box(0, -0.025, 0, 0.14, 0.045, 0.22)
    mb.add_box(0, 0.005, 0, 0.125, 0.018, 0.205)  # Side grip indentation
    # 2. Green Abrasive Scrub Pad Top
    mb.add_box(0, 0.024, 0, 0.142, 0.022, 0.222)
    # 3. Surface Scrub Ridges
    for z_off in (-0.07, -0.025, 0.025, 0.07):
        mb.add_box(0, 0.037, z_off, 0.13, 0.006, 0.018)
    write_obj("assets/models/tool_sponge.obj", mb.vertices, mb.faces)


def build_broom():
    mb = MeshBuilder()
    # 1. Angled Handle (slight tilt for sweeping ergonomics)
    mb.add_frustum(0, -0.45, 0.80, 0, 0.016, 0.016, segments=8, tilt_x=0.03)
    mb.add_frustum(0.03, 0.80, 0.92, 0, 0.021, 0.018, segments=8)
    # 2. Colored Binder Cap & Stitching Band
    mb.add_box(0, -0.49, 0, 0.24, 0.08, 0.055)
    mb.add_box(0, -0.60, 0, 0.28, 0.035, 0.062)
    # 3. Slanted Bristle Wedges (Segmented for chunky low-poly flair)
    for idx, x_off in enumerate((-0.11, -0.055, 0.0, 0.055, 0.11)):
        drop = idx * 0.012  # Angled cut across bottom of broom
        mb.add_box(x_off, -0.68 - drop * 0.5, 0, 0.052, 0.30 + drop, 0.05, rz=0.04 * (idx - 2))
    write_obj("assets/models/tool_broom.obj", mb.vertices, mb.faces)


def build_spray():
    mb = MeshBuilder()
    # 1. Contoured Reservoir Bottle Body
    mb.add_frustum(0, -0.18, -0.02, 0, 0.065, 0.060, segments=10, z_scale=0.85)
    mb.add_frustum(0, -0.02, 0.07, 0, 0.060, 0.024, segments=10, z_scale=0.85)
    # 2. Threaded Neck Ring
    mb.add_frustum(0, 0.07, 0.10, 0, 0.028, 0.028, segments=8)
    # 3. Ergonomic Trigger Shroud
    mb.add_box(0, 0.135, -0.015, 0.048, 0.065, 0.11)
    mb.add_box(0, 0.115, 0.025, 0.042, 0.05, 0.05, rx=0.35)
    # 4. Spray Nozzle Nut (Front -Z)
    mb.add_box(0, 0.135, -0.078, 0.030, 0.030, 0.022)
    # 5. Squeeze Trigger Lever
    mb.add_box(0, 0.075, -0.055, 0.016, 0.085, 0.018, rx=-0.28)
    write_obj("assets/models/tool_spray.obj", mb.vertices, mb.faces)


if __name__ == "__main__":
    build_mop()
    build_sponge()
    build_broom()
    build_spray()