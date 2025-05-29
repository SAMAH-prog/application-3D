"""
Torus primitive for 3D modeling application.
"""
import numpy as np
from ..core.object3d import Object3D
from ..core.face import Face

def create_torus(major_radius=1.0, minor_radius=0.3, center=None, n_major=20, n_minor=10):
    """
    Create a torus primitive.
    
    Args:
        major_radius (float): Major radius of the torus (distance from center to ring center)
        minor_radius (float): Minor radius of the torus (radius of the ring)
        center (list): Center position [x, y, z]
        n_major (int): Number of segments around the major radius
        n_minor (int): Number of segments around the minor radius
        
    Returns:
        Object3D: A new torus object
    """
    if center is None:
        center = [0, 0, 0]
    
    # Create a new 3D object
    torus = Object3D("Torus")
    
    # Convert center to numpy array
    center = np.array(center)
    
    # Generate vertices
    vertices = []
    
    for i in range(n_major):
        u = 2.0 * np.pi * i / n_major
        for j in range(n_minor):
            v = 2.0 * np.pi * j / n_minor
            
            # Calculate position on torus
            x = (major_radius + minor_radius * np.cos(v)) * np.cos(u)
            y = minor_radius * np.sin(v)
            z = (major_radius + minor_radius * np.cos(v)) * np.sin(u)
            
            vertices.append([x, y, z])
    
    # Set the vertices (and translate to center)
    torus.set_points(np.array(vertices) + center)
    
    # Generate faces (quads)
    faces = []
    
    for i in range(n_major):
        for j in range(n_minor):
            # Calculate vertex indices
            i_next = (i + 1) % n_major
            j_next = (j + 1) % n_minor
            
            v1 = i * n_minor + j
            v2 = i * n_minor + j_next
            v3 = i_next * n_minor + j_next
            v4 = i_next * n_minor + j
            
            # Add quad face
            faces.append([v1, v2, v3, v4])
    
    # Add faces to the torus
    for face_indices in faces:
        torus.add_face(Face(face_indices))
    
    return torus
