import os

def create_prop_scenes():
    props_dir = r"c:/Users/visita/OneDrive/Documents/Desktop/Test/Mopmentum/scenes/props"
    os.makedirs(props_dir, exist_ok=True)
    
    # 1. Muck Tree
    tree_muck_tscn = """[gd_scene load_steps=7 format=3 uid="uid://tree_muck"]

[sub_resource type="StandardMaterial3D" id="trunk_mat"]
albedo_color = Color(0.42, 0.26, 0.14, 1)
roughness = 0.9
diffuse_mode = 3

[sub_resource type="StandardMaterial3D" id="leaf_mat"]
albedo_color = Color(0.22, 0.68, 0.18, 1)
roughness = 0.9
diffuse_mode = 3

[sub_resource type="CylinderMesh" id="trunk_mesh"]
top_radius = 0.22
bottom_radius = 0.38
height = 3.2
radial_segments = 6
rings = 1

[sub_resource type="SphereMesh" id="foliage_mesh1"]
radius = 1.3
height = 2.4
radial_segments = 7
rings = 5

[sub_resource type="SphereMesh" id="foliage_mesh2"]
radius = 0.9
height = 1.7
radial_segments = 6
rings = 4

[sub_resource type="CylinderShape3D" id="col_shape"]
radius = 0.38
height = 3.2

[node name="TreeMuck" type="StaticBody3D"]

[node name="Trunk" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.6, 0)
mesh = SubResource("trunk_mesh")
surface_material_override/0 = SubResource("trunk_mat")

[node name="Foliage1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.2, 0)
mesh = SubResource("foliage_mesh1")
surface_material_override/0 = SubResource("leaf_mat")

[node name="Foliage2" type="MeshInstance3D" parent="."]
transform = Transform3D(0.9, 0, 0.4, 0, 1, 0, -0.4, 0, 0.9, 0.5, 2.6, 0.3)
mesh = SubResource("foliage_mesh2")
surface_material_override/0 = SubResource("leaf_mat")

[node name="Foliage3" type="MeshInstance3D" parent="."]
transform = Transform3D(0.8, 0, -0.5, 0, 0.9, 0, 0.5, 0, 0.8, -0.4, 2.7, -0.3)
mesh = SubResource("foliage_mesh2")
surface_material_override/0 = SubResource("leaf_mat")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.6, 0)
shape = SubResource("col_shape")
"""
    with open(os.path.join(props_dir, "tree_muck.tscn"), "w") as f:
        f.write(tree_muck_tscn)

    # 2. Muck Birch Tree
    tree_birch_tscn = """[gd_scene load_steps=7 format=3 uid="uid://tree_birch"]

[sub_resource type="StandardMaterial3D" id="birch_mat"]
albedo_color = Color(0.92, 0.92, 0.90, 1)
roughness = 0.8
diffuse_mode = 3

[sub_resource type="StandardMaterial3D" id="birch_leaf_mat"]
albedo_color = Color(0.38, 0.82, 0.24, 1)
roughness = 0.9
diffuse_mode = 3

[sub_resource type="CylinderMesh" id="trunk_mesh"]
top_radius = 0.16
bottom_radius = 0.28
height = 3.8
radial_segments = 6
rings = 1

[sub_resource type="SphereMesh" id="leaf_mesh1"]
radius = 1.15
height = 2.1
radial_segments = 6
rings = 4

[sub_resource type="SphereMesh" id="leaf_mesh2"]
radius = 0.85
height = 1.5
radial_segments = 6
rings = 4

[sub_resource type="CylinderShape3D" id="col_shape"]
radius = 0.28
height = 3.8

[node name="TreeBirch" type="StaticBody3D"]

[node name="Trunk" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.9, 0)
mesh = SubResource("trunk_mesh")
surface_material_override/0 = SubResource("birch_mat")

[node name="Foliage1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.8, 0)
mesh = SubResource("leaf_mesh1")
surface_material_override/0 = SubResource("birch_leaf_mat")

[node name="Foliage2" type="MeshInstance3D" parent="."]
transform = Transform3D(0.9, 0, 0.3, 0, 0.9, 0, -0.3, 0, 0.9, -0.35, 3.1, 0.2)
mesh = SubResource("leaf_mesh2")
surface_material_override/0 = SubResource("birch_leaf_mat")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.9, 0)
shape = SubResource("col_shape")
"""
    with open(os.path.join(props_dir, "tree_birch.tscn"), "w") as f:
        f.write(tree_birch_tscn)

    # 3. Muck Boulder (Large)
    rock_boulder_tscn = """[gd_scene load_steps=4 format=3 uid="uid://rock_boulder"]

[sub_resource type="StandardMaterial3D" id="rock_mat"]
albedo_color = Color(0.48, 0.52, 0.56, 1)
roughness = 0.95
diffuse_mode = 3

[sub_resource type="SphereMesh" id="rock_mesh"]
radius = 1.5
height = 2.4
radial_segments = 6
rings = 4

[sub_resource type="SphereShape3D" id="rock_col"]
radius = 1.4

[node name="RockBoulder" type="StaticBody3D"]

[node name="MeshInstance3D" type="MeshInstance3D" parent="."]
transform = Transform3D(1.2, 0, 0.3, 0, 0.85, 0, -0.3, 0, 1.1, 0, 0.8, 0)
mesh = SubResource("rock_mesh")
surface_material_override/0 = SubResource("rock_mat")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.8, 0)
shape = SubResource("rock_col")
"""
    with open(os.path.join(props_dir, "rock_boulder.tscn"), "w") as f:
        f.write(rock_boulder_tscn)

    # 4. Muck Small Rock
    rock_small_tscn = """[gd_scene load_steps=4 format=3 uid="uid://rock_small"]

[sub_resource type="StandardMaterial3D" id="rock_mat"]
albedo_color = Color(0.42, 0.46, 0.50, 1)
roughness = 0.95
diffuse_mode = 3

[sub_resource type="SphereMesh" id="rock_mesh"]
radius = 0.5
height = 0.8
radial_segments = 5
rings = 3

[sub_resource type="SphereShape3D" id="rock_col"]
radius = 0.45

[node name="RockSmall" type="StaticBody3D"]

[node name="MeshInstance3D" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.7, 0, 0, 0, 1, 0, 0.25, 0)
mesh = SubResource("rock_mesh")
surface_material_override/0 = SubResource("rock_mat")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.25, 0)
shape = SubResource("rock_col")
"""
    with open(os.path.join(props_dir, "rock_small.tscn"), "w") as f:
        f.write(rock_small_tscn)

    # 5. Red Mushroom
    mushroom_red_tscn = """[gd_scene load_steps=6 format=3 uid="uid://mushroom_red"]

[sub_resource type="StandardMaterial3D" id="stem_mat"]
albedo_color = Color(0.95, 0.94, 0.90, 1)
roughness = 0.8
diffuse_mode = 3

[sub_resource type="StandardMaterial3D" id="cap_mat"]
albedo_color = Color(0.92, 0.20, 0.15, 1)
roughness = 0.7
diffuse_mode = 3

[sub_resource type="CylinderMesh" id="stem_mesh"]
top_radius = 0.08
bottom_radius = 0.12
height = 0.35
radial_segments = 6

[sub_resource type="CylinderMesh" id="cap_mesh"]
top_radius = 0.1
bottom_radius = 0.38
height = 0.22
radial_segments = 7

[sub_resource type="CylinderShape3D" id="shroom_col"]
radius = 0.36
height = 0.45

[node name="MushroomRed" type="StaticBody3D"]

[node name="Stem" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.175, 0)
mesh = SubResource("stem_mesh")
surface_material_override/0 = SubResource("stem_mat")

[node name="Cap" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.35, 0)
mesh = SubResource("cap_mesh")
surface_material_override/0 = SubResource("cap_mat")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.25, 0)
shape = SubResource("shroom_col")
"""
    with open(os.path.join(props_dir, "mushroom_red.tscn"), "w") as f:
        f.write(mushroom_red_tscn)

    # 6. Blue Bioluminescent Mushroom
    mushroom_blue_tscn = """[gd_scene load_steps=6 format=3 uid="uid://mushroom_blue"]

[sub_resource type="StandardMaterial3D" id="stem_mat"]
albedo_color = Color(0.85, 0.90, 0.95, 1)
roughness = 0.8
diffuse_mode = 3

[sub_resource type="StandardMaterial3D" id="cap_blue_mat"]
albedo_color = Color(0.15, 0.70, 0.98, 1)
emission_enabled = true
emission = Color(0.12, 0.65, 0.95, 1)
emission_energy_multiplier = 1.2
roughness = 0.5
diffuse_mode = 3

[sub_resource type="CylinderMesh" id="stem_mesh"]
top_radius = 0.08
bottom_radius = 0.12
height = 0.38
radial_segments = 6

[sub_resource type="CylinderMesh" id="cap_mesh"]
top_radius = 0.08
bottom_radius = 0.36
height = 0.24
radial_segments = 7

[sub_resource type="CylinderShape3D" id="shroom_col"]
radius = 0.35
height = 0.5

[node name="MushroomBlue" type="StaticBody3D"]

[node name="Stem" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.19, 0)
mesh = SubResource("stem_mesh")
surface_material_override/0 = SubResource("stem_mat")

[node name="Cap" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.38, 0)
mesh = SubResource("cap_mesh")
surface_material_override/0 = SubResource("cap_blue_mat")

[node name="OmniLight3D" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.45, 0)
light_color = Color(0.2, 0.75, 1, 1)
light_energy = 0.8
omni_range = 2.5

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.25, 0)
shape = SubResource("shroom_col")
"""
    with open(os.path.join(props_dir, "mushroom_blue.tscn"), "w") as f:
        f.write(mushroom_blue_tscn)

    # 7. Dani's Milk Carton (Breakable!)
    milk_carton_tscn = """[gd_scene load_steps=8 format=3 uid="uid://milk_carton"]

[ext_resource type="Script" path="res://scripts/breakable_object.gd" id="1_break"]

[sub_resource type="StandardMaterial3D" id="carton_white"]
albedo_color = Color(0.96, 0.96, 0.98, 1)
roughness = 0.4
diffuse_mode = 3

[sub_resource type="StandardMaterial3D" id="carton_cyan"]
albedo_color = Color(0.18, 0.72, 0.95, 1)
roughness = 0.4
diffuse_mode = 3

[sub_resource type="BoxMesh" id="body_mesh"]
size = Vector3(0.2, 0.3, 0.2)

[sub_resource type="PrismMesh" id="top_mesh"]
left_to_right = 0.5
size = Vector3(0.2, 0.1, 0.2)

[sub_resource type="BoxMesh" id="label_mesh"]
size = Vector3(0.18, 0.16, 0.01)

[sub_resource type="BoxShape3D" id="col_shape"]
size = Vector3(0.22, 0.4, 0.22)

[node name="MilkCarton" type="RigidBody3D"]
mass = 0.7
script = ExtResource("1_break")
object_type = "milk"
break_threshold = 5.0
break_value = 350.0

[node name="Body" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.15, 0)
mesh = SubResource("body_mesh")
surface_material_override/0 = SubResource("carton_white")

[node name="Top" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.35, 0)
mesh = SubResource("top_mesh")
surface_material_override/0 = SubResource("carton_cyan")

[node name="LabelFront" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.15, 0.102)
mesh = SubResource("label_mesh")
surface_material_override/0 = SubResource("carton_cyan")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.2, 0)
shape = SubResource("col_shape")
"""
    with open(os.path.join(props_dir, "milk_carton.tscn"), "w") as f:
        f.write(milk_carton_tscn)

    # 8. Caution Wet Floor Sign (Breakable!)
    caution_sign_tscn = """[gd_scene load_steps=6 format=3 uid="uid://caution_sign"]

[ext_resource type="Script" path="res://scripts/breakable_object.gd" id="1_break"]

[sub_resource type="StandardMaterial3D" id="yellow_mat"]
albedo_color = Color(0.98, 0.84, 0.08, 1)
roughness = 0.5
diffuse_mode = 3

[sub_resource type="StandardMaterial3D" id="black_symbol"]
albedo_color = Color(0.12, 0.12, 0.12, 1)
roughness = 0.8
diffuse_mode = 3

[sub_resource type="BoxMesh" id="board_mesh"]
size = Vector3(0.3, 0.52, 0.03)

[sub_resource type="BoxMesh" id="symbol_mesh"]
size = Vector3(0.16, 0.16, 0.005)

[sub_resource type="BoxShape3D" id="col_shape"]
size = Vector3(0.32, 0.55, 0.28)

[node name="CautionSign" type="RigidBody3D"]
mass = 1.0
script = ExtResource("1_break")
object_type = "caution_sign"
break_threshold = 6.0
break_value = 120.0

[node name="LegLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.985, -0.174, 0, 0.174, 0.985, 0, 0.26, -0.07)
mesh = SubResource("board_mesh")
surface_material_override/0 = SubResource("yellow_mat")

[node name="LegRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.985, 0.174, 0, -0.174, 0.985, 0, 0.26, 0.07)
mesh = SubResource("board_mesh")
surface_material_override/0 = SubResource("yellow_mat")

[node name="WarningSymbol" type="MeshInstance3D" parent="."]
transform = Transform3D(0.707, -0.707, 0, 0.696, 0.696, 0.174, -0.123, -0.123, 0.985, 0, 0.28, 0.09)
mesh = SubResource("symbol_mesh")
surface_material_override/0 = SubResource("black_symbol")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.27, 0)
shape = SubResource("col_shape")
"""
    with open(os.path.join(props_dir, "caution_sign.tscn"), "w") as f:
        f.write(caution_sign_tscn)

    # 9. Golden Mop Trophy (Breakable!)
    golden_trophy_tscn = """[gd_scene load_steps=8 format=3 uid="uid://golden_trophy"]

[ext_resource type="Script" path="res://scripts/breakable_object.gd" id="1_break"]

[sub_resource type="StandardMaterial3D" id="marble_mat"]
albedo_color = Color(0.15, 0.15, 0.18, 1)
roughness = 0.3
metallic = 0.2
diffuse_mode = 3

[sub_resource type="StandardMaterial3D" id="gold_mat"]
albedo_color = Color(1.0, 0.82, 0.15, 1)
metallic = 0.75
roughness = 0.25
diffuse_mode = 3

[sub_resource type="BoxMesh" id="base_mesh"]
size = Vector3(0.24, 0.08, 0.24)

[sub_resource type="CylinderMesh" id="stem_mesh"]
top_radius = 0.04
bottom_radius = 0.05
height = 0.18
radial_segments = 6

[sub_resource type="CylinderMesh" id="cup_mesh"]
top_radius = 0.12
bottom_radius = 0.05
height = 0.18
radial_segments = 7

[sub_resource type="BoxMesh" id="star_mesh"]
size = Vector3(0.12, 0.12, 0.03)

[sub_resource type="BoxShape3D" id="col_shape"]
size = Vector3(0.26, 0.55, 0.26)

[node name="GoldenTrophy" type="RigidBody3D"]
mass = 1.2
script = ExtResource("1_break")
object_type = "trophy"
break_threshold = 4.5
is_fragile = true
break_value = 300.0

[node name="Base" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.04, 0)
mesh = SubResource("base_mesh")
surface_material_override/0 = SubResource("marble_mat")

[node name="Stem" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.17, 0)
mesh = SubResource("stem_mesh")
surface_material_override/0 = SubResource("gold_mat")

[node name="Cup" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.35, 0)
mesh = SubResource("cup_mesh")
surface_material_override/0 = SubResource("gold_mat")

[node name="Star" type="MeshInstance3D" parent="."]
transform = Transform3D(0.707, -0.707, 0, 0.707, 0.707, 0, 0, 0, 1, 0, 0.50, 0)
mesh = SubResource("star_mesh")
surface_material_override/0 = SubResource("gold_mat")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.28, 0)
shape = SubResource("col_shape")
"""
    with open(os.path.join(props_dir, "golden_trophy.tscn"), "w") as f:
        f.write(golden_trophy_tscn)

    # 10. Coffee Mug (Breakable!)
    coffee_mug_tscn = """[gd_scene load_steps=5 format=3 uid="uid://coffee_mug"]

[ext_resource type="Script" path="res://scripts/breakable_object.gd" id="1_break"]

[sub_resource type="StandardMaterial3D" id="mug_mat"]
albedo_color = Color(0.92, 0.40, 0.20, 1)
roughness = 0.3
diffuse_mode = 3

[sub_resource type="CylinderMesh" id="mug_mesh"]
top_radius = 0.06
bottom_radius = 0.055
height = 0.12
radial_segments = 7

[sub_resource type="CylinderShape3D" id="col_shape"]
radius = 0.075
height = 0.13

[node name="CoffeeMug" type="RigidBody3D"]
mass = 0.3
script = ExtResource("1_break")
object_type = "mug"
break_threshold = 3.5
is_fragile = true
break_value = 45.0

[node name="MugBody" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.06, 0)
mesh = SubResource("mug_mesh")
surface_material_override/0 = SubResource("mug_mat")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.06, 0)
shape = SubResource("col_shape")
"""
    with open(os.path.join(props_dir, "coffee_mug.tscn"), "w") as f:
        f.write(coffee_mug_tscn)

    # 11. Muck Barrel (Breakable!)
    barrel_tscn = """[gd_scene load_steps=7 format=3 uid="uid://muck_barrel"]

[ext_resource type="Script" path="res://scripts/breakable_object.gd" id="1_break"]

[sub_resource type="StandardMaterial3D" id="wood_mat"]
albedo_color = Color(0.55, 0.35, 0.18, 1)
roughness = 0.8
diffuse_mode = 3

[sub_resource type="StandardMaterial3D" id="iron_mat"]
albedo_color = Color(0.28, 0.30, 0.34, 1)
metallic = 0.6
roughness = 0.5
diffuse_mode = 3

[sub_resource type="CylinderMesh" id="barrel_mesh"]
top_radius = 0.32
bottom_radius = 0.38
height = 0.42
radial_segments = 8

[sub_resource type="CylinderMesh" id="barrel_mesh2"]
top_radius = 0.38
bottom_radius = 0.32
height = 0.42
radial_segments = 8

[sub_resource type="CylinderShape3D" id="col_shape"]
radius = 0.40
height = 0.84

[node name="MuckBarrel" type="RigidBody3D"]
mass = 5.0
script = ExtResource("1_break")
object_type = "barrel"
break_threshold = 9.0
break_value = 100.0

[node name="BottomHalf" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.21, 0)
mesh = SubResource("barrel_mesh")
surface_material_override/0 = SubResource("wood_mat")

[node name="TopHalf" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.63, 0)
mesh = SubResource("barrel_mesh2")
surface_material_override/0 = SubResource("wood_mat")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.42, 0)
shape = SubResource("col_shape")
"""
    with open(os.path.join(props_dir, "wooden_barrel.tscn"), "w") as f:
        f.write(barrel_tscn)

    # 12. Muck Chest
    chest_tscn = """[gd_scene load_steps=7 format=3 uid="uid://muck_chest"]

[sub_resource type="StandardMaterial3D" id="chest_wood"]
albedo_color = Color(0.48, 0.28, 0.12, 1)
roughness = 0.8
diffuse_mode = 3

[sub_resource type="StandardMaterial3D" id="chest_metal"]
albedo_color = Color(0.24, 0.26, 0.30, 1)
metallic = 0.7
roughness = 0.4
diffuse_mode = 3

[sub_resource type="StandardMaterial3D" id="latch_gold"]
albedo_color = Color(0.95, 0.78, 0.15, 1)
metallic = 0.8
roughness = 0.3
diffuse_mode = 3

[sub_resource type="BoxMesh" id="chest_base"]
size = Vector3(0.75, 0.45, 0.48)

[sub_resource type="CylinderMesh" id="chest_lid"]
top_radius = 0.24
bottom_radius = 0.24
height = 0.75
radial_segments = 6

[sub_resource type="BoxShape3D" id="col_shape"]
size = Vector3(0.75, 0.6, 0.48)

[node name="MuckChest" type="StaticBody3D"]

[node name="Base" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.225, 0)
mesh = SubResource("chest_base")
surface_material_override/0 = SubResource("chest_wood")

[node name="Lid" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, 0, 0.45, 0)
mesh = SubResource("chest_lid")
surface_material_override/0 = SubResource("chest_wood")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.3, 0)
shape = SubResource("col_shape")
"""
    with open(os.path.join(props_dir, "wooden_chest.tscn"), "w") as f:
        f.write(chest_tscn)

    # 13. Low-Poly Cloud
    cloud_tscn = """[gd_scene load_steps=5 format=3 uid="uid://lowpoly_cloud"]

[sub_resource type="StandardMaterial3D" id="cloud_mat"]
albedo_color = Color(0.98, 0.98, 1.0, 1)
roughness = 1.0
diffuse_mode = 3

[sub_resource type="SphereMesh" id="cloud_sphere1"]
radius = 2.0
height = 2.4
radial_segments = 6
rings = 4

[sub_resource type="SphereMesh" id="cloud_sphere2"]
radius = 1.5
height = 1.8
radial_segments = 6
rings = 4

[sub_resource type="SphereMesh" id="cloud_sphere3"]
radius = 1.3
height = 1.6
radial_segments = 6
rings = 4

[node name="LowPolyCloud" type="Node3D"]

[node name="Puff1" type="MeshInstance3D" parent="."]
mesh = SubResource("cloud_sphere1")
surface_material_override/0 = SubResource("cloud_mat")

[node name="Puff2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 1.6, -0.3, 0.2)
mesh = SubResource("cloud_sphere2")
surface_material_override/0 = SubResource("cloud_mat")

[node name="Puff3" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -1.5, -0.2, -0.2)
mesh = SubResource("cloud_sphere3")
surface_material_override/0 = SubResource("cloud_mat")
"""
    with open(os.path.join(props_dir, "lowpoly_cloud.tscn"), "w") as f:
        f.write(cloud_tscn)

    # 14. Fence Segment
    fence_tscn = """[gd_scene load_steps=5 format=3 uid="uid://fence_segment"]

[sub_resource type="StandardMaterial3D" id="fence_mat"]
albedo_color = Color(0.58, 0.40, 0.24, 1)
roughness = 0.9
diffuse_mode = 3

[sub_resource type="BoxMesh" id="post_mesh"]
size = Vector3(0.14, 1.0, 0.14)

[sub_resource type="BoxMesh" id="rail_mesh"]
size = Vector3(1.9, 0.08, 0.06)

[sub_resource type="BoxShape3D" id="col_shape"]
size = Vector3(1.95, 1.0, 0.2)

[node name="FenceSegment" type="StaticBody3D"]

[node name="Post1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.9, 0.5, 0)
mesh = SubResource("post_mesh")
surface_material_override/0 = SubResource("fence_mat")

[node name="Post2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.9, 0.5, 0)
mesh = SubResource("post_mesh")
surface_material_override/0 = SubResource("fence_mat")

[node name="RailTop" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.75, 0)
mesh = SubResource("rail_mesh")
surface_material_override/0 = SubResource("fence_mat")

[node name="RailBottom" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.35, 0)
mesh = SubResource("rail_mesh")
surface_material_override/0 = SubResource("fence_mat")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.5, 0)
shape = SubResource("col_shape")
"""
    with open(os.path.join(props_dir, "fence_segment.tscn"), "w") as f:
        f.write(fence_tscn)

    print("All prop scenes generated in scenes/props/")

if __name__ == "__main__":
    create_prop_scenes()
