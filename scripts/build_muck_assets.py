import math
import os
import random

def normalize(v):
    l = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if l == 0: return (0, 0, 0)
    return (v[0]/l, v[1]/l, v[2]/l)

def write_obj_file(filepath, meshes_data):
    """
    meshes_data: list of dicts with:
      'name': object name,
      'vertices': [(x,y,z), ...],
      'faces': [[i0, i1, i2], ...]
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write("# Muck Low-Poly 3D Asset\n")
        v_offset = 1
        
        for mesh in meshes_data:
            name = mesh.get('name', 'Object')
            f.write(f"o {name}\n")
            verts = mesh['vertices']
            faces = mesh['faces']
            
            # Write vertices
            for v in verts:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            
            # Calculate flat face normals
            normals = []
            for face in faces:
                v0 = verts[face[0]]
                v1 = verts[face[1]]
                v2 = verts[face[2]]
                e1 = (v1[0]-v0[0], v1[1]-v0[1], v1[2]-v0[2])
                e2 = (v2[0]-v0[0], v2[1]-v0[1], v2[2]-v0[2])
                nx = e1[1]*e2[2] - e1[2]*e2[1]
                ny = e1[2]*e2[0] - e1[0]*e2[2]
                nz = e1[0]*e2[1] - e1[1]*e2[0]
                l = math.sqrt(nx*nx + ny*ny + nz*nz)
                if l > 1e-6:
                    normals.append((nx/l, ny/l, nz/l))
                else:
                    normals.append((0.0, 1.0, 0.0))
            
            for n in normals:
                f.write(f"vn {n[0]:.4f} {n[1]:.4f} {n[2]:.4f}\n")
            
            for i, face in enumerate(faces):
                ni = i + 1  # Note: normals are relative to this group or global, but standard OBJ can use face-specific normal indices
                # Let's write normal index
                f_str = " ".join(f"{idx + v_offset}//{i + 1}" for idx in face)
                f.write(f"f {f_str}\n")
            
            v_offset += len(verts)

def create_icosphere(radius=1.0, subdivisions=1, jitter=0.0, seed=42):
    rng = random.Random(seed)
    t = (1.0 + math.sqrt(5.0)) / 2.0
    verts = [
        (-1,  t,  0), ( 1,  t,  0), (-1, -t,  0), ( 1, -t,  0),
        ( 0, -1,  t), ( 0,  1,  t), ( 0, -1, -t), ( 0,  1, -t),
        ( t,  0, -1), ( t,  0,  1), (-t,  0, -1), (-t,  0,  1)
    ]
    verts = [normalize(v) for v in verts]
    faces = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ]
    
    midpoint_cache = {}
    def get_midpoint(i1, i2):
        key = tuple(sorted((i1, i2)))
        if key in midpoint_cache:
            return midpoint_cache[key]
        v1 = verts[i1]
        v2 = verts[i2]
        mid = normalize(((v1[0]+v2[0])/2, (v1[1]+v2[1])/2, (v1[2]+v2[2])/2))
        idx = len(verts)
        verts.append(mid)
        midpoint_cache[key] = idx
        return idx

    for _ in range(subdivisions):
        new_faces = []
        for tri in faces:
            m01 = get_midpoint(tri[0], tri[1])
            m12 = get_midpoint(tri[1], tri[2])
            m20 = get_midpoint(tri[2], tri[0])
            new_faces.append([tri[0], m01, m20])
            new_faces.append([tri[1], m12, m01])
            new_faces.append([tri[2], m20, m12])
            new_faces.append([m01, m12, m20])
        faces = new_faces

    final_verts = []
    for v in verts:
        r = radius
        if jitter > 0:
            r *= (1.0 + rng.uniform(-jitter, jitter))
        final_verts.append((v[0]*r, v[1]*r, v[2]*r))
    return final_verts, faces

def create_cylinder(radius_bottom=0.5, radius_top=0.5, height=1.0, segments=6, center_y=True):
    verts = []
    faces = []
    y_b = -height/2.0 if center_y else 0.0
    y_t = height/2.0 if center_y else height
    
    # Bottom center = 0
    verts.append((0, y_b, 0))
    # Top center = 1
    verts.append((0, y_t, 0))
    
    for i in range(segments):
        theta = i * 2 * math.pi / segments
        x_b = radius_bottom * math.cos(theta)
        z_b = radius_bottom * math.sin(theta)
        verts.append((x_b, y_b, z_b))
        
        x_t = radius_top * math.cos(theta)
        z_t = radius_top * math.sin(theta)
        verts.append((x_t, y_t, z_t))
        
    for i in range(segments):
        b0 = 2 + i * 2
        t0 = 2 + i * 2 + 1
        b1 = 2 + ((i + 1) % segments) * 2
        t1 = 2 + ((i + 1) % segments) * 2 + 1
        
        # Side quad (2 tris)
        faces.append([b0, b1, t1])
        faces.append([b0, t1, t0])
        # Bottom cap
        faces.append([0, b1, b0])
        # Top cap
        faces.append([1, t0, t1])
        
    return verts, faces

def create_box(sx=1.0, sy=1.0, sz=1.0, ox=0.0, oy=0.0, oz=0.0):
    hx, hy, hz = sx/2.0, sy/2.0, sz/2.0
    verts = [
        (ox - hx, oy - hy, oz - hz),
        (ox + hx, oy - hy, oz - hz),
        (ox + hx, oy + hy, oz - hz),
        (ox - hx, oy + hy, oz - hz),
        (ox - hx, oy - hy, oz + hz),
        (ox + hx, oy - hy, oz + hz),
        (ox + hx, oy + hy, oz + hz),
        (ox - hx, oy + hy, oz + hz),
    ]
    faces = [
        [0, 2, 1], [0, 3, 2], # back
        [4, 5, 6], [4, 6, 7], # front
        [0, 1, 5], [0, 5, 4], # bottom
        [3, 6, 2], [3, 7, 6], # top
        [0, 4, 7], [0, 7, 3], # left
        [1, 2, 6], [1, 6, 5], # right
    ]
    return verts, faces

def merge_meshes(mesh_list):
    all_verts = []
    all_faces = []
    for verts, faces in mesh_list:
        offset = len(all_verts)
        all_verts.extend(verts)
        for f in faces:
            all_faces.append([idx + offset for idx in f])
    return all_verts, all_faces

def translate(verts, dx, dy, dz):
    return [(v[0]+dx, v[1]+dy, v[2]+dz) for v in verts]

def scale(verts, sx, sy, sz):
    return [(v[0]*sx, v[1]*sy, v[2]*sz) for v in verts]

# --- Generators for specific Muck props ---

def generate_muck_tree():
    # 6-sided faceted tapered trunk
    trunk_v, trunk_f = create_cylinder(radius_bottom=0.35, radius_top=0.22, height=3.2, segments=6, center_y=False)
    # Foliage clumps (low poly faceted icospheres)
    c1_v, c1_f = create_icosphere(radius=1.3, subdivisions=1, jitter=0.15, seed=10)
    c1_v = translate(c1_v, 0, 3.2, 0)
    c2_v, c2_f = create_icosphere(radius=0.9, subdivisions=1, jitter=0.15, seed=20)
    c2_v = translate(c2_v, 0.45, 2.5, 0.3)
    c3_v, c3_f = create_icosphere(radius=0.85, subdivisions=1, jitter=0.15, seed=30)
    c3_v = translate(c3_v, -0.4, 2.7, -0.3)
    c4_v, c4_f = create_icosphere(radius=0.7, subdivisions=1, jitter=0.12, seed=40)
    c4_v = translate(c4_v, 0, 4.1, 0)
    
    return [
        {'name': 'Trunk', 'vertices': trunk_v, 'faces': trunk_f},
        {'name': 'Foliage', 'vertices': merge_meshes([(c1_v, c1_f), (c2_v, c2_f), (c3_v, c3_f), (c4_v, c4_f)])[0], 
                            'faces': merge_meshes([(c1_v, c1_f), (c2_v, c2_f), (c3_v, c3_f), (c4_v, c4_f)])[1]}
    ]

def generate_muck_birch():
    # Birch has slightly thinner, taller trunk
    trunk_v, trunk_f = create_cylinder(radius_bottom=0.26, radius_top=0.16, height=3.8, segments=6, center_y=False)
    c1_v, c1_f = create_icosphere(radius=1.1, subdivisions=1, jitter=0.12, seed=55)
    c1_v = translate(c1_v, 0, 3.6, 0)
    c2_v, c2_f = create_icosphere(radius=0.8, subdivisions=1, jitter=0.15, seed=65)
    c2_v = translate(c2_v, -0.3, 2.9, 0.2)
    c3_v, c3_f = create_icosphere(radius=0.75, subdivisions=1, jitter=0.15, seed=75)
    c3_v = translate(c3_v, 0.3, 3.1, -0.25)
    
    return [
        {'name': 'Trunk', 'vertices': trunk_v, 'faces': trunk_f},
        {'name': 'Foliage', 'vertices': merge_meshes([(c1_v, c1_f), (c2_v, c2_f), (c3_v, c3_f)])[0], 
                            'faces': merge_meshes([(c1_v, c1_f), (c2_v, c2_f), (c3_v, c3_f)])[1]}
    ]

def generate_rock_boulder(seed=101, r=1.4):
    verts, faces = create_icosphere(radius=r, subdivisions=1, jitter=0.28, seed=seed)
    verts = scale(verts, 1.3, 0.8, 1.1)
    # shift up so bottom rests on ground
    min_y = min(v[1] for v in verts)
    verts = translate(verts, 0, -min_y, 0)
    return [{'name': 'RockBoulder', 'vertices': verts, 'faces': faces}]

def generate_muck_mushroom(is_blue=False):
    # Thick chunky stem
    stem_v, stem_f = create_cylinder(radius_bottom=0.14, radius_top=0.10, height=0.45, segments=6, center_y=False)
    # Faceted umbrella cap
    cap_v, cap_f = create_cylinder(radius_bottom=0.42, radius_top=0.08, height=0.25, segments=7, center_y=False)
    cap_v = translate(cap_v, 0, 0.42, 0)
    return [
        {'name': 'Stem', 'vertices': stem_v, 'faces': stem_f},
        {'name': 'Cap', 'vertices': cap_v, 'faces': cap_f}
    ]

def generate_dani_milk_carton():
    # Milk carton: box body + angled gable roof + spout
    body_v, body_f = create_box(sx=0.22, sy=0.35, sz=0.22, oy=0.175)
    # Gable roof
    roof_v = [
        (-0.11, 0.35, -0.11), (0.11, 0.35, -0.11),
        (0.11, 0.35, 0.11), (-0.11, 0.35, 0.11),
        (-0.11, 0.46, 0.0), (0.11, 0.46, 0.0)
    ]
    roof_f = [
        [0, 1, 5], [0, 5, 4], # back slope
        [3, 4, 5], [3, 5, 2], # front slope
        [0, 4, 3],            # left triangle
        [1, 2, 5]             # right triangle
    ]
    # Spout
    spout_v, spout_f = create_cylinder(radius_bottom=0.025, radius_top=0.025, height=0.03, segments=5, center_y=False)
    spout_v = translate(spout_v, 0.05, 0.40, 0.06)
    
    verts, faces = merge_meshes([(body_v, body_f), (roof_v, roof_f), (spout_v, spout_f)])
    return [{'name': 'MilkCarton', 'vertices': verts, 'faces': faces}]

def generate_caution_sign():
    # A-frame wet floor sign
    # Left leg
    l_v, l_f = create_box(sx=0.32, sy=0.55, sz=0.03, ox=0, oy=0.28, oz=-0.11)
    # Right leg
    r_v, r_f = create_box(sx=0.32, sy=0.55, sz=0.03, ox=0, oy=0.28, oz=0.11)
    # Top hinge/handle
    top_v, top_f = create_box(sx=0.28, sy=0.06, sz=0.06, ox=0, oy=0.55, oz=0)
    verts, faces = merge_meshes([(l_v, l_f), (r_v, r_f), (top_v, top_f)])
    return [{'name': 'CautionSign', 'vertices': verts, 'faces': faces}]

def generate_golden_trophy():
    # Marble base
    base_v, base_f = create_box(sx=0.25, sy=0.08, sz=0.25, oy=0.04)
    # Stem
    stem_v, stem_f = create_cylinder(radius_bottom=0.04, radius_top=0.05, height=0.22, segments=6, center_y=False)
    stem_v = translate(stem_v, 0, 0.08, 0)
    # Cup / Star
    cup_v, cup_f = create_cylinder(radius_bottom=0.06, radius_top=0.14, height=0.20, segments=7, center_y=False)
    cup_v = translate(cup_v, 0, 0.30, 0)
    # Star emblem
    star_v, star_f = create_box(sx=0.12, sy=0.12, sz=0.04, oy=0.54)
    verts, faces = merge_meshes([(base_v, base_f), (stem_v, stem_f), (cup_v, cup_f), (star_v, star_f)])
    return [{'name': 'GoldenTrophy', 'vertices': verts, 'faces': faces}]

def generate_coffee_mug():
    # Faceted mug body
    body_v, body_f = create_cylinder(radius_bottom=0.06, radius_top=0.065, height=0.12, segments=7, center_y=False)
    # Handle (3 small box links)
    h1_v, h1_f = create_box(0.04, 0.015, 0.015, ox=0.08, oy=0.09)
    h2_v, h2_f = create_box(0.015, 0.06, 0.015, ox=0.10, oy=0.06)
    h3_v, h3_f = create_box(0.04, 0.015, 0.015, ox=0.08, oy=0.03)
    verts, faces = merge_meshes([(body_v, body_f), (h1_v, h1_f), (h2_v, h2_f), (h3_v, h3_f)])
    return [{'name': 'CoffeeMug', 'vertices': verts, 'faces': faces}]

def generate_muck_chest():
    # Box base
    base_v, base_f = create_box(sx=0.75, sy=0.45, sz=0.48, oy=0.225)
    # Curved lid (half cylinder with 5 segments)
    lid_v = []
    lid_f = []
    # Latch
    latch_v, latch_f = create_box(sx=0.08, sy=0.10, sz=0.04, oy=0.38, oz=0.25)
    verts, faces = merge_meshes([(base_v, base_f), (latch_v, latch_f)])
    return [{'name': 'MuckChest', 'vertices': verts, 'faces': faces}]

def generate_muck_barrel():
    # 8-sided bulging barrel
    b1_v, b1_f = create_cylinder(radius_bottom=0.28, radius_top=0.34, height=0.35, segments=8, center_y=False)
    b2_v, b2_f = create_cylinder(radius_bottom=0.34, radius_top=0.28, height=0.35, segments=8, center_y=False)
    b2_v = translate(b2_v, 0, 0.35, 0)
    verts, faces = merge_meshes([(b1_v, b1_f), (b2_v, b2_f)])
    return [{'name': 'MuckBarrel', 'vertices': verts, 'faces': faces}]

def generate_lowpoly_cloud():
    c1_v, c1_f = create_icosphere(radius=1.8, subdivisions=1, jitter=0.1, seed=1)
    c2_v, c2_f = create_icosphere(radius=1.4, subdivisions=1, jitter=0.1, seed=2)
    c2_v = translate(c2_v, 1.5, -0.2, 0.2)
    c3_v, c3_f = create_icosphere(radius=1.3, subdivisions=1, jitter=0.1, seed=3)
    c3_v = translate(c3_v, -1.4, -0.1, -0.2)
    c4_v, c4_f = create_icosphere(radius=1.1, subdivisions=1, jitter=0.1, seed=4)
    c4_v = translate(c4_v, 0.2, 0.6, -0.1)
    verts, faces = merge_meshes([(c1_v, c1_f), (c2_v, c2_f), (c3_v, c3_f), (c4_v, c4_f)])
    # Flatten vertically a bit
    verts = scale(verts, 1.2, 0.65, 1.0)
    return [{'name': 'LowPolyCloud', 'vertices': verts, 'faces': faces}]

def generate_fence_segment():
    # Post 1
    p1_v, p1_f = create_box(sx=0.14, sy=1.0, sz=0.14, ox=-0.9, oy=0.5)
    # Post 2
    p2_v, p2_f = create_box(sx=0.14, sy=1.0, sz=0.14, ox=0.9, oy=0.5)
    # Rail 1 (top)
    r1_v, r1_f = create_box(sx=1.9, sy=0.08, sz=0.06, ox=0.0, oy=0.75)
    # Rail 2 (bottom)
    r2_v, r2_f = create_box(sx=1.9, sy=0.08, sz=0.06, ox=0.0, oy=0.35)
    verts, faces = merge_meshes([(p1_v, p1_f), (p2_v, p2_f), (r1_v, r1_f), (r2_v, r2_f)])
    return [{'name': 'FenceSegment', 'vertices': verts, 'faces': faces}]

def generate_cleaning_cart():
    # Janitor / cleaning cart
    base_v, base_f = create_box(sx=0.6, sy=0.08, sz=0.9, oy=0.15)
    frame_v, frame_f = create_box(sx=0.04, sy=0.85, sz=0.04, ox=-0.26, oy=0.55, oz=-0.4)
    frame2_v, frame2_f = create_box(sx=0.04, sy=0.85, sz=0.04, ox=0.26, oy=0.55, oz=-0.4)
    handle_v, handle_f = create_box(sx=0.56, sy=0.04, sz=0.04, ox=0.0, oy=0.95, oz=-0.4)
    bin_v, bin_f = create_box(sx=0.48, sy=0.55, sz=0.45, ox=0.0, oy=0.45, oz=0.15)
    verts, faces = merge_meshes([(base_v, base_f), (frame_v, frame_f), (frame2_v, frame2_f), (handle_v, handle_f), (bin_v, bin_f)])
    return [{'name': 'CleaningCart', 'vertices': verts, 'faces': faces}]

def main():
    base_dir = r"c:/Users/visita/OneDrive/Documents/Desktop/Test/Mopmentum/assets/models"
    os.makedirs(base_dir, exist_ok=True)
    
    models = {
        "muck_tree.obj": generate_muck_tree(),
        "muck_birch.obj": generate_muck_birch(),
        "muck_rock_large.obj": generate_rock_boulder(seed=202, r=1.6),
        "muck_rock_small.obj": generate_rock_boulder(seed=303, r=0.6),
        "muck_mushroom_red.obj": generate_muck_mushroom(is_blue=False),
        "muck_mushroom_blue.obj": generate_muck_mushroom(is_blue=True),
        "milk_carton.obj": generate_dani_milk_carton(),
        "caution_sign.obj": generate_caution_sign(),
        "golden_trophy.obj": generate_golden_trophy(),
        "coffee_mug.obj": generate_coffee_mug(),
        "muck_chest.obj": generate_muck_chest(),
        "muck_barrel.obj": generate_muck_barrel(),
        "lowpoly_cloud.obj": generate_lowpoly_cloud(),
        "fence_segment.obj": generate_fence_segment(),
        "cleaning_cart.obj": generate_cleaning_cart(),
    }
    
    for filename, mesh_data in models.items():
        out_path = os.path.join(base_dir, filename)
        write_obj_file(out_path, mesh_data)
        print(f"Generated {filename}")

if __name__ == "__main__":
    main()
