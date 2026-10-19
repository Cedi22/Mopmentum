import math
import os

def write_obj(filepath, vertices, faces, mtl_name=None):
    """
    Writes a low-poly Wavefront OBJ file with flat face normals.
    vertices: list of (x, y, z)
    faces: list of list of vertex indices (0-based)
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write("# Muck style low-poly asset\n")
        if mtl_name:
            f.write(f"usemtl {mtl_name}\n")
        for v in vertices:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
        
        # Calculate flat face normals for each face
        normals = []
        for face in faces:
            v0 = vertices[face[0]]
            v1 = vertices[face[1]]
            v2 = vertices[face[2]]
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
            ni = i + 1
            idx_str = " ".join(f"{idx+1}//{ni}" for idx in face)
            f.write(f"f {idx_str}\n")

print("OBJ generator helper loaded.")
