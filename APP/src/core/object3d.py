"""
3D object module for 3D modeling application.
"""
import numpy as np
import uuid

class Object3D:
    """
    Represents a 3D object with vertices, faces, and transformations.
    """
    
    def __init__(self, type_objet="Generic"):
        """
        Initialize a new 3D object.
        
        Args:
            type_objet (str): The type of the object (e.g., "Cube", "Sphere")
        """
        self.id = str(uuid.uuid4())
        self.type = type_objet
        self.name = f"{type_objet}_{self.id[:8]}"
        self.points = np.array([])  # Vertex coordinates
        self.faces = []  # List of Face instances
        self.visible = True
        self.wireframe = False
        self.color = (0.7, 0.7, 0.7)  # Default color (RGB)
        
        # Transformation properties
        self.position = np.array([0.0, 0.0, 0.0])
        self.rotation = np.array([0.0, 0.0, 0.0])  # Euler angles in degrees
        self.scale = np.array([1.0, 1.0, 1.0])
    
    def set_points(self, points):
        """
        Set the vertex coordinates for this object.
        
        Args:
            points (numpy.ndarray): Array of vertex coordinates
        """
        self.points = np.array(points, dtype=np.float32)
    
    def add_face(self, face):
        """
        Add a face to this object.
        
        Args:
            face: The Face instance to add
        """
        self.faces.append(face)
    
    def get_transformation_matrix(self):
        """
        Calculate the combined transformation matrix for this object.
        
        Returns:
            numpy.ndarray: 4x4 transformation matrix
        """
        # Create translation matrix
        translation = np.eye(4, dtype=np.float32)
        translation[0:3, 3] = self.position
        
        # Create rotation matrices (X, Y, Z)
        rx, ry, rz = np.radians(self.rotation)
        
        rot_x = np.eye(4, dtype=np.float32)
        rot_x[1, 1] = np.cos(rx)
        rot_x[1, 2] = -np.sin(rx)
        rot_x[2, 1] = np.sin(rx)
        rot_x[2, 2] = np.cos(rx)
        
        rot_y = np.eye(4, dtype=np.float32)
        rot_y[0, 0] = np.cos(ry)
        rot_y[0, 2] = np.sin(ry)
        rot_y[2, 0] = -np.sin(ry)
        rot_y[2, 2] = np.cos(ry)
        
        rot_z = np.eye(4, dtype=np.float32)
        rot_z[0, 0] = np.cos(rz)
        rot_z[0, 1] = -np.sin(rz)
        rot_z[1, 0] = np.sin(rz)
        rot_z[1, 1] = np.cos(rz)
        
        # Create scaling matrix
        scaling = np.eye(4, dtype=np.float32)
        scaling[0, 0] = self.scale[0]
        scaling[1, 1] = self.scale[1]
        scaling[2, 2] = self.scale[2]
        
        # Combine transformations: T * Rz * Ry * Rx * S
        return translation @ rot_z @ rot_y @ rot_x @ scaling
    
    def get_transformed_points(self):
        """
        Get the transformed vertex coordinates.
        
        Returns:
            numpy.ndarray: Transformed vertex coordinates
        """
        if len(self.points) == 0:
            return np.array([])
            
        # Add homogeneous coordinate (w=1)
        homogeneous_points = np.ones((len(self.points), 4), dtype=np.float32)
        homogeneous_points[:, 0:3] = self.points
        
        # Apply transformation
        transform = self.get_transformation_matrix()
        transformed = homogeneous_points @ transform.T
        
        # Return 3D coordinates
        return transformed[:, 0:3]
