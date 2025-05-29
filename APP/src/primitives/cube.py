"""
Cube primitive for 3D modeling application.
"""
import numpy as np
from ..core.object3d import Object3D
from ..core.face import Face

def create_cube(size=1.0, center=None):
    """
    Create a cube primitive.
    
    Args:
        size (float): Size of the cube
        center (list): Center position [x, y, z]
        
    Returns:
        Object3D: A new cube object
    """
    if center is None:
        center = [0, 0, 0]
    
    # Create a new 3D object
    cube = Object3D("Cube")
    
    # Half size for vertex calculation
    hs = size / 2
    center = np.array(center)
    
    # Define the 8 vertices of the cube
    vertices = np.array([
        [-hs, -hs, -hs],  # 0: left, bottom, back
        [hs, -hs, -hs],   # 1: right, bottom, back
        [hs, hs, -hs],    # 2: right, top, back
        [-hs, hs, -hs],   # 3: left, top, back
        [-hs, -hs, hs],   # 4: left, bottom, front
        [hs, -hs, hs],    # 5: right, bottom, front
        [hs, hs, hs],     # 6: right, top, front
        [-hs, hs, hs]     # 7: left, top, front
    ]) + center
    
    # Set the vertices
    cube.set_points(vertices)
    
    # Define the 6 faces of the cube (each face is a quad)
    # Each face is defined by 4 vertex indices
    faces = [
        [0, 1, 2, 3],  # Back face
        [4, 5, 6, 7],  # Front face
        [0, 4, 7, 3],  # Left face
        [1, 5, 6, 2],  # Right face
        [0, 1, 5, 4],  # Bottom face
        [3, 2, 6, 7]   # Top face
    ]
    
    # Colors for each face (optional)
    colors = [
        (1.0, 0.0, 0.0),  # Red
        (0.0, 1.0, 0.0),  # Green
        (0.0, 0.0, 1.0),  # Blue
        (1.0, 1.0, 0.0),  # Yellow
        (1.0, 0.0, 1.0),  # Magenta
        (0.0, 1.0, 1.0)   # Cyan
    ]
    
    # Add faces to the cube
    for i, face_indices in enumerate(faces):
        cube.add_face(Face(face_indices, colors[i]))
    
    return cube
