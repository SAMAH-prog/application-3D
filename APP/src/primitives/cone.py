"""
Cone primitive for 3D modeling application.
"""
import numpy as np
from ..core.object3d import Object3D
from ..core.face import Face

def create_cone(radius=1.0, height=2.0, center=None, n_segments=20):
    """
    Create a cone primitive.
    
    Args:
        radius (float): Radius of the cone base
        height (float): Height of the cone
        center (list): Center position [x, y, z]
        n_segments (int): Number of segments around the circumference
        
    Returns:
        Object3D: A new cone object
    """
    if center is None:
        center = [0, 0, 0]
    
    # Create a new 3D object
    cone = Object3D("Cone")
    
    # Convert center to numpy array
    center = np.array(center)
    
    # Half height for vertex calculation
    half_height = height / 2
    
    # Generate vertices
    vertices = []
    
    # Apex vertex (top point)
    vertices.append([0, half_height, 0])
    
    # Base center vertex
    vertices.append([0, -half_height, 0])
    
    # Base circle vertices
    for i in range(n_segments):
        theta = 2.0 * np.pi * i / n_segments
        x = radius * np.cos(theta)
        z = radius * np.sin(theta)
        vertices.append([x, -half_height, z])
    
    # Set the vertices (and translate to center)
    cone.set_points(np.array(vertices) + center)
    
    # Generate faces
    faces = []
    
    # Base faces (triangles)
    for i in range(n_segments):
        next_i = (i + 1) % n_segments
        base_i = i + 2  # +2 because we have apex and base center first
        base_next_i = next_i + 2
        faces.append([1, base_next_i, base_i])  # 1 is the base center
    
    # Side faces (triangles)
    for i in range(n_segments):
        next_i = (i + 1) % n_segments
        base_i = i + 2
        base_next_i = next_i + 2
        faces.append([0, base_i, base_next_i])  # 0 is the apex
    
    # Add faces to the cone
    for face_indices in faces:
        cone.add_face(Face(face_indices))
    
    return cone
