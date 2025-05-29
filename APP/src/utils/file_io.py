"""
File I/O utilities for 3D modeling application.
"""
import os
import numpy as np
from ..core.object3d import Object3D
from ..core.face import Face

def save_obj(filename, obj):
    """
    Save a 3D object to Wavefront OBJ format.
    
    Args:
        filename (str): Path to save the file
        obj: The Object3D instance to save
    """
    with open(filename, 'w') as f:
        # Write header
        f.write(f"# OBJ file created by 3D Modeling App\n")
        f.write(f"# Object: {obj.name}\n\n")
        
        # Write vertices
        for v in obj.points:
            f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
        
        f.write("\n")
        
        # Write faces (OBJ uses 1-based indexing)
        for face in obj.faces:
            f.write("f")
            for idx in face.indices:
                f.write(f" {idx + 1}")
            f.write("\n")
    
    return True

def load_obj(filename):
    """
    Load a 3D object from Wavefront OBJ format.
    
    Args:
        filename (str): Path to the OBJ file
        
    Returns:
        Object3D: The loaded 3D object
    """
    # Create a new object with the filename as name
    name = os.path.splitext(os.path.basename(filename))[0]
    obj = Object3D(name)
    
    vertices = []
    faces = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            
            if line.startswith('v '):  # Vertex
                parts = line.split()[1:]
                vertex = [float(parts[0]), float(parts[1]), float(parts[2])]
                vertices.append(vertex)
            
            elif line.startswith('f '):  # Face
                parts = line.split()[1:]
                # OBJ uses 1-based indexing, convert to 0-based
                # Also handle different face formats (v, v/vt, v/vt/vn)
                indices = []
                for part in parts:
                    index = int(part.split('/')[0]) - 1
                    indices.append(index)
                
                faces.append(indices)
    
    # Set vertices and faces
    obj.set_points(np.array(vertices))
    
    for face_indices in faces:
        obj.add_face(Face(face_indices))
    
    return obj

def save_scene(filename, scene):
    """
    Save a scene to a custom format.
    
    Args:
        filename (str): Path to save the file
        scene: The Scene instance to save
    """
    # Create directory for the scene if it doesn't exist
    scene_dir = os.path.splitext(filename)[0]
    os.makedirs(scene_dir, exist_ok=True)
    
    # Save each object as an OBJ file
    obj_files = []
    for i, obj in enumerate(scene.objects):
        obj_filename = os.path.join(scene_dir, f"{obj.name}.obj")
        save_obj(obj_filename, obj)
        obj_files.append(os.path.basename(obj_filename))
    
    # Save scene metadata
    with open(filename, 'w') as f:
        f.write(f"# Scene file created by 3D Modeling App\n")
        f.write(f"name: {scene.name}\n")
        f.write(f"objects: {len(scene.objects)}\n")
        
        for i, obj_file in enumerate(obj_files):
            obj = scene.objects[i]
            f.write(f"object: {obj_file}\n")
            f.write(f"position: {obj.position[0]} {obj.position[1]} {obj.position[2]}\n")
            f.write(f"rotation: {obj.rotation[0]} {obj.rotation[1]} {obj.rotation[2]}\n")
            f.write(f"scale: {obj.scale[0]} {obj.scale[1]} {obj.scale[2]}\n")
    
    return True
