#!/usr/bin/env python3
"""
scripts/build_breakable_props.py
Generates the 5 breakable household 3D .obj models AND their Godot 4 .tscn scenes:
  1. Antique Porcelain Vase ($250) -> assets/models/vase_porcelain.obj & scenes/vase.tscn
  2. Table Lamp ($180)             -> assets/models/table_lamp.obj     & scenes/lamp.tscn
  3. Retro CRT TV ($400)           -> assets/models/retro_tv.obj       & scenes/tv.tscn
  4. Drinking Glass ($35)          -> assets/models/drinking_glass.obj & scenes/glass.tscn
  5. Framed Painting ($450)        -> assets/models/framed_painting.obj& scenes/painting.tscn
"""

import os
from build_cleaning_tools import MeshBuilder, write_obj

def build_vase_obj():
    mb = MeshBuilder()
    # Lathe profile: (y, radius)
    profile = [
        (0.00, 0.09), (0.04, 0.08), (0.14, 0.16),
        (0.28, 0.15), (0.38, 0.06), (0.46, 0.07), (0.50, 0.10)
    ]
    for i in range(len(profile) - 1):
        y0, r0 = profile[i]
        y1, r1 = profile[i + 1]
        mb.add_frustum(0, y0, y1, 0, r0, r1, segments=10)
    write_obj("assets/models/vase_porcelain.obj", mb.vertices, mb.faces)


def build_lamp_obj():
    mb = MeshBuilder()
    # Weighted Base & Stem
    mb.add_frustum(0, 0.00, 0.04, 0, 0.12, 0.10, segments=10)
    mb.add_frustum(0, 0.04, 0.34, 0, 0.025, 0.020, segments=8)
    # Conical Pleated Lampshade
    mb.add_frustum(0, 0.28, 0.52, 0, 0.20, 0.11, segments=10)
    write_obj("assets/models/table_lamp.obj", mb.vertices, mb.faces)


def build_tv_obj():
    mb = MeshBuilder()
    # Chunky CRT Cabinet & Rear Tube Housing
    mb.add_box(0, 0.22, 0.0, 0.56, 0.42, 0.38)
    mb.add_box(0, 0.22, 0.24, 0.34, 0.28, 0.14)
    # Front Bezel & Bulging CRT Glass Screen
    mb.add_box(-0.05, 0.23, -0.195, 0.40, 0.32, 0.02)
    # Side Control Dials
    mb.add_box(0.21, 0.28, -0.195, 0.05, 0.05, 0.03)
    mb.add_box(0.21, 0.20, -0.195, 0.05, 0.05, 0.03)
    # Rabbit-Ear Antennae
    mb.add_box(0, 0.44, -0.05, 0.12, 0.04, 0.08)
    mb.add_box(-0.12, 0.58, -0.05, 0.015, 0.28, 0.015, rz=0.45)
    mb.add_box(0.12, 0.58, -0.05, 0.015, 0.28, 0.015, rz=-0.45)
    write_obj("assets/models/retro_tv.obj", mb.vertices, mb.faces)


def build_glass_obj():
    mb = MeshBuilder()
    # Heavy Tumbler Base & Tapered Body
    mb.add_frustum(0, 0.00, 0.03, 0, 0.042, 0.044, segments=8)
    mb.add_frustum(0, 0.03, 0.16, 0, 0.044, 0.055, segments=8)
    write_obj("assets/models/drinking_glass.obj", mb.vertices, mb.faces)


def build_painting_obj():
    mb = MeshBuilder()
    # Recessed Canvas Backing
    mb.add_box(0, 0.35, 0.0, 0.72, 0.52, 0.025)
    # 4 Chunky Wooden Frame Rails
    mb.add_box(0, 0.62, -0.01, 0.80, 0.06, 0.05)   # Top rail
    mb.add_box(0, 0.08, -0.01, 0.80, 0.06, 0.05)   # Bottom rail
    mb.add_box(-0.37, 0.35, -0.01, 0.06, 0.50, 0.05) # Left stile
    mb.add_box(0.37, 0.35, -0.01, 0.06, 0.50, 0.05)  # Right stile
    write_obj("assets/models/framed_painting.obj", mb.vertices, mb.faces)


TSCN_TEMPLATE = """[gd_scene load_steps=5 format=3 uid="uid://mopmentum_{scene_id}"]

[ext_resource type="Script" path="res://scripts/breakable_object.gd" id="1_break"]
[ext_resource type="ArrayMesh" path="res://assets/models/{obj_name}" id="2_mesh"]

[sub_resource type="StandardMaterial3D" id="Mat_Prop"]
transparency = {transparency}
diffuse_mode = 3
specular_mode = 1
albedo_color = Color({color})
roughness = {roughness}

[sub_resource type="BoxShape3D" id="Shape_Col"]
size = Vector3({col_size})

[node name="{node_name}" type="RigidBody3D"]
mass = {mass}
contact_monitor = true
max_contacts_reported = 4
script = ExtResource("1_break")
object_name = "{display_name}"
dollar_value = {value}
break_impulse_threshold = {threshold}

[node name="MeshInstance3D" type="MeshInstance3D" parent="."]
mesh = ExtResource("2_mesh")
surface_material_override/0 = SubResource("Mat_Prop")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, {col_y}, 0)
shape = SubResource("Shape_Col")
"""

def write_breakable_scenes():
    os.makedirs("scenes", exist_ok=True)
    specs = [
        {
            "file": "scenes/vase.tscn", "scene_id": "vase",
            "node_name": "PorcelainVase", "display_name": "Antique Porcelain Vase",
            "obj_name": "vase_porcelain.obj", "value": 250, "mass": 1.8, "threshold": 3.5,
            "color": "0.92, 0.95, 1.0, 1.0", "transparency": 0, "roughness": 0.15,
            "col_size": "0.32, 0.50, 0.32", "col_y": 0.25
        },
        {
            "file": "scenes/lamp.tscn", "scene_id": "lamp",
            "node_name": "TableLamp", "display_name": "Table Lamp",
            "obj_name": "table_lamp.obj", "value": 180, "mass": 2.2, "threshold": 4.5,
            "color": "1.0, 0.88, 0.42, 1.0", "transparency": 0, "roughness": 0.45,
            "col_size": "0.40, 0.52, 0.40", "col_y": 0.26
        },
        {
            "file": "scenes/tv.tscn", "scene_id": "tv",
            "node_name": "RetroTV", "display_name": "CRT Television",
            "obj_name": "retro_tv.obj", "value": 400, "mass": 12.0, "threshold": 8.0,
            "color": "0.32, 0.34, 0.38, 1.0", "transparency": 0, "roughness": 0.35,
            "col_size": "0.56, 0.44, 0.48", "col_y": 0.22
        },
        {
            "file": "scenes/glass.tscn", "scene_id": "glass",
            "node_name": "DrinkingGlass", "display_name": "Drinking Glass",
            "obj_name": "drinking_glass.obj", "value": 35, "mass": 0.35, "threshold": 1.2,
            "color": "0.75, 0.92, 1.0, 0.65", "transparency": 1, "roughness": 0.08,
            "col_size": "0.11, 0.16, 0.11", "col_y": 0.08
        },
        {
            "file": "scenes/painting.tscn", "scene_id": "painting",
            "node_name": "FramedPainting", "display_name": "Framed Painting",
            "obj_name": "framed_painting.obj", "value": 450, "mass": 2.5, "threshold": 4.0,
            "color": "0.72, 0.48, 0.22, 1.0", "transparency": 0, "roughness": 0.55,
            "col_size": "0.80, 0.60, 0.06", "col_y": 0.35
        },
    ]

    for s in specs:
        with open(s["file"], "w") as f:
            f.write(TSCN_TEMPLATE.format(**s))
        print(f"[OK] Wrote {s['file']} (${s['value']})")


if __name__ == "__main__":
    build_vase_obj()
    build_lamp_obj()
    build_tv_obj()
    build_glass_obj()
    build_painting_obj()
    write_breakable_scenes()