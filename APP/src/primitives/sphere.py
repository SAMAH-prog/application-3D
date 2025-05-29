"""
Sphere primitive for 3D modeling application.
"""
import numpy as np
from ..core.object3d import Object3D
from ..core.face import Face

def create_sphere(radius=1.0, center=None, n_meridians=20, n_parallels=20):
    """
    Create a sphere primitive.
    
    Args:
        radius (float): Radius of the sphere
        center (list): Center position [x, y, z]
        n_meridians (int): Number of meridians (longitude lines)
        n_parallels (int): Number of parallels (latitude lines)
        
    Returns:
        Object3D: A new sphere object
    """
    if center is None:
        center = [0, 0, 0]
    
    # Create a new 3D object
    sphere = Object3D("Sphere")
    
    # Convert center to numpy array
    center = np.array(center)
    
    # Generate vertices
    vertices = []
    
    # Add top vertex
    vertices.append([0, radius, 0])
    
    # Generate vertices for parallels
    for i in range(1, n_parallels):
        phi = np.pi * i / n_parallels
        for j in range(n_meridians):
            theta = 2.0 * np.pi * j / n_meridians
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.cos(phi)
            z = radius * np.sin(phi) * np.sin(theta)
            vertices.append([x, y, z])
    
    # Add bottom vertex
    vertices.append([0, -radius, 0])
    
    # Set the vertices (and translate to center)
    sphere.set_points(np.array(vertices) + center)
    
    # Generate faces
    faces = []
    
    # Top cap faces
    for i in range(n_meridians):
        next_i = (i + 1) % n_meridians
        faces.append([0, i + 1, next_i + 1])
    
    # Middle faces
    for p in range(1, n_parallels - 1):
        for m in range(n_meridians):
            # Calculate vertex indices
            i1 = 1 + (p - 1) * n_meridians + m
            i2 = 1 + (p - 1) * n_meridians + (m + 1) % n_meridians
            i3 = 1 + p * n_meridians + (m + 1) % n_meridians
            i4 = 1 + p * n_meridians + m
            
            # Add quad face (as two triangles)
            faces.append([i1, i2, i3, i4])
    
    # Bottom cap faces
    bottom_vertex = len(vertices) - 1
    for i in range(n_meridians):
        next_i = (i + 1) % n_meridians
        last_row_start = 1 + (n_parallels - 2) * n_meridians
        faces.append([bottom_vertex, last_row_start + next_i, last_row_start + i])
    
    # Add faces to the sphere
    for face_indices in faces:
        sphere.add_face(Face(face_indices))
    
    return sphere
