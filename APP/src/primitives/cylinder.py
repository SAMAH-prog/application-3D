"""
Cylinder primitive for 3D modeling application.
"""
import numpy as np
from ..core.object3d import Object3D
from ..core.face import Face

def create_cylinder(radius=1.0, height=2.0, center=None, n_segments=20):
    """
    Create a cylinder primitive.
    
    Args:
        radius (float): Radius of the cylinder
        height (float): Height of the cylinder
        center (list): Center position [x, y, z]
        n_segments (int): Number of segments around the circumference
        
    Returns:
        Object3D: A new cylinder object
    """
    if center is None:
        center = [0, 0, 0]
    
    # Create a new 3D object
    cylinder = Object3D("Cylinder")
    
    # Convert center to numpy array
    center = np.array(center)
    
    # Half height for vertex calculation
    half_height = height / 2
    
    # Generate vertices
    vertices = []
    
    # Top center vertex
    vertices.append([0, half_height, 0])
    
    # Top circle vertices
    for i in range(n_segments):
        theta = 2.0 * np.pi * i / n_segments
        x = radius * np.cos(theta)
        z = radius * np.sin(theta)
        vertices.append([x, half_height, z])
    
    # Bottom center vertex
    vertices.append([0, -half_height, 0])
    
    # Bottom circle vertices
    for i in range(n_segments):
        theta = 2.0 * np.pi * i / n_segments
        x = radius * np.cos(theta)
        z = radius * np.sin(theta)
        vertices.append([x, -half_height, z])
    
    # Set the vertices (and translate to center)
    cylinder.set_points(np.array(vertices) + center)
    
    # Generate faces
    faces = []
    
    # Top cap faces
    for i in range(n_segments):
        next_i = (i + 1) % n_segments
        faces.append([0, i + 1, next_i + 1])
    
    # Bottom cap faces
    bottom_center = n_segments + 1
    for i in range(n_segments):
        next_i = (i + 1) % n_segments
        bottom_i = bottom_center + 1 + i
        bottom_next_i = bottom_center + 1 + next_i
        faces.append([bottom_center, bottom_next_i, bottom_i])
    
    # Side faces (quads)
    for i in range(n_segments):
        next_i = (i + 1) % n_segments
        top_i = i + 1
        top_next_i = next_i + 1
        bottom_i = bottom_center + 1 + i
        bottom_next_i = bottom_center + 1 + next_i
        faces.append([top_i, top_next_i, bottom_next_i, bottom_i])
    
    # Add faces to the cylinder
    for face_indices in faces:
        cylinder.add_face(Face(face_indices))
    
    return cylinder
