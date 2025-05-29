"""
Face module for 3D modeling application.
"""
import numpy as np

class Face:
    """
    Represents a face (polygon) in a 3D object.
    """
    
    def __init__(self, indices_sommets, couleur=None):
        """
        Initialize a new face.
        
        Args:
            indices_sommets (list): List of vertex indices that form this face
            couleur (tuple): RGB color tuple (default: None, uses object color)
        """
        self.indices = indices_sommets
        self.nb_sommets = len(indices_sommets)
        self.couleur = couleur  # RGB tuple
    
    def calculate_normal(self, points):
        """
        Calculate the normal vector for this face.
        
        Args:
            points (numpy.ndarray): Array of vertex coordinates
            
        Returns:
            numpy.ndarray: Normalized normal vector
        """
        if self.nb_sommets < 3:
            return np.array([0, 0, 1])
            
        # Get three points from the face
        p1 = points[self.indices[0]]
        p2 = points[self.indices[1]]
        p3 = points[self.indices[2]]
        
        # Calculate two vectors from these points
        v1 = p2 - p1
        v2 = p3 - p1
        
        # Calculate cross product to get normal
        normal = np.cross(v1, v2)
        
        # Normalize the normal vector
        norm = np.linalg.norm(normal)
        if norm == 0:
            return np.array([0, 0, 1])
        return normal / norm
