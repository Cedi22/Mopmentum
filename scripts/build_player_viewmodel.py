#!/usr/bin/env python3
"""
scripts/build_player_viewmodel.py
Generates low-poly 3D Wavefront .obj meshes for the first-person rubber cleaning gloves:
  1. assets/models/glove_hand_r.obj (Right rubber cleaning glove)
  2. assets/models/glove_hand_l.obj (Left rubber cleaning glove)
"""

import math
import os
from build_cleaning_tools import MeshBuilder, write_obj

def build_glove(is_left=False):
    mb = MeshBuilder()

    # Forearm & Arm sleeve extending from camera towards wrist
    # Along Z axis: +Z is back towards player, -Z is forward towards tool socket
    # We will build along Z by creating cross-sectional frustums oriented along Z
    # Or by using boxes and frustums with rotation / custom rings.

    def add_cylinder_z(z0, z1, r0, r1, cx=0.0, cy=0.0, segments=10, z_scale=1.0):
        # Cylinder aligned along Z axis
        base_bot = len(mb.vertices)
        for i in range(segments):
            ang = (2.0 * math.pi * i) / segments
            x = cx + math.cos(ang) * r0
            y = cy + math.sin(ang) * r0 * z_scale
            mb.add_vert(x, y, z0)

        base_top = len(mb.vertices)
        for i in range(segments):
            ang = (2.0 * math.pi * i) / segments
            x = cx + math.cos(ang) * r1
            y = cy + math.sin(ang) * r1 * z_scale
            mb.add_vert(x, y, z1)

        for i in range(segments):
            ni = (i + 1) % segments
            mb.add_face(base_bot + i, base_top + i, base_top + ni, base_bot + ni)

        c_bot = mb.add_vert(cx, cy, z0)
        c_top = mb.add_vert(cx, cy, z1)
        for i in range(segments):
            ni = (i + 1) % segments
            mb.add_face(c_bot, base_bot + i, base_bot + ni)
            mb.add_face(c_top, base_top + ni, base_top + i)

    # 1. Rolled Rubber Sleeve Cuff (at player end, Z ~ 0.35)
    add_cylinder_z(0.32, 0.38, 0.062, 0.065, cx=0.0, cy=-0.04, segments=12, z_scale=0.9)
    add_cylinder_z(0.30, 0.33, 0.058, 0.062, cx=0.0, cy=-0.04, segments=10, z_scale=0.9)

    # 2. Forearm tapering down to wrist
    add_cylinder_z(0.16, 0.31, 0.046, 0.056, cx=0.0, cy=-0.035, segments=10, z_scale=0.88)
    add_cylinder_z(0.04, 0.17, 0.038, 0.046, cx=0.0, cy=-0.025, segments=10, z_scale=0.85)

    # 3. Wrist segment
    add_cylinder_z(-0.02, 0.05, 0.034, 0.038, cx=0.0, cy=-0.020, segments=10, z_scale=0.82)

    # 4. Palm / Hand Metacarpal Body (chunky stylized rubber glove)
    # Centered around (0, -0.015, -0.055)
    mb.add_box(0.0, -0.015, -0.052, 0.070, 0.048, 0.062)
    mb.add_box(0.0, -0.012, -0.075, 0.066, 0.042, 0.035)

    # 5. Knuckle Ridge Band
    mb.add_box(0.0, 0.008, -0.068, 0.068, 0.014, 0.030, rx=0.15)

    # 6. Gripping Fingers (curling around the tool handle socket at z ~ -0.065, y ~ -0.015)
    # 4 fingers along X (-0.024 to +0.024)
    finger_xs = [-0.022, -0.007, 0.008, 0.023]
    for fx in finger_xs:
        # Proximal phalanx curling under
        mb.add_box(fx, -0.028, -0.088, 0.013, 0.022, 0.024, rx=-0.35)
        # Distal curling back around handle
        mb.add_box(fx, -0.036, -0.072, 0.012, 0.018, 0.020, rx=-0.85)

    # 7. Opposable Thumb
    # Placed on inner side of right hand (towards -X for right hand)
    mb.add_box(-0.038, 0.002, -0.048, 0.022, 0.024, 0.032, ry=0.35, rz=-0.25)
    mb.add_box(-0.032, 0.014, -0.072, 0.018, 0.018, 0.030, rx=0.30, ry=-0.25)

    verts = mb.vertices
    faces = mb.faces

    if is_left:
        # Mirror along X axis: invert x and reverse face winding to maintain outward normals
        mirrored_verts = [(-v[0], v[1], v[2]) for v in verts]
        mirrored_faces = [list(reversed(f)) for f in faces]
        return mirrored_verts, mirrored_faces

    return verts, faces


def build_viewmodel_hands():
    r_verts, r_faces = build_glove(is_left=False)
    write_obj("assets/models/glove_hand_r.obj", r_verts, r_faces)

    l_verts, l_faces = build_glove(is_left=True)
    write_obj("assets/models/glove_hand_l.obj", l_verts, l_faces)


if __name__ == "__main__":
    build_viewmodel_hands()
