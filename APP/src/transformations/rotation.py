"""
Rotation transformation for 3D modeling application.
"""
import numpy as np

def apply_rotation(obj, rx=0.0, ry=0.0, rz=0.0):
    """
    Apply a rotation transformation to a 3D object.
    
    Args:
        obj: The Object3D instance to transform
        rx (float): Rotation around X axis in degrees
        ry (float): Rotation around Y axis in degrees
        rz (float): Rotation around Z axis in degrees
    """
    # Update the object's rotation
    obj.rotation += np.array([rx, ry, rz], dtype=np.float32)
    
    # Normalize angles to 0-360 range
    obj.rotation %= 360.0
    
    return obj
